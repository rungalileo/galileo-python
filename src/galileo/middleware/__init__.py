"""
Galileo middleware for web frameworks.

This module provides middleware for automatically extracting distributed tracing
headers from HTTP requests and making them available to the @log decorator.
"""

from galileo.middleware.tracing import TracingMiddleware

__all__ = ["TracingMiddleware"]
