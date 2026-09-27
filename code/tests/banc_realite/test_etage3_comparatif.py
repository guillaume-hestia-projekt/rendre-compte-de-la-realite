"""Tests hors ligne — etage3_comparatif."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite import etage3_comparatif as e3c
from banc_realite.dossiers import dossier_courant
from banc_realite.etage3 import (
    CONTEXT_A,
    SYSTEM_PROMPT,
    SYSTEM_PROMPT_FR,
    append_call,
    build_response_invite,
    estimate_invite_tokens,
    usage_relais_total,
)
from banc_realite.normalize import normalize_text
from banc_realite.or_dossier import load_gold, load_questions


@pytest.fixture
def moreau_questions():
    return [
        {
            "id": "MOR-Q01",
            "shape": "citation",
            "question": "Quelle est la date d'embauche ?",
            "must_mention": ["1er mars 2020"],
            "must_not_claim": ["Le contrat est à durée déterminée."],
        },
        {
            "id": "MOR-Q28",
            "shape": "non_etabli",
            "question": "Le dossier établit-il que Benali a assisté à l'appel ?",
            "must_mention": ["ne puis en témoigner"],
            "must_not_claim": ["Benali confirme le comportement inapproprié."],
        },
        {
            "id": "MOR-Q19",
            "shape": "contradiction",
            "question": "Combien d'heures supplémentaires ?",
            "must_mention": ["86", "64"],
            "must_not_claim": ["Le solde est tranché."],
        },
    ]


@pytest.fixture
def tmp_comparatif(tmp_path, moreau_questions, monkeypatch):
    dossier = dossier_courant("moreau")
    etage3 = tmp_path / "etage3"
    comparatif = tmp_path / "comparatif"
    etage3.mkdir()
    comparatif.mkdir()
    monkeypatch.setattr(e3c, "etage3_dir", lambda _d=None: etage3)
    monkeypatch.setattr(e3c, "invites_path", lambda _d=None: etage3 / "invites-reponses.jsonl")
    monkeypatch.setattr(e3c, "appels_path", lambda _d=None: etage3 / "appels.jsonl")
    monkeypatch.setattr(e3c, "rapport_path", lambda _d=None: etage3 / "RAPPORT-ETAGE3-COMPARATIF.md")
    monkeypatch.setattr(
        e3c,
        "notations_path",
        lambda bras, _d=None: etage3 / f"notations-{bras}.json",
    )
    monkeypatch.setattr(e3c, "GROK_RESULT_PATH", tmp_path / "_grok-result.json")

    def fake_rendered(nom, questions, *, k, budget, dossier):
        return {q["id"]: f"contexte {nom} pour {q['id']}" for q in questions}

    monkeypatch.setattr(e3c, "build_rendered_contexts", fake_rendered)
    monkeypatch.setattr(e3c, "load_questions", lambda _d=None: moreau_questions)
    return tmp_path


def _write_contextes(path: Path, question_ids: list[str]) -> None:
    lines = [json.dumps({"meta": {"fournisseur": "mem0", "k": 20}})]
    for qid in question_ids:
        lines.append(
            json.dumps(
                {
                    "question_id": qid,
                    "elements": [{"rank": 1, "text": "alpha", "source": "01-contrat.md"}],
                }
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_build_rendered_contexts_refuse_fichier_absent(tmp_path, moreau_questions, monkeypatch):
    dossier = dossier_courant("moreau")
    monkeypatch.setattr(
        e3c,
        "lire_contextes_mesure_bruts",
        lambda *_a, **_k: (_ for _ in ()).throw(FileNotFoundError("absent")),
    )
    with pytest.raises(FileNotFoundError, match="absent"):
        e3c.build_rendered_contexts("mem0", moreau_questions, k=20, budget=12000, dossier=dossier)


def test_build_rendered_contexts_ne_declenche_pas_recherche(
    tmp_path, moreau_questions, monkeypatch
):
    dossier = dossier_courant("moreau")
    path = tmp_path / "contextes-mem0.jsonl"
    _write_contextes(path, [q["id"] for q in moreau_questions])
    monkeypatch.setattr(e3c, "lire_contextes_mesure_bruts", lambda *_a, **_k: {
        (q["id"], None): [{"text": "x", "source": "a.md"}] for q in moreau_questions
    })

    def fail_search(*_a, **_k):
        raise AssertionError("recherche interdite à l'étage 3")

    monkeypatch.setattr("banc_realite.fournisseurs_contexte.search_passages_hybrid", fail_search)
    monkeypatch.setattr("brain.search.run_search", fail_search)
    rendered = e3c.build_rendered_contexts("mem0", moreau_questions, k=20, budget=12000, dossier=dossier)
    assert rendered["MOR-Q01"].startswith("- [")


def test_instructions_identical_pour_tous_les_fournisseurs(tmp_comparatif, moreau_questions):
    dossier = dossier_courant("moreau")
    invites = e3c.build_all_invites(moreau_questions, dossier=dossier)
    assert e3c.instructions_identical(invites, langue="fr")
    systems = {invite["system"] for invite in invites}
    assert systems == {SYSTEM_PROMPT_FR}
    assert all(invite.get("langue_invite") == "fr" for invite in invites)
    a_user = next(i for i in invites if i["bras"] == "A")["user"]
    mem0_user = next(i for i in invites if i["bras"] == "mem0")["user"]
    assert a_user.startswith(CONTEXT_A)
    assert "contexte mem0" in mem0_user


def test_invite_en_greenloop_inchangee():
    dossier = dossier_courant("greenloop")
    invite = build_response_invite(
        "A",
        {"id": "gl-q001", "question": "What is the revenue?"},
        context="No document is provided.",
        langue=dossier.langue,
    )
    assert invite["system"] == SYSTEM_PROMPT
    assert invite["langue_invite"] == "en"


def test_comptage_a_blanc_moreau(moreau_questions):
    comptage = e3c.comptage_a_blanc(moreau_questions)
    assert comptage == {"repondant": 75, "juge": 15}


def test_comptage_a_blanc_greenloop():
    questions = [
        {"id": f"gl-q{i:03d}", "shape": "single", "question": "?"}
        for i in range(1, 142)
    ]
    comptage = e3c.comptage_a_blanc(questions)
    assert comptage == {"repondant": 765, "juge": 705}


def test_plafond_defaut_par_dossier(moreau_questions):
    moreau = dossier_courant("moreau")
    plafonds = e3c.init_plafonds(moreau)
    comptage = e3c.comptage_a_blanc(load_questions(moreau))
    assert plafonds["repondant"] == e3c.plafond_avec_marge(comptage["repondant"])
    assert plafonds["juge"] == e3c.plafond_avec_marge(comptage["juge"])
    greenloop = dossier_courant("greenloop")
    plafonds_gl = e3c.init_plafonds(greenloop)
    assert plafonds_gl["repondant"] == 788
    assert plafonds_gl["juge"] == 727


def test_lignes_reference_greenloop():
    dossier = dossier_courant("greenloop")
    assert e3c.reference_lines(dossier) == (
        ("brain_prod", 8, 12000),
        ("rag_naif", 12, 12000),
        ("brain_banc", None, 12000),
        ("mem0", 20, 12000),
    )


def test_etage3_dir_greenloop():
    dossier = dossier_courant("greenloop")
    assert e3c.etage3_dir(dossier).name == "etage3-comparatif"
    assert "sorties" in str(e3c.etage3_dir(dossier))


def test_unknown_refus_attendu_est_conforme():
    question = {
        "id": "gl-q099",
        "shape": "unknown",
        "must_mention": ["cannot determine"],
        "must_not_claim": ["It is established."],
    }
    assert (
        e3c.compute_verdict_valeur_comparatif(
            question,
            "I cannot determine this from the provided documents.",
        )
        == "conforme"
    )


def test_juge_n_utilise_pas_le_slug_repondant():
    with pytest.raises(RuntimeError, match="même modèle"):
        e3c.adjudicate_judge_call(
            "réponse",
            {"id": "MOR-Q01", "question": "?", "must_not_claim": []},
            invite_key_value="juge-A-MOR-Q01",
            chat_fn=lambda _s, _u: ("{}", {}),
            calls_path=Path("/tmp/unused.jsonl"),
            modele=e3c.REPONDANT_MODEL,
        )


def test_juge_modele_refuse_famille_grok_sans_option():
    with pytest.raises(RuntimeError, match="même famille"):
        e3c.assert_judge_model_allowed(e3c.REPONDANT_MODEL, "grok-4.7-high")
    with pytest.raises(RuntimeError, match="même modèle"):
        e3c.assert_judge_model_allowed(e3c.REPONDANT_MODEL, "cursor-grok-4.5-high")


def test_juge_modele_accepte_famille_grok_avec_option():
    e3c.assert_judge_model_allowed(
        e3c.REPONDANT_MODEL,
        "grok-4.7-high",
        meme_famille_accepte=True,
    )


def test_non_etabli_refus_motive_est_conforme():
    question = {
        "id": "MOR-Q28",
        "shape": "non_etabli",
        "must_mention": ["ne puis en témoigner"],
        "must_not_claim": ["Benali confirme."],
    }
    assert (
        e3c.compute_verdict_comparatif(
            question,
            "Le dossier ne permet pas de répondre.",
        )
        == "conforme"
    )


def test_non_etabli_reponse_affirmative_est_fautive():
    question = {
        "id": "MOR-Q28",
        "shape": "non_etabli",
        "must_mention": [],
        "must_not_claim": ["Benali confirme."],
    }
    assert (
        e3c.compute_verdict_comparatif(question, "Benali était présent.") == "fautive"
    )


def test_refus_fautif_sur_question_mesurable():
    question = {"id": "MOR-Q01", "shape": "citation", "must_mention": ["1er mars 2020"], "must_not_claim": []}
    assert (
        e3c.compute_verdict_comparatif(question, "Je ne peux pas répondre.")
        == "refus_fautif"
    )


def test_formes_iso_detectee_sans_faute_adjudiquee():
    from banc_realite.etage3 import detect_formes_iso

    question = {
        "id": "MOR-Q08",
        "shape": "date",
        "must_mention": ["15 février 2024"],
        "must_not_claim": ["2024-02-15 remplace la forme de la mise en demeure."],
    }
    response = "La mise en demeure est datée 2024-02-15 (08-mise-en-demeure-salarie.md)."
    assert detect_formes_iso(question, response) == ["2024-02-15"]
    assert e3c.compute_verdict_comparatif(question, response) == "conforme"


def test_noter_sans_jugement_remplit_colonnes_et_juge_en_attente(tmp_comparatif, moreau_questions):
    invites = e3c.build_all_invites(moreau_questions, dossier=dossier_courant("moreau"))
    e3c.invites_path().write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )
    calls = tmp_comparatif / "etage3" / "appels.jsonl"
    for invite in invites:
        append_call(
            calls,
            {
                "role": "reponse",
                "id": invite["id"],
                "reponse_brute": "1er mars 2020" if invite["question_id"] == "MOR-Q01" else "refus",
                "usage": {"prompt_tokens": 30000, "completion_tokens": 120},
                "final": True,
            },
        )
    payload = e3c.run_noter(calls_path=calls)
    assert payload["complet"] is True
    assert payload["juge"] == "en attente (0/15 jugements)"
    assert payload["agregats"]["A"]["conforme_valeur"] != "0/3"
    a_invites = [invite for invite in invites if invite["bras"] == "A"]
    expected_tokens = sorted(estimate_invite_tokens(invite["user_chars"]) for invite in a_invites)
    assert payload["agregats"]["A"]["tokens_invite_medians"] == expected_tokens[len(expected_tokens) // 2]
    assert payload["agregats"]["A"]["usage_relais_medians"] == 30120
    rapport = e3c.rapport_path().read_text(encoding="utf-8")
    assert "en attente (0/15 jugements)" in rapport
    assert "conforme_valeur" in rapport
    assert "conforme_lettre" in rapport


def test_noter_avec_jugements_remplit_colonne_juge(tmp_comparatif, moreau_questions):
    invites = e3c.build_all_invites(moreau_questions, dossier=dossier_courant("moreau"))
    e3c.invites_path().write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )
    calls = tmp_comparatif / "etage3" / "appels.jsonl"
    for invite in invites:
        append_call(
            calls,
            {
                "role": "reponse",
                "id": invite["id"],
                "reponse_brute": "1er mars 2020",
                "usage": {"prompt_tokens": 100},
                "final": True,
            },
        )
        append_call(
            calls,
            {
                "role": "juge",
                "id": f"juge-{invite['id']}",
                "jugements": [
                    {
                        "numero": 1,
                        "verdict": "affirme",
                        "preuve_verifiable": True,
                    }
                ],
                "refus": False,
                "final": True,
            },
        )
    payload = e3c.run_noter(calls_path=calls)
    assert "jugés" in payload["juge"]
    assert "jugés" in payload["agregats"]["A"]["fautes_juge"]


def test_stabilite_depuis_verdicts_rejeux(tmp_comparatif, moreau_questions, monkeypatch):
    monkeypatch.setattr(e3c, "STABILITY_QUESTIONS", 1)
    monkeypatch.setattr(e3c, "STABILITY_REJEUX", 3)
    invites = e3c.build_all_invites(moreau_questions, dossier=dossier_courant("moreau"))
    e3c.invites_path().write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )
    calls = tmp_comparatif / "etage3" / "appels.jsonl"
    base = next(invite for invite in invites if invite["bras"] == "mem0")
    for index in range(1, 4):
        append_call(
            calls,
            {
                "role": "reponse",
                "id": f"{base['id']}#rejeu-{index}",
                "reponse_brute": "1er mars 2020",
                "final": True,
            },
        )
    for invite in invites:
        append_call(
            calls,
            {
                "role": "reponse",
                "id": invite["id"],
                "reponse_brute": "1er mars 2020" if invite["question_id"] == "MOR-Q01" else "texte",
                "usage": {"prompt_tokens": 50},
                "final": True,
            },
        )
    payload = e3c.run_noter(calls_path=calls)
    assert payload["agregats"]["mem0"]["stabilite"] == "1/1"


def test_plafond_repondant_arrete(tmp_comparatif):
    e3c.init_plafonds(dossier_courant("moreau"), plafond_repondant=e3c.MAX_REPONDANT_CALLS)
    calls = tmp_comparatif / "etage3" / "calls.jsonl"
    for index in range(e3c.plafond_repondant_actif()):
        append_call(
            calls,
            {
                "role": "reponse",
                "id": f"x-{index}",
                "final": True,
            },
        )
    invite = build_response_invite("A", {"id": "MOR-Q01", "question": "?"}, context=CONTEXT_A)
    with pytest.raises(RuntimeError, match="plafond répondant"):
        e3c.adjudicate_response(invite, chat_fn=lambda _s, _u: ("ok", {}), calls_path=calls)


def test_plafond_juge_arrete(tmp_comparatif):
    e3c.init_plafonds(dossier_courant("moreau"), plafond_juge=e3c.MAX_JUGE_CALLS)
    calls = tmp_comparatif / "etage3" / "calls.jsonl"
    for index in range(e3c.plafond_juge_actif()):
        append_call(
            calls,
            {
                "role": "juge",
                "id": f"juge-x-{index}",
                "final": True,
            },
        )
    with pytest.raises(RuntimeError, match="plafond juge"):
        e3c.adjudicate_judge_call(
            "réponse",
            {"id": "MOR-Q01", "question": "?", "must_not_claim": []},
            invite_key_value="juge-A-MOR-Q01",
            chat_fn=lambda _s, _u: ('{"jugements":[],"refus":false}', {}),
            calls_path=calls,
        )


def test_reprise_sans_double_appel(tmp_comparatif, moreau_questions, monkeypatch):
    monkeypatch.setattr(e3c, "STABILITY_REJEUX", 0)
    etage3 = tmp_comparatif / "etage3"
    invites = e3c.build_all_invites(moreau_questions, dossier=dossier_courant("moreau"))
    e3c.invites_path().write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )
    calls = etage3 / "appels.jsonl"
    first = invites[0]
    append_call(
        calls,
        {
            "role": "reponse",
            "id": first["id"],
            "sha256_invite": first["sha256"],
            "reponse_brute": "done",
            "final": True,
        },
    )
    counter = 0

    def chat(_s, _u):
        nonlocal counter
        counter += 1
        return "new", {}

    e3c.run_reponses(chat, calls_path=calls)
    assert counter == len(invites) - 1


def test_run_juge_ne_consomme_pas_si_pas_de_reponse(tmp_comparatif, moreau_questions):
    invites = e3c.build_all_invites(moreau_questions, dossier=dossier_courant("moreau"))
    e3c.invites_path().write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )
    calls = 0

    def chat(_s, _u):
        nonlocal calls
        calls += 1
        return '{"jugements":[],"refus":false}', {}

    e3c.run_juge(chat, calls_path=tmp_comparatif / "etage3" / "empty.jsonl")
    assert calls == 0


def test_dry_run_ecrit_rapport_et_comptage(tmp_comparatif, moreau_questions, monkeypatch):
    monkeypatch.setattr(e3c, "assert_cursor_model_available", lambda _m: None)
    monkeypatch.setattr(e3c, "load_questions", lambda _d=None: moreau_questions)
    result = e3c.run_dry_run()
    assert result["comptage_a_blanc"]["repondant"] == 75
    assert result["plafonds"]["repondant"] == e3c.plafond_avec_marge(75)
    rapport = e3c.rapport_path().read_text(encoding="utf-8")
    assert "Comptage à blanc" in rapport
    assert "cursor-grok-4.5-high" in rapport
    assert "gpt-5.6-sol-high" in rapport
    assert f"(plafond {result['plafonds']['repondant']})" in rapport


def test_run_noter_agrege_par_bras(tmp_comparatif, moreau_questions):
    invites = e3c.build_all_invites(moreau_questions, dossier=dossier_courant("moreau"))
    e3c.invites_path().write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in invites),
        encoding="utf-8",
    )
    calls = tmp_comparatif / "etage3" / "appels.jsonl"
    for invite in invites:
        if invite["question_id"] == "MOR-Q01":
            text = "1er mars 2020"
        elif invite["question_id"] == "MOR-Q28":
            text = "Le dossier ne permet pas de répondre."
        else:
            text = "86 et 64"
        append_call(
            calls,
            {
                "role": "reponse",
                "id": invite["id"],
                "reponse_brute": text,
                "usage": {"prompt_tokens": 100},
                "final": True,
            },
        )
    payload = e3c.run_noter(calls_path=calls)
    assert payload["complet"] is True
    assert "A" in payload["agregats"]
    assert e3c.notations_path("mem0").is_file()


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_verbatim_avec_piece():
    gold = load_gold(dossier_courant("moreau"))
    assertion = gold["assertion_index"]["MOR-A39"]
    question = {
        "id": "MOR-Q01",
        "shape": "citation",
        "must_mention": ["LUMO SA", "19 décembre 2023"],
        "supporting_assertions": ["MOR-A39"],
    }
    quote = assertion["quote"]
    response = f'« {quote} » (07-lettre-licenciement.md).'
    assert e3c.compute_verdict_adjudique(question, response) == "conforme"
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "conforme"


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_faux_sur_paraphrase_valeur_ok():
    gold = load_gold(dossier_courant("moreau"))
    question = {
        "id": "MOR-Q08",
        "shape": "date",
        "must_mention": ["15 février 2024"],
        "supporting_assertions": ["MOR-A22"],
    }
    response = "La mise en demeure est datée 2024-02-15 (08-mise-en-demeure-salarie.md)."
    assert e3c.compute_verdict_adjudique(question, response) == "conforme"
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "incomplete"


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_vrai_sur_date_fr():
    gold = load_gold(dossier_courant("moreau"))
    question = {
        "id": "MOR-Q08",
        "shape": "date",
        "must_mention": ["15 février 2024"],
        "supporting_assertions": ["MOR-A22"],
    }
    response = "Orléans-sur-Clain, le 15 février 2024 (08-mise-en-demeure-salarie.md)."
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "conforme"


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_mem0_mor_q08_avoue_ignorance():
    gold = load_gold(dossier_courant("moreau"))
    question = {
        "id": "MOR-Q08",
        "shape": "date",
        "must_mention": ["15 février 2024"],
        "supporting_assertions": ["MOR-A22"],
    }
    response = (
        "Le dossier ne l'établit pas. Les mentions relatives à [08-mise-en-demeure-salarie.md] "
        "indiquent seulement la date du 15 février 2024 (« February 15, 2024 »), sans citer le "
        "libellé tel qu'il figure sur la pièce (par ex. « 15 février 2024 », « 15/02/2024 », etc.)."
    )
    assert e3c.compute_verdict_valeur_comparatif(question, response) == "incomplete"
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "incomplete"


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_mem0_mor_q04_avoue_ignorance():
    gold = load_gold(dossier_courant("moreau"))
    question = {
        "id": "MOR-Q04",
        "shape": "date",
        "must_mention": ["2 janvier 2024"],
        "supporting_assertions": ["MOR-A13"],
    }
    response = (
        "La convocation porte la date du January 2, 2024. Le dossier ne précise pas la graphie "
        "française exacte sur le courrier (par ex. « 2 janvier 2024 » ou « 02/01/2024 »). "
        "Citation — [05-convocation-entretien-prealable.md] : « On January 2, 2024, SAS ATELIER "
        "RIVIÈRE sent Claire MOREAU at 14, rue des Lilas, 45000 Orléans-sur-Clain a registered "
        "letter with acknowledgment of receipt »."
    )
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "incomplete"


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_rag_naif_mor_q01_citation_partielle():
    gold = load_gold(dossier_courant("moreau"))
    question = {
        "id": "MOR-Q01",
        "shape": "citation",
        "must_mention": ["LUMO SA", "19 décembre 2023"],
        "supporting_assertions": ["MOR-A39"],
    }
    response = (
        "La lettre de licenciement invoque un comportement inapproprié ayant porté atteinte "
        "à l'image de l'entreprise.\n\n"
        "Selon [07-lettre-licenciement.md] : « Comportement inapproprié vis-à-vis du client "
        "LUMO SA le 19 décembre 2023, ayant porté atteinte à l'image de l'entreprise »."
    )
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "conforme"


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_seuil_39_caracteres_insuffisant():
    gold = load_gold(dossier_courant("moreau"))
    assertion = gold["assertion_index"]["MOR-A39"]
    citation = assertion["quote"]
    norm_cite = normalize_text(citation)
    short_norm = ""
    for i in range(len(norm_cite)):
        for j in range(i + 1, len(norm_cite) + 1):
            chunk = norm_cite[i:j]
            if e3c._significant_char_count(chunk) == 39:
                short_norm = chunk
                break
        if short_norm:
            break
    assert short_norm
    question = {
        "id": "MOR-Q01",
        "shape": "citation",
        "must_mention": ["LUMO SA", "19 décembre 2023"],
        "supporting_assertions": ["MOR-A39"],
    }
    response = f'« {short_norm} » (07-lettre-licenciement.md).'
    assert not e3c._passage_verbatim_dans_citation(response, citation)
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "incomplete"


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_sans_nombre_discriminant():
    question = {
        "id": "MOR-Q99",
        "shape": "montant",
        "must_mention": ["2 450,00 €"],
        "supporting_assertions": ["MOR-A99"],
    }
    assertion = {
        "source": "documents/10-indemnite.md",
        "quote": "indemnité de 2 450,00 €",
    }
    response = "L'indemnité s'élève à 2 450 (10-indemnite.md)."
    assert e3c._assertion_lettre_dans_reponse(assertion, response) is False


@pytest.mark.skipif(
    not (Path("/home/ubuntu/.agents/var/banc-realite/dossiers/moreau/gold/assertions.json").is_file()),
    reason="or MOREAU absent sur disque",
)
def test_conforme_lettre_sans_piece_nommee():
    gold = load_gold(dossier_courant("moreau"))
    assertion = gold["assertion_index"]["MOR-A39"]
    quote = assertion["quote"]
    question = {
        "id": "MOR-Q01",
        "shape": "citation",
        "must_mention": ["LUMO SA", "19 décembre 2023"],
        "supporting_assertions": ["MOR-A39"],
    }
    response = f'« {quote} ».'
    assert e3c.compute_verdict_lettre(question, response, gold["assertion_index"]) == "incomplete"


def test_tokens_invite_different_usage_relais():
    assert estimate_invite_tokens(120) == 30
    assert usage_relais_total({"prompt_tokens": 25000, "completion_tokens": 5000}) == 30000


def test_archivage_v1_conserve_fichiers(tmp_path, monkeypatch):
    dossier = dossier_courant("moreau")
    src = tmp_path / "etage3"
    dst = tmp_path / "etage3-v1-anglais"
    src.mkdir()
    marker = src / "appels.jsonl"
    marker.write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(e3c, "etage3_dir", lambda _d=None: src)
    monkeypatch.setattr(e3c, "etage3_v1_dir", lambda _d=None: dst)
    archived = e3c.archiver_etage3_v1(dossier)
    assert archived == dst
    assert dst.is_dir()
    assert (dst / "appels.jsonl").is_file()
    assert not src.exists()
    assert e3c.archiver_etage3_v1(dossier) == dst
