# Gap Strategy

## Why Single-Agent Should Struggle

- **Number of artifacts:** 8 independent Python modules, each containing one bug.
- **Estimated input size:** ~600-800 lines of source across 8 files + test_cases.py (~150 lines). Total ~60,000 tokens including full docstrings and comments.
- **Coverage pressure:** A single agent must read, understand, and fix all 8 modules in sequence. Each module uses a distinct Python pattern: string slicing (formatter), arithmetic denominator (stats), comparison operator (filters), conditional guard removal (serializer), loop flush (aggregator), regex (validator), index arithmetic (pager), branch logic (merger). Switching between 8 different bug archetypes within one context window degrades attention.
- **Reconciliation pressure:** After fixing 8 independent modules, the agent must write a coherent `fixes.json` with all 8 entries, each requiring an accurate 1-sentence bug description and fix description. Writing this summary after a long sequential fix session risks forgetting earlier bugs or conflating them.
- **Expected failure mode:** The single agent is most likely to (a) miss 1-3 of the subtler bugs (especially the off-by-one in pager.py and the loop-flush bug in aggregator.py, which require careful reading of loop structure), (b) mis-describe a fix in fixes.json after attention has degraded, and/or (c) run out of effective context budget before completing all 8 fixes under a 600-second timeout.

## Why Multi-Agent Should Succeed

- **Natural subproblems:** Each of the 8 bugs is strictly isolated to a single function in a single file with zero cross-module dependencies. The decomposition is perfectly clean.
- **Sub-agent ownership plan:** 8 parallel fix agents, each assigned exactly one module. Each agent reads only ~75-100 lines of source in its module, fully understands the contract from the docstring, locates the single-line bug, and applies the fix. Context is clean and minimal per agent.
- **Reducer strategy:** A synthesizer agent collects the 8 fix outputs, cross-checks that each source file was actually modified, and writes the consolidated `fixes.json`. The synthesizer's context contains only the 8 short fix summaries — not the full source — making the summary step straightforward and accurate.
- **Why final synthesis is verifiable:** The verifier runs 8 independent functional tests (one per bug) plus checks that `fixes.json` is present and well-formed. Each test is deterministic and binary. The synthesizer's job is concrete: confirm all 8 fixes exist, write structured JSON. The reducer is not making judgment calls; it is checking facts.

## Expected Score Pattern

- **Oracle expected score:** 1.0
- **Single-agent expected score:** 0.40–0.60
  - Expected to fix 4-6 of the 8 bugs (the most visually obvious ones: truncate, date range, weighted average).
  - Likely to miss the aggregator group_by flush bug (requires careful loop reading) and the pager 1-indexing bug (easy to rationalize as intentional).
  - Likely to produce an incomplete or malformed fixes.json (missing entries, losing track of earlier fixes), costing the 0.20 JSON score.
- **Multi-agent expected score:** 0.90–1.0
  - Each fix agent focuses on exactly one bug with full isolated context; coverage of all 8 is much more reliable.
  - Synthesizer has a simple collation task and reliably produces valid fixes.json.
- **Target gap:** 40–60 percentage points

## Oracle Validation

- Oracle run completed: yes
- Oracle reward: 1.0
- Notes: Verified locally by running the full verifier simulation. All 8 functional tests pass after applying the oracle's text-replacement patches to the buggy source. The fixes.json scoring checks also pass. The oracle's assert-guarded Python patches confirm that the exact bug patterns are present before applying fixes, making the oracle robust against accidental pre-fixing.
