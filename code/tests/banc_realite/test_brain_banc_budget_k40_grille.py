"""mem0 k40, g48 et grille budget égal (issue #127)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite import etage3_config_gagnante as ecg
from banc_realite.dossiers import dossier_courant
from banc_realite.fournisseurs_contexte import FournisseurFichier, comparatif_context_path
from banc_realite.mesure_comparatif_etage2 import (
    construire_grille_budget_egal,
    k_effectif_fournisseur,
)
from banc_realite.tiers_mem0 import Mem0Chemins


def test_mem0_context_path_k20_et_k40():
    moreau = dossier_courant("moreau")
    assert comparatif_context_path("mem0", dossier=moreau, k=20).name == "contextes-mem0.jsonl"
    assert comparatif_context_path("mem0", dossier=moreau, k=12).name == "contextes-mem0.jsonl"
    assert comparatif_context_path("mem0", dossier=moreau, k=40).name == "contextes-mem0-k40.jsonl"


def test_fournisseur_fichier_mem0_choisit_fichier_par_k(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    k20 = tmp_path / "contextes-mem0.jsonl"
    k40 = tmp_path / "contextes-mem0-k40.jsonl"
    k20.write_text(
        json.dumps({"meta": {"k": 20}})
        + "\n"
        + json.dumps(
            {
                "question_id": "gl-q001",
                "elements": [
                    {"rank": i, "text": f"t{i}", "source": "a.md", "provenance": {}}
                    for i in range(1, 21)
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    k40.write_text(
        json.dumps({"meta": {"k": 40}})
        + "\n"
        + json.dumps(
            {
                "question_id": "gl-q001",
                "elements": [
                    {"rank": i, "text": f"u{i}", "source": "a.md", "provenance": {}}
                    for i in range(1, 41)
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    def fake_path(_etiquette, dossier=None, *, k=20):
        return k20 if k <= 20 else k40

    monkeypatch.setattr(
        "banc_realite.tiers_mem0.comparatif_context_path",
        fake_path,
    )
    provider = FournisseurFichier("mem0", dossier=dossier_courant("greenloop"))
    out20 = provider.contexte({"id": "gl-q001", "question": "q?"}, k=20, connection=None)
    out40 = provider.contexte({"id": "gl-q001", "question": "q?"}, k=40, connection=None)
    assert len(out20) == 20
    assert out20[0]["text"] == "t1"
    assert len(out40) == 40
    assert out40[0]["text"] == "u1"

    missing = tmp_path / "contextes-mem0-k30.jsonl"
    monkeypatch.setattr(
        "banc_realite.tiers_mem0.comparatif_context_path",
        lambda *_a, **k: missing,
    )
    with pytest.raises(FileNotFoundError):
        FournisseurFichier("mem0").contexte(
            {"id": "gl-q001", "question": "q?"}, k=30, connection=None
        )


def test_contextes_k40_n_ecrase_pas_k20(monkeypatch, tmp_path: Path):
    import banc_realite.tiers_mem0 as tm

    class FakeMemory:
        @classmethod
        def from_config(cls, _config):
            return cls()

        def search(self, query, *, filters, top_k):
            return {"results": [{"memory": "s", "score": 0.9, "metadata": {"piece": "a.md"}}]}

    monkeypatch.setitem(__import__("sys").modules, "mem0", type("mem0", (), {"Memory": FakeMemory})())
    monkeypatch.setattr("brain.adapters.mistral_embeddings.load_api_key", lambda api_key=None: "secret")
    monkeypatch.setattr(tm, "_load_questions", lambda dossier=None: [{"id": "gl-q001", "question": "q?"}])
    monkeypatch.setattr(tm, "_choisir_modele_mistral", lambda _key: "mistral-large-latest")
    monkeypatch.setattr(tm, "COMPARATIF_DIR", tmp_path)
    k20 = tmp_path / "contextes-mem0.jsonl"
    k20.write_text(json.dumps({"meta": {"k": 20}}) + "\n", encoding="utf-8")
    tm.contextes(k=40)
    assert (tmp_path / "contextes-mem0-k40.jsonl").is_file()
    assert k20.read_text(encoding="utf-8").strip() == json.dumps({"meta": {"k": 20}})


def test_hybride_fenetres_g12_inchange_bit_pour_bit():
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


def test_g48_configuration():
    g48 = ecg.PORTE_PHRASE_HYBRIDE_FENETRES_G48
    assert g48["brute_k"] == 48
    assert g48["phrases"]["max_phrases"] == 48
    assert k_effectif_fournisseur("brain_banc_g48") == 48


def test_grille_budget_egal_synthetique():
    results = [
        {
            "fournisseur": "rag_naif",
            "k_fixe": False,
            "runs": [
                {
                    "budget": 8000,
                    "k": 12,
                    "k_effectif": 12,
                    "aggregate": {
                        "rendu": {"caracteres": {"mediane": 7900}},
                        "appui": {"tout_tient_sur_141": 10},
                        "appui_valeur": {"tout_tient_sur_141": 12},
                    },
                },
                {
                    "budget": 8000,
                    "k": 20,
                    "k_effectif": 20,
                    "aggregate": {
                        "rendu": {"caracteres": {"mediane": 8100}},
                        "appui": {"tout_tient_sur_141": 11},
                        "appui_valeur": {"tout_tient_sur_141": 13},
                    },
                },
            ],
        }
    ]
    payload = construire_grille_budget_egal(
        results,
        budgets=[8000],
        dossier=dossier_courant("greenloop"),
    )
    cell = payload["grille"]["rag_naif"]["8000"]
    assert cell[0] == 10
    assert cell[4] == 7900
