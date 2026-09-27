"""Corrections PR #95 — revue Codex P1-a/P1-b et champs rapport ingestion-2."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite.ingest_runner import IngestionConfig


# --- P1-a : systemd-run --pipe + lecture résumé depuis fichier d'état ---


def test_p1a_systemd_cmd_contains_pipe():
    from banc_realite.run_ingestion2 import build_ingestion_systemd_cmd

    cmd = build_ingestion_systemd_cmd(env={"PYTHONPATH": "/tmp"}, python="/usr/bin/python3")
    assert "--pipe" in cmd
    idx = cmd.index("systemd-run")
    assert cmd[idx : idx + 4] == ["systemd-run", "--user", "--wait", "--collect"]


def test_p1a_reads_indented_summary_from_status_file(tmp_path: Path):
    from banc_realite.run_ingestion2 import read_ingestion_status

    status = tmp_path / "_ingestion-status.json"
    payload = {
        "run_id": "run-95",
        "pieces": [{"file": "a.md", "statut": "complete", "duree_s": 12.5}],
        "partielles": [],
        "erreurs": [],
        "duree_s": 12.5,
    }
    status.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert read_ingestion_status(status) == payload


def test_p1a_missing_status_file_raises(tmp_path: Path):
    from banc_realite.run_ingestion2 import read_ingestion_status

    with pytest.raises(RuntimeError, match="fichier d'état"):
        read_ingestion_status(tmp_path / "_ingestion-status.json")


def test_p1a_unreadable_status_file_raises(tmp_path: Path):
    from banc_realite.run_ingestion2 import read_ingestion_status

    status = tmp_path / "_ingestion-status.json"
    status.write_text("{not-json", encoding="utf-8")
    with pytest.raises(RuntimeError, match="illisible"):
        read_ingestion_status(status)


def test_ingest_runner_writes_status_file(tmp_path: Path, monkeypatch):
    from banc_realite.ingest_runner import ingestion_status_path, run_ingestion

    cfg = IngestionConfig(output_dir=tmp_path, max_calls=5, include_prior_report=False)
    monkeypatch.setenv("BRAIN_POSTGREST_URL", "http://127.0.0.1:56100")
    monkeypatch.setenv("BRAIN_POSTGREST_SERVICE_KEY", "test-key")
    monkeypatch.setattr("banc_realite.ingest_runner.cluster_ready", lambda: True)
    monkeypatch.setattr(
        "banc_realite.ingest_runner.connect_existing",
        lambda: _fake_connection(),
    )
    monkeypatch.setattr("banc_realite.ingest_runner.list_corpus", lambda *_args, **_kwargs: [])
    monkeypatch.setattr(
        "banc_realite.ingest_runner.RelaySkillRunner",
        lambda **kwargs: _FakeRunner(),
    )

    summary = run_ingestion(config=cfg)
    status_path = ingestion_status_path(cfg)
    assert status_path.is_file()
    on_disk = json.loads(status_path.read_text(encoding="utf-8"))
    assert on_disk["run_id"] == summary["run_id"]
    assert "duree_s" in on_disk


# --- P1-b : arrêt sur plafond, corpus incomplet, erreur ; partielles nommées ---


def test_p1b_stop_on_arret_plafond_appels():
    from banc_realite.run_ingestion2 import evaluate_ingestion_outcome

    full = {"arret": "plafond_appels", "pieces": [{"file": "a.md", "statut": "complete"}]}
    reason, partielles = evaluate_ingestion_outcome(
        full, corpus_piece_count=10, calls=130, max_calls=130
    )
    assert reason is not None
    assert "plafond_appels" in reason
    assert partielles == []


def test_p1b_stop_on_incomplete_corpus():
    from banc_realite.run_ingestion2 import evaluate_ingestion_outcome

    full = {
        "pieces": [
            {"file": "a.md", "statut": "complete"},
            {"file": "b.md", "statut": "complete"},
        ]
    }
    reason, _ = evaluate_ingestion_outcome(full, corpus_piece_count=5, calls=10, max_calls=130)
    assert reason is not None
    assert "incomplet" in reason


def test_p1b_stop_on_error_piece():
    from banc_realite.run_ingestion2 import evaluate_ingestion_outcome

    full = {
        "pieces": [
            {"file": "ok.md", "statut": "complete"},
            {"file": "bad.md", "statut": "erreur"},
        ]
    }
    reason, _ = evaluate_ingestion_outcome(full, corpus_piece_count=2, calls=10, max_calls=130)
    assert reason is not None
    assert "bad.md" in reason


def test_p1b_partial_piece_does_not_stop_but_is_named():
    from banc_realite.run_ingestion2 import evaluate_ingestion_outcome

    full = {
        "pieces": [
            {"file": "ok.md", "statut": "complete"},
            {"file": "09-january-scale-export.md", "statut": "partielle"},
        ],
        "partielles": ["09-january-scale-export.md"],
    }
    reason, partielles = evaluate_ingestion_outcome(
        full, corpus_piece_count=2, calls=10, max_calls=130
    )
    assert reason is None
    assert partielles == ["09-january-scale-export.md"]


def test_p1b_stop_when_calls_reach_ceiling_even_without_arret_key():
    from banc_realite.run_ingestion2 import evaluate_ingestion_outcome

    full = {"pieces": [{"file": "a.md", "statut": "complete"}]}
    reason, _ = evaluate_ingestion_outcome(
        full, corpus_piece_count=1, calls=130, max_calls=130
    )
    assert reason is not None
    assert "130" in reason


# --- Rapport : durée, partielles, rejets tabulaires depuis le journal ---


def test_report_duration_from_ingestion_summary_not_zero():
    from banc_realite.run_ingestion2 import ingestion_duration_s

    full = {
        "duree_s": 1847.3,
        "pieces": [
            {"file": "a.md", "statut": "complete", "duree_s": 900.1},
            {"file": "b.md", "statut": "complete", "duree_s": 947.2},
        ],
    }
    assert ingestion_duration_s(full) == 1847.3


def test_report_partial_pieces_listed_not_aucune():
    from banc_realite.run_ingestion2 import format_piece_names

    assert format_piece_names(["09-january-scale-export.md"]) == "09-january-scale-export.md"
    assert format_piece_names([]) == "aucune"


def test_report_tabular_rejections_summed_from_ingest_log(tmp_path: Path):
    from banc_realite.run_ingestion2 import sum_tabular_rejections_from_journal

    log = tmp_path / "ingestion.jsonl"
    records = [
        {
            "file": "a.md",
            "tabular_marker_claims_dropped": 80,
            "tabular_marker_claims_dropped_unanchored": 30,
        },
        {
            "file": "b.csv",
            "tabular_marker_claims_dropped": 46,
            "tabular_marker_claims_dropped_unanchored": 19,
        },
    ]
    log.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8",
    )
    dropped, unanchored = sum_tabular_rejections_from_journal(log)
    assert dropped == 126
    assert unanchored == 49


def test_write_report_uses_correct_ingestion_fields(tmp_path: Path, monkeypatch):
    from banc_realite.run_ingestion2 import write_report

    report_path = tmp_path / "RAPPORT.md"
    ingest_log = tmp_path / "ingestion.jsonl"
    ingest_log.write_text(
        json.dumps(
            {
                "file": "x.md",
                "tabular_marker_claims_dropped": 126,
                "tabular_marker_claims_dropped_unanchored": 49,
                "duree_s": 42.0,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("banc_realite.run_ingestion2.REPORT", report_path)
    monkeypatch.setattr("banc_realite.run_ingestion2.CFG", IngestionConfig(output_dir=tmp_path))
    monkeypatch.setattr(
        "banc_realite.run_ingestion2.load_call_count",
        lambda _log: 99,
    )
    monkeypatch.setattr("banc_realite.run_ingestion2.load_stage1_fidelite", lambda: None)
    monkeypatch.setattr("banc_realite.run_ingestion2.load_stage1_etage2", lambda: None)

    full = {
        "fournisseur": "hermes_relay",
        "duree_s": 1847.3,
        "erreurs": [],
        "partielles": ["09-january-scale-export.md"],
        "pieces": [],
    }
    write_report(
        started=0.0,
        trial={},
        full=full,
        embed_stats={},
        coverage={},
        fidelite={"F1": {}},
        parity_payload={"parity": {}},
        standard={},
        quotas={},
        paires=[],
        prechauffage={},
        before_stats={
            "total": 0,
            "tabulaire": 0,
            "modele": 0,
            "note_body": 0,
            "relation_about": 0,
            "modele_anchored": 0,
        },
        after_stats={
            "total": 1,
            "tabulaire": 0,
            "modele": 1,
            "note_body": 0,
            "relation_about": 0,
            "modele_anchored": 0,
        },
        dispute_hits={},
        ingest_log=ingest_log,
    )
    body = report_path.read_text(encoding="utf-8")
    assert "1847.3 s" in body
    assert "09-january-scale-export.md" in body
    assert "dropped=126" in body
    assert "unanchored=49" in body


class _FakeRunner:
    run_id = "fake-run"
    calls = 0

    def primary_provider(self) -> str:
        return "hermes_relay"

    def assert_no_claude(self) -> None:
        return None


def _fake_connection():
    class _Conn:
        def execute(self, *_args, **_kwargs):
            class _Row:
                def fetchone(self):
                    return {"n": 0}

            return _Row()

    return _Conn()
