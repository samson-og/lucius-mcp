"""Helpers for normalizing user-facing AQL inputs."""

import re

_TAG_QUERY_PATTERN = re.compile(r"tag:(?P<tag>\S+)", re.IGNORECASE)
_OPERATORS = ("!=", "~=", ">=", "<=", "=", ">", "<")


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

    result: list[str] = []
    i = 0
    in_quotes = False
    while i < len(normalized):
        char = normalized[i]

        if char == '"' and (i == 0 or normalized[i - 1] != "\\"):
            in_quotes = not in_quotes
            result.append(char)
            i += 1
            continue

        if not in_quotes:
            operator = next((op for op in _OPERATORS if normalized.startswith(op, i)), None)
            if operator is not None:
                if result and result[-1] not in {" ", "\t"}:
                    result.append(" ")
                result.append(operator)
                next_index = i + len(operator)
                if next_index < len(normalized) and normalized[next_index] not in {" ", "\t"}:
                    result.append(" ")
                i = next_index
                continue

        result.append(char)
        i += 1

    return "".join(result)


def quote_aql_string(value: str) -> str:
    """Quote a raw string so it is safe inside an AQL string literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')
