---
title: Reporting Reality
authors: Hestia. (Guillaume Aubry)
date: 2026-09-27
lang: en
---

French original: https://hestia-projekt.com/recherche/rendre-compte-de-la-realite · English site version: https://hestia-projekt.com/recherche/reporting-reality · Licence: CC BY 4.0

# Reporting Reality

Agent memories versus passage retrieval: two cases, three stages, one shuffled control.

Guillaume Aubry, Hestia. — research · September 2026 · Version 1 (draft submitted for validation) · Synthetic data, protocol and results published · Instrumentation and execution: “reporting reality” bench, `brain` repository, 20–27 September 2026.

**Abstract.** We measure what an agent memory actually puts in front of a model when asked a question about a case — and whether the model answers correctly, and cites the letter. Four context providers are compared behind a single interface (*ingest the documents → return a context under budget*): a passage RAG, Brain in production, the Brain bench chain (atoms + windows, two gates) and mem0; a fifth arm answers with no memory. Two cases: an English business case of 28 documents (141 questions, 2,403 assertions) where *value* counts, and a French labor-court dispute of 12 documents (50 questions, 42 citations) where the *letter* is binding. Three stages: is the gold set in the context, under two presence modes; does the model answer correctly; does it cite. Each measure is paired with a *shuffled control* — the same measure on deliberately mismatched contexts — whose margin from the signal is the score.

Results. On the business case, the two-gate chain obtains the best net margin at every budget (61/141 against 39 for the RAG, shuffled control 23 against 46) and 78 value-conformant answers out of 141 at stage 3 against 65, with zero judge faults on 705 judgments; it returns both sides of 27 disputes out of 28. On the legal case, the passage RAG leads (35/43 against 12) but by volume: at 32,000 characters it returns the entire case and its net margin falls to 2; the Brain chain plateaus there by the *shape* of its units — a 12-character atom and a two-sentence window do not carry a 590-character clause — regardless of unit count or budget. mem0 answers correctly 31 times out of 50 but cites the letter only 5 times; its net margin is zero in value mode on the legal case. The largest measured gap does not oppose Brain to a competitor: it separates Brain in production (39/141, 1/43) from the chain the bench knows how to run (84/141, 12/43). A one- or two-edge graph hop, measured last, finds the right neighbors and contributes nothing in net.

## 1. The question

An agent memory promises two things: to forget nothing, and to invent nothing. Public conversational-memory benches (LoCoMo, LongMemEval) measure recall of conversations; they say nothing about what matters for a case — tables, dates in the document’s form, documents that contradict one another, clauses that must be cited as written. We put the question differently: **when a model answers a question about a case, did the memory give it enough to answer correctly, and enough to cite the reality of the facts without error or omission?** And that question has two versions, which we refuse to conflate: for a business fact, *value* is enough — “CA 2023: 4.2 M€” matches the table row; for a legal fact, only the *letter* is binding — a paraphrase shifts the scope without being noticed.

## 2. The ground: two cases, two natures of fact

| | GreenLoop Collect Ltd | MOREAU c/ ATELIER RIVIÈRE |
|---|---|---|
| nature | client case of an SME in food-waste collection: contracts, invoices, weighing logs, annual review, working papers | labor-court dispute: contract, amendment, payslips, schedule, summons, minutes, dismissal letter, formal notice, petition, briefs, attestation, email |
| authenticity | synthetic; form modeled on a real case, substance written entirely for the exercise; `.example` domains | 100% fictional, designed to look real on screen; fictional jurisdiction |
| language · documents · size | English · 28 files (27 sources) · 235,804 char. | French · 12 documents · 29,629 char. |
| gold set | 141 questions (50 single, 21 aggregate, 28 disputes, 21 status, 14 unknown, 7 trajectory) · 2,403 assertions | 50 questions (7 citation, 7 date, 5 délai, 10 montant, 4 contradiction, 5 chronologie, 5 qualification, 7 non établi) · 42 word-for-word citations |
| what the gold set requires | the value, with its source | the letter, with its document; never a date in ISO form absent from the documents |
| share of the corpus returned by 12,000 characters | 5.1% | 40.5% |

The legal gold set was not written by a model: it was *built by deterministic reading* of the documents — every citation recovered word for word in its file, every full sentence, every value asserted by a fact carried by a citation, every question attached to the support that carries its answer. Four corrective passes were needed to hold these four rules; the last rewired 17 questions whose support did not carry the answer. It was validated by the author before any measurement. Seven “non établi” questions expect a motivated abstention; they are reserved for stage 3 and leave the stage 2 denominator (43 measurable questions).

## 3. The systems compared

Every competitor sits behind the same interface: `ingest(documents)` then `context(question, budget) → elements`. The respondent, the scoring, and the judge are identical for all. A single extractor — Grok 4.5 served by Cursor — is used for Brain atomization and for mem0 memories on both cases, so as not to compare two extractions from different models.

| arm | what is ingested | how it searches | what it returns |
|---|---|---|---|
| **A** — no memory | nothing | — | the question alone (floor) |
| **naive RAG** | the documents as passages (1,200 char. GreenLoop, 2,500 MOREAU; overlap computed on the longest gold-set citation, rule “passage ≥ 4 × overlap”), vectorized (Mistral) | structured query, hybrid lexical + vector search, top-k | whole passages, with their document |
| **Brain prod** | entity · attribute · value atoms extracted from the documents (15,780 GreenLoop, 637 MOREAU), median 12 characters | `run_search`, simple search, k = 8 — the real production path | `[claim_hit] entity attribute : value (document)` |
| **Brain banc** (g12) | the same atoms + the raw layer + a cache of vectorized two-sentence windows | two gates without score fusion: atoms in hybrid 12 + 6 over two rounds (the second seeks the other side of a dispute); 12 windows by similarity | atoms and windows, side by side |
| **mem0** 2.1 | memories extracted by the model (598 GreenLoop in 89 calls and 51 min; 71 MOREAU in 24 calls and 2 min), median 255 characters, pgvector | vector search, k = 20 (and 40) | memories, with the source document |

Brain banc was tuned on GreenLoop (fourteen tuning disputes); fourteen held-out disputes never served for tuning and are reported separately. MOREAU served for no tuning. The other competitors arrive as-is and receive a sweep of k and budget. Letta was not measured; MRFS, Brain’s situations model, was unfrozen for the bench but its ingestion chain produced no situation after 273 calls — that is not a result, it is an open workstream.

## 4. The instruments

### 4.1 Three stages

**Stage 2 — is the gold set in the context?** No model call. For each question, are the supporting assertions present in the context returned under budget? Two counts: “fully supported” (all assertions) and “at least one”. **Stage 3 — does the model answer correctly, and does it cite?** A single respondent (Grok 4.5 via Cursor) reads the context persisted by stage 2 — never a new search — and answers; the adjudicated scoring recognizes sources by file name, numbers and dates in value, both sides of a dispute, the expected abstention; a separate judge, never the model that answers, checks forbidden claims (`must_not_claim`); five questions per arm are replayed three times for stability. (Stage 1, extraction fidelity, served to build the chains; it is not comparative.)

### 4.2 Two presence modes

The presence of an assertion is judged *verbatim* — the gold-set citation is found literally in an element coming from the announced document — or in *value* — same document, and all discriminants of the citation recovered: numbers compared in value with their anchor (unit or neighborhood gate; `86` does not hold inside `1986`), dates under all their forms, identifiers in text; a citation without a discriminant requires 80% of its significant words and no missing rare word. Two invariants are tested on the 2,445 assertions of both gold sets: the verbatim mode is frozen bit for bit, and **value mode contains verbatim** — a literal citation cannot be rejected in value. Both columns are always published together.

> Bias trace, declared: value mode was added *after* seeing mem0 obtain 2/141 on the verbatim criterion. Verbatim therefore did not move, so that every prior measure remains comparable.

### 4.3 The shuffled control

Every presence measure is replayed with mismatched contexts — question *i* evaluated against the context of question *i + 1*, deterministic rotation. The shuffled control measures what a context obtains without answering the question: instrument permissiveness and context width confounded. **The published score is the triplet signal · shuffled control · margin, and it is the margin that ranks.** The shuffled control rereads the contexts persisted by the measure; it never searches.

### 4.4 What the bench refuses to do

It refuses to measure a case whose gold set does not match the documents, whose atoms are not in the table the readers read, whose gate returns no element, whose provider searches the wrong vault. Each of these refusals was added after a defect produced a plausible and false table — six times in two days, a GreenLoop constant left on the path of a MOREAU measure would have returned a “0/50” indistinguishable from a true result. Reproducibility is measured: two runs of each search, 0 unstable questions out of 141 and out of 43.

## 5. The experiments, in order

### E1 — Stage 2 on GreenLoop, four providers, a single mode (23 September)

Budget 12,000 characters, verbatim presence, “fully supported” on 141: naive RAG 85, Brain banc 84, Brain prod 39, mem0 2. The RAG returns 11,458 median characters, Brain banc 9,417, Brain prod 2,795. On the 28 disputes returned on both sides: Brain banc 24, RAG 14, Brain prod 1, mem0 1. Immediate reading: mem0’s 2 is an artifact — its memory paraphrases, the instrument required the letter.

### E2 — Two modes, then the shuffled control, then the tightening (24 September)

In value mode, mem0 goes from 2 to 47. The shuffled control, introduced at once, shows what that jump was worth — and something else:

| GreenLoop, 12,000, verbatim | signal | shuffled control | margin |
|---|---:|---:|---:|
| naive RAG | 85 | 46 | 39 |
| Brain banc | 84 | 23 | 61 |
| Brain prod | 39 | 4 | 35 |
| mem0 | 2 | 0 | 2 |

The RAG’s 85 — the bench’s best raw score — is reached at 46 by a context that does not answer the question: more than half of its score is within reach of any context of that size. An independent review then showed that value mode accepted “The annual fee is 3 percent” against “Appendix 3” (number without its unit) and “No bank statement accompanies this note” against the same sentence ending in “application”; the tightening first made value mode stricter than verbatim on tabular content (811 literal citations rejected — a number between two bars has neither unit nor neighbor), hence the invariant. Final figures for value mode, signal · shuffled control: Brain prod 45 · 4, RAG 86 · 48, Brain banc 87 · 24, **mem0 23 · 11**. Half of mem0’s jump rested on bare numbers.

### E3 — The blind half of the disputes

Brain banc was tuned on fourteen disputes. On the fourteen it never saw: Brain banc 11/14, RAG 7/14, Brain prod 1/14, mem0 1/14. Its lead does not come from tuning.

### E4 — The legal case at stage 2 (25 September)

| MOREAU, 12,000, fully supported /43 | verbatim | value | shuffled control | verbatim margin | char. returned |
|---|---:|---:|---:|---:|---:|
| naive RAG | 35 | 35 | 14 | 21 | 11,303 |
| Brain banc | 12 | 16 | 3 | 9 | 6,131 |
| Brain prod | 1 | 5 | 0 | 1 | 1,927 |
| mem0 | 0 | 5 | 0 · 5 | 0 | 6,977 |

The two modes look alike: on a case where the letter is binding, tolerance for paraphrase recovers almost nothing. mem0 in value: 5 in signal, 5 in shuffled control — zero margin. Brain prod and mem0 do not cite the letter, and the reason is measured before the measure: an atom is 12 characters at the median, a memory 255, a gold-set citation 85 (p90 271, maximum 590). Brain banc plateaus: 6,131 characters returned regardless of budget, and only 26 of the 42 citations fit whole in a two-sentence window; the window calibrated on the gold set (3 sentences) lifts coverage to 28/42 and the signal to 13 — the fourteen remaining citations are in tables, cut by a 600-character bound, or without a window: a shape ceiling, not a search ceiling.

### E5 — Budget, units, and the right comparison (26 September)

Budget was raised to 24,000 (GreenLoop) and 32,000 (MOREAU, the entire case); each provider received the same candidate units (k = 12, 20, 40; mem0 at k = 40; Brain banc in variants at 24, 36, 48 units, on separate rows labeled “tuned to the budget”); the shuffled control was recomputed at each budget.

| net margin verbatim | GreenLoop /141 ||||| MOREAU /43 |||||
| budget | 8,000 | 12,000 | 16,000 | 24,000 | 8,000 | 12,000 | 16,000 | 24,000 | 32,000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| naive RAG | 36 | 39 | 36 | 31 | 17 | 21 | 20 | 13 | 2 |
| Brain banc g12 | 56 | 61 | 61 | 61 | 9 | 9 | 9 | 9 | 9 |
| g24 / g36 / g48 | 24 / 22 / 23 | 42 / 26 / 22 | 52 / 34 / 32 | 53 / 50 / 46 | 9 / 2 / 0 | 7 / 9 / 7 | 6 / 5 / 7 | 6 / 5 / 5 | 6 / 5 / 5 |
| Brain prod | 32 | 32 | 32 | 32 | 1 | 1 | 1 | 1 | 1 |
| mem0 | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |

The RAG’s shuffled control rises almost as fast as its signal (GreenLoop 31 → 65; MOREAU 9 → 40): its net lead peaks between 12,000 and 16,000 then declines, and cancels when it returns the entire case. Brain banc g12 keeps the best GreenLoop net margin at every budget; giving it more units never improves it above g12 and degrades it sharply under 12,000 — wide pools reorder the fusion, and the budget cut keeps the wrong elements. On MOREAU, Brain banc stays at 12 with 48 units and 21,330 characters returned: it never returns the whole passage.

### E6 — Stage 3 on the legal case (26 September)

A first pass, with the English prompt inherited from GreenLoop, had dates translated (“1 March 2022”): the letter was lost by construction and value scoring counted as conformant answers that cited nothing. It is archived. The published pass asks in French to cite word for word with the document and to keep dates and amounts in the document’s form. The *letter* holds under four conditions: a verbatim passage of at least 40 characters from the support, all its discriminants, the named document, no admission of ignorance — an earlier rule accepted an answer that listed the expected form among hypotheses it admitted not knowing.

| MOREAU, 50 questions | value-conformant | letter-conformant | correct abstentions /7 | both sides /4 | stability /5 | judge faults flagged → confirmed | prompt tokens |
|---|---:|---:|---:|---:|---:|---:|---:|
| A — no memory | 7 | 0 | 6 | 0 | 0 | 0 | 30 |
| naive RAG | 39 | 30 | 3 | 4 | 5 | 3 → 0 | 2,838 |
| Brain banc | 36 | 19 | 3 | 4 | 4 | 0 | 1,557 |
| mem0 | 31 | 5 | 2 | 4 | 3 | 1 → 0 | 1,770 |
| Brain prod | 25 | 3 | 3 | 1 | 4 | 1 → 0 | 515 |

Value and letter do not say the same thing: mem0 answers correctly 31 times and cites 5 times — conversational memory knows *what* the documents say, not *how*. The judge (gpt-5.6-sol, via the Codex CLI after Cursor quota exhaustion) flagged five faults; reread one by one, all five were judge errors — the answers wrote “28 janvier 2024” [date as printed in the document], “14 700,00 €” [amount as printed in the document], the document’s form that the trap forbade betraying. Abstention remains everyone’s weak point: with a context, the model accepts saying “the case does not establish it” only two or three times out of seven.

### E7 — Stage 3 on the business case, homogeneous arm (26 September)

| GreenLoop, 141 questions | conformant | both sides /28 | correct `unknown` abstentions /14 | judge faults flagged → confirmed | stability /5 | prompt tokens |
|---|---:|---:|---:|---:|---:|---:|
| A — no memory | 15 | 0 | 14 | 1 → 0 | 0 | 28 |
| Brain banc | 78 | 27 | 2 | 0 | 3 | 2,382 |
| naive RAG | 65 | 28 | 4 | 7 → 7 | 3 | 2,886 |
| Brain prod | 49 | 13 | 4 | 8 → 8 | 2 | 721 |
| mem0 | 49 | 12 | 1 | 2 → 1 | 3 | 1,446 |

The 23 September reference (Brain banc 75/141, with another judge) holds. This time the judge faults are real: on disputes, Brain prod (8) and the RAG (7) answer a single value — “*12 collections*”, “les deux sources concordent” [both sources agree] — where the trap forbids deciding; Brain banc, 27 disputes out of 28 returned on both sides, has none. When both versions arrive side by side, the model reports them; when only one arrives, it asserts it. Stability of 2 to 3 out of 5 (the respondent goes through a CLI agent that tries tools before answering) is worth a margin of a few points across the whole column.

### E8 — One or two graph edges (27 September)

The graph is implicit in the atoms table: 33 entities and 103 typed edges on MOREAU, 460 and 135 on GreenLoop. A neighborhood gate hops from the entities of the returned atoms to their temporal, monetary, or status atoms (quota 6), then follows relations to a second entity (6 more). A first version, which filtered predicates, was inert and was not measured — a gate that returns zero elements fails the measure. Returned as an atom, the neighbor contributes nothing (g12 = v1 = v2). Returned by its sentence or its passage, it contributes three real supports per case — the hiring sentence and the amendment sentence on a chronology — and the shuffled control rises by as much: net margin 61 → 59 then 58 on GreenLoop, 9 → 9 on MOREAU, for 22 to 81% more characters. At this graph scale and with these units, structure does not complete better than similarity finds.

## 6. What is most effective — where, when, how, why

- **When the case fits in the reading budget, the best memory is the case.** At 40% of the corpus returned, the passage RAG holds 35 clauses out of 43; at 100%, 42 — and its net margin falls to 2, because there is nothing left to *find*. Search is not the problem of a small case; filtering and return are. A memory that summarizes, atomizes, or windows loses the letter for nothing.
- **When the case exceeds the budget, structure wins in net, and volume loses.** On 236,000 characters, the two-gate chain keeps a net margin of 56 to 61 at every budget, with a flat shuffled control; the RAG peaks at 39 and falls back when given more, because its shuffled control climbs with its signal. The mechanism that counts is the *second round* toward the other version of a fact: 27 disputes out of 28, zero assertion of a single value.
- **More units is not more recall.** Widening the pools reorders the fusion and the budget cut keeps the wrong elements: at 8,000 characters, 24 units score 39 where 12 score 79. Expansion is a gain only beyond the budget where everything can be kept — and it never reaches the net of the tight configuration.
- **On a case where the letter is binding, what decides is neither search nor the graph: it is the shape of the returned unit.** A 12-character atom cites nothing; a two-sentence window does not carry a 590-character clause; a 255-character memory paraphrases it. Only the whole passage carries it. That is the only change the bench justifies for the chain to carry: return the passage when the question targets a clause or when the budget allows.
- **Conversational memory retains value, not the letter.** mem0: 31 correct answers out of 50, 5 citations; zero net margin in value on the legal case, 2 on the business case. It is not its search that limits it — k = 20 or 40, same score — it is what it retained.
- **Memory gives assurance, including when it should not.** Without context, the model abstains 14 times out of 14 when it should, and 126 times when it should not; with context, it abstains only 1 to 4 times out of 14. No provider solves abstention; that is the column an independent judge must hold.
- **The gap that counts is internal.** Brain in production — 39/141, 1/43, 25 | 3 at legal stage 3 — is last or second-to-last everywhere. The distance between what runs and what the bench knows how to run is greater than the distance between Brain and any measured competitor.

## 7. What the method learned about itself

A bench that does not measure its own noise measures nothing: without the shuffled control, the RAG was “better” at 85 against 84. An instrument changed after seeing a score declares itself, and the old one remains published. Artifacts of a measure expire when the instrument changes — the GreenLoop JSON still carried the figures from before the tightening — and must be regenerated, the old kept as evidence. A judge errs: 5 faults out of 5 false on the legal case, 16 true out of 18 on the business case; one publishes the audit, not the raw count. A gate that returns zero elements, a provider that searches the wrong vault, a gold set whose documents are missing, a table that ingestion writes and readers do not read: each of these defects produced, at least once, a plausible and false table, and each became an explicit bench refusal. Finally, the gold set is not written with the measured system, and ingestion never reads the gold set — a chain that proposed to “align its objects on the gold set” was stopped.

## 8. Limits

- Two cases, synthetic, one team: the Brain chain was tuned on GreenLoop; the blind half of the disputes controls this bias, it does not cancel it.
- A single respondent (Grok 4.5), served by a CLI agent whose tooling weighs on usage and stability (2 to 3 identical replays out of 3); a single judge per stage, audited by hand.
- The shuffled control confounds instrument permissiveness and context width; it is a precision measure, not a pure noise floor.
- Verbatim mode requires the full gold-set citation: it penalizes any unit shorter than the clause, which is the point on the legal case and a convention on the business case.
- Letta is not measured; MRFS has no ingestion that builds situations; LoCoMo, the ground of conversational memories, remains to be done.
- The bench’s “naive” RAG is not so naive: structured query, hybrid search, overlap calibrated on the gold set. It is the bar to beat, not a lazy baseline.

## 9. Reproducibility and data

Both cases, their gold sets, the results by provider and by configuration, the persisted contexts, the reports and the shuffled controls are published with the frozen protocol, separately from the results, and a fingerprint manifest. Stage 2 replays without a model call; stage 3 names its respondent, its judge and its ceilings. Every figure in this paper carries, in the repository, the commit and the file that produced it.

## 10. Conclusion

There is no memory better in itself; there is a good unit shape for a case size and a nature of fact. When the case fits in the hand, one returns it. When it no longer fits, one structures — and the structure that wins is modest: atoms and the sentence they come from, searched separately, returned together, with a second round for the other version. When the letter is binding, one returns the passage. And in every case, one measures what chance would yield, one publishes both, and one writes what one changed after seeing.

Internal references: ADR 0023 “Comparative bench: Brain against third-party memories” (decisions 1–9), ADR 0024 “Porting the bench chain to production” (accepted 27 September 2026), issues #117, #119, #120, #127, #129, #135, #137 of the `brain` repository. Prior position paper: *Reconstruct Before Reasoning* (August 2026, pre-empirical).
