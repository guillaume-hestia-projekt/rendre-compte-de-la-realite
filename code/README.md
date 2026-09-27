# Bench code — snapshot

Verbatim extract of `scripts/banc_realite/`, `tests/banc_realite/` and ADR 0023/0024 from the
private `brain` repository at commit `c619bbbf5578e20ed181ce0bc303e8d33dc1b746` (27 September 2026).

Roughly a third of the scripts import the Brain runtime (`src/brain`, Postgres bench cluster,
Mistral embeddings, Cursor/Codex CLIs) and are published here for reading and provenance, not for
standalone execution. The model-free parts — the two-mode scorer (`holders.py`), the pair
classifier, the matching and agreement helpers, the case descriptors — import standalone; CI checks the
dataset manifest and that import (`.github/workflows/stage2-offline.yml`). The test suite
(`tests/banc_realite/`, 65 files) shares fixtures with the Brain runtime and replays inside the `brain`
repository at the recorded commit, not here. Every stage-2 figure in the paper can be
recomputed from `dataset/results/*/stage2/contextes-*.jsonl` with `holders.classify_pair`.
