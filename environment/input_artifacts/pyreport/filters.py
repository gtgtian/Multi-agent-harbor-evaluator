"""
filters.py - Row-level filtering helpers for tabular report data.

Bug #3: `filter_date_range` uses a strict `<` for the end-date check,
so records on exactly the end date are excluded.  The correct behaviour
is to include records where date <= end_date (inclusive range).

Fix: change `record_date < end_date` to `record_date <= end_date`.
"""

from datetime import date
from typing import Any, Dict, List, Optional


def filter_by_value(
    rows: List[Dict[str, Any]],
    column: str,
    value: Any,
) -> List[Dict[str, Any]]:
    """Return rows where rows[column] == value."""
    return [r for r in rows if r.get(column) == value]


def filter_date_range(
    rows: List[Dict[str, Any]],
    date_column: str,
    start_date: date,
    end_date: date,
) -> List[Dict[str, Any]]:
    """Return rows where start_date <= row[date_column] <= end_date."""
    result = []
    for row in rows:
        raw = row.get(date_column)
        if raw is None:
            continue
        if isinstance(raw, str):
            record_date = date.fromisoformat(raw)
        else:
            record_date = raw
        # BUG: end_date check should be <= not <
        if start_date <= record_date < end_date:
            result.append(row)
    return result


def filter_top_n(
    rows: List[Dict[str, Any]],
    column: str,
    n: int,
    descending: bool = True,
) -> List[Dict[str, Any]]:
    """Return the top-n rows sorted by column."""
    valid = [r for r in rows if column in r]
    sorted_rows = sorted(valid, key=lambda r: r[column], reverse=descending)
    return sorted_rows[:n]
