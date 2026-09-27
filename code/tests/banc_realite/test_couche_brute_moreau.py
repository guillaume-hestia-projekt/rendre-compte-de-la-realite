"""Tests hors ligne — couche brute MOREAU."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from banc_realite.couche_brute_moreau import (
    CouvertureDecoupeError,
    build_couche_brute_moreau,
    controle_couverture_citations,
    controle_couverture_retroactif,
    lister_passages_dossier,
    verifier_couverture_citations,
)
from banc_realite.decoupe_dossier import (
    RATIO_PASSAGE_RECUVREMENT,
    parametres_decoupe_depuis_or,
    parametres_decoupe_greenloop,
)
from banc_realite.passages import (
    MAX_CHARS,
    OVERLAP_CHARS,
    calculer_recouvrement_depuis_or,
    chunk_piece,
    stats_duplication,
)
from banc_realite.dossiers import dossier_courant


class _FakeConnection:
    def __init__(self) -> None:
        self.rows: list[dict] = []
        self._id = 0

    def execute(self, query, params=None):
        sql = " ".join(query.split())
        params = params or ()
        if sql.startswith("SET search_path"):
            return self
        if "ALTER TABLE" in sql or "CREATE INDEX" in sql or "UPDATE public.memory_chunks" in sql:
            return self
        if "INSERT INTO public.memory_chunks" in sql:
            self._id += 1
            piece, content, meta_json, _vec, vault_ref = params
            meta = json.loads(meta_json)
            self.rows.append(
                {
                    "id": self._id,
                    "source_ref": piece,
                    "content": content,
                    "metadata": meta,
                    "vault_ref": vault_ref,
                }
            )
            return self
        if "FROM public.memory_chunks" in sql and "vault_ref = %s OR vault_ref IS NULL" in sql:
            vault_ref = params[0]
            filtered = [
                r
                for r in self.rows
                if r.get("vault_ref") == vault_ref or r.get("vault_ref") is None
            ]
            return _Result(filtered)
        if "FROM public.memory_chunks" in sql and "vault_ref = %s" in sql:
            vault_ref = params[0]
            filtered = [r for r in self.rows if r.get("vault_ref") == vault_ref]
            return _Result(filtered)
        return _Result([])


class _Result:
    def __init__(self, rows):
        self._rows = rows

    def fetchall(self):
        return list(self._rows)


def _fake_embed(text: str) -> list[float]:
    return [0.1] * 8


def test_chunk_recollage_contient_texte_origine(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    original = (
        "# Titre\n\n"
        "Premier paragraphe avec assez de texte pour tenir.\n\n"
        "Deuxième paragraphe complémentaire.\n"
    )
    piece = "01-demo.md"
    (corpus / piece).write_text(original, encoding="utf-8")
    passages = chunk_piece(piece, corpus=corpus)
    recolle = "\n".join(p.content for p in passages)
    assert "Premier paragraphe" in recolle
    assert "Deuxième paragraphe" in recolle
    assert len(original.replace("\r\n", "\n")) <= len(recolle) + 200


def test_isolation_dossier_greenloop_vs_moreau():
    conn = _FakeConnection()
    conn.rows = [
        {"id": 1, "source_ref": "gl.md", "content": "green", "vault_ref": "greenloop"},
        {"id": 2, "source_ref": "mor.md", "content": "moreau", "vault_ref": "moreau"},
        {"id": 3, "source_ref": "legacy.md", "content": "legacy", "vault_ref": None},
    ]
    gl = lister_passages_dossier(conn, "greenloop")
    mo = lister_passages_dossier(conn, "moreau")
    assert {r["source_ref"] for r in gl} == {"gl.md", "legacy.md"}
    assert {r["source_ref"] for r in mo} == {"mor.md"}


def test_reprise_ne_double_pas_passage(tmp_path, monkeypatch):
    sorties = tmp_path / "couche-brute"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    texte = "Texte unique pour reprise."
    (corpus / "01-demo.md").write_text(f"# A\n\n{texte}\n", encoding="utf-8")
    fake_dossier = type(
        "D",
        (),
        {
            "nom": "moreau",
            "corpus_dir": corpus,
            "vault_ref": "moreau",
        },
    )()
    monkeypatch.setattr(
        "banc_realite.couche_brute_moreau.dossier_courant",
        lambda _nom=None: fake_dossier,
    )
    monkeypatch.setattr(
        "banc_realite.couche_brute_moreau.load_gold",
        lambda _dossier=None: {
            "assertions": [
                {"id": "MOR-A01", "piece": "01-demo.md", "quote": texte},
            ]
        },
    )

    conn = _FakeConnection()
    calls: list[str] = []

    def counting_embed(text: str) -> list[float]:
        calls.append(text)
        return _fake_embed(text)

    build_couche_brute_moreau(
        conn, embed_fn=counting_embed, sorties_dir=sorties, dossier="moreau"
    )
    first_calls = len(calls)
    assert first_calls >= 1

    build_couche_brute_moreau(
        conn, embed_fn=counting_embed, sorties_dir=sorties, dossier="moreau"
    )
    assert len(calls) == first_calls


def test_couverture_detecte_citation_coupee(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    piece = "01-demo.md"
    full = (
        "Intro\n"
        "Début de la citation longue sans fin.\n"
        "fin de la citation longue attendue.\n"
    )
    (corpus / piece).write_text(full, encoding="utf-8")
    passages = [
        type(
            "P",
            (),
            {
                "piece": piece,
                "content": "Début de la citation longue sans fin.",
                "line_start": 2,
                "line_end": 2,
            },
        )(),
        type(
            "P",
            (),
            {
                "piece": piece,
                "content": "fin de la citation longue attendue.",
                "line_start": 3,
                "line_end": 3,
            },
        )(),
    ]
    quote = "Début de la citation longue sans fin. fin de la citation longue attendue."
    assertions = [{"id": "MOR-A99", "piece": piece, "quote": quote}]
    result = controle_couverture_citations(passages, assertions, corpus_dir=corpus)
    assert result["citations_retrouvees"] == "0/1"
    assert result["citations_coupees"][0]["cause"] == "citation_coupee_par_decoupe"


def test_couverture_detecte_citation_absente():
    passages = [
        type(
            "P",
            (),
            {
                "piece": "01-demo.md",
                "content": "Texte sans la citation attendue.",
                "line_start": 1,
                "line_end": 1,
            },
        )()
    ]
    assertions = [
        {
            "id": "MOR-A99",
            "piece": "01-demo.md",
            "quote": "citation absente du corpus",
        }
    ]
    result = controle_couverture_citations(passages, assertions)
    assert result["citations_retrouvees"] == "0/1"
    assert result["citations_manquantes"][0]["cause"] == "citation_absente"


def test_recouvrement_contient_citation_a_cheval(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    piece = "01-demo.md"
    block = "Z" * 2200
    quote = block[800:1400]
    (corpus / piece).write_text(f"# T\n\n{block}\n", encoding="utf-8")
    assertions = [{"id": "MOR-A99", "piece": piece, "quote": quote}]
    decoupe = parametres_decoupe_depuis_or(assertions)
    overlap = decoupe["recouvrement_chars"]
    assert overlap >= len(quote) - 1
    passages = chunk_piece(
        piece,
        corpus=corpus,
        max_chars=decoupe["max_chars_passage"],
        overlap_chars=overlap,
    )
    result = controle_couverture_citations(passages, assertions, corpus_dir=corpus)
    assert result["citations_retrouvees"] == "1/1"


def test_recouvrement_calcule_depuis_or():
    short = [{"id": "A1", "quote": "x" * 50}]
    long = [{"id": "A2", "quote": "y" * 500}]
    short_ov = calculer_recouvrement_depuis_or(short)["recouvrement_chars"]
    long_ov = calculer_recouvrement_depuis_or(long)["recouvrement_chars"]
    assert long_ov > short_ov
    assert long_ov >= 500 - 1


def test_porte_couverture_nomme_citations_fautives():
    result = controle_couverture_citations(
        [],
        [{"id": "MOR-A77", "piece": "01-demo.md", "quote": "absente"}],
    )
    with pytest.raises(CouvertureDecoupeError) as exc:
        verifier_couverture_citations(result)
    assert "MOR-A77" in str(exc.value)


def test_citation_dans_deux_passages_recouvrants_comptee_une_fois():
    piece = "01-demo.md"
    shared = "citation partagée entre deux passages recouvrants."
    passages = [
        type(
            "P",
            (),
            {
                "piece": piece,
                "content": f"début {shared} fin1",
                "line_start": 1,
                "line_end": 1,
            },
        )(),
        type(
            "P",
            (),
            {
                "piece": piece,
                "content": f"début2 {shared} fin2",
                "line_start": 2,
                "line_end": 2,
            },
        )(),
    ]
    assertions = [{"id": "MOR-A88", "piece": piece, "quote": shared}]
    result = controle_couverture_citations(passages, assertions)
    assert result["citations_retrouvees"] == "1/1"
    assert result["citations_retrouvees_ids"] == ["MOR-A88"]


def test_controle_retroactif_sans_reconstruction(monkeypatch):
    conn = _FakeConnection()
    quote = "Texte déjà indexé mot pour mot."
    conn.rows = [
        {
            "id": 1,
            "source_ref": "01-demo.md",
            "content": f"Intro.\n{quote}\nFin.",
            "vault_ref": "moreau",
        }
    ]
    fake_dossier = type(
        "D",
        (),
        {"nom": "moreau", "corpus_dir": Path("/tmp"), "vault_ref": "moreau"},
    )()
    monkeypatch.setattr(
        "banc_realite.dossiers.dossier_courant",
        lambda _nom=None: fake_dossier,
    )
    monkeypatch.setattr(
        "banc_realite.couche_brute_moreau.load_gold",
        lambda _dossier=None: {
            "assertions": [
                {"id": "MOR-A01", "piece": "01-demo.md", "quote": quote},
            ]
        },
    )
    result = controle_couverture_retroactif(conn, "moreau")
    assert result["retroactif"] is True
    assert result["citations_retrouvees"] == "1/1"
    assert result["passages_en_base"] == 1


def test_construction_echoue_si_citation_non_couverte(tmp_path, monkeypatch):
    sorties = tmp_path / "couche-brute"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "01-demo.md").write_text("Texte sans la citation attendue.\n", encoding="utf-8")
    fake_dossier = type(
        "D",
        (),
        {
            "nom": "moreau",
            "corpus_dir": corpus,
            "vault_ref": "moreau",
        },
    )()
    monkeypatch.setattr(
        "banc_realite.couche_brute_moreau.dossier_courant",
        lambda _nom=None: fake_dossier,
    )
    monkeypatch.setattr(
        "banc_realite.couche_brute_moreau.load_gold",
        lambda _dossier=None: {
            "assertions": [
                {
                    "id": "MOR-A99",
                    "piece": "01-demo.md",
                    "quote": "citation absente du corpus",
                }
            ]
        },
    )
    conn = _FakeConnection()
    with pytest.raises(CouvertureDecoupeError) as exc:
        build_couche_brute_moreau(
            conn, embed_fn=_fake_embed, sorties_dir=sorties, dossier="moreau"
        )
    assert "MOR-A99" in str(exc.value)


def test_regle_passage_quatre_fois_recouvrement():
    short = [{"id": "A1", "quote": "x" * 50}]
    long = [{"id": "A2", "quote": "y" * 500}]
    short_d = parametres_decoupe_depuis_or(short)
    long_d = parametres_decoupe_depuis_or(long)
    assert long_d["recouvrement_chars"] > short_d["recouvrement_chars"]
    assert long_d["max_chars_passage"] > short_d["max_chars_passage"]
    assert long_d["max_chars_passage"] >= RATIO_PASSAGE_RECUVREMENT * long_d["recouvrement_chars"]


def test_piece_courte_un_passage_zero_duplication(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    piece = "01-demo.md"
    texte = "Citation courte intégralement couverte."
    (corpus / piece).write_text(f"# T\n\n{texte}\n", encoding="utf-8")
    assertions = [{"id": "MOR-A01", "piece": piece, "quote": texte}]
    decoupe = parametres_decoupe_depuis_or(assertions)
    passages = chunk_piece(
        piece,
        corpus=corpus,
        max_chars=decoupe["max_chars_passage"],
        overlap_chars=decoupe["recouvrement_chars"],
    )
    assert len(passages) == 1
    dup = stats_duplication(passages, corpus_dir=corpus)
    assert dup["caracteres_dupliques"] == 0
    assert dup["duplication_pct"] == 0.0


def test_moreau_or_42_sur_42_couverture():
    from banc_realite.or_dossier import load_gold

    moreau = dossier_courant("moreau")
    gold = load_gold("moreau")
    decoupe = parametres_decoupe_depuis_or(gold["assertions"])
    passages = []
    for path in sorted(moreau.corpus_dir.iterdir()):
        if not path.is_file():
            continue
        passages.extend(
            chunk_piece(
                path.name,
                corpus=moreau.corpus_dir,
                max_chars=decoupe["max_chars_passage"],
                overlap_chars=decoupe["recouvrement_chars"],
            )
        )
    result = controle_couverture_citations(
        passages, gold["assertions"], corpus_dir=moreau.corpus_dir
    )
    assert result["citations_retrouvees"] == "42/42"


def test_greenloop_decoupe_inchangee_par_regle():
    gl = parametres_decoupe_greenloop()
    assert gl["max_chars_passage"] == MAX_CHARS
    assert gl["recouvrement_chars"] == OVERLAP_CHARS


def test_plafond_arrete_construction(tmp_path, monkeypatch):
    monkeypatch.setattr("banc_realite.couche_brute_moreau.MAX_EMBED_CALLS", 1)
    sorties = tmp_path / "couche-brute"
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "01-demo.md").write_text("# A\n\nUn.\n\n# B\n\nDeux.\n", encoding="utf-8")
    (corpus / "02-demo.md").write_text("# C\n\nTrois.\n", encoding="utf-8")
    fake_dossier = type(
        "D",
        (),
        {
            "nom": "moreau",
            "corpus_dir": corpus,
            "vault_ref": "moreau",
        },
    )()
    monkeypatch.setattr(
        "banc_realite.couche_brute_moreau.dossier_courant",
        lambda _nom=None: fake_dossier,
    )
    monkeypatch.setattr(
        "banc_realite.couche_brute_moreau.load_gold",
        lambda _dossier=None: {
            "assertions": [
                {"id": "MOR-A01", "piece": "01-demo.md", "quote": "Un."},
                {"id": "MOR-A02", "piece": "01-demo.md", "quote": "Deux."},
                {"id": "MOR-A03", "piece": "02-demo.md", "quote": "Trois."},
            ]
        },
    )

    conn = _FakeConnection()
    result = build_couche_brute_moreau(
        conn, embed_fn=_fake_embed, sorties_dir=sorties, dossier="moreau"
    )
    assert result["status"] == "plafond_atteint"
    assert conn.rows
    assert len(conn.rows) <= 1
