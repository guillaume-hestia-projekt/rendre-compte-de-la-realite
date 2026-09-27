"""Tests hors ligne — mesure_comparatif_etage2."""
from __future__ import annotations

import json
from pathlib import Path

from banc_realite.controle_budget_egal import _aggregate_config_rows
from banc_realite.dossiers import dossier_courant
from banc_realite.mesure_comparatif_etage2 import (
    _compile_row,
    _disputes_denominators,
    _format_table_couts,
    _format_table_disputes,
    _format_table_par_forme,
    _fournisseur_label,
    _instancier,
    contextes_mesure_path,
    mesurer_stabilite_fournisseur,
)


class FakeProvider:
    etiquette = "fake"

    def __init__(self, elements):
        self._elements = elements

    def contexte(self, question, *, k, connection):
        del question, k, connection
        return list(self._elements)


def test_instancier_fournisseur_fichier(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.comparatif_context_path",
        lambda name, dossier=None, **kwargs: tmp_path / f"contextes-{name}.jsonl",
    )
    provider = _instancier("mem0", {})
    assert provider.etiquette == "mem0"
    letta = _instancier("letta_archive", {})
    assert letta.chemin == tmp_path / "contextes-letta_archive.jsonl"


def test_compile_row_appui(monkeypatch):
    question = {
        "id": "gl-q001",
        "shape": "single",
        "supporting_assertions": ["a1"],
    }
    gold = {
        "assertion_index": {
            "a1": {"id": "a1", "content": "foo", "quote": "foo", "source": "a.md"},
        },
        "disputes": {},
        "situations": {},
        "trajectories": {},
    }
    claims_index = {
        "c1": {
            "claim_id": "c1",
            "value": "foo",
            "source_file_path": "a.md",
            "text": "foo",
        }
    }
    evidence = [
        {
            "kind": "claim_hit",
            "id": "c1",
            "text": "foo",
            "source": "a.md",
            "payload": {"claim": claims_index["c1"]},
        }
    ]

    def fake_present(aid):
        return True, 1

    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._make_present_fn",
        lambda *_a, **_k: fake_present,
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.compute_verdict",
        lambda *_a, **_k: {"verdict": "complet"},
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._appui_summary",
        lambda *_a, **_k: {"tient": ["a1"], "candidat": [], "absents": []},
    )
    row = _compile_row(
        question,
        evidence,
        "rendered",
        gold=gold,
        claims_index=claims_index,
        assertion_index=gold["assertion_index"],
        holder_table={},
    )
    assert row["appui_tout_tient"] is True
    assert row["appui_au_moins_une"] is True


def test_agregation_par_forme_et_moitie():
    rows = [
        {
            "question_id": "gl-q084",
            "shape": "dispute",
            "evidence_count": 4,
            "caracteres": 100,
            "appui_tout_tient": False,
            "appui_au_moins_une": True,
            "deux_cotes_dans_contexte": True,
        },
        {
            "question_id": "gl-q096",
            "shape": "dispute",
            "evidence_count": 4,
            "caracteres": 100,
            "appui_tout_tient": False,
            "appui_au_moins_une": False,
            "deux_cotes_dans_contexte": False,
        },
        {
            "question_id": "gl-q001",
            "shape": "single",
            "evidence_count": 2,
            "caracteres": 50,
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
        },
    ]
    dispute_rows = [row for row in rows if row["shape"] == "dispute"]
    agg = _aggregate_config_rows(
        rows,
        dispute_rows,
        reglage_ids={"gl-q084"},
        ecart_ids={"gl-q096"},
    )
    assert agg["disputes"]["reglage_sur_14"] == 1
    assert agg["disputes"]["ecart_sur_14"] == 0
    assert agg["appui"]["par_shape"]["single"]["tout_tient"] == 1


def test_disputes_denominators_population_partielle():
    dispute_rows: list[dict] = []
    denom = _disputes_denominators(dispute_rows, reglage_ids={"gl-q084"}, ecart_ids={"gl-q096"})
    assert denom == {"disputes_total": 0, "reglage_mesure": 0, "ecart_mesure": 0}


def test_format_table_disputes_run_limite_sans_dispute():
    results = [
        {
            "fournisseur": "rag_naif",
            "k_fixe": False,
            "runs": [
                {
                    "k": 8,
                    "budget": 12000,
                    "aggregate": {
                        "disputes": {
                            "deux_cotes_sur_28": 0,
                            "reglage_sur_14": 0,
                            "ecart_sur_14": 0,
                            "disputes_total": 0,
                            "reglage_mesure": 0,
                            "ecart_mesure": 0,
                        },
                        "appui": {"par_shape": {}},
                        "appui_valeur": {"par_shape": {}},
                        "disputes_valeur": {
                            "deux_cotes_sur_28": 0,
                            "reglage_sur_14": 0,
                            "ecart_sur_14": 0,
                        },
                    },
                }
            ],
        }
    ]
    table = _format_table_par_forme(results, run_limite=5)
    assert "RUN LIMITÉ À 5 QUESTIONS — pas un résultat du banc" in table
    disputes = _format_table_disputes(
        results,
        dossier=dossier_courant("greenloop"),
        meta={
            "disputes_total": 0,
            "dispute_shape": "dispute",
            "denominateur_appui": 141,
            "questions_mesurables": 141,
            "non_etabli": 0,
        },
    )
    assert "0/0" in disputes


def test_fournisseur_label_brain_prod():
    assert _fournisseur_label("brain_prod", 8) == "brain_prod"
    assert _fournisseur_label("brain_prod", 12) == "brain_prod (variante k=12)"
    assert _fournisseur_label("rag_naif", 12) == "rag_naif"


def test_mesurer_fournisseur_journalise_extracteur_mem0(tmp_path, monkeypatch):
    contextes = tmp_path / "contextes-mem0.jsonl"
    contextes.write_text(
        json.dumps({"meta": {"k": 20, "extracteur": "cursor", "modele": "cursor-grok-4.5-high"}})
        + "\n"
        + json.dumps(
            {
                "question_id": "gl-q001",
                "elements": [
                    {"rank": 1, "score": 0.9, "text": "alpha", "source": "a.md", "provenance": {}},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2.comparatif_context_path",
        lambda name, dossier=None, **kwargs: tmp_path / f"contextes-{name}.jsonl",
    )
    greenloop = dossier_courant("greenloop")
    monkeypatch.setattr(
        type(greenloop),
        "comparatif_dir",
        property(lambda self, _p=tmp_path: _p),
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._compile_row",
        lambda *_a, **_k: {
            "question_id": "gl-q001",
            "shape": "single",
            "evidence_count": 1,
            "caracteres": 10,
            "tokens_estimes": 2.5,
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "verdict": "complet",
        },
    )
    from banc_realite.mesure_comparatif_etage2 import mesurer_fournisseur

    payload = mesurer_fournisseur(
        "mem0",
        connection=None,
        ks=[8],
        budgets=[12000],
        questions=[{"id": "gl-q001", "question": "q?", "shape": "single"}],
        gold={"assertion_index": {}, "disputes": {}, "situations": {}, "trajectories": {}},
        claims_index={},
        assertion_index={},
        holder_table={},
        embed_cache={},
        reglage_ids=set(),
        ecart_ids=set(),
    )
    assert payload["extracteur"] == "cursor"
    assert payload["modele"] == "cursor-grok-4.5-high"
    assert contextes_mesure_path("mem0", dossier=greenloop).is_file()


def test_mesurer_fournisseur_ecrit_contextes_recherche(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant
    from banc_realite.mesure_comparatif_etage2 import mesurer_fournisseur

    greenloop = dossier_courant("greenloop")
    monkeypatch.setattr(type(greenloop), "comparatif_dir", property(lambda self, _p=tmp_path: _p))

    class Provider:
        etiquette = "rag_naif"

        def contexte(self, question, *, k, connection):
            del connection
            return [
                {
                    "kind": "file_hit",
                    "id": f"{question['id']}:{k}",
                    "text": f"texte {question['id']}",
                    "source": "a.md",
                }
            ]

    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._instancier",
        lambda *_a, **_k: Provider(),
    )
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._compile_row",
        lambda *_a, **_k: {
            "question_id": "gl-q001",
            "shape": "single",
            "evidence_count": 1,
            "caracteres": 10,
            "tokens_estimes": 2.5,
            "appui_tout_tient": True,
            "appui_au_moins_une": True,
            "appui_tout_tient_valeur": True,
            "appui_au_moins_une_valeur": True,
            "verdict": "complet",
        },
    )
    mesurer_fournisseur(
        "rag_naif",
        connection=None,
        ks=[8],
        budgets=[12000],
        questions=[{"id": "gl-q001", "question": "q?", "shape": "single"}],
        gold={"assertion_index": {}, "disputes": {}, "situations": {}, "trajectories": {}},
        claims_index={},
        assertion_index={},
        holder_table={},
        embed_cache={},
        reglage_ids=set(),
        ecart_ids=set(),
        dossier=greenloop,
    )
    path = contextes_mesure_path("rag_naif", dossier=greenloop)
    assert path.is_file()
    payload = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert payload[0]["meta"]["fournisseur"] == "rag_naif"
    assert any(row.get("question_id") == "gl-q001" for row in payload[1:])


def test_stabilite_compte_question_instable(tmp_path, monkeypatch):
    from banc_realite.dossiers import dossier_courant

    greenloop = dossier_courant("greenloop")
    monkeypatch.setattr(type(greenloop), "comparatif_dir", property(lambda self, _p=tmp_path: _p))

    class Provider:
        etiquette = "rag_naif"

        def __init__(self):
            self.calls = 0

        def contexte(self, question, *, k, connection):
            del connection
            self.calls += 1
            text = "alpha" if self.calls == 1 else "beta"
            return [{"kind": "file_hit", "id": str(self.calls), "text": text, "source": "a.md"}]

    provider = Provider()
    monkeypatch.setattr(
        "banc_realite.mesure_comparatif_etage2._instancier",
        lambda *_a, **_k: provider,
    )
    questions = [
        {
            "id": "gl-q001",
            "shape": "single",
            "supporting_assertions": ["a1"],
            "question": "q?",
        }
    ]
    assertion_index = {
        "a1": {"id": "a1", "quote": "alpha", "content": "alpha", "source": "a.md"},
    }
    payload = mesurer_stabilite_fournisseur(
        "rag_naif",
        connection=None,
        ks=[8],
        budgets=[12000],
        questions=questions,
        assertion_index=assertion_index,
        claims_index={},
        embed_cache={},
        stabilite=2,
        dossier=greenloop,
    )
    assert payload["instables"] == 1
    assert payload["par_mode"]["verbatim"] == "1/1"


def test_format_table_couts_cursor_sans_montant_mistral(tmp_path, monkeypatch):
    from banc_realite.tiers_mem0 import Mem0Chemins

    class FakeChemins:
        racine = tmp_path

        def sortie_a_blanc(self, extracteur: str) -> Path:
            return tmp_path / f"ingestion-mem0-{extracteur}.a-blanc.json"

    monkeypatch.setattr(Mem0Chemins, "pour", lambda dossier=None: FakeChemins())
    payload = {
        "appels_prevus": 5,
        "cout_ingestion_eur": None,
        "cout_contextes_eur": 0.001,
        "appels_contextes_prevus": 3,
        "cout": "quota Cursor, 5 appels prévus",
    }
    (tmp_path / "ingestion-mem0-cursor.a-blanc.json").write_text(json.dumps(payload), encoding="utf-8")
    table = _format_table_couts()
    assert "quota Cursor, 5 appels prévus" in table
    assert "None €" not in table
