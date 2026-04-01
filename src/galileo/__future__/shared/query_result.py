"""Deprecated: use galileo.shared.query_result instead of galileo.__future__.shared.query_result."""

import warnings

warnings.warn(
    "Importing from galileo.__future__.shared.query_result is deprecated. Use galileo.shared.query_result instead.",
    DeprecationWarning,
    stacklevel=2,
)

from galileo.shared.query_result import QueryResult, _flatten_dict  # noqa: E402

__all__ = ["QueryResult", "_flatten_dict"]
