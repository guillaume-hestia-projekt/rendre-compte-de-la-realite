"""Fenêtre calibrée sur l'or MOREAU — calcul, caches séparés, invariants GreenLoop."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite import etage3_config_gagnante as ecg
from banc_realite.dossiers import dossier_courant
from banc_realite.embarquer_phrases import (
    calculer_fenetre_depuis_or,
    compter_citations_dans_fenetres,
    run_embarquer_phrases_calibrees,
)
from banc_realite.fournisseurs_contexte import BrainBanc, BrainBancCalibre
from banc_realite.mesure_comparatif_etage2 import _instancier
from banc_realite.porte_phrase import phrases_du_passage


def _passages_from_pieces(pieces: dict[str, str]) -> list[tuple[str, str, str]]:
    return [(str(index), name, text) for index, (name, text) in enumerate(pieces.items())]


def test_calculer_fenetre_grandit_avec_citation_longue():
    piece = "doc.md"
    short = {
        "id": "A-short",
        "source": piece,
        "quote": "Phrase courte avec assez de caractères pour compter.",
    }
    passages_short = _passages_from_pieces(
        {piece: "Phrase courte avec assez de caractères pour compter."}
    )
    dossier = dossier_courant("moreau")
    cal_short = calculer_fenetre_depuis_or(passages_short, [short], dossier=dossier)
    long_quote = (
        "Première phrase assez longue pour le test de calibration des fenêtres. "
        "Deuxième phrase qui prolonge le passage sans le fermer trop tôt. "
        "Troisième phrase indispensable pour contenir entièrement la citation calibrée."
    )
    long = {"id": "A-long", "source": piece, "quote": long_quote}
    passages_long = _passages_from_pieces({piece: long_quote})
    cal_long = calculer_fenetre_depuis_or(passages_long, [long], dossier=dossier)
    assert cal_short["fenetre_phrases"] <= cal_long["fenetre_phrases"]
    assert cal_long["fenetre_phrases"] >= 3


def test_cache_calibre_ne_remplace_pas_cache_origine(tmp_path, monkeypatch):
    moreau = dossier_courant("moreau")
    origine = tmp_path / "phrases-embeddings.json"
    calibre = tmp_path / "phrases-embeddings-calibrees.json"
    meta = tmp_path / "fenetre-calibree.json"
    origine.write_text(json.dumps({"unité origine": [0.1, 0.2]}), encoding="utf-8")
    calibre.write_text("{}", encoding="utf-8")
    meta.write_text(json.dumps({"fenetre_phrases": 3}), encoding="utf-8")

    monkeypatch.setattr(moreau.__class__, "cache_phrases_embeddings", property(lambda _s: origine))
    monkeypatch.setattr(
        moreau.__class__,
        "cache_phrases_embeddings_calibrees",
        property(lambda _s: calibre),
    )
    monkeypatch.setattr(moreau.__class__, "meta_fenetre_calibree", property(lambda _s: meta))

    passages = [("1", "doc.md", "Brand new calibrated unit with enough length here.")]
    calls: list[list[str]] = []

    def fake_embed(batch: list[str]) -> list[list[float]]:
        calls.append(batch)
        return [[0.3] * 1024 for _ in batch]

    monkeypatch.setattr(
        "banc_realite.embarquer_phrases._fetch_passages",
        lambda _conn, vault_ref=None: passages,
    )
    monkeypatch.setattr(
        "banc_realite.embarquer_phrases.calculer_fenetre_depuis_or",
        lambda *_a, **_k: {
            "fenetre_phrases": 3,
            "calcul": "test",
            "citations_dans_une_fenetre": "1/1",
            "citations_manquantes": [],
            "citations_manquantes_detail": [],
            "fenetre_origine_2": "1/1",
        },
    )

    summary = run_embarquer_phrases_calibrees(
        moreau,
        dry_run=False,
        connection=object(),
        embed_fn=fake_embed,
        max_appels=10,
    )
    assert summary["embeddings"] == 1
    assert json.loads(origine.read_text()) == {"unité origine": [0.1, 0.2]}
    calibre_payload = json.loads(calibre.read_text())
    assert any("Brand new calibrated unit" in key for key in calibre_payload)


def test_brain_banc_origine_inchange():
    assert ecg.PORTE_PHRASE_HYBRIDE_FENETRES_G12 == {
        "etiquette": "hyb_vec_f2_b12_g12",
        "hybride": {"k": 18, "n_tours": 2, "k_tour1": 12},
        "brute_k": 12,
        "phrases": {
            "n_par_passage": 2,
            "max_phrases": 12,
            "mode": "vectoriel",
            "selection": "globale",
            "fenetre": 2,
        },
    }
    provider = BrainBanc({}, dossier=dossier_courant("moreau"))
    assert provider._config is ecg.CONFIGURATIONS["hybride_fenetres_g12"]["porte_phrase_config"]


def test_brain_banc_calibre_utilise_config_et_cache_separes(tmp_path, monkeypatch):
    moreau = dossier_courant("moreau")
    meta = tmp_path / "fenetre-calibree.json"
    cache = tmp_path / "phrases-embeddings-calibrees.json"
    meta.write_text(json.dumps({"fenetre_phrases": 4}), encoding="utf-8")
    cache.write_text(json.dumps({"unit": [0.5] * 1024}), encoding="utf-8")
    monkeypatch.setattr(moreau.__class__, "meta_fenetre_calibree", property(lambda _s: meta))
    monkeypatch.setattr(
        moreau.__class__,
        "cache_phrases_embeddings_calibrees",
        property(lambda _s: cache),
    )
    provider = BrainBancCalibre({}, dossier=moreau)
    assert provider._config["phrases"]["fenetre"] == 4
    assert provider._phrases() == {"unit": [0.5] * 1024}


def test_greenloop_chemins_cache_inchanges():
    greenloop = dossier_courant("greenloop")
    assert str(greenloop.cache_phrases_embeddings).endswith("sorties/phrases-embeddings.json")
    assert str(greenloop.cache_phrases_embeddings_calibrees).endswith(
        "sorties/phrases-embeddings-calibrees.json"
    )
    with pytest.raises(RuntimeError, match="GreenLoop"):
        run_embarquer_phrases_calibrees("greenloop", dry_run=True, connection=object())


def test_instancier_brain_banc_calibre():
    moreau = dossier_courant("moreau")
    meta_path = moreau.meta_fenetre_calibree
    if not meta_path.is_file():
        pytest.skip("métadonnées calibrées absentes sur ce VPS")
    provider = _instancier("brain_banc_calibre", {}, dossier=moreau)
    assert provider.etiquette == "brain_banc_calibre"


def test_fenetre3_couvre_citation_trois_phrases():
    from banc_realite.porte_phrase import _max_chars_fenetre

    assert _max_chars_fenetre(2) == 450
    assert _max_chars_fenetre(3) == 600
    s1 = "A" * 150
    s2 = "B" * 150
    s3 = "C" * 150
    prose = f"{s1}. {s2}. {s3}."
    quote = f"{s1}. {s2}. {s3}"
    passages = _passages_from_pieces({"doc.md": prose})
    assertion = {"id": "x", "source": "doc.md", "quote": quote}
    cov2 = compter_citations_dans_fenetres(passages, [assertion], fenetre=2)
    assert cov2["citations_dans_une_fenetre"] == "0/1"
    cov3 = compter_citations_dans_fenetres(passages, [assertion], fenetre=3)
    assert cov3["citations_dans_une_fenetre"] == "1/1"
