import json
import os
from pathlib import Path

import pytest

from banc_realite import etage3 as e3


@pytest.fixture
def gold_questions():
    return e3.load_questions()


@pytest.fixture
def tmp_etage3(tmp_path, gold_questions, monkeypatch):
    monkeypatch.setattr(e3, "BRAS_B_PATH", tmp_path / "bras-B-questions.json")
    monkeypatch.setattr(e3, "INVITES_REPONSES_PATH", tmp_path / "invites-reponses.jsonl")
    monkeypatch.setattr(e3, "APPELS_PATH", tmp_path / "appels.jsonl")
    monkeypatch.setattr(e3, "SORTIES_ETAGE3", tmp_path)
    return tmp_path


def test_stratified_sample_is_deterministic_and_respects_minimum(gold_questions):
    first = e3.stratified_sample_bras_b(gold_questions)
    second = e3.stratified_sample_bras_b(gold_questions)
    assert first == second
    assert len(first) == e3.BRAS_B_SIZE
    from collections import Counter

    by_shape = Counter(item["shape"] for item in first)
    assert all(count >= e3.BRAS_B_MIN_PER_SHAPE for count in by_shape.values())
    assert sum(by_shape.values()) == e3.BRAS_B_SIZE


def test_frozen_bras_b_is_not_regenerated(tmp_etage3, gold_questions):
    payload = e3.load_or_create_bras_b_questions(gold_questions)
    ids = list(payload["question_ids"])
    payload["question_ids"] = ["gl-q999"]
    e3.BRAS_B_PATH.write_text(json.dumps(payload), encoding="utf-8")
    reloaded = e3.load_or_create_bras_b_questions(gold_questions)
    assert reloaded["question_ids"] == ["gl-q999"]
    assert reloaded["question_ids"] != ids


def test_instructions_identical_across_bras(gold_questions):
    cadres = {
        q["id"]: {"rendered": f"context for {q['id']}", "frame_id": "f", "caracteres": 10, "genres": {}}
        for q in gold_questions
    }
    sampled = e3.stratified_sample_bras_b(gold_questions)
    invites = e3.build_all_response_invites(
        gold_questions,
        {q["id"] for q in sampled},
        corpus_context="=== doc.md ===\nbody",
        cadres_c=cadres,
    )
    assert len(invites) == 141 + 141 + 42
    assert e3.instructions_identical(invites)
    systems = {invite["system"] for invite in invites}
    assert systems == {e3.SYSTEM_PROMPT}
    a_user = next(i for i in invites if i["bras"] == "A")["user"]
    c_user = next(i for i in invites if i["bras"] == "C")["user"]
    assert "Question:" in a_user and "Question:" in c_user
    assert a_user.startswith(e3.CONTEXT_A)


def test_must_mention_integer_token_cases():
    assert e3.must_mention_present("2", "value is 2 only")
    assert not e3.must_mention_present("2", "year 2025")
    assert not e3.must_mention_present("2", "there are 12 items")
    assert e3.must_mention_present("9,761.87", "total 9761.87 EUR")
    assert e3.must_mention_present("13.334 t", "mass 13.334 tonnes")
    assert e3.must_mention_present("Copper Kettle", "customer Copper Kettle signed")


def test_validate_judge_response_alphabet_and_citation():
    response = "Payment is due on receipt for this account."
    ok = e3.validate_judge_response(
        {
            "jugements": [
                {"numero": 1, "verdict": "affirme", "citation": "due on receipt"},
            ],
            "refus": False,
        },
        response_text=response,
        expected_count=1,
    )
    assert ok["ok"] is True
    assert ok["jugements"][0]["preuve_verifiable"] is True
    bad_alpha = e3.validate_judge_response(
        {"jugements": [{"numero": 1, "verdict": "maybe", "citation": ""}], "refus": False},
        response_text=response,
        expected_count=1,
    )
    assert bad_alpha["ok"] is False
    bad_cite = e3.validate_judge_response(
        {
            "jugements": [
                {"numero": 1, "verdict": "affirme", "citation": "not in text"},
            ],
            "refus": False,
        },
        response_text=response,
        expected_count=1,
    )
    assert bad_cite["jugements"][0]["preuve_verifiable"] is False


def test_judge_illisible_after_one_retry(tmp_path):
    calls = 0

    def chat(_system, _user):
        nonlocal calls
        calls += 1
        return "not json", {}

    question = {
        "id": "gl-q001",
        "question": "What is the account-card payment term?",
        "must_not_claim": ["Due on receipt is the account-card term."],
    }
    result = e3.adjudicate_judge(
        "some answer",
        question,
        invite_key="juge-A-gl-q001",
        chat_fn=chat,
        calls_path=tmp_path / "calls.jsonl",
    )
    assert calls == 2
    assert result.get("illisible") is True


def test_judge_shuffle_order_is_hashlib_deterministic():
    claims = [
        "One of the documents establishes the correct value.",
        "The account card term is due on receipt.",
        "The contract was signed in 2024.",
    ]
    response = "A fixed response for deterministic shuffle."
    question_id = "gl-q001"
    _, order = e3.build_judge_user(
        response,
        claims,
        question_id=question_id,
        question_text="What is the account-card payment term?",
    )
    assert order == [3, 1, 2]


def test_judge_invite_includes_question_before_answer(gold_questions):
    question = gold_questions[0]
    user, _order = e3.build_judge_user(
        "A sample answer without forbidden content.",
        question["must_not_claim"],
        question_id=question["id"],
        question_text=question["question"],
    )
    q_pos = user.index("Question asked:")
    a_pos = user.index("Answer to judge:")
    assert q_pos < a_pos
    assert question["question"] in user


def test_judge_invite_is_blind(gold_questions):
    question = gold_questions[0]
    user, _order = e3.build_judge_user(
        "A sample answer without forbidden content.",
        question["must_not_claim"],
        question_id=question["id"],
        question_text=question["question"],
    )
    assert "Question asked:" in user
    assert question["question"] in user
    errors = e3.audit_judge_invite(user, question)
    assert errors == []
    bad = user + "\n" + question["answer"]
    assert e3.audit_judge_invite(bad, question) != []


def test_verdict_conforme_incomplete_fautive():
    question = {
        "must_mention": ["30 days", "account card"],
        "must_not_claim": ["Due on receipt is the account-card term."],
        "shape": "single",
    }
    judge_ok = {"jugements": [{"verdict": "n_affirme_pas", "preuve_verifiable": True}], "refus": False}
    assert e3.compute_verdict(question, "term is 30 days on the account card", judge_ok) == "conforme"
    assert (
        e3.compute_verdict(question, "term is 30 days", judge_ok) == "incomplete"
    )
    judge_bad = {
        "jugements": [{"verdict": "affirme", "preuve_verifiable": True}],
        "refus": False,
    }
    assert (
        e3.compute_verdict(
            question,
            "Due on receipt is the account-card term and 30 days on account card",
            judge_bad,
        )
        == "fautive"
    )


def test_x4_illisible_verdict_is_indetermine():
    question = {
        "must_mention": ["30 days"],
        "must_not_claim": ["Due on receipt is the account-card term."],
        "shape": "single",
    }
    judge = {"jugements": [], "refus": False, "illisible": True}
    assert e3.compute_verdict(question, "some answer", judge) == "indetermine"


def test_p1_affirme_sans_citation_verifiable_est_a_verifier():
    question = {
        "must_mention": ["30 days"],
        "must_not_claim": ["Due on receipt is the account-card term."],
        "shape": "single",
    }
    judge = {
        "jugements": [
            {
                "verdict": "affirme",
                "preuve_verifiable": False,
                "citation": "not in text",
            }
        ],
        "refus": False,
    }
    assert e3.compute_verdict(question, "term is 30 days", judge) == "a_verifier"


def test_x5_numero_invalide_declenche_relance(tmp_path):
    calls = 0

    def chat(_system, _user):
        nonlocal calls
        calls += 1
        if calls == 1:
            return json.dumps(
                {
                    "jugements": [{"numero": "x", "verdict": "n_affirme_pas", "citation": ""}],
                    "refus": False,
                }
            ), {}
        return json.dumps(
            {
                "jugements": [{"numero": 1, "verdict": "n_affirme_pas", "citation": ""}],
                "refus": False,
            }
        ), {}

    question = {
        "id": "gl-q001",
        "question": "What is the account-card payment term?",
        "must_not_claim": ["Due on receipt is the account-card term."],
    }
    result = e3.adjudicate_judge(
        "some answer",
        question,
        invite_key="juge-A-gl-q001",
        chat_fn=chat,
        calls_path=tmp_path / "calls.jsonl",
    )
    assert calls == 2
    assert result["ok"] is True


def test_x1_run_juge_sans_reponse_ne_consomme_pas_d_appel(tmp_path, gold_questions):
    invites_path = tmp_path / "invites.jsonl"
    calls_path = tmp_path / "calls.jsonl"
    invite = e3.build_response_invite("A", gold_questions[0], context=e3.CONTEXT_A)
    invites_path.write_text(json.dumps(invite, ensure_ascii=False) + "\n", encoding="utf-8")
    calls = 0

    def chat(_system, _user):
        nonlocal calls
        calls += 1
        return "{}", {}

    e3.run_juge(chat, calls_path=calls_path)
    assert calls == 0
    assert not calls_path.exists()


def test_x2_juge_non_final_peut_reprendre(tmp_path):
    calls_path = tmp_path / "calls.jsonl"
    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:00+00:00",
            "role": "juge",
            "id": "juge-A-gl-q001",
            "question_id": "gl-q001",
            "sha256_invite": "abc",
            "reponse_brute": "bad",
            "tentative": 1,
            "final": False,
        },
    )
    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:01+00:00",
            "role": "reponse",
            "id": "A-gl-q001",
            "reponse_brute": "answer text",
            "final": True,
        },
    )
    completed, invite_hashes = e3.load_journal_state(calls_path)
    assert "juge-A-gl-q001" not in completed
    assert "juge-A-gl-q001" in invite_hashes
    calls = 0

    def chat(_system, _user):
        nonlocal calls
        calls += 1
        return json.dumps(
            {
                "jugements": [{"numero": 1, "verdict": "n_affirme_pas", "citation": ""}],
                "refus": False,
            }
        ), {}

    question = {
        "id": "gl-q001",
        "question": "Q?",
        "must_not_claim": ["claim one"],
    }
    e3.adjudicate_judge(
        "answer text",
        question,
        invite_key="juge-A-gl-q001",
        chat_fn=chat,
        calls_path=calls_path,
    )
    assert calls == 1


def test_x3_stabilite_utilise_identifiant_rejeu(tmp_path, gold_questions):
    calls_path = tmp_path / "calls.jsonl"
    invite = e3.build_response_invite("C", gold_questions[0], context="ctx")
    calls = 0

    def chat(_system, _user):
        nonlocal calls
        calls += 1
        return f"answer-{calls}", {}

    e3.adjudicate_response(invite, chat_fn=chat, calls_path=calls_path)
    e3.adjudicate_response(
        invite,
        chat_fn=chat,
        calls_path=calls_path,
        record_id=e3.stability_rejeu_id(invite["id"]),
    )
    records = e3.load_journal_records(calls_path)
    ids = [r["id"] for r in records if r.get("role") == "reponse"]
    assert ids == ["C-gl-q001", "C-gl-q001#rejeu"]
    obs = e3._response_observations(calls_path, invite["id"])
    assert len(obs) == 2


def test_x6_run_depuis_journal_transmet_invites_path(tmp_path, gold_questions, monkeypatch):
    invites_path = tmp_path / "invites.jsonl"
    calls_path = tmp_path / "calls.jsonl"
    output_path = tmp_path / "notations.json"
    invite = e3.build_response_invite("A", gold_questions[0], context=e3.CONTEXT_A)
    invites_path.write_text(json.dumps(invite, ensure_ascii=False) + "\n", encoding="utf-8")
    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:00+00:00",
            "role": "reponse",
            "id": invite["id"],
            "reponse_brute": "term is 30 days on the account card",
            "final": True,
        },
    )
    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:01+00:00",
            "role": "juge",
            "id": f"juge-{invite['id']}",
            "jugements": [{"verdict": "n_affirme_pas", "preuve_verifiable": True}],
            "refus": False,
            "final": True,
        },
    )
    seen: dict[str, Path | None] = {"invites_path": None}
    original = e3.run_noter

    def spy(*, calls_path=None, invites_path=None, output_path=None):
        seen["invites_path"] = invites_path
        return original(
            calls_path=calls_path,
            invites_path=invites_path,
            output_path=output_path or tmp_path / "notations-spy.json",
        )

    monkeypatch.setattr(e3, "run_noter", spy)
    e3.run_depuis_journal(calls_path=calls_path, invites_path=invites_path)
    assert seen["invites_path"] == invites_path


def test_p2_nombres_attendus_et_controle_tableaux(tmp_path, gold_questions):
    question = {
        "id": "gl-q002",
        "shape": "single",
        "must_mention": ["2023-05-24", "Copper Kettle"],
        "must_not_claim": [],
    }
    nombres = e3.compute_nombres_fields(question, "signed on 2023-05-24 by Copper Kettle")
    assert nombres["nombres_attendus"] == ["2023-05-24"]
    assert nombres["tous_les_nombres"] is True
    notes = [
        {
            "shape": "single",
            "bras": "A",
            "question_id": "gl-q002",
            "verdict": "incomplete",
            "tous_les_nombres": False,
        },
        {
            "shape": "single",
            "bras": "B",
            "question_id": "gl-q002",
            "verdict": "conforme",
            "tous_les_nombres": True,
        },
    ]
    tableaux = e3._build_tableaux(notes, bras_b_ids={"gl-q002"})
    assert tableaux["bras_B"]["single"]["B"]["tous_les_nombres"] == "1/1"


def test_p3_stabilite_rapporte_taux_identiques(tmp_path, gold_questions):
    calls_path = tmp_path / "calls.jsonl"
    _bras, qid = e3.stability_pairs(gold_questions)[0]
    base_id = e3.invite_id("C", qid)
    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:00+00:00",
            "role": "reponse",
            "id": base_id,
            "reponse_brute": "same text 13.334",
            "final": True,
        },
    )
    e3.append_call(
        calls_path,
        {
            "horodatage": "2026-01-01T00:00:01+00:00",
            "role": "reponse",
            "id": e3.stability_rejeu_id(base_id),
            "reponse_brute": "same text 13.334",
            "final": True,
        },
    )
    stats = e3.compute_stabilite(calls_path, gold_questions)
    assert stats["couples"] >= 1
    assert stats["reponses_identiques"].startswith("1/")


def test_call_cap_counts_each_attempt(tmp_path, gold_questions):
    calls = 0

    def chat(_system, _user):
        nonlocal calls
        calls += 1
        return "answer text", {}

    invite = e3.build_response_invite("A", gold_questions[0], context=e3.CONTEXT_A)
    e3.MAX_CALLS = 1
    e3.adjudicate_response(invite, chat_fn=chat, calls_path=tmp_path / "cap.jsonl")
    assert calls == 1
    with pytest.raises(RuntimeError, match="plafond"):
        e3.adjudicate_response(invite, chat_fn=chat, calls_path=tmp_path / "cap.jsonl")
    e3.MAX_CALLS = 800


def test_resume_stops_when_invite_hash_changes(tmp_path, gold_questions):
    invite = e3.build_response_invite("A", gold_questions[0], context=e3.CONTEXT_A)
    calls_path = tmp_path / "calls.jsonl"

    def chat(_system, _user):
        return "answer", {}

    e3.adjudicate_response(invite, chat_fn=chat, calls_path=calls_path)
    invite["user"] = invite["user"] + " changed"
    invite["sha256"] = e3.sha256_text(invite["user"])
    completed, hashes = e3.load_journal_state(calls_path)
    with pytest.raises(RuntimeError, match="invite modifiée"):
        e3.verify_invite_hash(invite["id"], hashes[invite["id"]], invite)


def test_limite_omits_unprocessed(tmp_path, gold_questions):
    calls_path = tmp_path / "calls.jsonl"
    invites_path = tmp_path / "invites.jsonl"
    invites = [
        e3.build_response_invite("A", gold_questions[0], context=e3.CONTEXT_A),
        e3.build_response_invite("A", gold_questions[1], context=e3.CONTEXT_A),
    ]
    invites_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )

    def chat(_system, _user):
        return "answer", {}

    e3.adjudicate_response(invites[0], chat_fn=chat, calls_path=calls_path)
    payload = e3.run_noter(
        calls_path=calls_path,
        invites_path=invites_path,
        output_path=tmp_path / "notes.json",
    )
    assert payload["complet"] is False
    assert invites[1]["id"] in payload["manquants"]


def test_relay_factory_raises_under_pytest():
    os.environ["PYTEST_CURRENT_TEST"] = "tests/banc_realite/test_etage3.py::test_relay"
    try:
        with pytest.raises(RuntimeError, match="interdit sous pytest"):
            e3.make_relay_chat_fn()
    finally:
        del os.environ["PYTEST_CURRENT_TEST"]


def test_compile_cadre_prod_rejette_retrieval_failed(monkeypatch):
    def fake_compile_call_frame(_req, search_fn=None):
        return {
            "rendered": "",
            "retrieval": {"evidence": [], "warnings": ["retrieval_failed:RuntimeError"]},
        }

    monkeypatch.setattr("brain.call_frame.compile_call_frame", fake_compile_call_frame)
    question = {"id": "gl-q001", "question": "What is the term?"}
    cache = {"What is the term?": [0.1, 0.2]}
    with pytest.raises(RuntimeError, match="recherche production échouée"):
        e3.compile_cadre_prod(question, top_k=8, embed_cache=cache)
