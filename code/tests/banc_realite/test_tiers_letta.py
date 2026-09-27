"""Tests hors ligne — tiers_letta (sans import letta au chargement)."""
from __future__ import annotations

import json

import pytest

import sys

import banc_realite.tiers_letta as tl


def test_passages_journalises_reprise(tmp_path, monkeypatch):
    journal = tmp_path / "appels-ingestion-letta.jsonl"
    journal.write_text('{"passage_id": "p1"}\n', encoding="utf-8")
    monkeypatch.setattr(tl, "JOURNAL_INGESTION", journal)
    assert tl._passages_journalises() == {"p1"}


def test_a_blanc_format_contextes(monkeypatch, tmp_path):
    class FakeClient:
        def __init__(self, base_url):
            self.base_url = base_url

        class agents:
            @staticmethod
            def list():
                return [type("Agent", (), {"id": "agent-1", "name": "greenloop"})()]

            class passages:
                @staticmethod
                def search(*, agent_id, query, limit):
                    return [
                        type(
                            "Hit",
                            (),
                            {"text": "passage", "metadata": {"piece": "a.md"}, "score": 0.8},
                        )()
                    ]

    monkeypatch.setitem(
        __import__("sys").modules,
        "letta_client",
        type("letta_client", (), {"Letta": FakeClient})(),
    )
    monkeypatch.setattr(tl, "_state_path", lambda: tmp_path / "state.json")
    (tmp_path / "state.json").write_text(json.dumps({"port": 56200}), encoding="utf-8")
    monkeypatch.setattr(tl, "_load_questions", lambda: [{"id": "gl-q001", "question": "q?"}])
    monkeypatch.setattr(tl, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr("banc_realite.fournisseurs_contexte.COMPARATIF_DIR", tmp_path)
    out = tl.contextes(k=3)
    assert out["status"] == "complete"
    lines = (tmp_path / "contextes-letta_archive.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert json.loads(lines[0])["meta"]["k"] == 3
    row = json.loads(lines[1])
    assert row["elements"][0]["source"] == "a.md"


def test_contextes_conserve_k_demande(monkeypatch, tmp_path):
    captured: list[int] = []

    class FakeClient:
        def __init__(self, base_url):
            self.base_url = base_url

        class agents:
            @staticmethod
            def list():
                return [type("Agent", (), {"id": "agent-1", "name": "greenloop"})()]

            class passages:
                @staticmethod
                def search(*, agent_id, query, limit):
                    captured.append(limit)
                    return [
                        type(
                            "Hit",
                            (),
                            {
                                "text": f"passage-{idx}",
                                "metadata": {"piece": "a.md"},
                                "score": 0.8,
                            },
                        )()
                        for idx in range(limit)
                    ]

    monkeypatch.setitem(
        __import__("sys").modules,
        "letta_client",
        type("letta_client", (), {"Letta": FakeClient})(),
    )
    monkeypatch.setattr(tl, "_state_path", lambda: tmp_path / "state.json")
    (tmp_path / "state.json").write_text(json.dumps({"port": 56200}), encoding="utf-8")
    monkeypatch.setattr(tl, "_load_questions", lambda: [{"id": "gl-q001", "question": "q?"}])
    monkeypatch.setattr(tl, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr("banc_realite.fournisseurs_contexte.COMPARATIF_DIR", tmp_path)
    out = tl.contextes(k=25)
    assert out["status"] == "complete"
    assert captured == [25]
    lines = (tmp_path / "contextes-letta_archive.jsonl").read_text(encoding="utf-8").strip().split("\n")
    assert json.loads(lines[0])["meta"]["k"] == 25
    row = json.loads(lines[1])
    assert len(row["elements"]) == 25


def test_write_arret(tmp_path, monkeypatch):
    monkeypatch.setattr(tl, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr(tl, "ARRET_PATH", tmp_path / "_letta-arret.json")
    tl.write_arret("mémoire insuffisante")
    payload = json.loads((tmp_path / "_letta-arret.json").read_text(encoding="utf-8"))
    assert payload["status"] == "arret"


def test_import_letta_arret(monkeypatch, tmp_path):
    monkeypatch.setattr(tl, "_try_demarrer_serveur_archive", lambda: (None, "module absent"))
    monkeypatch.setattr(tl, "COMPARATIF_DIR", tmp_path)
    monkeypatch.setattr(tl, "ARRET_PATH", tmp_path / "_letta-arret.json")
    monkeypatch.setattr(tl, "export_runtime_env", lambda: None)
    monkeypatch.setattr(sys, "argv", ["tiers_letta.py", "serveur"])
    code = tl.main()
    assert code == 1
    assert (tmp_path / "_letta-arret.json").is_file()
