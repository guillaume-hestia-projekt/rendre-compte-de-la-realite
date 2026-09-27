"""Étage 3 hybride — registre, chemins et construction d'évidence."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from banc_realite import etage3_config_gagnante as ecg
from banc_realite.config import BANC_ROOT


def test_configurations_registry_contient_variantes_budget():
    assert set(ecg.CONFIGURATIONS) == {
        "fine_tours_k12",
        "hybride_fenetres_g12",
        "hybride_fenetres_g24",
        "hybride_fenetres_g36",
        "hybride_fenetres_g48",
        "hybride_fenetres_calibrees",
    }
    assert len(ecg.CONFIGURATIONS) == 6


def test_fine_tours_k12_garde_constantes_et_chemins_historiques():
    assert ecg.CONFIG == "fine_tours_k12"
    assert ecg.TOP_K == 12
    assert ecg.MODE == "trois_tours"
    assert ecg.SORTIES_CONFIG == BANC_ROOT / "sorties" / "etage3-config-gagnante"
    assert ecg.CADRES_PATH == ecg.SORTIES_CONFIG / "cadres.json"
    assert ecg.INVITES_PATH == ecg.SORTIES_CONFIG / "invites-reponses.jsonl"
    assert ecg.APPELS_PATH == ecg.SORTIES_CONFIG / "appels.jsonl"
    assert ecg.NOTATIONS_PATH == ecg.SORTIES_CONFIG / "notations.json"
    assert ecg.RAPPORT_PATH == ecg.SORTIES_CONFIG / "RAPPORT-CONFIG-GAGNANTE.md"
    assert ecg.ARRET_PATH == BANC_ROOT / "_etage3-config-arret.json"
    assert ecg.RESULT_PATH == BANC_ROOT / "_etage3-config-result.json"


def test_hybride_chemins_derivent_du_nom():
    paths = ecg.config_paths("hybride_fenetres_g12")
    assert paths["sorties_config"] == BANC_ROOT / "sorties" / "etage3-hybride-fenetres"
    assert paths["cadres"] == paths["sorties_config"] / "cadres.json"
    assert paths["invites"] == paths["sorties_config"] / "invites-reponses.jsonl"
    assert paths["appels"] == paths["sorties_config"] / "appels.jsonl"
    assert paths["notations"] == paths["sorties_config"] / "notations.json"
    assert paths["rapport"] == paths["sorties_config"] / "RAPPORT-HYBRIDE-FENETRES.md"
    assert paths["result"] == ecg.HYBRIDE_MARKER_DIR / "_etage3-hybride-result.json"
    assert paths["arret"] == ecg.HYBRIDE_MARKER_DIR / "_etage3-hybride-arret.json"


def test_fine_tours_uses_trois_tours_mode(monkeypatch):
    captured: dict[str, str | int] = {}

    def fake_build(*_args, **kwargs):
        captured["mode"] = kwargs.get("mode")
        captured["k"] = kwargs.get("k")
        return ([], {"completion": {"faits_ajoutes": 0}})

    monkeypatch.setattr(ecg, "build_evidence_for_mode", fake_build)
    monkeypatch.setattr(ecg, "_render_markdown_with_budget", lambda *_a, **_k: ("ctx", 0))
    monkeypatch.setattr(ecg, "_load_embed_cache", lambda: {"q?": [0.1]})
    ecg.select_config("fine_tours_k12")
    ecg._compile_cadre_for_question(
        {"id": "gl-q001", "question": "q?"},
        connection=object(),
        embed_cache={"q?": [0.1]},
        gold={},
        claims_index={},
        config_name="fine_tours_k12",
    )
    assert captured["mode"] == "trois_tours"
    assert captured["k"] == 12


def test_hybride_builds_evidence_via_porte_phrase_config(monkeypatch):
    calls: list[tuple[str, dict]] = []
    fine_item = {"kind": "file_hit", "id": "fine-1", "text": "fine passage"}
    phrase_item = {"kind": "phrase_hit", "id": "phrase-1", "text": "phrase courte"}

    def fake_porte(connection, question, config, *, embed_cache, phrases_cache):
        calls.append(
            (
                "porte",
                {
                    "hybride": config.get("hybride"),
                    "brute_k": config.get("brute_k"),
                    "phrases": config.get("phrases"),
                    "question": question["question"],
                    "embed_cache": embed_cache,
                    "phrases_cache": phrases_cache,
                },
            )
        )
        return [fine_item, phrase_item], [{"kind": "file_hit"}], {"unites_sans_vecteur": 0}

    monkeypatch.setattr(ecg, "build_evidence_for_porte_phrase_config", fake_porte)
    monkeypatch.setattr(ecg, "_render_markdown_with_budget", lambda *_a, **_k: ("ctx", 0))
    monkeypatch.setattr(ecg, "_load_embed_cache", lambda: {"q?": [0.1]})
    row = ecg._compile_cadre_for_question(
        {"id": "gl-q001", "question": "q?"},
        connection=object(),
        embed_cache={"q?": [0.1]},
        gold={},
        claims_index={},
        phrases_cache={"unit": [0.2]},
        config_name="hybride_fenetres_g12",
    )
    assert len(calls) == 1
    _, payload = calls[0]
    assert payload["hybride"] == {"k": 18, "n_tours": 2, "k_tour1": 12}
    assert payload["brute_k"] == 12
    assert payload["phrases"] == {
        "n_par_passage": 2,
        "max_phrases": 12,
        "mode": "vectoriel",
        "selection": "globale",
        "fenetre": 2,
    }
    assert payload["phrases_cache"] == {"unit": [0.2]}
    assert row["genres"]["file_hit"] == 1
    assert row["genres"]["phrase_hit"] == 1
    assert row["evidence_count"] == 2


def test_hybride_fenetres_apres_elements_fins(monkeypatch):
    order: list[str] = []

    def fake_build_evidence_for_mode(connection, question, **kwargs):
        couche = kwargs.get("couche")
        order.append(str(couche))
        return [{"kind": "file_hit", "id": f"{couche}-1", "text": str(couche)}], {}

    def fake_porte(question, brute_passages, **kwargs):
        order.append("phrases")
        return [{"kind": "phrase_hit", "id": "p1", "text": "phrase"}], {"unites_sans_vecteur": 0}

    from banc_realite import mesure_porte_phrase as mpp

    monkeypatch.setattr(mpp, "build_evidence_for_mode", fake_build_evidence_for_mode)
    monkeypatch.setattr(mpp, "porte_phrase", fake_porte)
    config = ecg.PORTE_PHRASE_HYBRIDE_FENETRES_G12
    evidence, _brute, _stats = mpp.build_evidence_for_porte_phrase_config(
        object(),
        {"id": "gl-q001", "question": "q?"},
        config,
        embed_cache={"q?": [0.1]},
        phrases_cache={"unit": [0.2]},
    )
    assert order == ["fine", "brute", "phrases"]
    assert evidence[0]["kind"] == "file_hit"
    assert evidence[1]["kind"] == "phrase_hit"


def test_select_config_active_paths():
    ecg.select_config("hybride_fenetres_g12")
    paths = ecg.active_paths()
    assert paths["sorties_config"].name == "etage3-hybride-fenetres"
    ecg.select_config("fine_tours_k12")


def test_write_noter_report_compare_colonnes(tmp_path):
    local_payload = {
        "notes": [
            {
                "bras": "hybride_fenetres_g12",
                "question_id": "gl-q001",
                "shape": "single",
                "verdict": "conforme",
                "nombres_attendus": 1,
                "tous_les_nombres": True,
                "refus": False,
            },
            {
                "bras": "hybride_fenetres_g12",
                "question_id": "gl-q073",
                "shape": "dispute",
                "verdict": "conforme",
                "nombres_attendus": 2,
                "tous_les_nombres": True,
                "refus": False,
            },
        ],
        "stabilite": {"reponses_identiques": "1/1", "tous_les_nombres_identiques": "1/1"},
    }
    reference_payload = {
        "notes": [
            {
                "bras": "fine_tours_k12",
                "question_id": "gl-q001",
                "shape": "single",
                "verdict": "incomplete",
                "nombres_attendus": 1,
                "tous_les_nombres": False,
                "refus": True,
            },
            {
                "bras": "fine_tours_k12",
                "question_id": "gl-q073",
                "shape": "dispute",
                "verdict": "conforme",
                "nombres_attendus": 2,
                "tous_les_nombres": True,
                "refus": False,
            },
        ],
        "stabilite": {"reponses_identiques": "0/1", "tous_les_nombres_identiques": "0/1"},
    }
    reference_path = tmp_path / "fine-notations.json"
    output_path = tmp_path / "rapport.md"
    reference_path.write_text(__import__("json").dumps(reference_payload), encoding="utf-8")
    ecg.write_noter_report(
        local_payload,
        reference_path=reference_path,
        output_path=output_path,
        local_name="hybride_fenetres_g12",
        reference_name="fine_tours_k12",
    )
    text = output_path.read_text(encoding="utf-8")
    assert "Conformes /141" in text
    assert "Disputes conformes /28" in text
    assert "Refus" in text
    assert "Stabilité" in text
