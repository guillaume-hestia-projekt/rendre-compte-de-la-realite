"""Tests hors ligne — ingestion Brain MOREAU (config, isolation, plafond, reprise)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from banc_realite.config import INSTANCES_PATH, SUPABASE_CREDENTIALS_PATH, write_banc_config_files
from banc_realite.dossiers import dossier_courant
from banc_realite.ingest_runner import (
    IngestionConfig,
    IngestionContext,
    append_reprise_record,
    ensure_area,
    last_ingest_record,
    piece_status,
    run_ingestion,
)
from banc_realite.ingestion_moreau import verify_isolation
from banc_realite.relay import RelaySkillRunner


class _FakeConnection:
    def __init__(self, rows: list[dict] | None = None) -> None:
        self.rows = list(rows or [])

    def execute(self, query, params=None):
        sql = " ".join(query.split())
        params = params or ()
        if "COUNT(*) AS n FROM brain.claims" in sql and "vault_ref = %s" in sql:
            source_path, vault_ref = params
            count = sum(
                1
                for row in self.rows
                if row.get("source_file_path") == source_path
                and row.get("vault_ref") == vault_ref
                and row.get("lifecycle_status") == "active"
            )
            return _Row({"n": count})
        if "FROM brain.claims WHERE lifecycle_status = 'active'" in sql:
            vault_ref = params[0] if params else None
            filtered = [
                row
                for row in self.rows
                if row.get("lifecycle_status") == "active"
                and (vault_ref is None or row.get("vault_ref") == vault_ref)
            ]
            if "source_file_path LIKE" in sql:
                pattern = params[1].strip("%")
                filtered = [
                    row
                    for row in filtered
                    if pattern in str(row.get("source_file_path") or "")
                ]
                return _Row(filtered[0] if filtered else None)
            return _Rows(filtered)
        if sql.startswith("DELETE FROM brain.claims"):
            source_path, vault_ref = params
            self.rows = [
                row
                for row in self.rows
                if not (
                    row.get("source_file_path") == source_path and row.get("vault_ref") == vault_ref
                )
            ]
            return self
        return _Rows([])


class _Row:
    def __init__(self, data: dict | None):
        self._data = data

    def fetchone(self):
        return self._data


class _Rows:
    def __init__(self, rows: list[dict]):
        self._rows = rows

    def fetchall(self):
        return list(self._rows)


def test_write_banc_config_files_deux_instances_area_root_distincts(tmp_path, monkeypatch):
    instances = tmp_path / "instances.yaml"
    credentials = tmp_path / "supabase-credentials.yaml"
    monkeypatch.setattr("banc_realite.config.INSTANCES_PATH", instances)
    monkeypatch.setattr("banc_realite.config.SUPABASE_CREDENTIALS_PATH", credentials)
    greenloop_area = tmp_path / "aire-greenloop"
    moreau_area = tmp_path / "aire-moreau"
    greenloop_area.mkdir()
    (greenloop_area / "semantic-memory").mkdir()
    marker = greenloop_area / "semantic-memory" / "pages" / "keep.md"
    marker.parent.mkdir(parents=True)
    marker.write_text("préservé\n", encoding="utf-8")

    def _area_roots():
        return {
            "greenloop": greenloop_area,
            "moreau": moreau_area,
        }

    monkeypatch.setattr("banc_realite.config._instance_area_roots", _area_roots)
    write_banc_config_files(preserve_existing_areas=False)
    blob = yaml.safe_load(instances.read_text(encoding="utf-8"))
    assert set(blob["instances"]) == {"greenloop", "moreau"}
    assert blob["instances"]["greenloop"]["area_root"] == str(greenloop_area)
    assert blob["instances"]["moreau"]["area_root"] == str(moreau_area)
    assert marker.read_text(encoding="utf-8") == "préservé\n"
    cred_blob = yaml.safe_load(credentials.read_text(encoding="utf-8"))
    assert set(cred_blob["instances"]) == {"greenloop", "moreau"}


def test_isolation_moreau_greenloop(tmp_path, monkeypatch):
    gl_area = tmp_path / "greenloop-aire"
    mo_area = tmp_path / "moreau-aire"
    (gl_area / "semantic-memory").mkdir(parents=True)
    (mo_area / "semantic-memory").mkdir(parents=True)
    monkeypatch.setattr(
        "banc_realite.ingestion_moreau.GREENLOOP_DOSSIER",
        type(
            "D",
            (),
            {"vault_ref": "greenloop", "area_root": gl_area},
        )(),
    )
    monkeypatch.setattr(
        "banc_realite.ingestion_moreau.MOREAU_DOSSIER",
        type(
            "D",
            (),
            {"vault_ref": "moreau", "area_root": mo_area},
        )(),
    )
    conn = _FakeConnection(
        [
            {
                "claim_id": "1",
                "vault_ref": "moreau",
                "lifecycle_status": "active",
                "source_file_path": "semantic-memory/pages/01.md",
            },
            {
                "claim_id": "2",
                "vault_ref": "greenloop",
                "lifecycle_status": "active",
                "source_file_path": "semantic-memory/pages/22.md",
            },
        ]
    )
    result = verify_isolation(conn)
    assert result["isolation_ok"] is True
    assert result["moreau_atom_count"] == 1
    assert result["greenloop_atom_count"] == 1


def test_plafond_appels_arrete_ingestion(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    for idx in range(3):
        (corpus / f"{idx:02d}-demo.md").write_text(f"# P{idx}\n\nTexte {idx}.\n", encoding="utf-8")
    dossier = type(
        "D",
        (),
        {
            "nom": "moreau",
            "corpus_dir": corpus,
            "area_root": tmp_path / "aire",
            "vault_ref": "moreau",
        },
    )()
    ctx = IngestionContext(dossier=dossier)
    cfg = IngestionConfig(
        output_dir=tmp_path / "sorties",
        max_calls=1,
        include_prior_report=False,
        dossier_name="moreau",
        call_log_name="appels.jsonl",
    )

    class _StubRunner:
        calls = 0
        providers = ["grok_cli"]
        run_id = "test-run"

        def run_skill(self, name, args):
            self.calls += 1
            return {"claims": []}

        def primary_provider(self):
            return "grok_cli"

        def assert_no_claude(self):
            return None

    monkeypatch.setattr("banc_realite.ingest_runner.IngestionContext.for_name", lambda _name: ctx)

    def _ingest_piece(path, **kwargs):
        runner = kwargs["runner"]
        runner.calls += 1
        return {
            "file": path.name,
            "statut": "complete",
            "zones_completees": [1],
            "zones_manquantes": [],
            "appels_modele": 1,
        }

    monkeypatch.setattr("banc_realite.ingest_runner.cluster_ready", lambda: True)
    monkeypatch.setattr("banc_realite.ingest_runner.connect_existing", lambda: _FakeConnection())
    monkeypatch.setattr("banc_realite.ingest_runner.ensure_area", lambda _ctx=None: None)
    monkeypatch.setattr("banc_realite.ingest_runner.ingest_piece", _ingest_piece)
    monkeypatch.setattr(
        "banc_realite.ingest_runner.RelaySkillRunner",
        lambda **kwargs: _StubRunner(),
    )
    monkeypatch.setenv("BRAIN_POSTGREST_URL", "http://127.0.0.1:56100")
    monkeypatch.setenv("BRAIN_POSTGREST_SERVICE_KEY", "test-key")

    summary = run_ingestion(config=cfg)
    assert summary.get("arret") == "plafond_appels"
    assert cfg.reprise_log.is_file()
    reprise_lines = [
        json.loads(line) for line in cfg.reprise_log.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    assert any(row.get("arret") == "plafond_appels" for row in reprise_lines)


def test_reprise_ne_reingere_pas_piece_completee(tmp_path, monkeypatch):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    piece = "01-demo.md"
    (corpus / piece).write_text("# A\n\nTexte.\n", encoding="utf-8")
    dossier = type(
        "D",
        (),
        {
            "nom": "moreau",
            "corpus_dir": corpus,
            "area_root": tmp_path / "aire",
            "vault_ref": "moreau",
        },
    )()
    ctx = IngestionContext(dossier=dossier)
    output = tmp_path / "sorties"
    ingest_log = output / "ingestion.jsonl"
    ingest_log.parent.mkdir(parents=True)
    ingest_log.write_text(
        json.dumps(
            {
                "file": piece,
                "statut": "complete",
                "run_id": "prev",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    conn = _FakeConnection(
        [
            {
                "claim_id": "c1",
                "vault_ref": "moreau",
                "lifecycle_status": "active",
                "source_file_path": f"semantic-memory/pages/{piece}",
            }
        ]
    )
    assert piece_status(conn, piece, ingest_log=ingest_log, ctx=ctx) == "complete"
    calls = {"n": 0}

    def _ingest_piece(*args, **kwargs):
        calls["n"] += 1
        return {"file": piece, "statut": "complete"}

    monkeypatch.setattr("banc_realite.ingest_runner.IngestionContext.for_name", lambda _name: ctx)
    monkeypatch.setattr("banc_realite.ingest_runner.cluster_ready", lambda: True)
    monkeypatch.setattr("banc_realite.ingest_runner.connect_existing", lambda: conn)
    monkeypatch.setattr("banc_realite.ingest_runner.ensure_area", lambda _ctx=None: None)
    monkeypatch.setattr("banc_realite.ingest_runner.ingest_piece", _ingest_piece)
    monkeypatch.setattr(
        "banc_realite.ingest_runner.RelaySkillRunner",
        lambda **kwargs: type(
            "R",
            (),
            {"calls": 0, "providers": [], "run_id": "r2", "primary_provider": lambda self: None, "assert_no_claude": lambda self: None},
        )(),
    )
    monkeypatch.setenv("BRAIN_POSTGREST_URL", "http://127.0.0.1:56100")
    monkeypatch.setenv("BRAIN_POSTGREST_SERVICE_KEY", "test-key")

    cfg = IngestionConfig(
        output_dir=output,
        max_calls=10,
        include_prior_report=False,
        dossier_name="moreau",
        journal_path=ingest_log,
        call_log_name="appels.jsonl",
    )
    summary = run_ingestion(config=cfg)
    assert calls["n"] == 0
    assert piece in summary.get("skipped", [])


def test_ensure_area_moreau_n_ecrit_pas_dans_greenloop(tmp_path, monkeypatch):
    gl_area = tmp_path / "greenloop-aire"
    mo_area = tmp_path / "moreau-aire"
    gl_pages = gl_area / "semantic-memory" / "pages"
    gl_pages.mkdir(parents=True)
    sentinel = gl_pages / "legacy.md"
    sentinel.write_text("legacy greenloop\n", encoding="utf-8")

    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "01-moreau.md").write_text("# M\n\nContenu MOREAU.\n", encoding="utf-8")
    dossier = type(
        "D",
        (),
        {
            "nom": "moreau",
            "corpus_dir": corpus,
            "area_root": mo_area,
            "vault_ref": "moreau",
        },
    )()
    ensure_area(IngestionContext(dossier=dossier))
    assert (mo_area / "semantic-memory" / "pages" / "01-moreau.md").is_file()
    assert sentinel.read_text(encoding="utf-8") == "legacy greenloop\n"
    assert not (gl_pages / "01-moreau.md").exists()
