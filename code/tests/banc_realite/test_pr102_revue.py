"""PR #102 — reprise : rejeu stabilité manquant, agrégation journal par run_id."""

import json
from pathlib import Path

from banc_realite import etage3 as e3
from banc_realite import etage3_config_gagnante as ecg
from banc_realite.run_ingestion2 import sum_tabular_rejections_from_journal
from banc_realite.run_ingestion3 import sum_journal_scopes


def test_run_reponses_rattrape_rejeu_stabilite_manquant(tmp_path, monkeypatch):
    calls_path = tmp_path / "calls.jsonl"
    gold_questions = e3.load_questions()
    stab_qid = ecg.stability_pairs_config(gold_questions)[0][1]
    stab_ident = e3.invite_id(ecg.CONFIG, stab_qid)
    other_q = next(q for q in gold_questions if q["id"] != stab_qid)
    questions = [q for q in gold_questions if q["id"] in {stab_qid, other_q["id"]}]
    cadres = {q["id"]: {"rendered": f"ctx {q['id']}"} for q in questions}
    invites = ecg.build_response_invites(questions, cadres)
    other_invite = next(inv for inv in invites if inv["id"] != stab_ident)
    stab_invite = next(inv for inv in invites if inv["id"] == stab_ident)

    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:00+00:00",
            "role": "reponse",
            "id": stab_ident,
            "bras": ecg.CONFIG,
            "question_id": stab_qid,
            "sha256_invite": stab_invite["sha256"],
            "reponse_brute": "stab main",
            "final": True,
        },
    )
    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:01+00:00",
            "role": "reponse",
            "id": other_invite["id"],
            "bras": ecg.CONFIG,
            "question_id": other_invite["question_id"],
            "sha256_invite": other_invite["sha256"],
            "reponse_brute": "other done",
            "final": True,
        },
    )

    call_count = 0

    def chat(_system, _user):
        nonlocal call_count
        call_count += 1
        return "rejeu answer", {}

    monkeypatch.setattr(ecg, "load_invites_reponses", lambda path=None: invites)
    ecg.run_reponses(chat, calls_path=calls_path)

    assert call_count == 1
    records = e3.load_journal_records(calls_path)
    rejeu_id = e3.stability_rejeu_id(stab_ident)
    assert any(r.get("id") == rejeu_id for r in records)


def test_sum_tabular_rejections_filters_by_run_id(tmp_path: Path):
    log = tmp_path / "ingestion.jsonl"
    records = [
        {
            "run_id": "run-a",
            "tabular_marker_claims_dropped": 10,
            "tabular_marker_claims_dropped_unanchored": 3,
        },
        {
            "run_id": "run-b",
            "tabular_marker_claims_dropped": 20,
            "tabular_marker_claims_dropped_unanchored": 7,
        },
    ]
    log.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8",
    )
    dropped, unanchored = sum_tabular_rejections_from_journal(log, run_id="run-b")
    assert dropped == 20
    assert unanchored == 7
    dropped_all, unanchored_all = sum_tabular_rejections_from_journal(log)
    assert dropped_all == 30
    assert unanchored_all == 10


def test_sum_journal_scopes_filters_by_run_id(tmp_path: Path):
    log = tmp_path / "ingestion.jsonl"
    records = [
        {
            "run_id": "run-a",
            "mode": "tabulaire-ordinaire-reprise",
            "faits_ligne": 10,
            "faits_cellule": 5,
        },
        {
            "run_id": "run-b",
            "mode": "tabulaire-ordinaire-reprise",
            "faits_ligne": 20,
            "faits_cellule": 15,
        },
    ]
    log.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
        encoding="utf-8",
    )
    ligne, cellule = sum_journal_scopes(
        log, mode="tabulaire-ordinaire-reprise", run_id="run-b"
    )
    assert ligne == 20
    assert cellule == 15
    ligne_all, cellule_all = sum_journal_scopes(log, mode="tabulaire-ordinaire-reprise")
    assert ligne_all == 30
    assert cellule_all == 20
