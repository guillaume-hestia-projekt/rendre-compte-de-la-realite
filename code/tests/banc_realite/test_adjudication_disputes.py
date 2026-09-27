import json

from banc_realite import etage3 as e3


def _gl_q073_dispute() -> dict:
    return {
        "id": "gl-q073",
        "shape": "dispute",
        "must_mention": [
            "657",
            "683",
            "register",
            "internal service review",
            "customer review",
            "unresolved",
        ],
        "must_not_claim": [
            "One of the documents establishes the correct value.",
            "The difference can be silently discarded as rounding or a typo.",
        ],
    }


def _gl_q073_response() -> str:
    return (
        "Sources disagree on the Copper Kettle account total for 2024: "
        "**683** collections (`24-customer-review.md`) / "
        "**657** collections (`20-internal-service-review.md`, "
        "`17-collection-register.md`)"
    )


def _judge_ok() -> dict:
    return {
        "jugements": [
            {"numero": 1, "verdict": "n_affirme_pas", "preuve_verifiable": True},
            {"numero": 2, "verdict": "n_affirme_pas", "preuve_verifiable": True},
        ],
        "refus": False,
    }


def test_must_mention_present_source_filename_matching():
    assert e3.must_mention_present("customer review", "see `24-customer-review.md`")
    assert e3.must_mention_present("weigh-ticket index", "18-weigh-ticket-index.md")
    assert e3.must_mention_present("CSV", "22-recorded-visits.csv")
    assert not e3.must_mention_present("register", "registered")
    assert e3.must_mention_present("657", "657 collections")
    assert not e3.must_mention_present("657", "6570")


def test_dispute_conforme_when_sources_cited_by_filename_without_unresolved():
    question = _gl_q073_dispute()
    response = _gl_q073_response()
    assert e3.compute_verdict(question, response, _judge_ok()) == "conforme"
    scoring = e3.must_mention_scoring_fields(question, response)
    assert scoring["must_mention_manquants"] == []
    assert scoring["termes_exemptes"] == ["unresolved"]


def test_dispute_incomplete_when_number_missing_and_unresolved_not_listed():
    question = _gl_q073_dispute()
    response = _gl_q073_response().replace("683", "six hundred")
    scoring = e3.must_mention_scoring_fields(question, response)
    assert e3.compute_verdict(question, response, _judge_ok()) == "incomplete"
    assert "683" in scoring["must_mention_manquants"]
    assert "unresolved" not in scoring["must_mention_manquants"]


def test_dispute_fautive_when_judge_affirms_with_proof():
    question = _gl_q073_dispute()
    judge = {
        "jugements": [
            {
                "numero": 1,
                "verdict": "affirme",
                "citation": "establishes the correct value",
                "preuve_verifiable": True,
            }
        ],
        "refus": False,
    }
    assert e3.compute_verdict(question, _gl_q073_response(), judge) == "fautive"


def test_dispute_a_verifier_when_judge_affirms_without_proof():
    question = _gl_q073_dispute()
    judge = {
        "jugements": [
            {
                "numero": 1,
                "verdict": "affirme",
                "citation": "not in text",
                "preuve_verifiable": False,
            }
        ],
        "refus": False,
    }
    assert e3.compute_verdict(question, _gl_q073_response(), judge) == "a_verifier"


def test_single_shape_still_requires_unresolved():
    question = {
        "id": "gl-q001",
        "shape": "single",
        "must_mention": ["30 days", "unresolved"],
        "must_not_claim": [],
    }
    assert e3.compute_verdict(question, "term is 30 days", _judge_ok()) == "incomplete"
    scoring = e3.must_mention_scoring_fields(question, "term is 30 days")
    assert scoring["termes_exemptes"] == []
    assert "unresolved" in scoring["must_mention_manquants"]


def test_termes_exemptes_on_notation_line(tmp_path):
    dispute = _gl_q073_dispute()
    single = {
        "id": "gl-q001",
        "shape": "single",
        "must_mention": ["30 days"],
        "must_not_claim": [],
        "question": "What is the term?",
    }
    invites_path = tmp_path / "invites.jsonl"
    calls_path = tmp_path / "calls.jsonl"
    invites = [
        {
            "id": "fine_tours_k12-gl-q073",
            "bras": "fine_tours_k12",
            "config": "fine_tours_k12",
            "question_id": "gl-q073",
        },
        {
            "id": "A-gl-q001",
            "bras": "A",
            "question_id": "gl-q001",
        },
    ]
    invites_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )
    call_rows: list[dict] = []
    for invite in invites:
        call_rows.append(
            {
                "id": invite["id"],
                "role": "reponse",
                "reponse_brute": _gl_q073_response()
                if invite["question_id"] == "gl-q073"
                else "term is 30 days",
            }
        )
        call_rows.append(
            {
                "id": f"juge-{invite['id']}",
                "role": "juge",
                **(
                    _judge_ok()
                    if invite["question_id"] == "gl-q073"
                    else {"jugements": [], "refus": False}
                ),
            }
        )
    calls_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in call_rows),
        encoding="utf-8",
    )
    payload = e3.run_noter(
        calls_path=calls_path,
        invites_path=invites_path,
        output_path=tmp_path / "notes.json",
    )
    dispute_line = next(n for n in payload["notes"] if n["question_id"] == "gl-q073")
    single_line = next(n for n in payload["notes"] if n["question_id"] == "gl-q001")
    assert dispute_line["termes_exemptes"] == ["unresolved"]
    assert single_line["termes_exemptes"] == []
