#!/usr/bin/env python3
"""
verify.py - Executable verifier for the pyreport multi-bug task.

Scoring:
  - 8 functional tests, each worth 0.10 (total 0.80)
  - fixes.json present and well-formed: 0.10
  - fixes.json has exactly 8 entries with required keys: 0.10
  Total max: 1.00

Reward is written to /logs/verifier/reward.txt.
"""

import importlib
import json
import os
import sys
import traceback
from pathlib import Path

# Ensure the workspace is importable
sys.path.insert(0, "/workspace")

REWARD_PATH = Path("/logs/verifier/reward.txt")
FIXES_PATH = Path("/logs/agent/fixes.json")
REQUIRED_FIX_KEYS = {"module", "function", "bug_description", "fix_description"}
WEIGHT_PER_TEST = 0.10
WEIGHT_JSON_PRESENT = 0.10
WEIGHT_JSON_VALID = 0.10
NUM_TESTS = 8

score = 0.0
results = []


def run_test(name: str, fn) -> bool:
    try:
        # Force reimport of pyreport modules so fixes are picked up
        mods_to_remove = [k for k in sys.modules if k.startswith("pyreport")]
        for mod in mods_to_remove:
            del sys.modules[mod]
        passed = fn()
        results.append((name, passed, ""))
        return passed
    except Exception as e:
        tb = traceback.format_exc()
        results.append((name, False, str(e)))
        return False


# ── Load test cases ──────────────────────────────────────────────────────────
try:
    # Remove cached module if present
    if "test_cases" in sys.modules:
        del sys.modules["test_cases"]
    import test_cases
    ALL_TESTS = test_cases.ALL_TESTS
except Exception as e:
    print(f"FATAL: could not load test_cases.py: {e}")
    REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    REWARD_PATH.write_text("0.0")
    sys.exit(1)

# ── Run functional tests ─────────────────────────────────────────────────────
for test_name, test_fn in ALL_TESTS:
    passed = run_test(test_name, test_fn)
    if passed:
        score += WEIGHT_PER_TEST

# ── Check fixes.json ─────────────────────────────────────────────────────────
fixes_present = FIXES_PATH.exists()
if fixes_present:
    score += WEIGHT_JSON_PRESENT
    try:
        fixes_data = json.loads(FIXES_PATH.read_text())
        fixes = fixes_data.get("fixes", [])
        if (
            isinstance(fixes, list)
            and len(fixes) == NUM_TESTS
            and all(
                isinstance(f, dict) and REQUIRED_FIX_KEYS.issubset(f.keys())
                for f in fixes
            )
        ):
            score += WEIGHT_JSON_VALID
            fixes_valid = True
        else:
            fixes_valid = False
    except Exception as e:
        fixes_valid = False
        print(f"fixes.json parse error: {e}")
else:
    fixes_valid = False

# ── Write reward ─────────────────────────────────────────────────────────────
REWARD_PATH.parent.mkdir(parents=True, exist_ok=True)
final_score = round(min(score, 1.0), 4)
REWARD_PATH.write_text(str(final_score))

# ── Print report ─────────────────────────────────────────────────────────────
print("=" * 60)
print("pyreport multi-bug verifier")
print("=" * 60)
for name, passed, err in results:
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {name} ({WEIGHT_PER_TEST})")
    if err:
        print(f"         Error: {err}")
print("-" * 60)
print(f"  [{'PASS' if fixes_present else 'FAIL'}] fixes.json present ({WEIGHT_JSON_PRESENT})")
print(f"  [{'PASS' if fixes_valid else 'FAIL'}] fixes.json valid 8-entry ({WEIGHT_JSON_VALID})")
print("=" * 60)
print(f"  FINAL SCORE: {final_score}")
print("=" * 60)

# Exit code: 0 only if perfect score
sys.exit(0 if final_score >= 1.0 else 1)
