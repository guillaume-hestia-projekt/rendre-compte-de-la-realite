"""Tests cursor-agent — fabrique make_cursor_chat_fn et choisir_chat_fn."""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from banc_realite import cursor_chat as cc
from banc_realite import etage3_config_gagnante as ecg


def _success_payload(result: str = "answer text") -> str:
    return json.dumps(
        {
            "type": "result",
            "subtype": "success",
            "is_error": False,
            "result": result,
            "session_id": "sess-1",
            "request_id": "req-1",
            "duration_api_ms": 5912,
            "usage": {
                "inputTokens": 21426,
                "outputTokens": 128,
                "cacheReadTokens": 512,
                "cacheWriteTokens": 0,
            },
        }
    )


def test_success_returns_text_and_meta(tmp_path):
    captured: dict = {}

    def run_fn(argv, *, cwd, env, timeout):
        captured["argv"] = argv
        captured["cwd"] = cwd
        captured["env"] = env
        captured["timeout"] = timeout
        return 0, _success_payload("**30 days after issue**"), ""

    workdir = tmp_path / "vide"
    workdir.mkdir()
    chat = cc.make_cursor_chat_fn(model="cursor-grok-4.5-high", workdir=workdir, run_fn=run_fn)
    system = "You are an agent."
    user = "When is payment due?"
    text, meta = chat(system, user)

    assert text == "**30 days after issue**"
    assert meta["fournisseur"] == "cursor-agent"
    assert meta["finish_reason"] is None
    assert meta["usage"]["prompt_tokens"] == 21426
    assert meta["usage"]["completion_tokens"] == 128
    assert meta["usage"]["cache_read_tokens"] == 512
    assert meta["usage"]["cache_write_tokens"] == 0
    assert captured["cwd"] == workdir
    assert captured["env"] == cc.CURSOR_ENV
    argv = captured["argv"]
    assert argv[:2] == [str(cc.CURSOR_AGENT), "--model"]
    assert "cursor-grok-4.5-high" in argv
    assert "--mode" in argv
    assert "ask" in argv
    assert "--output-format" in argv
    assert "json" in argv
    assert argv[-1] == system + "\n\n" + user


def test_is_error_then_success(monkeypatch, tmp_path):
    calls = 0

    def run_fn(_argv, *, cwd, env, timeout):
        nonlocal calls
        calls += 1
        if calls == 1:
            return 0, json.dumps({"type": "result", "subtype": "success", "is_error": True}), ""
        return 0, _success_payload("recovered"), ""

    sleeps: list[float] = []
    monkeypatch.setattr(cc.time, "sleep", lambda s: sleeps.append(s))

    workdir = tmp_path / "vide"
    workdir.mkdir()
    chat = cc.make_cursor_chat_fn(workdir=workdir, run_fn=run_fn)
    text, meta = chat("sys", "usr")

    assert calls == 2
    assert sleeps == [5.0]
    assert text == "recovered"
    assert meta["fournisseur"] == "cursor-agent"


def test_two_failures_raise_after_two_calls(monkeypatch, tmp_path):
    calls = 0

    def run_fn(_argv, *, cwd, env, timeout):
        nonlocal calls
        calls += 1
        return 0, json.dumps({"type": "result", "subtype": "success", "is_error": True}), "err body"

    monkeypatch.setattr(cc.time, "sleep", lambda _s: None)

    workdir = tmp_path / "vide"
    workdir.mkdir()
    chat = cc.make_cursor_chat_fn(workdir=workdir, run_fn=run_fn)

    with pytest.raises(RuntimeError):
        chat("sys", "usr")
    assert calls == 2


def test_invalid_json_raises(tmp_path):
    def run_fn(_argv, *, cwd, env, timeout):
        return 0, "not json", ""

    workdir = tmp_path / "vide"
    workdir.mkdir()
    chat = cc.make_cursor_chat_fn(workdir=workdir, run_fn=run_fn)

    with pytest.raises(RuntimeError, match="JSON illisible"):
        chat("sys", "usr")


def test_nonempty_workdir_raises_at_factory(tmp_path):
    workdir = tmp_path / "sale"
    workdir.mkdir()
    (workdir / "fichier.txt").write_text("x", encoding="utf-8")

    with pytest.raises(RuntimeError, match="non vide"):
        cc.make_cursor_chat_fn(workdir=workdir, run_fn=lambda *a, **k: (0, "", ""))


def test_factory_raises_under_pytest_without_run_fn():
    os.environ["PYTEST_CURRENT_TEST"] = "tests/banc_realite/test_cursor_chat.py::test_factory"
    try:
        with pytest.raises(RuntimeError, match="interdit sous pytest"):
            cc.make_cursor_chat_fn()
    finally:
        del os.environ["PYTEST_CURRENT_TEST"]


def test_choisir_chat_fn_relais():
    relais_called = False
    cursor_called = False

    def fabrique_relais():
        nonlocal relais_called
        relais_called = True
        return lambda s, u: ("r", {})

    def fabrique_cursor(modele):
        nonlocal cursor_called
        cursor_called = True
        return lambda s, u: ("c", {})

    fn = ecg.choisir_chat_fn("relais", "cursor-grok-4.5-high", fabrique_relais=fabrique_relais, fabrique_cursor=fabrique_cursor)
    assert relais_called
    assert not cursor_called
    assert fn("a", "b") == ("r", {})


def test_choisir_chat_fn_cursor():
    relais_called = False
    cursor_called = False
    seen_modele = None

    def fabrique_relais():
        nonlocal relais_called
        relais_called = True
        return lambda s, u: ("r", {})

    def fabrique_cursor(modele):
        nonlocal cursor_called, seen_modele
        cursor_called = True
        seen_modele = modele
        return lambda s, u: ("c", {})

    fn = ecg.choisir_chat_fn("cursor", "cursor-grok-4.5-high", fabrique_relais=fabrique_relais, fabrique_cursor=fabrique_cursor)
    assert cursor_called
    assert not relais_called
    assert seen_modele == "cursor-grok-4.5-high"
    assert fn("a", "b") == ("c", {})


def test_choisir_chat_fn_unknown_raises():
    with pytest.raises(ValueError, match="fournisseur inconnu"):
        ecg.choisir_chat_fn("autre", "x", fabrique_relais=lambda: None, fabrique_cursor=lambda m: None)
