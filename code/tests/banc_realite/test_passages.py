"""Découpage déterministe des passages — inerte."""
from __future__ import annotations

from pathlib import Path

from banc_realite.passages import MAX_CHARS, chunk_corpus, chunk_piece


def test_chunk_deterministic(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    text = (
        "# Section A\n\n"
        "Paragraph one with enough text.\n\n"
        "## Section B\n\n"
        "| Col | Val |\n"
        "| --- | --- |\n"
        "| a | 1 |\n"
        "| b | 2 |\n"
    )
    (corpus / "01-demo.md").write_text(text, encoding="utf-8")
    first = chunk_piece("01-demo.md", corpus=corpus)
    second = chunk_piece("01-demo.md", corpus=corpus)
    assert first == second
    assert all(len(p.content) <= MAX_CHARS for p in first)
    assert any(p.section_path for p in first)


def test_table_row_never_split(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    long_cell = "x" * 500
    row = f"| {long_cell} | value |"
    (corpus / "02-table.md").write_text(f"# T\n\n{row}\n", encoding="utf-8")
    passages = chunk_piece("02-table.md", corpus=corpus)
    for passage in passages:
        for line in passage.content.splitlines():
            if line.strip().startswith("|"):
                assert line.count("|") >= 2


def test_corpus_piece_count():
    corpus = Path(
        "/home/ubuntu/.worktrees/ambactos-brain/dossier-greenloop/benchmark/dossiers/greenloop/documents"
    )
    pieces_on_disk = sorted(p.name for p in corpus.iterdir() if p.is_file())
    assert len(pieces_on_disk) == 28
    passages = chunk_corpus(corpus=corpus)
    pieces = {p.piece for p in passages}
    assert pieces == set(pieces_on_disk)
