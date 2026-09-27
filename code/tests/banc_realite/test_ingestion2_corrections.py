"""Corrections ingestion-2 — budget par exécution, mémoire vide, dossier de sortie, pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from banc_realite.fidelite import measure
from banc_realite.ingest_runner import IngestionConfig, piece_status
from banc_realite.production import plan_brain_to_public_pipeline
from banc_realite.relay import RelaySkillRunner, ensure_call_log_header, load_call_count


# --- 1 : budget par exécution (journal neuf, plafond local) ---


def test_fresh_call_log_starts_at_zero_without_prior_report(tmp_path: Path):
    log = tmp_path / "skill-calls.jsonl"
    ensure_call_log_header(log, run_id="ingestion-2", include_prior_report=False)
    assert load_call_count(log) == 0
    assert log.read_text(encoding="utf-8").strip() == ""


def test_relay_runner_counts_only_current_execution_log(tmp_path: Path):
    old_log = tmp_path / "old.jsonl"
    old_log.write_text(
        json.dumps({"event": "end", "call_n": 137, "skill": "coarse-map"}) + "\n",
        encoding="utf-8",
    )
    new_log = tmp_path / "ingestion-2" / "skill-calls.jsonl"
    runner = RelaySkillRunner(log_path=new_log, run_id="run-2", include_prior_report=False)
    assert runner.calls == 0
    assert load_call_count(old_log) == 137


def test_ingestion_config_default_max_calls_unchanged():
    cfg = IngestionConfig()
    assert cfg.max_calls == 160
    assert cfg.output_dir.name == "sorties"


def test_ingestion_config_ingestion2_budget():
    cfg = IngestionConfig.for_ingestion2()
    assert cfg.max_calls == 130
    assert cfg.output_dir.name == "ingestion-2"
    assert cfg.call_log.name == "skill-calls.jsonl"


# --- 2 : piece_status ne saute pas via un journal d'une autre exécution ---


class _FakeStatusConnection:
    def execute(self, query: str, params: tuple[Any, ...] | None = None):
        return SimpleNamespace(fetchone=lambda: {"n": 12})


def test_piece_status_ignores_complete_from_other_run_when_db_nonempty(
    tmp_path: Path, monkeypatch
):
    old_log = tmp_path / "old-ingestion.jsonl"
    old_log.write_text(
        json.dumps({"file": "doc.md", "statut": "complete", "run_id": "etape1"}) + "\n",
        encoding="utf-8",
    )
    new_log = tmp_path / "ingestion-2" / "ingestion.jsonl"
    monkeypatch.setattr("banc_realite.ingest_runner.INGEST_LOG", new_log)
    status = piece_status(_FakeStatusConnection(), "doc.md", ingest_log=new_log)
    assert status == "partial"


# --- 3 : sorties sous un sous-dossier sans écraser l'étage 1 ---


def test_measure_writes_under_output_dir(tmp_path: Path, monkeypatch):
    out_dir = tmp_path / "ingestion-2"
    out_dir.mkdir()
    stage1 = tmp_path / "sorties" / "fidelite-C.json"
    stage1.parent.mkdir(parents=True)
    stage1.write_text('{"status":"stage1"}\n', encoding="utf-8")

    def fake_measure_body(out_path, *_args, **_kwargs):
        payload = {
            "status": "ok",
            "seed": 20260920,
            "F1": {"global": 0.5},
            "memoire": {"claims_total": 1},
        }
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        return payload

    monkeypatch.setattr("banc_realite.fidelite._measure_body", fake_measure_body)
    result = measure(output_dir=out_dir)
    assert result["status"] == "ok"
    assert (out_dir / "fidelite-C.json").is_file()
    assert stage1.read_text(encoding="utf-8") == '{"status":"stage1"}\n'


# --- 4 : enchaînement explicite brain → ingestion → embeddings → public → parité ---


def test_pipeline_plan_order():
    steps = plan_brain_to_public_pipeline()
    assert steps == [
        "postgrest_brain",
        "ingestion",
        "embeddings",
        "copy_public",
        "postgrest_public",
        "parity",
    ]
