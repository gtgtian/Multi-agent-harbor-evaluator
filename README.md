# pyreport Multi-Bug Repair Task

This project is a multi-bug repair benchmark for the `pyreport` Python reporting library. It is designed to evaluate automated program repair systems, especially in multi-agent or parallelized settings.

## Overview

`pyreport` is a lightweight Python library for building, filtering, aggregating, and exporting report data. The library is split into eight independent modules, each with a single intentionally introduced bug. Each bug is isolated to a single function in its respective module.

## Dependency

This project is designed to be compatible with the **Harbor** multi-agent framework. https://github.com/harbor-framework/harbor.git
The decomposition and coordination patterns follow Harbor conventions, and the `decomposition.yaml` explicitly declares `harbor` as a required framework. To run this benchmark in a multi-agent setting, you should use the Harbor framework for agent orchestration and task execution.

## Directory Structure

```
.
├── environment/
│   ├── Dockerfile
│   └── input_artifacts/
│       ├── pyreport/
│       │   ├── aggregator.py
│       │   ├── filters.py
│       │   ├── formatter.py
│       │   ├── merger.py
│       │   ├── pager.py
│       │   ├── serializer.py
│       │   ├── stats.py
│       │   └── validator.py
│       └── test_cases.py
├── solution/
│   └── solve.sh
├── tests/
│   ├── test.sh
│   └── verify.py
├── .vscode/
│   └── settings.json
├── decomposition.yaml
├── gap_strategy.md
├── instruction.md
├── task.toml
└── .gitignore
```

## The Bugs

Each of the following modules contains one bug:

| Module      | File                          | Buggy Function      | Bug Description (Short)                                  |
|-------------|------------------------------ |---------------------|----------------------------------------------------------|
| formatter   | pyreport/formatter.py         | `truncate`          | Truncates strings incorrectly, may exceed max length     |
| stats       | pyreport/stats.py             | `weighted_average`  | Uses wrong denominator, ignores weights                  |
| filters     | pyreport/filters.py           | `filter_date_range` | Excludes end date, should be inclusive                   |
| serializer  | pyreport/serializer.py        | `serialize_record`  | Drops fields with `None` values                          |
| aggregator  | pyreport/aggregator.py        | `group_by`          | Discards the last group in grouping                      |
| validator   | pyreport/validator.py         | `validate_email`    | Accepts invalid emails (no TLD, empty local part)        |
| pager       | pyreport/pager.py             | `paginate`          | Treats pages as 0-indexed, should be 1-indexed           |
| merger      | pyreport/merger.py            | `deep_merge`        | Overwrites lists instead of concatenating them           |

## Task

**Goal:**  
Fix all eight bugs in-place in their respective source files under `/workspace/pyreport/`.  
After fixing, generate a summary file at `/logs/agent/fixes.json` listing each fix.

**Constraints:**
- Only modify the buggy function in each module.
- Do not change unrelated code or files.
- Do not modify the test cases.
- Do not install extra packages.

## Testing and Verification

- The canonical test suite is [`test_cases.py`](environment/input_artifacts/test_cases.py).
- Use [`tests/verify.py`](tests/verify.py) to run all tests and check the validity of your fixes and summary file.
- The verification script expects `/logs/agent/fixes.json` to contain exactly 8 entries, one per module, each with:
  - `module`
  - `function`
  - `bug_description`
  - `fix_description`

## How to Run

1. **Build the Environment:**
   - Use the provided Dockerfile in `environment/` to build a containerized environment.

2. **Apply Fixes:**
   - Manually fix each bug, or use an automated repair agent.

3. **Run Verification:**
   - Execute `tests/test.sh` or run `tests/verify.py` directly to check your fixes.

4. **Check Results:**
   - The final score and test results will be printed to the console.
   - The reward is written to `/logs/verifier/reward.txt`.

## Multi-Agent Decomposition

This benchmark is designed for multi-agent repair strategies and explicitly supports the Harbor framework. See [decomposition.yaml](decomposition.yaml) for the recommended sub-task breakdown and [gap_strategy.md](gap_strategy.md) for the rationale behind the multi-agent approach.

## References

- [instructions](instruction.md): Full task description and requirements.
- [gap_strategy.md](gap_strategy.md): Rationale for multi-agent decomposition.
- [decomposition.yaml](decomposition.yaml): Sub-task definitions and dependencies.
- [task.toml](task.toml): Task metadata and configuration.

---
