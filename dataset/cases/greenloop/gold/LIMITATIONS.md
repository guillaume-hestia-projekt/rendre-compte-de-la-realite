# Known limitations of this gold

The gold is a reference, not scripture. What makes it usable is that it was annotated without ever seeing the
answer key of the person who built the dossier, then counter-read by an independent blind reader, then corrected
twice against a written boundary. What follows is what we know is imperfect in it, stated so that nobody
discovers it by surprise.

## One contradiction the blind annotation did not capture

A working note states that the December collection invoice is missing. That invoice is in the dossier. Both
assertions are in the gold, but no dispute joins them, so a system that correctly surfaces this contradiction
earns nothing for it and is not penalised either. We know about it because the dossier's builder had planted it.

We chose not to add it after the fact. Patching a gold from the builder's key is how a benchmark starts rewarding
what its author planted rather than what the documents say. The miss is cheaper than the precedent.

## The gold's own recall is not one

Coverage measured by the blind counter-reader on six documents read in full, unit by unit, was 0.944, and about
0.96 after sorting out false positives. The measure was not extended to the twenty-two other documents. A system
may therefore hold something true that the gold does not carry, and be counted as a false positive for it. Report
such cases: they correct the gold for the next version.

## What is frozen and what is not

Frozen: the 28 document checksums, `situations.json`, `escalations.json`, `tensions.json`, `questions.json`, and
the version of the protocol they were built against. Not frozen: the thresholds in the protocol, which are
proposals until pinned, and the frame catalogue, which does not exist yet for this line of work. The gold names
29 distinct gaps in it.

## Where the answer key lives

The tensions the builder planted, the traps, and the true status of all 285 visits stay outside the repository
while a new blind annotation of the same dossier is still possible. They travel with the dossier once that is no
longer the case, so that anyone can replay the comparison end to end.
