"""Étage 3 — appels modèle via cursor-agent (Grok servi par Cursor)."""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

from .etage3 import ChatFn

CURSOR_AGENT = Path("/home/ubuntu/.local/bin/cursor-agent")
CURSOR_WORKDIR = Path.home() / ".agents/var/banc-realite/cursor-vide"
CURSOR_ENV = {
    "HOME": "/home/ubuntu",
    "PATH": "/home/ubuntu/.local/bin:/usr/local/bin:/usr/bin:/bin",
}

RunFn = Callable[..., tuple[int, str, str]]


def _default_run_fn(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: int,
) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            timeout=timeout,
            capture_output=True,
            text=True,
        )
    except subprocess.TimeoutExpired:
        # Un dépassement vaut un échec ordinaire : la seconde tentative s'applique.
        return 124, "", f"délai de {timeout} s dépassé"
    return result.returncode, result.stdout, result.stderr


def _ensure_empty_workdir(workdir: Path) -> None:
    workdir.mkdir(parents=True, exist_ok=True)
    if any(workdir.iterdir()):
        raise RuntimeError(f"dossier de travail cursor non vide: {workdir}")


def _parse_cursor_json(stdout: str) -> dict[str, Any]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    if not lines:
        raise ValueError("stdout vide")
    return json.loads(lines[-1])


def _meta_from_payload(payload: dict[str, Any], model: str) -> dict[str, Any]:
    usage_raw = payload.get("usage") or {}
    return {
        "model_returned": model,
        "fournisseur": "cursor-agent",
        "finish_reason": None,
        "usage": {
            "prompt_tokens": usage_raw.get("inputTokens"),
            "completion_tokens": usage_raw.get("outputTokens"),
            "cache_read_tokens": usage_raw.get("cacheReadTokens"),
            "cache_write_tokens": usage_raw.get("cacheWriteTokens"),
        },
        "session_id": payload.get("session_id"),
        "request_id": payload.get("request_id"),
        "duration_api_ms": payload.get("duration_api_ms"),
    }


def assert_cursor_model_available(model: str) -> None:
    result = subprocess.run(
        [str(CURSOR_AGENT), "--list-models"],
        capture_output=True,
        text=True,
        timeout=30,
        env=CURSOR_ENV,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"cursor-agent --list-models a échoué ({result.returncode}): "
            f"{result.stderr[:200]}"
        )
    for line in result.stdout.splitlines():
        slug = line.split(" - ", 1)[0].strip()
        if slug == model:
            return
    raise RuntimeError(f"modèle cursor indisponible: {model}")


def make_cursor_chat_fn(
    *,
    model: str = "cursor-grok-4.5-high",
    workdir: Path = CURSOR_WORKDIR,
    timeout_s: int = 300,
    run_fn: RunFn | None = None,
) -> ChatFn:
    if run_fn is None and os.environ.get("PYTEST_CURRENT_TEST"):
        raise RuntimeError("appel cursor-agent interdit sous pytest")

    _ensure_empty_workdir(workdir)
    runner = run_fn or _default_run_fn

    def _invoke(system: str, user: str) -> tuple[int, str, str]:
        prompt = system + "\n\n" + user
        argv = [
            str(CURSOR_AGENT),
            "--model",
            model,
            "--mode",
            "ask",
            "--print",
            "--output-format",
            "json",
            "--trust",
            prompt,
        ]
        return runner(
            argv,
            cwd=workdir,
            env=CURSOR_ENV,
            timeout=timeout_s,
        )

    def _attempt(system: str, user: str) -> tuple[str, dict[str, Any]]:
        returncode, stdout, stderr = _invoke(system, user)
        if returncode != 0:
            raise RuntimeError(
                f"cursor-agent code {returncode}: {stderr[:200]}"
            )
        try:
            payload = _parse_cursor_json(stdout)
        except (ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"JSON illisible: {exc}") from exc
        if payload.get("type") != "result":
            raise RuntimeError(f"subtype {payload.get('subtype')}: {stderr[:200]}")
        if payload.get("subtype") != "success":
            raise RuntimeError(f"subtype {payload.get('subtype')}: {stderr[:200]}")
        if payload.get("is_error"):
            raise RuntimeError(f"subtype {payload.get('subtype')}: {stderr[:200]}")
        result = str(payload.get("result") or "").strip()
        if not result:
            raise RuntimeError(f"subtype {payload.get('subtype')}: {stderr[:200]}")
        return result, _meta_from_payload(payload, model)

    def chat(system: str, user: str) -> tuple[str, dict[str, Any]]:
        try:
            return _attempt(system, user)
        except RuntimeError:
            time.sleep(5)
            try:
                return _attempt(system, user)
            except RuntimeError as exc:
                raise RuntimeError(str(exc)) from exc

    return chat
