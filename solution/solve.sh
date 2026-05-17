#!/bin/bash
# Oracle solution for pyreport multi-bug task.
# Applies all 8 fixes in-place and writes fixes.json.
set -e

# ── Fix #1: formatter.py — truncate slices to max_len-3 before appending "..." ──
python3 - <<'PYEOF'
import re, pathlib
path = pathlib.Path("/workspace/pyreport/formatter.py")
src = path.read_text()
# Replace the buggy return line inside truncate
old = "        return text[:max_len] + \"...\""
new = "        return text[:max_len - 3] + \"...\""
assert old in src, f"Pattern not found in formatter.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #1 applied: formatter.py truncate")
PYEOF

# ── Fix #2: stats.py — divide by sum(weights) not len(values) ───────────────
python3 - <<'PYEOF'
import pathlib
path = pathlib.Path("/workspace/pyreport/stats.py")
src = path.read_text()
old = "    return numerator / len(values)"
new = "    return numerator / sum(weights)"
assert old in src, f"Pattern not found in stats.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #2 applied: stats.py weighted_average")
PYEOF

# ── Fix #3: filters.py — use <= for end_date comparison ─────────────────────
python3 - <<'PYEOF'
import pathlib
path = pathlib.Path("/workspace/pyreport/filters.py")
src = path.read_text()
old = "        if start_date <= record_date < end_date:"
new = "        if start_date <= record_date <= end_date:"
assert old in src, f"Pattern not found in filters.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #3 applied: filters.py filter_date_range")
PYEOF

# ── Fix #4: serializer.py — keep None values in output ──────────────────────
python3 - <<'PYEOF'
import pathlib
path = pathlib.Path("/workspace/pyreport/serializer.py")
src = path.read_text()
old = (
    "        # BUG: None values are dropped; they should be kept as null\n"
    "        if v is not None:\n"
    "            if isinstance(v, (date, datetime)):\n"
    "                out[field] = v.isoformat()\n"
    "            else:\n"
    "                out[field] = v"
)
new = (
    "        if isinstance(v, (date, datetime)):\n"
    "            out[field] = v.isoformat()\n"
    "        else:\n"
    "            out[field] = v"
)
assert old in src, f"Pattern not found in serializer.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #4 applied: serializer.py serialize_record")
PYEOF

# ── Fix #5: aggregator.py — flush the final group after the loop ─────────────
python3 - <<'PYEOF'
import pathlib
path = pathlib.Path("/workspace/pyreport/aggregator.py")
src = path.read_text()
old = (
    "    # BUG: the last group is never flushed — missing line:\n"
    "    # groups[current_key] = current_group\n"
    "\n"
    "    return groups"
)
new = (
    "    # Flush the final group\n"
    "    groups[current_key] = current_group\n"
    "\n"
    "    return groups"
)
assert old in src, f"Pattern not found in aggregator.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #5 applied: aggregator.py group_by")
PYEOF

# ── Fix #6: validator.py — tighten email regex ───────────────────────────────
python3 - <<'PYEOF'
import pathlib
path = pathlib.Path("/workspace/pyreport/validator.py")
src = path.read_text()
old = '_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\\-]*@[a-zA-Z0-9.\\-]+$")'
new = '_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}$")'
assert old in src, f"Pattern not found in validator.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #6 applied: validator.py validate_email")
PYEOF

# ── Fix #7: pager.py — use (page - 1) * page_size for 1-indexed pages ───────
python3 - <<'PYEOF'
import pathlib
path = pathlib.Path("/workspace/pyreport/pager.py")
src = path.read_text()
old = "    # BUG: treats page as 0-indexed; should be (page - 1) * page_size\n    start = page * page_size"
new = "    start = (page - 1) * page_size"
assert old in src, f"Pattern not found in pager.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #7 applied: pager.py paginate")
PYEOF

# ── Fix #8: merger.py — concatenate lists instead of overwriting ─────────────
python3 - <<'PYEOF'
import pathlib
path = pathlib.Path("/workspace/pyreport/merger.py")
src = path.read_text()
old = "                # BUG: should concatenate, but instead overwrites\n                result[k] = v"
new = "                result[k] = result[k] + v"
assert old in src, f"Pattern not found in merger.py:\n{src}"
path.write_text(src.replace(old, new, 1))
print("Fix #8 applied: merger.py deep_merge")
PYEOF

# ── Write fixes.json ─────────────────────────────────────────────────────────
mkdir -p /logs/agent
cat > /logs/agent/fixes.json <<'JSON'
{
  "fixes": [
    {
      "module": "formatter",
      "function": "truncate",
      "bug_description": "The slice took max_len characters then appended '...', making the result max_len+3 characters long.",
      "fix_description": "Changed slice to max_len-3 before appending '...' so the result is at most max_len characters."
    },
    {
      "module": "stats",
      "function": "weighted_average",
      "bug_description": "The denominator used len(values) instead of sum(weights), giving an incorrect result when weights differ.",
      "fix_description": "Changed denominator from len(values) to sum(weights)."
    },
    {
      "module": "filters",
      "function": "filter_date_range",
      "bug_description": "The end-date comparison used strict less-than (<), excluding records on the end date itself.",
      "fix_description": "Changed the comparison to less-than-or-equal (<=) so the end date is included."
    },
    {
      "module": "serializer",
      "function": "serialize_record",
      "bug_description": "Fields with None values were skipped with an 'if v is not None' guard, silently dropping null fields.",
      "fix_description": "Removed the None guard so all schema fields are always written to the output dict."
    },
    {
      "module": "aggregator",
      "function": "group_by",
      "bug_description": "The final group was never appended to the result dict after the loop ended, discarding its rows.",
      "fix_description": "Added groups[current_key] = current_group after the loop to flush the final group."
    },
    {
      "module": "validator",
      "function": "validate_email",
      "bug_description": "The email regex allowed empty local parts and domain names without a dot (no TLD), accepting invalid addresses.",
      "fix_description": "Tightened the regex to require a non-empty local part and a domain with at least one dot and a 2+ letter TLD."
    },
    {
      "module": "pager",
      "function": "paginate",
      "bug_description": "The start index was computed as page*page_size (0-indexed), so page=1 returned the second page.",
      "fix_description": "Changed start computation to (page-1)*page_size so pages are correctly 1-indexed."
    },
    {
      "module": "merger",
      "function": "deep_merge",
      "bug_description": "When both values were lists, the override list replaced the base list instead of being concatenated.",
      "fix_description": "Changed the list branch to concatenate: result[k] = result[k] + v."
    }
  ]
}
JSON

echo "Oracle solution complete. All 8 fixes applied and fixes.json written."
