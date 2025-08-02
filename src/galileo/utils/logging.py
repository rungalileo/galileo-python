from galileo.schema.trace import SPAN_TYPE


def is_textual_span_type(span_type: SPAN_TYPE) -> bool:
    """
    Check if the span type has a string-based input and output.

    Args:
        span_type: The type of span

    Returns:
        bool: True if the span type has a string-based input and output, False otherwise
    """
    return span_type in ["tool", "workflow", "agent"]


def is_concludable_span_type(span_type: SPAN_TYPE) -> bool:
    """
    Check if the span type requires conclusion (via `conclude()`).

    Args:
        span_type: The type of span

    Returns:
        bool: True if the span type requires conclusion, False otherwise
    """
    return span_type in ["workflow", "agent"]
