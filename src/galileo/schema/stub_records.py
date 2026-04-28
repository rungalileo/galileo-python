"""SDK-side re-exports and helpers for read-side stub record types (DT 2.0).

The schemas themselves live in ``galileo_core.schemas.shared.stub_records``,
which mirrors how ``ContentPart`` (read side) lives in galileo-core while
``IngestContentBlock`` (write side) lives in the SDK.

This module exists purely so SDK consumers do not have to dig into the core
namespace, and so that an ``is_stub_record(x)`` helper is available for the
common pattern-match case.
"""

from typing import Any

from galileo_core.schemas.shared.stub_records import StubSpanRecord, StubTraceRecord


def is_stub_record(record: Any) -> bool:
    """Return True if ``record`` is a synthesized stub (missing trace or span).

    Useful when iterating over a tree returned by the API and rendering
    placeholder UI for nodes that have not been ingested yet.
    """
    return isinstance(record, StubSpanRecord | StubTraceRecord)


__all__ = ["StubSpanRecord", "StubTraceRecord", "is_stub_record"]
