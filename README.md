# Reporting Reality — agent memories vs. plain retrieval on two synthetic cases

Research paper, dataset and results for the benchmark *« Rendre compte de la réalité »*
run by Hestia. (September 2026): can an agent memory report the facts of a case
without error or omission, compared with a plain hybrid RAG over the same documents?

- **Paper (English)**: [`paper.en.md`](paper.en.md)
- **French version**: https://hestia-projekt.com/recherche/rendre-compte-de-la-realite
- **English version on the site**: https://hestia-projekt.com/recherche/reporting-reality
- **Dataset and results**: [`dataset/`](dataset/) — integrity: `sha256sum -c dataset/MANIFEST.sha256`
- **Bench code**: [`code/`](code/) — verbatim snapshot of `scripts/banc_realite/` and its tests (see `code/README.md`, `BRAIN_COMMIT`)

## Interim paper (10 October 2026): what the bench has measured so far

Three cases (GreenLoop, MOREAU, and Les Granges — a real tenant's Drive read in place, not published), more than twenty retrieval lines at equal budget, no model call at query time. Three results hold: retrieval alone does not detect contradictions; reconstruction at ingestion is worth nothing alone and changes everything in composition (24/34 on Les Granges against 3/34 for plain RAG); the filter does all the work and must come from the structure of the content, not from the question — an ontology filter without reconstruction reaches only 5/34.

- **English**: [`paper.intermediaire-2026-10-10.en.md`](paper.intermediaire-2026-10-10.en.md)
- **Français**: [`paper.intermediaire-2026-10-10.fr.md`](paper.intermediaire-2026-10-10.fr.md)

## What is compared

| Provider | What it is |
|---|---|
| `rag_naif` | Raw layer: fixed-size passages, hybrid lexical + vector retrieval (Mistral embeddings) |
| `brain_prod` | Brain as it runs in production: `run_search` k=8 → `compile_call_frame`, atoms (median 12 characters) |
| `brain_banc` (`g12`) | Bench Brain: hybrid atoms 12+6 over two rounds + 12 two-sentence windows ; variants g24–g48, v1–v4 (neighborhood gate) |
| `mem0` 2.1 | Third-party agent memory, 598 memories (GreenLoop) / 71 (MOREAU) |
| `A` | No memory at all (stage 3 only) |

Extractor everywhere: Grok 4.5 via Cursor. Stage 3 judge: `gpt-5.6-sol` via the Codex CLI.

## Two cases, both synthetic

- **GreenLoop** (business, English, 28 documents, 141 questions, 2,445 gold assertions) — fictional company, authored for the benchmark; a versioned leak checker against a private blocklist recorded zero leaks.
- **MOREAU c/ ATELIER RIVIÈRE** (French labour-law dispute, 12 documents, 43 measured questions, 42 gold assertions) — 100 % fictional demonstration file, marked as such on every document.

No real person, organisation, amount or date appears in either case.

## Layout

```
dataset/
  cases/<case>/documents/      the documents ingested by every provider
  cases/<case>/gold/           questions, assertions, coverage — read only, never ingested
  results/<case>/stage2/       persisted contexts per provider (contextes-*.jsonl), scored runs (etage2-*.json),
                               reports and the shuffled control (TEMOIN-BRASSAGE.md)
  results/<case>/stage3/       prompts and answers, notations per provider, judge report
  MANIFEST.sha256
```

Stage 2 is model-free: a context is scored against the gold set in two modes (verbatim / value). The
shuffled control re-reads the persisted context of question *i+1* for question *i*; the net margin is
signal minus control. Stage 3 has a model answer from each context and an independent judge.

## Licence

Paper and dataset: CC BY 4.0. Code: Apache 2.0. See [`LICENSE`](LICENSE).
