"""
formatter.py - Formats report sections into human-readable strings.

Bug #1: `truncate` uses `>` instead of `>=`, so strings of exactly `max_len`
characters are incorrectly truncated and gain the ellipsis suffix, producing
a result that is longer than `max_len` and failing equality checks.

Fix: change `if len(text) > max_len:` to `if len(text) >= max_len:`.
Wait — actually the correct semantic is: truncate only when the string is
STRICTLY longer than max_len, keeping strings of exactly max_len intact.
The real bug is that the ellipsis is appended AFTER slicing to max_len,
making the output max_len+3 chars.  Fix: slice to max_len - 3 before
appending the ellipsis, i.e. text[:max_len - 3] + "...".
"""


def truncate(text: str, max_len: int) -> str:
    """Return text truncated to max_len characters (including ellipsis)."""
    if len(text) > max_len:
        # BUG: slices to full max_len then appends "...", exceeding max_len
        return text[:max_len] + "..."
    return text


def center_heading(title: str, width: int = 60) -> str:
    """Return title centered within a line of dashes."""
    padded = f" {title} "
    dash_count = max(0, width - len(padded))
    left = dash_count // 2
    right = dash_count - left
    return "-" * left + padded + "-" * right


def bullet_list(items: list, indent: int = 2) -> str:
    """Return a bulleted list string."""
    prefix = " " * indent + "- "
    return "\n".join(prefix + str(item) for item in items)
