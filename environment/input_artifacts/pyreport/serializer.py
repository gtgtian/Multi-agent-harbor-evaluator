"""
serializer.py - Serializes report records to JSON-compatible dicts.

Bug #4: `serialize_record` skips fields whose value is `None`, so null
fields are silently lost from the output.  Consumers that expect all
declared schema fields to be present will receive incomplete records.

Fix: remove the `if v is not None` guard so that None values are kept
(they will serialize correctly to JSON null).
"""

import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional


_SCHEMA_FIELDS = ["id", "name", "category", "amount", "date", "active", "notes"]


def serialize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Return a JSON-safe dict for a single record, keeping schema field order."""
    out: Dict[str, Any] = {}
    for field in _SCHEMA_FIELDS:
        v = record.get(field)
        # BUG: None values are dropped; they should be kept as null
        if v is not None:
            if isinstance(v, (date, datetime)):
                out[field] = v.isoformat()
            else:
                out[field] = v
    return out


def serialize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Serialize a list of records."""
    return [serialize_record(r) for r in records]


def to_json(records: List[Dict[str, Any]], indent: int = 2) -> str:
    """Return pretty-printed JSON string for a list of serialized records."""
    return json.dumps(serialize_records(records), indent=indent)
