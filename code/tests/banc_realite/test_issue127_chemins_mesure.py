"""Tests hors ligne — issue #127 cache/contextes/comparatif par dossier."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite.config import SORTIES
from banc_realite.dossiers import dossier_courant
from banc_realite.fournisseurs_contexte import FournisseurFichier, comparatif_context_path
from banc_realite.measure_etage2 import _embed_cache_path, _load_embed_cache
from banc_realite.mesure_comparatif_etage2 import run_mesure


def test_load_embed_cache_suit_dossier(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    moreau_file = tmp_path / "moreau.json"
    green_file = tmp_path / "green.json"
    moreau_file.write_text(json.dumps({"m": [1.0]}), encoding="utf-8")
    green_file.write_text(json.dumps({"g": [2.0]}), encoding="utf-8")

    def fake_path(dossier=None):
        if dossier is not None and dossier.nom == "moreau":
            return moreau_file
        return green_file

    monkeypatch.setattr("banc_realite.measure_etage2._embed_cache_path", fake_path)
    assert _load_embed_cache(dossier_courant("moreau")) == {"m": [1.0]}
    assert _load_embed_cache() == {"g": [2.0]}


def test_embed_cache_path_greenloop_non_regression() -> None:
    greenloop = dossier_courant("greenloop")
    assert _embed_cache_path(greenloop) == SORTIES / "etage2-question-embeddings.json"
    assert _embed_cache_path() == SORTIES / "etage2-question-embeddings.json"


def test_comparatif_context_path_moreau_et_greenloop() -> None:
    moreau = dossier_courant("moreau")
    greenloop = dossier_courant("greenloop")
    moreau_path = comparatif_context_path("mem0", dossier=moreau)
    green_path = comparatif_context_path("mem0")
    assert "moreau/mem0/contextes-mem0.jsonl" in str(moreau_path)
    assert str(green_path).endswith("sorties/comparatif/contextes-mem0.jsonl")
    letta_moreau = comparatif_context_path("letta_archive", dossier=moreau)
    assert "moreau/comparatif/contextes-letta_archive.jsonl" in str(letta_moreau)
    letta_green = comparatif_context_path("letta_archive")
    assert str(letta_green).endswith("sorties/comparatif/contextes-letta_archive.jsonl")


def test_fournisseur_fichier_refuse_prefixe_incoherent_moreau(tmp_path: Path) -> None:
    path = tmp_path / "contextes-mem0.jsonl"
    path.write_text(
        json.dumps({"question_id": "gl-q001", "elements": []}) + "\n",
        encoding="utf-8",
    )
    provider = FournisseurFichier("letta_archive", path, dossier=dossier_courant("moreau"))
    with pytest.raises(ValueError, match="préfixe"):
        provider._load()


def test_verifier_seulement_sans_score_ni_rapport(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    moreau = dossier_courant("moreau")

    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.export_runtime_env",
        lambda: None,
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.load_questions",
        lambda _d: [{"id": "MOR-Q01", "question": "q1"}],
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.load_gold",
        lambda _d: {"assertions": [], "assertion_index": {}},
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.verifier_or_coherent",
        lambda *_a, **_k: None,
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.verifier_parite",
        lambda _d: None,
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.exiger_contextes_dossier",
        lambda *_a, **_k: None,
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._load_embed_cache",
        lambda _d: {"q1": [0.1]},
    )

    ctx = tmp_path / "contextes-mem0.jsonl"
    ctx.write_text(
        json.dumps({"meta": {"k": 20}})
        + "\n"
        + json.dumps({"question_id": "MOR-Q01", "elements": []})
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.comparatif_context_path",
        lambda _nom, dossier=None, **kwargs: ctx,
    )

    def fail_ecrire_rapport(*_a, **_k) -> None:
        raise AssertionError("ecrire_rapport ne doit pas être appelé")

    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.ecrire_rapport",
        fail_ecrire_rapport,
    )

    result = run_mesure(
        fournisseurs=["mem0"],
        ks=[20],
        budgets=[12000],
        dossier=moreau,
        verifier_seulement=True,
    )
    assert result["status"] == "verifie"
    assert "chemins" in result


def test_start_cluster_ne_fait_rien_quand_port_repond(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple] = []

    monkeypatch.setattr(
        "banc_realite.infra.is_running",
        lambda: {"56102": True, "56101": True, "56100": True},
    )
    monkeypatch.setattr(
        "banc_realite.infra.subprocess.run",
        lambda *args, **kwargs: calls.append((args, kwargs)),
    )
    from banc_realite.infra import start_cluster

    start_cluster()
    assert calls == []
