"""Tests hors ligne — issue #127 brain_prod par dossier et proxy cluster."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from banc_realite import etage3 as e3
from banc_realite.config import BANC_ROOT
from banc_realite.dossiers import dossier_courant
from banc_realite.mesure_comparatif_etage2 import _fichier_mesure_complet, run_mesure


def test_compile_cadre_prod_greenloop_run_search_inchange(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_run_search(query: str, **kwargs: Any) -> dict[str, Any]:
        captured.update(kwargs)
        return {"evidence": [], "warnings": []}

    def fake_compile_call_frame(_req, search_fn=None):
        if search_fn is not None:
            search_fn("probe", 8)
        return {"rendered": "", "retrieval": {"evidence": [], "warnings": []}}

    monkeypatch.setattr("brain.search.run_search", fake_run_search)
    monkeypatch.setattr("brain.call_frame.compile_call_frame", fake_compile_call_frame)
    monkeypatch.setattr("banc_realite.search_health.is_search_healthy", lambda _r: (True, ""))

    greenloop = dossier_courant("greenloop")
    question = {"id": "gl-q001", "question": "What is the term?"}
    cache = {"What is the term?": [0.1, 0.2]}
    e3.compile_cadre_prod(question, top_k=8, embed_cache=cache)
    assert captured["instance"] == "greenloop"
    assert captured["vault_ref"] == "greenloop"
    assert captured["repo_root"] == greenloop.area_root


def test_compile_cadre_prod_moreau_replie_embedding_structure(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[str] = []

    def fake_run_search(query: str, **kwargs: Any) -> dict[str, Any]:
        seen.append(query)
        return {"evidence": [], "warnings": []}

    def fake_compile_call_frame(req, search_fn=None):
        if search_fn is not None:
            search_fn(f"{req['user_message']} MOREAU", 8)
        return {"rendered": "", "retrieval": {"evidence": [], "warnings": []}}

    monkeypatch.setattr("brain.search.run_search", fake_run_search)
    monkeypatch.setattr("brain.call_frame.compile_call_frame", fake_compile_call_frame)
    monkeypatch.setattr("banc_realite.search_health.is_search_healthy", lambda _r: (True, ""))

    moreau = dossier_courant("moreau")
    question = {"id": "MOR-Q01", "question": "Question MOREAU ?"}
    cache = {"Question MOREAU ?": [0.3, 0.4]}
    e3.compile_cadre_prod(question, top_k=8, embed_cache=cache, dossier=moreau)
    assert seen == ["Question MOREAU ? MOREAU"]


def test_compile_cadre_prod_moreau_parametres_et_isolation_vault(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_run_search(query: str, **kwargs: Any) -> dict[str, Any]:
        captured.update(kwargs)
        vault_ref = kwargs.get("vault_ref")
        if vault_ref == "moreau":
            return {
                "evidence": [
                    {
                        "kind": "claim_hit",
                        "source": "01-contrat-travail-cdi.md",
                        "text": "MOREAU",
                    }
                ],
                "warnings": [],
            }
        return {
            "evidence": [{"kind": "claim_hit", "source": "09-january-scale-export.md", "text": "GL"}],
            "warnings": [],
        }

    def fake_compile_call_frame(req, search_fn=None):
        assert req["responsibility"] == "MOREAU"
        assert req["conversation_state"]["responsibility_context"] == "MOREAU"
        result = search_fn("probe", 8) if search_fn else {"evidence": [], "warnings": []}
        return {"rendered": "", "retrieval": result}

    monkeypatch.setattr("brain.search.run_search", fake_run_search)
    monkeypatch.setattr("brain.call_frame.compile_call_frame", fake_compile_call_frame)
    monkeypatch.setattr("banc_realite.search_health.is_search_healthy", lambda _r: (True, ""))

    moreau = dossier_courant("moreau")
    question = {"id": "MOR-Q01", "question": "Question MOREAU ?"}
    cache = {"Question MOREAU ?": [0.3, 0.4]}
    cadre = e3.compile_cadre_prod(question, top_k=8, embed_cache=cache, dossier=moreau)
    assert captured["instance"] == "moreau"
    assert captured["vault_ref"] == "moreau"
    assert captured["repo_root"] == moreau.area_root
    sources = [item.get("source") for item in cadre["evidence"]]
    assert sources == ["01-contrat-travail-cdi.md"]
    assert "09-january-scale-export.md" not in sources


def test_is_running_rapporte_trois_couches(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("banc_realite.infra._tcp_open", lambda port: port == 56102)
    monkeypatch.setattr("banc_realite.infra._postgrest_layer_ready", lambda: True)
    monkeypatch.setattr("banc_realite.infra._proxy_layer_ready", lambda: False)
    from banc_realite.infra import cluster_ready, is_running

    status = is_running()
    assert status == {"56102": True, "56101": True, "56100": False}
    assert cluster_ready() is False


def test_start_cluster_relance_couches_sans_postgres(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    def fake_status() -> dict[str, bool]:
        return {"56102": True, "56101": False, "56100": False}

    monkeypatch.setattr("banc_realite.infra.is_running", fake_status)
    monkeypatch.setattr(
        "banc_realite.infra.demarrer_cluster",
        lambda **kwargs: calls.append(f"demarrer:{kwargs}"),
    )
    monkeypatch.setattr(
        "banc_realite.infra.subprocess.run",
        lambda *args, **kwargs: calls.append("subprocess"),
    )
    from banc_realite.infra import start_cluster

    start_cluster()
    assert calls == ["demarrer:{'postgres': False}"]
    assert "subprocess" not in calls


def test_start_cluster_ne_touche_pas_postgres_quand_56102_repond(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []

    monkeypatch.setattr(
        "banc_realite.infra.is_running",
        lambda: {"56102": True, "56101": True, "56100": True},
    )
    monkeypatch.setattr(
        "banc_realite.infra.demarrer_cluster",
        lambda **kwargs: calls.append("demarrer"),
    )
    from banc_realite.infra import start_cluster

    start_cluster()
    assert calls == []


def test_reprendre_saute_fichier_complet_et_recalcule_partiel(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    moreau = dossier_courant("moreau")
    comparatif = tmp_path / "comparatif"
    comparatif.mkdir()
    monkeypatch.setattr(
        type(moreau),
        "comparatif_dir",
        property(lambda self: comparatif),
    )

    questions = [{"id": "MOR-Q01", "question": "q1", "shape": "citation"}]
    complete = {
        "fournisseur": "rag_naif",
        "k_fixe": False,
        "runs": [
            {
                "k": 8,
                "budget": 12000,
                "questions": [{"question_id": "MOR-Q01", "shape": "citation"}],
            }
        ],
    }
    partial = {
        "fournisseur": "brain_prod",
        "k_fixe": False,
        "runs": [
            {
                "k": 8,
                "budget": 12000,
                "questions": [],
            }
        ],
    }
    (comparatif / "etage2-rag_naif.json").write_text(json.dumps(complete), encoding="utf-8")
    (comparatif / "etage2-brain_prod.json").write_text(json.dumps(partial), encoding="utf-8")

    assert _fichier_mesure_complet(
        comparatif / "etage2-rag_naif.json",
        nom="rag_naif",
        ks=[8],
        budgets=[12000],
        questions=questions,
    )
    assert not _fichier_mesure_complet(
        comparatif / "etage2-brain_prod.json",
        nom="brain_prod",
        ks=[8],
        budgets=[12000],
        questions=questions,
    )

    mesures: list[str] = []

    def fake_mesurer(nom: str, **kwargs: Any) -> dict[str, Any]:
        mesures.append(nom)
        return {"fournisseur": nom, "k_fixe": False, "runs": complete["runs"]}

    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2.export_runtime_env", lambda: None)
    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2.load_questions", lambda _d: questions)
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.load_gold",
        lambda _d: {"assertions": [], "assertion_index": {}},
    )
    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2.verifier_or_coherent", lambda *_a, **_k: None)
    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2.verifier_parite", lambda _d: None)
    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2.exiger_contextes_dossier", lambda *_a, **_k: None)
    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2._load_embed_cache", lambda _d: {"q1": [0.1]})
    monkeypatch.setattr("banc_realite.infra.start_cluster", lambda: None)
    monkeypatch.setattr("banc_realite.production.restart_postgrest_public", lambda **_k: None)
    monkeypatch.setattr("banc_realite.infra.connect_existing", lambda: object())
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._read_public_claims",
        lambda _c, vault_ref=None: [],
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.build_holder_table",
        lambda *_a, **_k: ({}, None, None),
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.partager",
        lambda _q: ([], []),
    )
    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2.ecrire_rapport", lambda *_a, **_k: None)
    monkeypatch.setattr("banc_realite.mesure_comparatif_etage2.mesurer_fournisseur", fake_mesurer)

    run_mesure(
        fournisseurs=["rag_naif", "brain_prod"],
        ks=[8],
        budgets=[12000],
        dossier=moreau,
        reprendre=True,
    )
    assert mesures == ["brain_prod"]
