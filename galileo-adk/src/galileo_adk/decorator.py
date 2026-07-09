"""Decorators for marking ADK tools with Galileo observability metadata."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def splunk_ao_retriever(func: Callable[..., Any]) -> Callable[..., Any]:
    """Mark a function as a retriever for Galileo observability.

    When a function decorated with @splunk_ao_retriever is wrapped in a
    FunctionTool, Galileo will log it as a retriever span (node_type="retriever")
    instead of a tool span, enabling RAG quality metrics.

    Example
    -------
    >>> from galileo_adk import splunk_ao_retriever
    >>> @splunk_ao_retriever
    ... def my_search(query: str) -> str:
    ...     return search_docs(query)
    >>> tool = FunctionTool(my_search)
    """
    func._splunk_ao_is_retriever = True  # type: ignore[attr-defined]
    return func
