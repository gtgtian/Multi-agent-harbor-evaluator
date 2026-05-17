"""
pager.py - Pagination helpers for report output.

Bug #7: `paginate` treats `page` as 0-indexed when the documented API
says pages are 1-indexed.  Requesting page=1 actually returns the second
page of results; page=0 is never valid but returns the first page.

Fix: change the slice computation from
    start = page * page_size
to
    start = (page - 1) * page_size
and add a guard that raises ValueError when page < 1.
"""

from typing import Any, Dict, List, TypeVar

T = TypeVar("T")


def paginate(items: List[T], page: int, page_size: int) -> List[T]:
    """
    Return one page of items.

    Pages are 1-indexed: page=1 returns the first page_size items.
    """
    if page_size <= 0:
        raise ValueError("page_size must be positive")
    # BUG: treats page as 0-indexed; should be (page - 1) * page_size
    start = page * page_size
    return items[start : start + page_size]


def total_pages(total_items: int, page_size: int) -> int:
    """Return the number of pages needed to display total_items."""
    if page_size <= 0:
        raise ValueError("page_size must be positive")
    if total_items == 0:
        return 0
    return (total_items + page_size - 1) // page_size
