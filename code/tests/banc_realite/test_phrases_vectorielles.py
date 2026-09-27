"""Porte phrase vectorielle — sélection, dry-run, cache, configurations."""

from __future__ import annotations

import json
from pathlib import Path

from banc_realite.embarquer_phrases import compter_unites_phrases, run_embarquer_phrases
from banc_realite.mesure_porte_phrase import CONFIGURATIONS
from banc_realite.porte_phrase import porte_phrase, score_phrase


def _file_hit(ident: str, text: str, *, piece: str = "contract.md") -> dict:
    return {
        "kind": "file_hit",
        "id": ident,
        "text": text,
        "source": piece,
        "score": 0.9,
        "provenance": {"source_file_path": piece},
    }


def _unit_vector(x: float, y: float) -> list[float]:
    return [x, y, 0.0]


def test_porte_phrase_vectoriel_plus_proche():
    question = "alpha topic"
    q_vec = _unit_vector(1.0, 0.0)
    cache = {
        "Alpha beta gamma delta epsilon zeta eta theta.": _unit_vector(0.9, 0.1),
        "Quantum physics unrelated sentence here for testing.": _unit_vector(0.0, 1.0),
    }
    evidence = [_file_hit("p1", "Alpha beta gamma delta epsilon zeta eta theta.")]
    hits, stats = porte_phrase(
        question,
        evidence,
        mode="vectoriel",
        question_vector=q_vec,
        cache=cache,
        n_par_passage=1,
        max_phrases=1,
    )
    assert len(hits) == 1
    assert "Alpha beta" in hits[0]["text"]
    assert stats["unites_sans_vecteur"] == 0


def test_porte_phrase_vectoriel_unite_sans_vecteur():
    evidence = [_file_hit("p1", "Missing vector sentence with enough length here.")]
    _, stats = porte_phrase(
        "topic",
        evidence,
        mode="vectoriel",
        question_vector=_unit_vector(1.0, 0.0),
        cache={},
        n_par_passage=1,
        max_phrases=1,
    )
    assert stats["unites_sans_vecteur"] == 1


def test_porte_phrase_globale_respecte_limites():
    q_vec = _unit_vector(1.0, 0.0)
    cache = {
        "First long sentence from passage one for vector ranking.": _unit_vector(0.95, 0.0),
        "Second long sentence from passage one still relevant.": _unit_vector(0.90, 0.0),
        "Third long sentence from passage one lower score here.": _unit_vector(0.50, 0.0),
        "First long sentence from passage two with good match.": _unit_vector(0.85, 0.0),
        "Second long sentence from passage two medium match.": _unit_vector(0.80, 0.0),
        "Third long sentence from passage two weaker match.": _unit_vector(0.40, 0.0),
    }
    evidence = [
        _file_hit(
            "p1",
            "\n".join(
                [
                    "First long sentence from passage one for vector ranking.",
                    "Second long sentence from passage one still relevant.",
                    "Third long sentence from passage one lower score here.",
                ]
            ),
            piece="a.md",
        ),
        _file_hit(
            "p2",
            "\n".join(
                [
                    "First long sentence from passage two with good match.",
                    "Second long sentence from passage two medium match.",
                    "Third long sentence from passage two weaker match.",
                ]
            ),
            piece="b.md",
        ),
    ]
    hits, stats = porte_phrase(
        "match",
        evidence,
        mode="vectoriel",
        question_vector=q_vec,
        cache=cache,
        selection="globale",
        n_par_passage=2,
        max_phrases=3,
    )
    assert stats["unites_sans_vecteur"] == 0
    assert len(hits) == 3
    per_passage = {}
    for hit in hits:
        pid = hit["provenance"]["passage_id"]
        per_passage[pid] = per_passage.get(pid, 0) + 1
    assert all(count <= 2 for count in per_passage.values())


def test_porte_phrase_lexical_inchange():
    question = "customer responsible contents collection WT tickets"
    passage = """\
The customer remains responsible for contents until collection.
Only WT-series tickets are included; other forms are excluded.
This restriction lasts for seven years after the service ends; extensions apply.
"""
    evidence = [_file_hit("p1", passage, piece="a.md")]
    hits, stats = porte_phrase(
        question,
        evidence,
        mode="lexical",
        n_par_passage=2,
        max_phrases=2,
    )
    assert stats["unites_sans_vecteur"] == 0
    assert len(hits) == 2
    assert hits[0]["score"] == score_phrase(question, hits[0]["text"])


def test_compter_unites_phrases_dry_run():
    passages = [
        ("1", "First sentence with enough characters here for unit one."),
        ("2", "First sentence with enough characters here for unit one.\nAnother unique sentence with enough characters."),
    ]
    stats = compter_unites_phrases(passages)
    assert stats["passages"] == 2
    assert stats["unites"] == 2
    assert stats["caracteres"] > 0
    assert stats["tokens_estimes"] == round(stats["caracteres"] / 4, 2)
    assert stats["cout_estime_usd"] == round(stats["tokens_estimes"] * 0.10 / 1_000_000, 6)
    assert "formule_cout" in stats


def test_embarquer_phrases_reprise_cache(tmp_path, monkeypatch):
    cache_path = tmp_path / "phrases-embeddings.json"
    existing = {"Already embedded sentence with enough length here.": [0.1, 0.2, 0.3]}
    cache_path.write_text(json.dumps(existing), encoding="utf-8")

    passages = [
        ("1", "piece.md", "Already embedded sentence with enough length here."),
        ("2", "piece.md", "Brand new sentence with enough length for embedding test."),
    ]
    calls = {"count": 0}

    def fake_embed(batch: list[str]) -> list[list[float]]:
        calls["count"] += 1
        return [[0.4] * 1024 for _ in batch]

    monkeypatch.setattr(
        "banc_realite.embarquer_phrases.CACHE_PATH",
        cache_path,
    )
    monkeypatch.setattr(
        "banc_realite.embarquer_phrases._fetch_passages",
        lambda _conn: passages,
    )

    summary = run_embarquer_phrases(dry_run=False, connection=object(), embed_fn=fake_embed)
    assert summary["deja_cache"] == 1
    assert calls["count"] == 1
    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    assert len(payload) == 2
