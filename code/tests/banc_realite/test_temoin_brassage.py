"""Tests hors ligne — témoin de brassage."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite.mesure_comparatif_etage2 import selection_questions_mesure
from banc_realite.temoin_brassage import (
    appariement_brassage,
    assertions_temoin_valeur,
    charger_contextes_mesure,
    charger_signal_etage2,
    compter_brassage,
    ecrire_temoin_rapport,
    formater_tableau,
    formater_tableau_avant_apres,
    mesurer_fournisseur_temoin,
    _lecture_ecarts,
)


def _element(text: str, source: str = "documents/piece-a.md") -> dict:
    return {"kind": "file_hit", "id": f"e:{text[:8]}", "text": text, "source": source}


def _assertion(aid: str, quote: str, source: str = "documents/piece-a.md") -> dict:
    return {"id": aid, "quote": quote, "content": quote, "source": source}


def test_appariement_brassage_stable_et_sans_auto():
    ids = ["gl-q003", "gl-q001", "gl-q002"]
    first = appariement_brassage(ids)
    second = appariement_brassage(ids)
    assert first == second
    assert first == {"gl-q001": "gl-q002", "gl-q002": "gl-q003", "gl-q003": "gl-q001"}
    for qid, donor in first.items():
        assert qid != donor


def test_signal_100_temoin_0_sur_jeu_aligne():
    questions = [
        {"id": "gl-q001", "supporting_assertions": ["a1"]},
        {"id": "gl-q002", "supporting_assertions": ["a2"]},
        {"id": "gl-q003", "supporting_assertions": ["a3"]},
    ]
    assertion_index = {
        "a1": _assertion("a1", "alpha unique 1111"),
        "a2": _assertion("a2", "beta unique 2222"),
        "a3": _assertion("a3", "gamma unique 3333"),
    }
    contexts = {
        "gl-q001": [_element("alpha unique 1111")],
        "gl-q002": [_element("beta unique 2222")],
        "gl-q003": [_element("gamma unique 3333")],
    }
    for mode in ("verbatim", "valeur"):
        result = compter_brassage(
            questions,
            contexts,
            assertion_index=assertion_index,
            claims_index={},
            mode_presence=mode,
        )
        assert result["signal"] == 3
        assert result["temoin"] == 0
        assert result["ecart"] == 3


def test_contextes_identiques_signal_egal_temoin():
    shared = [_element("texte commun avec quatre mots discriminants 42")]
    questions = [
        {"id": "gl-q001", "supporting_assertions": ["a1"]},
        {"id": "gl-q002", "supporting_assertions": ["a2"]},
    ]
    assertion_index = {
        "a1": _assertion("a1", "quatre mots discriminants 42"),
        "a2": _assertion("a2", "quatre mots discriminants 42"),
    }
    contexts = {"gl-q001": shared, "gl-q002": shared}
    for mode in ("verbatim", "valeur"):
        result = compter_brassage(
            questions,
            contexts,
            assertion_index=assertion_index,
            claims_index={},
            mode_presence=mode,
        )
        assert result["signal"] == result["temoin"]


def test_charger_signal_etage2_exclut_non_etabli(tmp_path, monkeypatch):
    etage2 = {
        "fournisseur": "mem0",
        "k_fixe": False,
        "runs": [
            {
                "k": 20,
                "budget": 12000,
                "questions": [
                    {
                        "question_id": "MOR-Q01",
                        "shape": "citation",
                        "appui_tout_tient": True,
                        "appui_au_moins_une": True,
                        "appui_tout_tient_valeur": True,
                        "appui_au_moins_une_valeur": True,
                    },
                    {
                        "question_id": "MOR-Q02",
                        "shape": "non_etabli",
                        "appui_tout_tient": True,
                        "appui_au_moins_une": True,
                        "appui_tout_tient_valeur": True,
                        "appui_au_moins_une_valeur": True,
                    },
                ],
            }
        ],
    }
    from banc_realite.dossiers import dossier_courant

    moreau = dossier_courant("moreau")
    monkeypatch.setattr(
        type(moreau),
        "comparatif_dir",
        property(lambda self, _p=tmp_path: _p),
    )
    (tmp_path / "etage2-mem0.json").write_text(json.dumps(etage2), encoding="utf-8")
    signal = charger_signal_etage2("mem0", k=20, budget=12000, k_fixe=False, dossier=moreau)
    assert signal == {"verbatim": 1, "valeur": 1}


def test_deux_modes_sans_modifier_signal_etage2(tmp_path, monkeypatch):
    etage2 = {
        "fournisseur": "mem0",
        "k_fixe": False,
        "runs": [
            {
                "k": 20,
                "budget": 12000,
                "questions": [
                    {
                        "question_id": "gl-q001",
                        "shape": "single",
                        "appui_tout_tient": True,
                        "appui_au_moins_une": True,
                        "appui_tout_tient_valeur": True,
                        "appui_au_moins_une_valeur": True,
                    },
                    {
                        "question_id": "gl-q002",
                        "shape": "single",
                        "appui_tout_tient": False,
                        "appui_au_moins_une": False,
                        "appui_tout_tient_valeur": False,
                        "appui_au_moins_une_valeur": False,
                    },
                ],
            }
        ],
    }
    from banc_realite.dossiers import dossier_courant

    greenloop = dossier_courant("greenloop")
    monkeypatch.setattr(
        type(greenloop),
        "comparatif_dir",
        property(lambda self, _p=tmp_path: _p),
    )
    (tmp_path / "etage2-mem0.json").write_text(json.dumps(etage2), encoding="utf-8")

    questions = [
        {"id": "gl-q001", "supporting_assertions": ["a1"]},
        {"id": "gl-q002", "supporting_assertions": ["a2"]},
    ]
    assertion_index = {
        "a1": _assertion("a1", "alpha 1000"),
        "a2": _assertion("a2", "beta 9999 introuvable"),
    }
    contexts = {
        "gl-q001": [_element("alpha 1000")],
        "gl-q002": [_element("beta 2000 sans correspondance")],
    }
    signal = charger_signal_etage2("mem0", k=20, budget=12000, k_fixe=False)
    assert signal == {"verbatim": 1, "valeur": 1}

    lignes, assertions = mesurer_fournisseur_temoin(
        "mem0",
        questions,
        k=20,
        budget=12000,
        k_fixe=False,
        assertion_index=assertion_index,
        claims_index={},
        contexts=contexts,
        signal_etage2=signal,
        denominateur=2,
    )
    assert len(lignes) == 2
    assert {row["mode"] for row in lignes} == {"verbatim", "valeur"}
    assert all(row["signal"] == 1 for row in lignes)
    assert all(row["temoin"] == 0 for row in lignes)
    assert assertions == []


def test_lecture_partielle_ne_nomme_pas_fournisseur_absent():
    lignes = [
        {
            "fournisseur": "mem0",
            "mode": "valeur",
            "signal": 40,
            "temoin": 15,
            "ecart": 25,
            "total": 141,
        }
    ]
    lecture = _lecture_ecarts(
        lignes,
        fournisseurs_attendus=["mem0", "brain_prod", "rag_naif", "brain_banc"],
    )
    assert "Exécution partielle" in lecture
    assert "mem0" in lecture
    assert "brain_prod :" not in lecture
    assert "2→47" not in lecture
    assert "témoin 0/141" not in lecture
    assert "dépasse nettement" not in lecture


def test_non_etabli_hors_numerateur_et_denominateur():
    questions = [
        {"id": "MOR-Q01", "shape": "citation", "supporting_assertions": ["a1"]},
        {"id": "MOR-Q02", "shape": "non_etabli", "supporting_assertions": []},
        {"id": "MOR-Q03", "shape": "citation", "supporting_assertions": ["a2"]},
    ]
    mesure = selection_questions_mesure(questions)
    assertion_index = {
        "a1": _assertion("a1", "alpha unique 1111"),
        "a2": _assertion("a2", "beta unique 2222"),
    }
    contexts = {
        "MOR-Q01": [_element("alpha unique 1111")],
        "MOR-Q02": [_element("alpha unique 1111")],
        "MOR-Q03": [_element("beta unique 2222")],
    }
    result = compter_brassage(
        mesure,
        contexts,
        assertion_index=assertion_index,
        claims_index={},
        mode_presence="verbatim",
    )
    assert result["total"] == 2
    assert result["signal"] == 2
    assert result["temoin"] == 0


def test_sans_appui_jamais_tout_tient():
    questions = [
        {"id": "gl-q001", "shape": "unknown", "supporting_assertions": []},
        {"id": "gl-q002", "shape": "single", "supporting_assertions": ["a1"]},
        {"id": "gl-q003", "shape": "single", "supporting_assertions": ["a2"]},
    ]
    assertion_index = {
        "a1": _assertion("a1", "alpha unique 1111"),
        "a2": _assertion("a2", "beta unique 2222"),
    }
    shared = [_element("alpha unique 1111 beta unique 2222")]
    contexts = {"gl-q001": shared, "gl-q002": shared, "gl-q003": shared}
    for mode in ("verbatim", "valeur"):
        result = compter_brassage(
            questions,
            contexts,
            assertion_index=assertion_index,
            claims_index={},
            mode_presence=mode,
        )
        assert result["signal"] == 2
        assert result["temoin"] == 2


def test_denominateur_imprime_dans_lignes():
    lignes = [
        {
            "fournisseur": "rag_naif",
            "mode": "verbatim",
            "signal": 35,
            "temoin": 13,
            "ecart": 22,
            "total": 43,
        }
    ]
    table = formater_tableau(lignes)
    assert "35/43" in table
    assert "13/43" in table
    assert "/50" not in table


def test_assertions_temoin_valeur_liste_discriminant():
    questions = [{"id": "gl-q001", "supporting_assertions": ["a1"]}]
    assertion_index = {"a1": _assertion("a1", "Article 3 du règlement")}
    contexts = {
        "gl-q001": [_element("autre contenu")],
        "gl-q002": [_element("voir Article 3 du règlement interne")],
    }
    rows = assertions_temoin_valeur(
        questions,
        contexts,
        assertion_index=assertion_index,
        claims_index={},
        pairing={"gl-q001": "gl-q002"},
    )
    assert len(rows) == 1
    assert rows[0]["assertion_id"] == "a1"
    assert "3" in rows[0]["discriminant"] or "Article" in rows[0]["discriminant"]


def _write_etage2(tmp_path: Path, fournisseur: str, rows: list[dict], *, k: int = 20) -> None:
    payload = {
        "fournisseur": fournisseur,
        "k_fixe": fournisseur == "brain_banc",
        "runs": [{"k": k, "budget": 12000, "questions": rows}],
    }
    (tmp_path / f"etage2-{fournisseur}.json").write_text(json.dumps(payload), encoding="utf-8")


def test_signal_temoin_egale_signal_mesure_deux_fournisseurs(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant

    moreau = dossier_courant("moreau")
    monkeypatch.setattr(type(moreau), "comparatif_dir", property(lambda self, _p=tmp_path: _p))

    rows_a = [
        {
            "question_id": "MOR-Q01",
            "shape": "citation",
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "appui_tout_tient_valeur": True,
            "appui_au_moins_une_valeur": True,
        },
        {
            "question_id": "MOR-Q02",
            "shape": "citation",
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "appui_tout_tient_valeur": True,
            "appui_au_moins_une_valeur": True,
        },
    ]
    rows_b = [
        {
            "question_id": "MOR-Q01",
            "shape": "citation",
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "appui_tout_tient_valeur": True,
            "appui_au_moins_une_valeur": True,
        },
        {
            "question_id": "MOR-Q02",
            "shape": "citation",
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "appui_tout_tient_valeur": True,
            "appui_au_moins_une_valeur": True,
        },
    ]
    _write_etage2(tmp_path, "mem0", rows_a, k=20)
    _write_etage2(tmp_path, "rag_naif", rows_b, k=12)

    questions = [
        {"id": "MOR-Q01", "shape": "citation", "supporting_assertions": ["a1"]},
        {"id": "MOR-Q02", "shape": "citation", "supporting_assertions": ["a2"]},
    ]
    assertion_index = {
        "a1": _assertion("a1", "alpha unique 1111"),
        "a2": _assertion("a2", "beta unique 2222"),
    }
    contexts = {
        "MOR-Q01": [_element("alpha unique 1111")],
        "MOR-Q02": [_element("beta unique 2222")],
    }

    for nom, k, k_fixe, expected in (
        ("mem0", 20, False, {"verbatim": 2, "valeur": 2}),
        ("rag_naif", 12, False, {"verbatim": 2, "valeur": 2}),
    ):
        signal = charger_signal_etage2(nom, k=k, budget=12000, k_fixe=k_fixe, dossier=moreau)
        assert signal == expected
        lignes, _assertions = mesurer_fournisseur_temoin(
            nom,
            questions,
            k=k,
            budget=12000,
            k_fixe=k_fixe,
            assertion_index=assertion_index,
            claims_index={},
            contexts=contexts,
            signal_etage2=signal,
            denominateur=2,
        )
        for row in lignes:
            assert row["signal"] == signal[row["mode"]]


def test_rapport_moreau_sans_bloc_greenloop(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant

    moreau = dossier_courant("moreau")
    monkeypatch.setattr(type(moreau), "comparatif_dir", property(lambda self, _p=tmp_path: _p))
    lignes = [
        {
            "fournisseur": "brain_banc",
            "mode": "valeur",
            "signal": 16,
            "temoin": 3,
            "ecart": 13,
            "total": 43,
        }
    ]
    ecrire_temoin_rapport(lignes, {}, dossier=moreau)
    text = (tmp_path / "TEMOIN-BRASSAGE.md").read_text(encoding="utf-8")
    assert "MOREAU n'a pas servi au réglage" in text
    assert "84 | 23" not in text
    assert "Avant / après resserrement" not in text


def test_rapport_greenloop_garde_bloc_historique(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant

    greenloop = dossier_courant("greenloop")
    monkeypatch.setattr(type(greenloop), "comparatif_dir", property(lambda self, _p=tmp_path: _p))
    lignes = [
        {
            "fournisseur": "brain_banc",
            "mode": "valeur",
            "signal": 87,
            "temoin": 24,
            "ecart": 63,
            "total": 141,
        }
    ]
    ecrire_temoin_rapport(lignes, {}, dossier=greenloop)
    text = (tmp_path / "TEMOIN-BRASSAGE.md").read_text(encoding="utf-8")
    assert "Avant / après resserrement / après correction invariant" in text
    assert "84 | 23" in formater_tableau_avant_apres(lignes)
    assert "84 | 23" in text


def test_charger_contextes_mesure_refuse_fichier_manquant(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant

    moreau = dossier_courant("moreau")
    monkeypatch.setattr(type(moreau), "comparatif_dir", property(lambda self, _p=tmp_path: _p))
    with pytest.raises(FileNotFoundError, match="contextes persistés absents"):
        charger_contextes_mesure(
            "rag_naif",
            [{"id": "MOR-Q01", "question": "q?"}],
            k=12,
            budget=12000,
            dossier=moreau,
        )


def test_signal_temoin_egale_signal_json(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant
    from banc_realite.mesure_comparatif_etage2 import ecrire_contextes_mesure

    moreau = dossier_courant("moreau")
    monkeypatch.setattr(type(moreau), "comparatif_dir", property(lambda self, _p=tmp_path: _p))
    _write_etage2(
        tmp_path,
        "rag_naif",
        [
            {
                "question_id": "MOR-Q01",
                "shape": "citation",
                "appui_tout_tient": True,
                "appui_au_moins_une": True,
                "appui_tout_tient_valeur": True,
                "appui_au_moins_une_valeur": True,
            },
            {
                "question_id": "MOR-Q02",
                "shape": "citation",
                "appui_tout_tient": False,
                "appui_au_moins_une": False,
                "appui_tout_tient_valeur": False,
                "appui_au_moins_une_valeur": False,
            },
        ],
        k=12,
    )
    questions = [
        {"id": "MOR-Q01", "question": "q1?", "shape": "citation", "supporting_assertions": ["a1"]},
        {"id": "MOR-Q02", "question": "q2?", "shape": "citation", "supporting_assertions": ["a2"]},
    ]
    ecrire_contextes_mesure(
        "rag_naif",
        ks=[12],
        questions=questions,
        elements_par_question_k={
            ("MOR-Q01", 12): [_element("alpha unique 1111")],
            ("MOR-Q02", 12): [_element("beta sans correspondance")],
        },
        dossier=moreau,
    )
    contexts = charger_contextes_mesure(
        "rag_naif",
        questions,
        k=12,
        budget=12000,
        dossier=moreau,
    )
    signal = charger_signal_etage2("rag_naif", k=12, budget=12000, k_fixe=False, dossier=moreau)
    lignes, _assertions = mesurer_fournisseur_temoin(
        "rag_naif",
        questions,
        k=12,
        budget=12000,
        k_fixe=False,
        assertion_index={
            "a1": _assertion("a1", "alpha unique 1111"),
            "a2": _assertion("a2", "beta unique 2222"),
        },
        claims_index={},
        contexts=contexts,
        signal_etage2=signal,
        denominateur=2,
    )
    assert lignes[0]["signal"] == signal["verbatim"] == 1


def test_decoupe_budget_change_temoin_sur_jeu_synthetique():
    from banc_realite.dossiers import dossier_courant
    from banc_realite.mesure_comparatif_etage2 import rendre_contexte

    needle = "Article 3 du règlement interne"
    questions = [
        {"id": "MOR-Q01", "supporting_assertions": ["a1"]},
        {"id": "MOR-Q02", "supporting_assertions": ["a2"]},
    ]
    assertion_index = {
        "a1": _assertion("a1", needle),
        "a2": _assertion("a2", "beta unique 2222"),
    }
    q2_elements = [
        _element("filler sans rapport"),
        _element("contexte " * 500 + needle),
    ]
    moreau = dossier_courant("moreau")
    _, kept_low = rendre_contexte(
        q2_elements,
        budget_chars=80,
        question_id="MOR-Q02",
        style="rag_naif",
        dossier=moreau,
    )
    _, kept_high = rendre_contexte(
        q2_elements,
        budget_chars=8000,
        question_id="MOR-Q02",
        style="rag_naif",
        dossier=moreau,
    )
    contexts_low = {
        "MOR-Q01": [_element(needle)],
        "MOR-Q02": kept_low,
    }
    contexts_high = {
        "MOR-Q01": [_element(needle)],
        "MOR-Q02": kept_high,
    }
    low = compter_brassage(
        questions,
        contexts_low,
        assertion_index=assertion_index,
        claims_index={},
        mode_presence="valeur",
    )
    high = compter_brassage(
        questions,
        contexts_high,
        assertion_index=assertion_index,
        claims_index={},
        mode_presence="valeur",
    )
    assert low["temoin"] != high["temoin"]


def test_grille_temoin_sans_null_quand_lignes_completes():
    from banc_realite.mesure_comparatif_etage2 import construire_grille_budget_egal
    from banc_realite.dossiers import dossier_courant

    results = [
        {
            "fournisseur": "rag_naif",
            "k_fixe": False,
            "runs": [
                {
                    "budget": 8000,
                    "k": 12,
                    "aggregate": {
                        "rendu": {"caracteres": {"mediane": 7900}},
                        "appui": {"tout_tient_sur_141": 10},
                        "appui_valeur": {"tout_tient_sur_141": 11},
                    },
                },
                {
                    "budget": 12000,
                    "k": 12,
                    "aggregate": {
                        "rendu": {"caracteres": {"mediane": 11800}},
                        "appui": {"tout_tient_sur_141": 12},
                        "appui_valeur": {"tout_tient_sur_141": 13},
                    },
                },
            ],
        }
    ]
    temoin_lignes = [
        {
            "fournisseur": "rag_naif",
            "mode": "verbatim",
            "budget": 8000,
            "k": 12,
            "temoin": 3,
            "ecart": 7,
            "total": 141,
        },
        {
            "fournisseur": "rag_naif",
            "mode": "verbatim",
            "budget": 12000,
            "k": 12,
            "temoin": 5,
            "ecart": 7,
            "total": 141,
        },
    ]
    payload = construire_grille_budget_egal(
        results,
        budgets=[8000, 12000],
        dossier=dossier_courant("greenloop"),
        temoin_lignes=temoin_lignes,
    )
    for budget in ("8000", "12000"):
        cell = payload["grille"]["rag_naif"][budget]
        assert cell[2] is not None
        assert cell[3] is not None


def test_budgets_produit_une_cellule_par_budget(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant
    from banc_realite.temoin_brassage import _mesurer_grille_temoin

    moreau = dossier_courant("moreau")
    monkeypatch.setattr(type(moreau), "comparatif_dir", property(lambda self, _p=tmp_path: _p))
    budgets = [8000, 12000]
    rows = [
        {
            "question_id": "MOR-Q01",
            "shape": "citation",
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "appui_tout_tient_valeur": True,
            "appui_au_moins_une_valeur": True,
        },
        {
            "question_id": "MOR-Q02",
            "shape": "citation",
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "appui_tout_tient_valeur": True,
            "appui_au_moins_une_valeur": True,
        },
    ]
    payload = {
        "fournisseur": "rag_naif",
        "k_fixe": False,
        "runs": [
            {
                "k": 12,
                "budget": budget,
                "questions": rows,
                "aggregate": {
                    "rendu": {"caracteres": {"mediane": budget - 100}},
                    "appui": {"tout_tient_sur_141": 2},
                    "appui_valeur": {"tout_tient_sur_141": 2},
                },
            }
            for budget in budgets
        ],
    }
    (tmp_path / "etage2-rag_naif.json").write_text(json.dumps(payload), encoding="utf-8")

    from banc_realite.mesure_comparatif_etage2 import ecrire_contextes_mesure

    questions = [
        {"id": "MOR-Q01", "shape": "citation", "supporting_assertions": ["a1"]},
        {"id": "MOR-Q02", "shape": "citation", "supporting_assertions": ["a2"]},
    ]
    ecrire_contextes_mesure(
        "rag_naif",
        ks=[12],
        questions=questions,
        elements_par_question_k={
            ("MOR-Q01", 12): [_element("alpha unique 1111")],
            ("MOR-Q02", 12): [_element("beta unique 2222")],
        },
        dossier=moreau,
    )
    results = [payload]
    assertion_index = {
        "a1": _assertion("a1", "alpha unique 1111"),
        "a2": _assertion("a2", "beta unique 2222"),
    }
    grille = _mesurer_grille_temoin(
        ["rag_naif"],
        budgets,
        results,
        questions=questions,
        questions_mesure=questions,
        assertion_index=assertion_index,
        claims_index={},
        denominateur=2,
        dossier=moreau,
    )
    budgets_vus = sorted({int(row["budget"]) for row in grille if row["mode"] == "verbatim"})
    assert budgets_vus == budgets


def test_verifier_reference_12000_inchangee():
    from banc_realite.dossiers import dossier_courant
    from banc_realite.temoin_brassage import verifier_reference_12000_inchangee

    lignes = [
        {"fournisseur": "brain_prod", "mode": "verbatim", "temoin": 4, "budget": 12000},
        {"fournisseur": "rag_naif", "mode": "verbatim", "temoin": 46, "budget": 12000},
        {"fournisseur": "brain_banc", "mode": "verbatim", "temoin": 23, "budget": 12000},
        {"fournisseur": "mem0", "mode": "verbatim", "temoin": 0, "budget": 12000},
    ]
    assert verifier_reference_12000_inchangee(lignes, dossier=dossier_courant("greenloop"))
    lignes[-1]["temoin"] = 1
    assert not verifier_reference_12000_inchangee(lignes, dossier=dossier_courant("greenloop"))
