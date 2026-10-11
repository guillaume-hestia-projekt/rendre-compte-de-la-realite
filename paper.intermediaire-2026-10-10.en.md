---
title: Reporting Reality — interim paper
authors: Hestia. (Guillaume Aubry)
date: 2026-10-11
lang: en
---

Interim paper of the "reporting reality" bench, work items brain#140, #154, #158. French version: paper.intermediaire-2026-10-10.fr.md. Gold sets, case documents and outputs are not published. Licence: CC BY 4.0.

# Reporting Reality: what the bench has measured so far

*Interim paper, 10 October 2026. Work items brain#140, #154, #158. Authors: Guillaume Aubry (gold sets, decisions, criterion) and the bench agents (construction, measurement). Intended for the public "Ambactos Brain" repository; contains no document from any case.*

## Summary

We are looking for the best way to give a language model the context it needs to answer a question about a business case without inventing anything, and above all while detecting what is subtle in a case: contradictions between documents, versions that change, what is not established. Three cases, three gold sets written or validated by a human, more than twenty retrieval lines tried at equal budget, no model call at query time. Three results hold across the three cases:

1. **Retrieval alone does not detect contradictions.** It holds simple facts and citations; on disputes it returns one side only (14/28 on GreenLoop, 0/8 on Les Granges).
2. **Reconstruction at ingestion, that is re-reading the documents entity by entity and writing out facts, rules, disagreements and the not-established with the exact line, is worth nothing alone, and changes everything in composition.** Alone: a net margin of 37 on GreenLoop, 1 on MOREAU, 15/34 on Les Granges. Composed with retrieval: the best line on all three cases.
3. **The filter does all the work.** With a perfect filter that knows the right documents, retrieval holds 113 questions out of 141; no real filter built from the questions comes close. The only filter that works comes from the structure of the content, not from the question.

This last point converges, by experiment, with the "composite retrieval" Jonas Roman describes in production: filter by structure, hybrid search on the reduced space, relations afterwards. The difference is where the structure comes from: for him a schema set by hand; for us an ontology proposed from the content and then decided in conversation with the user. First measure of that path: reconstruction guided by the decided ontology yields 25/34 against 24 without it, and 20/34 alone against 15.

## 1. The bench

**What is measured is stage 2**: the context handed to the model, not the answer. A question is "held" when all the letter expected by the gold set (the supporting assertions, quoted word for word with their document) is present in the returned context, within a budget fixed in characters. The model is not called at measurement time: the measure is deterministic and replayable.

**The shuffled control.** For every line we also take the same count on a context retrieved for another question. The margin, signal minus control, is what ranks: a line that fills the context with the whole case has a high signal and a high control, and is worth nothing.

**Equal budget.** All lines are compared at 12,000 characters, sometimes 24,000. A line measured at 24,000 against another at 12,000 has proved nothing; we did it once (stage 3 of 27 September) and withdrew it.

**The gold set is only for measuring.** It never enters ingestion or retrieval. The "perfect filter" ceiling is the only instrument that reads it, and it is not a line of the comparison. The bench is not modified to improve a score; a fix to the bench (a chunker that lost lines, 10 October) is replayed on every line.

**Three cases**, so as not to keep a line by luck:

| Case | Nature | Documents | Questions | Gold set |
|---|---|---:|---:|---|
| GreenLoop | business, prose and short registers | 28 | 141 | written before the measurements, 28 disputes |
| MOREAU | legal, letters and briefs | ~10 | 43 | written before the measurements |
| Les Granges | spreadsheets, quotes, invoices, forecasts, read from a Google Drive without import, local OCR | 118 | 37 (34 measurable) | 37 questions proposed from the disagreements found, validated and corrected by Guillaume (one "contradiction" was two deposits) |

## 2. The lines

| Line | What it returns |
|---|---|
| Plain RAG | passages of the raw layer (BM25 + vectors), context filled to the budget |
| g12 | the hybrid chain of the production Brain, sentence windows, fixed volume |
| MRFS alone / g12 then MRFS | facts extracted statement by statement (52 to 97 characters), ranked |
| Composite situations | reconstructed situations (type, actors, chronology, what each party says, whole lines), median 1,366 characters |
| Reconstruction by entity | facts, rules, disagreements, not established, per entity and per range of months, with the exact line |
| Disagreements first then RAG | the three disagreements closest to the question first, retrieval behind |
| Filter (entities, meaning, RAG, situations) then RAG | chosen documents, then retrieval within those documents only |
| Objects by meaning then filtered RAG | reconstructed objects ranked by vector, then retrieval filtered on their documents |

All reconstruction lines make their model calls at ingestion, once (167 calls for GreenLoop, 309 for Les Granges), never at query time.

## 3. The results

### GreenLoop, 141 questions, 12,000 characters (signal / control / margin)

| Line | Signal | Control | Margin | Disputes both sides /28 |
|---|---:|---:|---:|---:|
| Ceiling: perfect filter then RAG | 113 | — | — | 26 |
| g12 then composite situations | 88 | 26 | 62 | 24 |
| g12 | 84 | 23 | 61 | 24 |
| Disagreements first then g12 | 83 | 22 | 61 | 28 |
| Ranked objects then filtered RAG | 95 | 43 | 52 | 22 |
| Disagreements first then RAG filtered by meaning | 92 | 45 | 47 | 28 |
| Plain RAG | 84 | 44 | 40 | 14 |
| MRFS alone (best budget, 24,000) | 45 | 8 | 37 | 0 |
| Filter by entities then RAG | 85 | 48 | 37 | 21 |

### MOREAU, 43 questions (margin at each line's best budget)

| Line | Verbatim margin | Budget |
|---|---:|---:|
| Plain RAG | 21 | 12,000 |
| g12 then composite situations | 18 | 24,000 |
| Composite situations alone | 14 | 24,000 |
| g12 then MRFS | 13 | 12,000 |
| g12 | 9 | 12,000 |
| MRFS alone | 1 | 12,000 |

On this short case (30,000 characters of documents for 52,000 of evidence), plain RAG keeps the best margin at 12,000; at 24,000 it falls to 14 and the composition moves ahead. No line returns the chronologies (0/5).

### Les Granges, 34 questions, 12,000 characters ("everything holds", no control)

| Line | Everything holds | ≥ 1 evidence | Contradictions /8 | Amounts /14 | Dates /4 | Citations /6 |
|---|---|---|---|---|---|---|
| Plain RAG | 3 | 12 | 0 | 2 | 0 | 1 |
| Reconstruction alone | 15 | 15 | 3 | 9 | 2 | 0 |
| Disagreements first then RAG | 13 | 21 | 5 | 5 | 1 | 1 |
| Disagreements then filtered RAG | 14 | 22 | 5 | 6 | 1 | 1 |
| Filter by meaning then RAG | 8 | 17 | 2 | 5 | 0 | 1 |
| **Objects by meaning then filtered RAG** | **24** | **26** | **6** | **10** | **4** | 2 |
| Composite RAG filtered by ontology v1, no reconstruction | 5 | 16 | 0 | 4 | 0 | 1 |
| Reconstruction guided by ontology v1, alone | 20 | 20 | 7 | 10 | 2 | 0 |
| **Reconstruction guided by ontology v1, objects by meaning then filtered RAG** | **25** | **26** | 6 | **11** | **4** | 2 |

On a case made of spreadsheets, retrieval alone holds almost nothing: a table row without its header says nothing, and chunking into passages separates it from what gives it meaning. Reconstruction holds the amounts; the composition holds the rest. The remaining gap: citations from "plain reading" documents (articles of association, lease, accounts), which are in no reconstructed object.

## 4. What is established

- **Same picture on the three cases**: plain retrieval at the bottom, reconstruction alone in the middle, composition on top; the form of the documents (prose, letters, spreadsheets) changes the numbers, not the order.
- **The relation "versions of one fact" is what brings back contradictions.** Putting disagreements first returns 28/28 disputes on GreenLoop whatever the rest of the context. No line without reconstruction gets there.
- **The useful budget is 12,000 to 24,000 characters.** Beyond that the control rises faster than the signal: at 96,000, a context retrieved for another question already holds 25 questions out of 43.
- **The filter is the lever**, and it must come from the content. Filters built from the question (3 documents per filter) discard the right documents more than one time in two (55 to 67 questions well filtered out of 139) and do worse than no filter at all.
- **Status questions fail everywhere**, even with the perfect filter (2/21): the answer requires joining a row, a rule and an invoice, and nothing joins them yet.

## 5. What is not established

- **No answer has been judged on these lines**: everything is stage 2. Stage 3 on 20–23 September showed that a judge's "conformant" rating is blind to disputes; a judging protocol remains to be redone.
- **Les Granges has no shuffled control**: the counts are raw "everything holds".
- **Cost is known only at ingestion** (calls, duration); no comparison of total cost per case.
- **More than twenty lines on the same GreenLoop gold set**: the risk of keeping one by luck exists, which is why the other two cases matter.

## 6. What reconstruction learned by getting it wrong

The measured errors are part of the result; they say where the model, left alone, invents structure.

| Trap | Measure | Fix |
|---|---|---|
| Quote numbers read as months (`2024-41`) | 97 units on false periods | months 01–12 only |
| One unit per spreadsheet quantity | 798 units, 740 of them tiny | packing, 304 units |
| Table rows summarised instead of quoted | 7,209 lines never quoted out of 9,404 | kept as searchable line blocks, not as facts |
| Chunker that cut lines | 621 lines lost over 888 passages | lossless chunking, 0 lines lost, every line replayed |
| Duplicate entities (BPI / BPI-R, two names for one craftsman) | 40 entities listed, 2 merges decided by the user | ontology v1, 38 active entities |

Jonas Roman warns that model-generated entities make "a mess". We put a number on it: 798 units, 536 leftover groups. The common cause is that no schema had been set beforehand.

## 7. What comes next: the ontology, by conversation

The filter must come from the content. For Jonas Roman, that is a data model set by hand per use case. We try something else: **the system proposes the tenant's ontology from its content** (document families, entity types, entities and their keys, relations, concepts), then **the user decides it in conversation**: merges, splits, missing types, documents that are authoritative alone. Every answer is a timestamped decision; nothing is erased. The ontology is **frozen in use** (one version tags, filters, guides) and **evolves between versions**, the core (types, relations, families) changing rarely, the instances often. Versioned ontologies are common practice elsewhere; we do not set it as a rule, we will test it.

Three bench lines separate three questions:

| Line | Isolates |
|---|---|
| Composite RAG filtered by the ontology, no reconstruction | what the ontology alone is worth (Jonas Roman's path, no model call after tagging) |
| Reconstruction guided by the ontology, then filtered composite RAG | what reconstruction adds to the ontology |
| Objects by meaning then filtered RAG (24/34) | the reference without ontology; the gap with the previous line is the price, or the gain, of the conversation |

The first is measured: 5/34. Without reconstruction, the ontology only lifts plain RAG from 3 to 5: 14 questions out of 37 name no entity (fallback), and 443 passages out of 888, the table rows, carry none. The ontology says *what* a document is about; only reconstruction attaches a row to its entity.

The second was measured on 11 October: **25/34**, against 24 for the reference. The entity census no longer goes through a model; it comes from the decided ontology (38 entities, two merges); periods are taken from the previous register; 54 units out of 302 are reused without a call, 238 reconstructed, 10 fail. The net gain is on **reconstruction alone: from 15 to 20** (four more contradictions and one more amount), because the entities decided by the user group documents that the model's census kept apart. Behind it, the composite gains only one question (an amount): the filtered RAG was already catching most of the gaps. What v1 does not fix: the month boundaries of units (hence the low reuse) and the citations from documents read as-is (2/6, unchanged). The rule is unchanged: no filter inferred from the meaning of the question; only ontology keys found literally.

## 8. Reproducing

Bench code: `brain` repository, `scripts/banc_realite/` (PR #155, #159). Gold sets, documents and outputs are outside the repository and are not published; the detailed per-measurement reports (`RAPPORT-*.md`) will be released with this paper. Every measurement is replayable without model calls from the ingestion caches; the call and embedding caps of each campaign are recorded in a decision log.
