"""Corrections PR #91 K1–K4 — tests écrits avant implémentation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from brain.adapters.supabase_claims import AtomicClaim, VersionedWriteResult, compute_natural_key
from brain.claiming.tabular import TABULAR_SKILL
from banc_realite.fidelite import (
    F1_KEY_CLAIMS_TOTAL,
    F1_KEY_GLOBAL,
    F1_KEY_MEMOIRE,
    F1_KEY_PAR_VOIE,
    F1_KEY_PROSE,
    F1_KEY_SEUIL_ATTEINT,
    F1_KEY_TABULAIRE,
    claim_has_ordering_date,
    evaluate_trajectory_order,
    extract_ordering_date,
)
from banc_realite.ingest_runner import (
    count_tabular_claims,
    rewrite_tabular_piece,
    source_path_for,
    sync_tabular_claims_for_piece,
)
from banc_realite.run_etape2 import MEASURE_SUMMARY_PATHS, summarize_fidelite


def _fake_measure_result(**overrides: Any) -> dict[str, Any]:
    base = {
        "status": "ok",
        F1_KEY_SEUIL_ATTEINT: True,
        "F1": {
            F1_KEY_GLOBAL: 0.82,
            "denominateur": 100,
            F1_KEY_PAR_VOIE: {
                F1_KEY_PROSE: 0.75,
                F1_KEY_TABULAIRE: 0.91,
            },
        },
        F1_KEY_MEMOIRE: {F1_KEY_CLAIMS_TOTAL: 42},
    }
    base.update(overrides)
    return base


# --- K1 : clés F1 du résumé ---


def test_k1_summarize_reads_par_voie_not_missing_keys():
    fidelite = _fake_measure_result()
    summary = summarize_fidelite(fidelite)
    assert summary["F1_prose"] == 0.75
    assert summary["F1_tabulaire"] == 0.91
    assert summary["F1"] == 0.82
    assert summary["claims"] == 42
    assert summary["seuil_atteint"] is True


def test_k1_every_measure_path_used_by_summary_exists():
    fidelite = _fake_measure_result()
    for path in MEASURE_SUMMARY_PATHS:
        node: Any = fidelite
        for key in path:
            assert key in node, f"clé manquante dans measure(): {'.'.join(path)}"
            node = node[key]


# --- K2 : total des faits tabulaires avec pièce skipped ---


def test_k2_counts_tabular_from_journal_including_skipped(tmp_path, monkeypatch):
    log = tmp_path / "ingestion.jsonl"
    piece = "22-recorded-visits.csv"
    records = [
        {
            "file": piece,
            "claims_tabulaires": 7,
            "statut": "complete",
            "skipped": False,
        },
        {
            "file": piece,
            "skipped": True,
            "raison": "deja_complete",
            "claims_en_base": 7,
        },
        {
            "file": "other.md",
            "claims_tabulaires": 3,
            "statut": "complete",
        },
    ]
    log.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    monkeypatch.setattr("banc_realite.ingest_runner.INGEST_LOG", log)

    full = {
        "pieces": [
            {"file": piece, "skipped": True, "raison": "deja_complete"},
            {"file": "other.md", "claims_tabulaires": 3, "statut": "complete"},
        ]
    }
    assert count_tabular_claims(full) == 10


def test_k2_journal_last_record_per_piece_not_double_counted(tmp_path, monkeypatch):
    log = tmp_path / "ingestion.jsonl"
    piece = "24-customer-review.md"
    log.write_text(
        "\n".join(
            json.dumps(r)
            for r in [
                {"file": piece, "claims_tabulaires": 5, "statut": "complete"},
                {"file": piece, "claims_tabulaires": 99, "statut": "erreur", "erreur": "boom"},
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("banc_realite.ingest_runner.INGEST_LOG", log)
    full = {"pieces": [{"file": piece, "claims_tabulaires": 0, "skipped": True}]}
    assert count_tabular_claims(full) == 99


# --- K3 : F6 ordre restituable ---


def _trajectory(*versions: tuple[str, str | None]):
    return {
        "id": "gl-tr-test",
        "versions": [
            {"assertion": aid, "validity_start": start, "validity_end": None}
            for aid, start in versions
        ],
    }


def _gold(aid: str, piece: str = "doc.md") -> dict[str, Any]:
    return {
        "assertion_index": {
            aid: {"id": aid, "source": f"semantic-memory/pages/{piece}", "quote": aid}
        }
    }


def test_k3_all_present_without_dates_not_restituable():
    gold = _gold("gl-a1")
    trajectory = _trajectory(("gl-a1", "2020-01-01"))
    by_piece = {
        "doc.md": [{"text": "gl-a1", "claim_id": "c1", "extracted_by_skill": "model"}],
    }
    result = evaluate_trajectory_order(trajectory, gold, by_piece)
    assert result["versions_presentes"] == 1
    assert result["versions_datees"] == 0
    assert result["ordre_restituable"] is False
    assert result["motif"] == "non datées"


def test_k3_dated_but_wrong_order_not_restituable():
    gold = {
        "assertion_index": {
            "gl-a1": {"id": "gl-a1", "source": "semantic-memory/pages/doc.md", "quote": "first"},
            "gl-a2": {"id": "gl-a2", "source": "semantic-memory/pages/doc.md", "quote": "second"},
        }
    }
    trajectory = _trajectory(("gl-a1", "2020-01-01"), ("gl-a2", "2022-01-01"))
    by_piece = {
        "doc.md": [
            {
                "text": "first",
                "claim_id": "c1",
                "value": "x",
                "qualifiers": {"valid_from": "2022-01-01"},
            },
            {
                "text": "second",
                "claim_id": "c2",
                "value": "y",
                "qualifiers": {"valid_from": "2020-01-01"},
            },
        ]
    }
    result = evaluate_trajectory_order(trajectory, gold, by_piece)
    assert result["versions_presentes"] == 2
    assert result["versions_datees"] == 2
    assert result["ordre_restituable"] is False
    assert result["motif"] == "ordre incorrect"


def test_k3_present_dated_correct_order_restituable():
    gold = {
        "assertion_index": {
            "gl-a1": {"id": "gl-a1", "source": "semantic-memory/pages/doc.md", "quote": "first"},
            "gl-a2": {"id": "gl-a2", "source": "semantic-memory/pages/doc.md", "quote": "second"},
        }
    }
    trajectory = _trajectory(("gl-a1", "2020-01-01"), ("gl-a2", "2022-01-01"))
    by_piece = {
        "doc.md": [
            {"text": "first", "claim_id": "c1", "qualifiers": {"date": "2020-01-01"}},
            {"text": "second", "claim_id": "c2", "qualifiers": {"since": "2022-01-01"}},
        ]
    }
    result = evaluate_trajectory_order(trajectory, gold, by_piece)
    assert result["versions_presentes"] == 2
    assert result["versions_datees"] == 2
    assert result["ordre_restituable"] is True
    assert result.get("motif") is None


def test_k3_ordering_date_detects_iso_in_value_and_qualifiers():
    assert claim_has_ordering_date({"value": "2021-06"})
    assert claim_has_ordering_date({"value": "text", "qualifiers": {"period": "2021-06-15"}})
    assert not claim_has_ordering_date({"value": "no date here", "qualifiers": {}})
    assert extract_ordering_date({"qualifiers": {"periode_debut": "2019"}}) == "2019"


# --- K4 : tabulaire-seul — suppression après écriture réussie ---


@dataclass
class _FakeClaimRow:
    claim_id: str
    entity_id: str
    predicate: str
    value: Any
    qualifiers: dict[str, Any]
    modality: str = "asserted"
    extracted_by_skill: str = TABULAR_SKILL
    lifecycle_status: str = "active"
    source_file_path: str = ""


class FakeTabularConnection:
    def __init__(self, rows: list[_FakeClaimRow] | None = None):
        self.rows = list(rows or [])
        self.deleted_ids: list[str] = []

    def execute(self, query: str, params: tuple[Any, ...] | None = None):
        params = params or ()
        q = " ".join(query.split()).lower()
        if q.startswith("select claim_id, entity_id, predicate, value, qualifiers, modality"):
            file_name = params[0]
            skill = params[2]
            matched = [
                r
                for r in self.rows
                if r.source_file_path == file_name
                and r.extracted_by_skill == skill
                and r.lifecycle_status == "active"
            ]
            return SimpleNamespace(fetchall=lambda: [vars(r) for r in matched])
        if q.startswith("delete from brain.claims where claim_id = any"):
            ids = set(params[0])
            self.deleted_ids.extend(ids)
            self.rows = [r for r in self.rows if r.claim_id not in ids]
            return SimpleNamespace(rowcount=len(ids))
        raise AssertionError(f"unexpected query: {query}")


def _tabular_claim(entity: str, value: str, file_name: str = "data.csv") -> _FakeClaimRow:
    return _FakeClaimRow(
        claim_id=f"id-{entity}-{value}",
        entity_id=entity,
        predicate="note.body",
        value=value,
        qualifiers={"attribute_id": entity},
        source_file_path=source_path_for(file_name),
    )


def _parsed_claim(entity: str, value: str) -> dict[str, Any]:
    return {
        "entity_id": entity,
        "predicate": "note.body",
        "value": value,
        "qualifiers": {"attribute_id": entity},
        "modality": "asserted",
        "extracted_by_skill": TABULAR_SKILL,
    }


def test_k4_write_failure_keeps_old_claims_and_deletes_nothing():
    file_name = "data.csv"
    connection = FakeTabularConnection(
        [_tabular_claim("row-a", "1", file_name), _tabular_claim("row-b", "2", file_name)]
    )

    def failing_writer(claims, **_kwargs):
        raise RuntimeError("write failed")

    result = sync_tabular_claims_for_piece(
        file_name=file_name,
        parsed_claims=[_parsed_claim("row-a", "1")],
        connection=connection,
        write_fn=failing_writer,
    )
    assert result["statut"] == "erreur"
    assert result["claims_retires"] == 0
    assert len(connection.rows) == 2
    assert connection.deleted_ids == []


def test_k4_success_removes_only_stale_keys():
    file_name = "data.csv"
    connection = FakeTabularConnection(
        [_tabular_claim("row-a", "1", file_name), _tabular_claim("row-b", "2", file_name)]
    )

    def ok_writer(claims, **_kwargs):
        return VersionedWriteResult(
            written=[{"natural_key": compute_natural_key(claims[0])}],
            unchanged=[],
        )

    result = sync_tabular_claims_for_piece(
        file_name=file_name,
        parsed_claims=[_parsed_claim("row-a", "1")],
        connection=connection,
        write_fn=ok_writer,
    )
    assert result["statut"] == "complete"
    assert result["claims_ecrits"] == 1
    assert result["claims_inchanges"] == 0
    assert result["claims_retires"] == 1
    assert {r.entity_id for r in connection.rows} == {"row-a"}


def test_k4_identical_rerun_zero_written_zero_removed():
    file_name = "data.csv"
    connection = FakeTabularConnection([_tabular_claim("row-a", "1", file_name)])
    key = compute_natural_key(
        AtomicClaim(
            entity_id="row-a",
            predicate="note.body",
            value="1",
            qualifiers={"attribute_id": "row-a"},
            modality="asserted",
        )
    )

    def noop_writer(claims, **_kwargs):
        return VersionedWriteResult(written=[], unchanged=[{"natural_key": key}])

    result = sync_tabular_claims_for_piece(
        file_name=file_name,
        parsed_claims=[_parsed_claim("row-a", "1")],
        connection=connection,
        write_fn=noop_writer,
    )
    assert result["claims_ecrits"] == 0
    assert result["claims_inchanges"] == 1
    assert result["claims_retires"] == 0
    assert len(connection.rows) == 1


def test_k4_rewrite_tabular_piece_does_not_delete_before_read(monkeypatch, tmp_path):
    calls: list[str] = []

    def track_delete(connection, file_name):
        calls.append("delete")
        return 0

    def track_extract(**_kwargs):
        calls.append("extract")
        return SimpleNamespace(claims=[], tables=[], data_row_count=0, illisible_lines=0)

    monkeypatch.setattr("banc_realite.ingest_runner.delete_tabular_claims_for_piece", track_delete)
    monkeypatch.setattr("brain.claiming.tabular.extract_tabular_claims", track_extract)
    path = tmp_path / "data.csv"
    path.write_text("| A |\n| --- |\n| 1 |\n", encoding="utf-8")

    rewrite_tabular_piece(
        path,
        db_url="http://localhost",
        db_key="key",
        connection=FakeTabularConnection(),
    )
    assert calls == ["extract"]
