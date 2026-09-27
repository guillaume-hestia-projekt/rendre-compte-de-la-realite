"""Tests hors ligne — or par dossier et garde-fous de mesure."""
from __future__ import annotations

import copy

import pytest

from banc_realite import config
from banc_realite.dossiers import dossier_courant
from banc_realite.fidelite import load_gold
from banc_realite.holders import classify_pair
from banc_realite.measure_etage2 import load_questions
from banc_realite.or_dossier import verifier_or_coherent

MOREAU_GOLD = config.BANC_ROOT / "dossiers" / "moreau" / "gold" / "questions.json"
GREENLOOP_COUNTS = {
    "questions": 141,
    "assertions": 2403,
    "disputes": 45,
}


def test_load_gold_sans_argument_non_regression():
    gold = load_gold()
    assert len(gold["assertions"]) == GREENLOOP_COUNTS["assertions"]
    assert len(gold["disputes"]) == GREENLOOP_COUNTS["disputes"]
    assert len(gold["situations"]) > 0
    assert gold["assertion_index"]


def test_load_questions_sans_argument_non_regression():
    questions = load_questions()
    assert len(questions) == GREENLOOP_COUNTS["questions"]
    assert all(q["id"].startswith("gl-q") for q in questions)


@pytest.mark.skipif(
    not MOREAU_GOLD.is_file(),
    reason="or MOREAU absent sur disque (~/.agents/var/banc-realite/dossiers/moreau/gold)",
)
def test_load_questions_moreau():
    questions = load_questions("moreau")
    assert len(questions) == 50
    assert all(q["id"].startswith("MOR-Q") for q in questions)


@pytest.mark.skipif(
    not MOREAU_GOLD.is_file(),
    reason="or MOREAU absent sur disque (~/.agents/var/banc-realite/dossiers/moreau/gold)",
)
def test_load_gold_moreau_source_depuis_piece():
    gold = load_gold("moreau")
    assert len(gold["assertions"]) == 42
    for assertion in gold["assertions"]:
        piece = assertion.get("piece") or ""
        source = assertion.get("source") or ""
        assert source, f"{assertion['id']} sans source"
        assert source == piece, f"{assertion['id']} : source={source!r} piece={piece!r}"


@pytest.mark.skipif(
    not MOREAU_GOLD.is_file(),
    reason="or MOREAU absent sur disque (~/.agents/var/banc-realite/dossiers/moreau/gold)",
)
def test_moreau_classify_pair_verbatim_bout_en_bout():
    gold = load_gold("moreau")
    assertion = gold["assertion_index"]["MOR-A01"]
    piece = assertion["source"]
    corpus_path = dossier_courant("moreau").corpus_dir / piece
    text = corpus_path.read_text(encoding="utf-8")
    element = {
        "kind": "file_hit",
        "id": "f1",
        "text": text,
        "source": piece,
    }
    assert classify_pair(assertion, element, {}, mode_presence="verbatim") == "tient"


@pytest.mark.skipif(
    not MOREAU_GOLD.is_file(),
    reason="or MOREAU absent sur disque (~/.agents/var/banc-realite/dossiers/moreau/gold)",
)
def test_moreau_disputes_sont_contradictions():
    gold = load_gold("moreau")
    questions = load_questions("moreau")
    contradictions = [q for q in questions if q.get("shape") == "contradiction"]
    assert len(gold["disputes"]) == len(contradictions)
    assert {q["id"] for q in gold["disputes"]} == {q["id"] for q in contradictions}


def test_garde_fou_prefixe_greenloop_sur_dossier_moreau():
    dossier = dossier_courant("moreau")
    questions = load_questions("greenloop")
    gold = load_gold("moreau")
    with pytest.raises(ValueError, match=r"préfixe attendu 'MOR-Q', trouvé 'gl-q'"):
        verifier_or_coherent(dossier, questions, gold)


def test_garde_fou_piece_absente_du_corpus():
    dossier = dossier_courant("moreau")
    questions = load_questions("moreau")
    gold = load_gold("moreau")
    gold = copy.deepcopy(gold)
    gold["assertions"] = list(gold["assertions"])
    gold["assertions"].append(
        {
            "id": "MOR-A-test",
            "piece": "99-piece-inexistante.md",
            "source": "99-piece-inexistante.md",
            "quote": "test",
        }
    )
    with pytest.raises(ValueError, match=r"pièce '99-piece-inexistante.md' absente du corpus"):
        verifier_or_coherent(dossier, questions, gold)
