"""Deprecated: use galileo.shared.filter instead of galileo.__future__.shared.filter."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.filter is deprecated. Use galileo.shared.filter instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.filter import (  # noqa: E402
    BooleanFilter,
    DateFilter,
    Filter,
    NumberFilter,
    TextFilter,
    boolean,
    date,
    number,
    text,
)

__all__ = ["BooleanFilter", "DateFilter", "Filter", "NumberFilter", "TextFilter", "boolean", "date", "number", "text"]
