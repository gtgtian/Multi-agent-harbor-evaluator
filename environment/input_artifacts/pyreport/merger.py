"""
merger.py - Merges multiple report dicts into a unified summary.

Bug #8: `deep_merge` overwrites list values from `source` with those from
`override` entirely, instead of extending (concatenating) them.  When
merging incremental report shards the earlier shards' list entries are lost.

Fix: when both values are lists, use `base[k] + override[k]` (or extend)
instead of a plain assignment.
"""

from typing import Any, Dict, List


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge `override` into a copy of `base`.

    - Dicts are merged recursively.
    - Lists are **concatenated** (base list + override list).
    - All other values: override wins.
    """
    result = dict(base)
    for k, v in override.items():
        if k in result:
            if isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = deep_merge(result[k], v)
            elif isinstance(result[k], list) and isinstance(v, list):
                # BUG: should concatenate, but instead overwrites
                result[k] = v
            else:
                result[k] = v
        else:
            result[k] = v
    return result


def merge_shards(shards: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge a list of report shard dicts into one unified dict."""
    if not shards:
        return {}
    result = dict(shards[0])
    for shard in shards[1:]:
        result = deep_merge(result, shard)
    return result
