"""Verdict functions and holders instrument — no network, no database."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from banc_realite.holders import (
    PieceCache,
    build_holder_table,
    classify_pair,
    overlap_index,
)
from banc_realite.restitution import (
    compute_verdict,
    verdict_aggregate,
    verdict_dispute,
    verdict_single,
    verdict_status,
    verdict_unknown,
)


def _gold():
    assertion = {
        "id": "a1",
        "source": "documents/x.md",
        "quote": "two containers",
        "content": "two containers removed",
    }
    return {
        "assertion_index": {
            "a1": assertion,
            "a2": {**assertion, "id": "a2", "quote": "three containers"},
            "a3": {**assertion, "id": "a3", "quote": "four containers"},
        },
        "disputes": [
            {
                "id": "d1",
                "question": "How many?",
                "sides": [{"assertion": "a1"}, {"assertion": "a2"}],
            }
        ],
        "situations": [
            {
                "id": "s1",
                "trajectory": "tr1",
                "assertions": [{"id": "a1"}],
            }
        ],
        "trajectories": [{"id": "tr1", "versions": [{"assertion": "a1"}, {"assertion": "a2"}]}],
        "assertions": [assertion],
    }


def _claims():
    return {
        "c-tab": {
            "claim_id": "c-tab",
            "entity_id": "e",
            "value": "two containers removed",
            "text": "two containers removed",
            "piece": "x.md",
            "source_file_path": "documents/x.md",
            "extracted_by_skill": "tabulaire-deterministe",
            "source_span": {"raw_line": "two containers removed from site"},
            "qualifiers": {},
        },
        "c-model": {
            "claim_id": "c-model",
            "entity_id": "containers",
            "value": "2",
            "text": "2",
            "piece": "x.md",
            "source_file_path": "documents/x.md",
            "extracted_by_skill": "note.body",
            "qualifiers": {"attribute_id": "count"},
            "source_span": {"line_start": 10, "line_end": 10},
        },
        "c-other": {
            "claim_id": "c-other",
            "entity_id": "containers",
            "value": "2",
            "text": "2",
            "piece": "y.md",
            "source_file_path": "documents/y.md",
            "extracted_by_skill": "note.body",
            "qualifiers": {"attribute_id": "count"},
        },
        "c1": {
            "claim_id": "c1",
            "text": "two containers removed",
            "piece": "x.md",
            "value": "two",
            "qualifiers": {},
        },
        "c2": {
            "claim_id": "c2",
            "text": "three containers removed",
            "piece": "x.md",
            "value": "three",
            "qualifiers": {},
        },
    }


def test_tient_tabular_raw_line():
    gold = _gold()
    claims = _claims()
    assertion = gold["assertion_index"]["a1"]
    element = {"kind": "claim_hit", "id": "c-tab", "text": "x"}
    assert classify_pair(assertion, element, claims) == "tient"


def test_tient_passage_same_piece():
    gold = _gold()
    claims = _claims()
    assertion = gold["assertion_index"]["a1"]
    element = {
        "kind": "file_hit",
        "id": "f1",
        "text": "we removed two containers today",
        "source": "documents/x.md",
    }
    assert classify_pair(assertion, element, claims) == "tient"


def test_non_passage_other_piece():
    gold = _gold()
    claims = _claims()
    assertion = gold["assertion_index"]["a1"]
    element = {
        "kind": "file_hit",
        "id": "f1",
        "text": "we removed two containers today",
        "source": "documents/y.md",
    }
    assert classify_pair(assertion, element, claims) == "non"


def test_candidat_model_same_piece():
    gold = _gold()
    claims = _claims()
    assertion = gold["assertion_index"]["a1"]
    element = {"kind": "claim_hit", "id": "c-model", "text": "2"}
    assert classify_pair(assertion, element, claims) == "candidat"


def test_non_model_other_piece():
    gold = _gold()
    claims = _claims()
    assertion = gold["assertion_index"]["a1"]
    element = {"kind": "claim_hit", "id": "c-other", "text": "2"}
    assert classify_pair(assertion, element, claims) == "non"


def test_plancher_differs_from_plafond():
    gold = _gold()
    claims = _claims()
    question = {
        "shape": "aggregate",
        "supporting_assertions": ["a1"],
    }
    evidence = [{"kind": "claim_hit", "id": "c-model"}]
    present_plancher = lambda aid: (False, None)
    present_plafond = lambda aid: (True, 1)
    v_plancher = verdict_aggregate(question, present_plancher)
    v_plafond = verdict_aggregate(question, present_plafond)
    assert v_plancher["verdict"] == "echec"
    assert v_plafond["verdict"] == "reussi"


def test_dispute_un_seul_cote_plancher_and_plafond():
    gold = _gold()
    claims = _claims()
    question = {"shape": "dispute", "question": "How many?", "supporting_assertions": ["a1", "a2"]}
    evidence = [{"kind": "claim_hit", "id": "c1"}]
    present = lambda aid: (aid == "a1", 1)
    for mode_label in ("plancher", "plafond"):
        verdict = verdict_dispute(question, present, disputes=gold["disputes"])
        assert verdict["verdict"] == "un_seul_cote", mode_label


def test_dispute_complet_and_aucun():
    gold = _gold()
    question = {"shape": "dispute", "question": "How many?", "supporting_assertions": ["a1", "a2"]}
    present_both = lambda aid: (True, 1)
    present_none = lambda aid: (False, None)
    assert verdict_dispute(question, present_both, disputes=gold["disputes"])["verdict"] == "complet"
    assert verdict_dispute(question, present_none, disputes=gold["disputes"])["verdict"] == "aucun"


def test_unknown_never_judged():
    gold = _gold()
    question = {"shape": "unknown", "supporting_assertions": ["a1"]}
    present = lambda aid: (True, 1)
    verdict = verdict_unknown(question, [{"score": 0.9}], present)
    assert verdict["verdict"] == "non_mesurable_etage2"


def test_no_hors_de_portee_verdict():
    gold = _gold()
    question = {"shape": "single", "supporting_assertions": ["a9"]}
    present = lambda aid: (False, None)
    verdict = verdict_single(question, present)
    assert verdict["verdict"] == "echec"
    assert verdict.get("verdict") != "hors_de_portee"


def test_b5_attribution_categories():
    from banc_realite.diagnostic import attribute_missing_support

    gold = _gold()
    claims = list(_claims().values())
    claims_index = _claims()
    holder = {"a1": [{"claim_id": "c1", "piece": "x.md"}]}
    question = {"id": "q1", "question": "How many?", "supporting_assertions": ["a1"]}
    connection = object()

    with patch("banc_realite.diagnostic.jambe_diagnostic", return_value={}):
        d1 = attribute_missing_support(
            assertion_id="a1",
            question=question,
            evidence_k20=[],
            fused_k50=[],
            holder_table={},
            claims=[],
            claims_index=claims_index,
            gold=gold,
            connection=connection,
        )
        assert d1["cause"] == "jamais en mémoire"

        d2 = attribute_missing_support(
            assertion_id="a1",
            question=question,
            evidence_k20=[],
            fused_k50=[],
            holder_table={},
            claims=[claims_index["c-model"]],
            claims_index=claims_index,
            gold=gold,
            connection=connection,
        )
        assert d2["cause"] == "en mémoire, candidat seulement"

        d3 = attribute_missing_support(
            assertion_id="a1",
            question=question,
            evidence_k20=[],
            fused_k50=[{"id": "other"}],
            holder_table=holder,
            claims=claims,
            claims_index=claims_index,
            gold=gold,
            connection=connection,
        )
        assert d3["cause"] == "en mémoire, hors du classement nu à 50"

        fused_long = [{"id": f"x{i}"} for i in range(25)] + [{"id": "c1"}]
        d4 = attribute_missing_support(
            assertion_id="a1",
            question=question,
            evidence_k20=[],
            fused_k50=fused_long,
            holder_table=holder,
            claims=claims,
            claims_index=claims_index,
            gold=gold,
            connection=connection,
        )
        assert d4["cause"] == "dans le classement nu, coupé par k"
        assert d4["rang"] == 26

        d5 = attribute_missing_support(
            assertion_id="a1",
            question=question,
            evidence_k20=[],
            fused_k50=[{"id": "c1"}],
            holder_table=holder,
            claims=claims,
            claims_index=claims_index,
            gold=gold,
            connection=connection,
        )
        assert d5["cause"] == "dans le classement nu, écarté à la composition"
        assert d5["rang"] == 1


def test_paires_dedup():
    from banc_realite.measure_etage2 import _dedupe_paires

    rows = [
        {
            "assertion_id": "a1",
            "claim_id": "c1",
            "overlap": 0.5,
            "question_id": "q1",
            "assertion": {"id": "a1"},
            "fait": {"claim_id": "c1"},
        },
        {
            "assertion_id": "a1",
            "claim_id": "c1",
            "overlap": 0.5,
            "question_id": "q2",
            "assertion": {"id": "a1"},
            "fait": {"claim_id": "c1"},
        },
    ]
    out = _dedupe_paires(rows)
    assert len(out) == 1
    assert sorted(out[0]["questions"]) == ["q1", "q2"]


def test_cache_avoids_double_read(tmp_path: Path):
    piece = tmp_path / "x.md"
    piece.write_text("line1\nline2 two containers\nline3\n", encoding="utf-8")
    cache = PieceCache(corpus=tmp_path)
    cache.find_quote_line("x.md", "two containers")
    cache.find_quote_line("x.md", "two containers")
    assert cache.read_count == 1


def test_default_path_skips_etape0_and_purge():
    from banc_realite.run_etage2 import plan_etage2_steps

    steps = plan_etage2_steps()
    assert "run_partie_a" not in steps
    assert "purge_markers" not in steps
    assert "verify_parity_readonly" in steps
    assert "run_tests" not in steps

    etape0_steps = plan_etage2_steps(etape0=True, purge_markers=True)
    assert "run_partie_a" in etape0_steps
    assert "purge_markers" in etape0_steps


def test_status_version_perimee_seule():
    gold = _gold()
    question = {"shape": "status", "supporting_assertions": ["a1"]}
    present = lambda aid: (True, 1)
    verdict = verdict_status(
        question,
        present,
        situations=gold["situations"],
        trajectories=gold["trajectories"],
    )
    assert verdict.get("version_perimee_seule") is True


def test_overlap_index_sorting():
    gold = _gold()
    assertion = gold["assertion_index"]["a1"]
    high = {
        "entity_id": "containers",
        "value": "two",
        "qualifiers": {"attribute_id": "removed"},
    }
    low = {"entity_id": "zzz", "value": "999", "qualifiers": {}}
    assert overlap_index(assertion, high) > overlap_index(assertion, low)


def test_tient_requires_same_piece_for_claim():
    gold = _gold()
    claims = _claims()
    assertion = gold["assertion_index"]["a1"]
    duplicate_other_piece = {
        "claim_id": "c-dup",
        "entity_id": "e",
        "value": "two containers removed",
        "text": "two containers removed",
        "piece": "y.md",
        "source_file_path": "documents/y.md",
        "extracted_by_skill": "tabulaire-deterministe",
        "source_span": {"raw_line": "two containers removed from site"},
        "qualifiers": {},
    }
    claims["c-dup"] = duplicate_other_piece
    element = {"kind": "claim_hit", "id": "c-dup", "text": "two containers removed"}
    assert classify_pair(assertion, element, claims) == "non"


def test_search_health_rejects_degraded_warning():
    from banc_realite.search_health import is_search_healthy

    ok, _ = is_search_healthy(
        {
            "strategy": {"fusion": "rrf_v1", "notes": []},
            "warnings": ["claims_vector_mistral_embed_unavailable: HTTP 429"],
        }
    )
    assert not ok
    ok2, _ = is_search_healthy(
        {
            "strategy": {"fusion": "rrf_v1", "notes": []},
            "warnings": ["assets_metadata_no_perceptual_memory"],
        }
    )
    assert ok2


def test_cached_embed_fn_raises_on_missing_text():
    from banc_realite.measure_etage2 import cached_embed_factory

    cache = {"What is the total?": [0.1, 0.2]}
    embed_fn = cached_embed_factory(cache)
    assert embed_fn("What is the total?") == [0.1, 0.2]
    with pytest.raises(RuntimeError, match="cache froid"):
        embed_fn("What is the total? GreenLoop")


def test_ingest_log_redirected_to_tmp_path(tmp_path):
    from banc_realite import ingest_runner

    assert str(ingest_runner.INGEST_LOG).startswith(str(tmp_path))
    ingest_runner.INGEST_LOG.write_text('{"file":"data.csv"}\n', encoding="utf-8")
    assert ingest_runner.INGEST_LOG.is_file()
    assert "/home/ubuntu/.agents/var/banc-realite/sorties/ingestion.jsonl" != str(
        ingest_runner.INGEST_LOG
    )


def test_build_holder_table_fast():
    gold = _gold()
    claims = list(_claims().values())
    table, elapsed, _ = build_holder_table(claims, gold)
    assert elapsed < 120
    assert any(h["claim_id"] == "c-tab" for h in table["a1"])
