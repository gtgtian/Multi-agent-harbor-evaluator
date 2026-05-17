"""
aggregator.py - Groups and aggregates tabular report data.

Bug #5: `group_by` iterates over rows and flushes the current group only
when the key *changes*, but never flushes the **final** group after the
loop ends.  The last group of rows is always silently discarded.

Fix: after the loop, append the final pending group to the result if it
is non-empty.
"""

from typing import Any, Dict, List


def group_by(rows: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    Group rows by the value of `key`.

    Assumes rows are pre-sorted by key (like SQL GROUP BY over sorted data).
    Returns a dict mapping each key value to the list of rows in that group.
    """
    if not rows:
        return {}

    groups: Dict[Any, List[Dict[str, Any]]] = {}
    current_key = rows[0].get(key)
    current_group: List[Dict[str, Any]] = []

    for row in rows:
        row_key = row.get(key)
        if row_key != current_key:
            # flush previous group
            groups[current_key] = current_group
            current_key = row_key
            current_group = []
        current_group.append(row)

    # BUG: the last group is never flushed — missing line:
    # groups[current_key] = current_group

    return groups


def sum_column(rows: List[Dict[str, Any]], column: str) -> float:
    """Return sum of `column` across rows, treating missing values as 0."""
    return sum(float(r.get(column, 0)) for r in rows)


def count_distinct(rows: List[Dict[str, Any]], column: str) -> int:
    """Return count of distinct non-None values in `column`."""
    return len({r[column] for r in rows if column in r and r[column] is not None})
