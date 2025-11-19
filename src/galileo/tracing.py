"""Utilities for distributed tracing with Galileo."""

from galileo.decorator import galileo_context


def get_tracing_headers() -> dict[str, str]:
    """
    Get tracing headers for distributed tracing (decorator usage).

    Returns headers from the singleton logger context that can be passed to downstream services.
    For direct logger instances, use logger.get_tracing_headers() instead.

    Returns
    -------
    dict[str, str]
        Dictionary with X-Galileo-SDK-Trace-ID and X-Galileo-SDK-Parent-ID headers

    Raises
    ------
    GalileoLoggerException
        If not in distributed mode or if no trace has been started

    Examples
    --------
    Using with decorators to propagate trace context to downstream services:

    ```python
    from galileo import log, get_tracing_headers
    import httpx

    @log()
    async def orchestrator():
        # Get headers to pass to downstream service
        headers = get_tracing_headers()

        # Call downstream service with trace context
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://service:8000/process",
                headers=headers,
                json={"data": "..."}
            )
    ```
    """
    return galileo_context.get_logger_instance().get_tracing_headers()
