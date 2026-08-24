from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def build_where_filter(filters: Mapping[str, Sequence[str] | str | None]) -> dict[str, Any] | None:
    """Build a Chroma metadata filter.

    Multiple values for the same field are combined with $in (logical OR).
    Different fields are combined with $and.
    """
    predicates: list[dict[str, Any]] = []
    for key, raw_values in filters.items():
        if raw_values is None:
            continue
        if isinstance(raw_values, str):
            values = [raw_values]
        else:
            values = [value for value in raw_values if value]
        if not values:
            continue
        if len(values) == 1:
            predicates.append({key: values[0]})
        else:
            predicates.append({key: {"$in": values}})

    if not predicates:
        return None
    if len(predicates) == 1:
        return predicates[0]
    return {"$and": predicates}
