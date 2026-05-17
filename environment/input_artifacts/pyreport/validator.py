"""
validator.py - Input validation helpers for report record fields.

Bug #6: `validate_email` uses a regex that accepts strings like
"user@domain" (no TLD / dot in domain part) and also accepts empty
local parts such as "@example.com".

Fix: tighten the regex so the local part requires at least one character
and the domain part requires at least one dot followed by 2+ letters, e.g.:
  r'^[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}$'
"""

import re
from typing import Any, Dict, List, Tuple


# BUG: regex does not require a dot in the domain part
_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]*@[a-zA-Z0-9.\-]+$")


def validate_email(email: str) -> bool:
    """Return True if email looks like a valid address."""
    return bool(_EMAIL_RE.match(email))


def validate_positive_number(value: Any) -> bool:
    """Return True if value is a number strictly greater than zero."""
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def validate_record(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a report record.

    Returns (is_valid, list_of_error_messages).
    """
    errors: List[str] = []

    if not record.get("id"):
        errors.append("id is required")

    if not record.get("name"):
        errors.append("name is required")

    email = record.get("email")
    if email is not None and not validate_email(email):
        errors.append(f"invalid email: {email!r}")

    amount = record.get("amount")
    if amount is not None and not validate_positive_number(amount):
        errors.append(f"amount must be positive, got {amount!r}")

    return (len(errors) == 0, errors)
