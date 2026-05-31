"""Helpers for normalizing user-facing AQL inputs."""

import re

_TAG_QUERY_PATTERN = re.compile(r"tag:(?P<tag>\S+)", re.IGNORECASE)
_COMPACT_OPERATOR_PATTERN = re.compile(r"(?<=\S)(!=|~=|>=|<=|=|>|<)(?=\S)")


def normalize_aql(query: str) -> str:
    """Normalize a user-provided AQL string into backend-friendly syntax.

    This keeps valid AQL intact while smoothing over common user shortcuts:
    - compact operators such as ``status="Draft"`` -> ``status = "Draft"``
    - simple tag shorthand such as ``tag:smoke`` -> ``tag = "smoke"``
    """
    normalized = query.strip()

    if normalized and all(part.lower().startswith("tag:") for part in normalized.split()):
        tags = [match.group("tag") for match in _TAG_QUERY_PATTERN.finditer(normalized)]
        if tags:
            return " and ".join(f'tag = "{tag}"' for tag in tags)

    return _COMPACT_OPERATOR_PATTERN.sub(r" \1 ", normalized)


def quote_aql_string(value: str) -> str:
    """Quote a raw string so it is safe inside an AQL string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')
