"""Tests hors ligne — fournisseurs_contexte."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite.fournisseurs_contexte import (
    BrainProd,
    FournisseurContexte,
    FournisseurFichier,
    RagNaif,
    rendre_contexte,
)


def test_protocol_fournisseur_fichier():
    provider = FournisseurFichier("letta_archive", Path("/tmp/absent.jsonl"))
    assert isinstance(provider, FournisseurContexte)
    assert provider.etiquette == "letta_archive"


def test_fournisseur_fichier_refuse_absent_et_incomplet(tmp_path):
    import pytest

    absent = FournisseurFichier("letta_archive", tmp_path / "contextes-letta.jsonl")
    with pytest.raises(FileNotFoundError):
        absent.contexte({"id": "gl-q001", "question": "q?"}, k=2, connection=None)
    path = tmp_path / "contextes-letta.jsonl"
    path.write_text(json.dumps({"question_id": "gl-q001", "elements": []}) + "\n", encoding="utf-8")
    partiel = FournisseurFichier("letta_archive", path)
    assert partiel.contexte({"id": "gl-q001", "question": "q?"}, k=2, connection=None) == []
    with pytest.raises(KeyError):
        partiel.contexte({"id": "gl-q002", "question": "q?"}, k=2, connection=None)


def test_fournisseur_fichier_retourne_k_premiers(tmp_path):
    path = tmp_path / "contextes-letta.jsonl"
    path.write_text(
        json.dumps(
            {
                "question_id": "gl-q001",
                "elements": [
                    {"rank": 1, "score": 0.9, "text": "alpha", "source": "a.md", "provenance": {}},
                    {"rank": 2, "score": 0.8, "text": "beta", "source": "b.md", "provenance": {}},
                    {"rank": 3, "score": 0.7, "text": "gamma", "source": "c.md", "provenance": {}},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    provider = FournisseurFichier("letta_archive", path)
    out = provider.contexte({"id": "gl-q001", "question": "q?"}, k=2, connection=None)
    assert len(out) == 2
    assert out[0]["text"] == "alpha"
    assert out[1]["text"] == "beta"


def test_rendre_contexte_respecte_budget_texte():
    elements = [
        {"rank": 1, "text": "aaaa" * 20, "source": "a.md"},
        {"rank": 2, "text": "bbbb" * 20, "source": "b.md"},
        {"rank": 3, "text": "cccc" * 20, "source": "c.md"},
    ]
    rendered, kept = rendre_contexte(elements, budget_chars=50, style="texte")
    assert len(rendered) <= 50
    assert len(kept) < 3


def test_rendre_contexte_texte_inclut_etiquette_source():
    elements = [
        {"rank": 1, "text": "alpha", "source": "a.md"},
        {"rank": 2, "text": "beta", "provenance": {"source_file_path": "b.md"}},
        {"rank": 3, "text": "gamma"},
    ]
    rendered, kept = rendre_contexte(elements, budget_chars=500, style="texte")
    assert "[a.md]" in rendered
    assert "[b.md]" in rendered
    assert "[source inconnue]" in rendered
    assert len(kept) == 3


def test_rendre_contexte_texte_compte_etiquette_dans_budget():
    elements = [
        {"rank": 1, "text": "x" * 40, "source": "a.md"},
        {"rank": 2, "text": "y" * 40, "source": "b.md"},
    ]
    rendered, kept = rendre_contexte(elements, budget_chars=60, style="texte")
    assert len(rendered) <= 60
    assert len(kept) == 1
    assert rendered.startswith("- [")


def test_fournisseur_fichier_expose_meta(tmp_path):
    path = tmp_path / "contextes-letta.jsonl"
    path.write_text(
        json.dumps({"meta": {"k": 20, "extracteur": "mistral", "modele": "mistral-large-latest"}})
        + "\n"
        + json.dumps({"question_id": "gl-q001", "elements": []})
        + "\n",
        encoding="utf-8",
    )
    provider = FournisseurFichier("letta_archive", path)
    assert provider.meta == {"k": 20, "extracteur": "mistral", "modele": "mistral-large-latest"}


def test_fournisseur_fichier_refuse_k_superieur_au_fichier(tmp_path):
    path = tmp_path / "contextes-letta.jsonl"
    path.write_text(
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
    provider = FournisseurFichier("letta_archive", path)
    assert len(provider.contexte({"id": "gl-q001", "question": "q?"}, k=20, connection=None)) == 20
    with pytest.raises(ValueError, match="k=30"):
        provider.contexte({"id": "gl-q001", "question": "q?"}, k=30, connection=None)


def test_rag_naif_utilise_requete_structuree(monkeypatch):
    captured: dict[str, object] = {}

    def fake_search(connection, query, *, query_vector, top_k, vault_ref=None):
        captured.update(
            {
                "connection": connection,
                "query": query,
                "query_vector": query_vector,
                "top_k": top_k,
            }
        )
        return []

    monkeypatch.setattr(
        "banc_realite.fournisseurs_contexte.search_passages_hybrid",
        fake_search,
    )
    cache = {"What is the term?": [0.1, 0.2]}
    provider = RagNaif(cache)
    question = {"id": "gl-q001", "question": "What is the term?"}
    provider.contexte(question, k=8, connection=object())
    assert captured["query_vector"] == [0.1, 0.2]
    assert "What is the term?" in str(captured["query"])
    assert "GreenLoop" in str(captured["query"])


def test_brain_prod_via_compile_cadre_prod(monkeypatch):
    calls: list[dict] = []

    def fake_compile_cadre_prod(question, *, top_k, embed_cache, dossier=None):
        calls.append({"question": question, "top_k": top_k, "embed_cache": embed_cache})
        return {
            "evidence": [
                {
                    "kind": "claim_hit",
                    "id": "c1",
                    "score": 1.0,
                    "rank": 1,
                    "text": "prod evidence",
                    "source": "piece.md",
                    "snippet": "prod evidence",
                    "payload": {},
                    "provenance": {"source_file_path": "piece.md"},
                }
            ]
        }

    monkeypatch.setattr(
        "banc_realite.fournisseurs_contexte.compile_cadre_prod",
        fake_compile_cadre_prod,
    )
    cache = {"What is the term?": [0.1, 0.2]}
    provider = BrainProd(cache)
    question = {"id": "gl-q001", "question": "What is the term?"}
    out = provider.contexte(question, k=8, connection=None)
    assert len(out) == 1
    assert out[0]["text"] == "prod evidence"
    assert calls[0]["top_k"] == 8


def test_brain_prod_arrete_sur_retrieval_failed(monkeypatch):
    def fake_compile_call_frame(_req, search_fn=None):
        return {
            "rendered": "",
            "retrieval": {"evidence": [], "warnings": ["retrieval_failed:RuntimeError"]},
        }

    monkeypatch.setattr("brain.call_frame.compile_call_frame", fake_compile_call_frame)
    cache = {"What is the term?": [0.1, 0.2]}
    provider = BrainProd(cache)
    with pytest.raises(RuntimeError, match="recherche production échouée"):
        provider.contexte({"id": "gl-q001", "question": "What is the term?"}, k=8, connection=None)


def test_brain_prod_arrete_sur_search_degrade(monkeypatch):
    def fake_run_search(*_args, **_kwargs):
        return {"strategy": {"fusion": "legacy"}, "warnings": []}

    def fake_compile_call_frame(_req, search_fn=None):
        search_fn("query", 8)
        return {"rendered": "", "retrieval": {"evidence": []}}

    monkeypatch.setattr("brain.search.run_search", fake_run_search)
    monkeypatch.setattr("brain.call_frame.compile_call_frame", fake_compile_call_frame)
    cache = {"What is the term?": [0.1, 0.2]}
    provider = BrainProd(cache)
    with pytest.raises(RuntimeError, match="run_search dégradé"):
        provider.contexte({"id": "gl-q001", "question": "What is the term?"}, k=8, connection=None)


def test_rendre_contexte_brain_style():
    elements = [
        {
            "kind": "claim_hit",
            "id": "c1",
            "score": 1.0,
            "rank": 1,
            "text": "Fait court",
            "source": "piece.md",
            "snippet": "Fait court",
            "payload": {},
            "provenance": {"source_file_path": "piece.md"},
        }
    ]
    rendered, kept = rendre_contexte(elements, budget_chars=12000, question_id="gl-q001", style="brain")
    assert "Fait court" in rendered
    assert len(kept) == 1
