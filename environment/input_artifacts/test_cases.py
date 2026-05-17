"""
test_cases.py - The canonical test suite for pyreport.

These tests are run by verify.py against the agent's fixed code.
Each test corresponds to exactly one bug.
"""

import sys
import os
from datetime import date

# Add the workspace to the path so we can import pyreport
sys.path.insert(0, "/workspace")


def test_bug1_truncate() -> bool:
    """
    Bug #1 (formatter.py): truncate should return a string of at most max_len chars.
    A string of length 10 truncated to max_len=8 should be exactly 8 chars.
    """
    from pyreport.formatter import truncate
    result = truncate("HelloWorld", 8)
    # Must be at most 8 characters and end with "..."
    return len(result) <= 8 and result.endswith("...")


def test_bug2_weighted_average() -> bool:
    """
    Bug #2 (stats.py): weighted_average([1, 2, 3], [1, 1, 8]) should be
    (1*1 + 2*1 + 3*8) / (1+1+8) = 27/10 = 2.7, not 9.0.
    """
    from pyreport.stats import weighted_average
    result = weighted_average([1.0, 2.0, 3.0], [1.0, 1.0, 8.0])
    return abs(result - 2.7) < 1e-9


def test_bug3_filter_date_range_inclusive() -> bool:
    """
    Bug #3 (filters.py): filter_date_range should include rows on the end_date.
    """
    from pyreport.filters import filter_date_range
    rows = [
        {"date": "2024-01-01", "val": "a"},
        {"date": "2024-01-15", "val": "b"},
        {"date": "2024-01-31", "val": "c"},
    ]
    result = filter_date_range(rows, "date", date(2024, 1, 1), date(2024, 1, 31))
    return len(result) == 3


def test_bug4_serialize_none_fields() -> bool:
    """
    Bug #4 (serializer.py): serialize_record must preserve None values as null,
    not silently drop them.
    """
    from pyreport.serializer import serialize_record
    record = {"id": "r1", "name": "Alice", "category": None, "amount": 50.0,
              "date": None, "active": True, "notes": None}
    result = serialize_record(record)
    # All schema fields must be present, with None values kept
    return (
        "category" in result and result["category"] is None and
        "date" in result and result["date"] is None and
        "notes" in result and result["notes"] is None
    )


def test_bug5_group_by_last_group() -> bool:
    """
    Bug #5 (aggregator.py): group_by must not drop the final group.
    """
    from pyreport.aggregator import group_by
    rows = [
        {"cat": "A", "v": 1},
        {"cat": "A", "v": 2},
        {"cat": "B", "v": 3},
        {"cat": "B", "v": 4},
        {"cat": "C", "v": 5},
    ]
    result = group_by(rows, "cat")
    return "C" in result and len(result["C"]) == 1 and result["C"][0]["v"] == 5


def test_bug6_validate_email_rejects_no_tld() -> bool:
    """
    Bug #6 (validator.py): validate_email must reject addresses without a dot
    in the domain part (no TLD), e.g. 'user@domain'.
    """
    from pyreport.validator import validate_email
    return (
        not validate_email("user@domain") and      # no TLD — must be rejected
        not validate_email("@example.com") and     # empty local — must be rejected
        validate_email("user@example.com") and     # valid — must pass
        validate_email("a.b+c@sub.domain.org")     # valid complex — must pass
    )


def test_bug7_paginate_1indexed() -> bool:
    """
    Bug #7 (pager.py): paginate is 1-indexed; page=1 should return items[0:5].
    """
    from pyreport.pager import paginate
    items = list(range(20))
    page1 = paginate(items, page=1, page_size=5)
    page2 = paginate(items, page=2, page_size=5)
    return page1 == [0, 1, 2, 3, 4] and page2 == [5, 6, 7, 8, 9]


def test_bug8_deep_merge_concatenates_lists() -> bool:
    """
    Bug #8 (merger.py): deep_merge must concatenate lists, not overwrite them.
    """
    from pyreport.merger import deep_merge
    base = {"tags": ["a", "b"], "meta": {"count": 1}}
    override = {"tags": ["c", "d"], "meta": {"count": 2}}
    result = deep_merge(base, override)
    return result["tags"] == ["a", "b", "c", "d"] and result["meta"]["count"] == 2


ALL_TESTS = [
    ("bug1_formatter_truncate",        test_bug1_truncate),
    ("bug2_stats_weighted_average",    test_bug2_weighted_average),
    ("bug3_filters_date_range",        test_bug3_filter_date_range_inclusive),
    ("bug4_serializer_none_fields",    test_bug4_serialize_none_fields),
    ("bug5_aggregator_group_by",       test_bug5_group_by_last_group),
    ("bug6_validator_email",           test_bug6_validate_email_rejects_no_tld),
    ("bug7_pager_1indexed",            test_bug7_paginate_1indexed),
    ("bug8_merger_list_concat",        test_bug8_deep_merge_concatenates_lists),
]
