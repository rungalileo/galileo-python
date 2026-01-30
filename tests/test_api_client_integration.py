from typing import Callable

import pytest

from galileo.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
)
from galileo.resources import errors
from galileo.resources.api.health import healthcheck_healthcheck_get
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient


def test_common_http_errors_raise_specific_exceptions(mock_request: Callable) -> None:
    """
    Tests that common HTTP error codes raise specific exceptions with actionable messages.
    """
    client = ApiClient(host="https://api.galileo.ai/", jwt_token="dummy-token")

    # Test 400 Bad Request
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=400, text="Bad Request")
    with pytest.raises(BadRequestError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 400
    assert "Bad request" in str(exc_info.value)

    # Test 401 Unauthorized
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=401, text="Unauthorized")
    with pytest.raises(AuthenticationError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 401
    assert "Authentication failed" in str(exc_info.value)

    # Test 403 Forbidden
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=403, text="Forbidden")
    with pytest.raises(ForbiddenError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 403
    assert "Permission denied" in str(exc_info.value)

    # Test 404 Not Found
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=404, text="Not Found")
    with pytest.raises(NotFoundError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 404
    assert "Resource not found" in str(exc_info.value)

    # Test 409 Conflict
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=409, text="Conflict")
    with pytest.raises(ConflictError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 409
    assert "Resource conflict" in str(exc_info.value)

    # Test 429 Rate Limit
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=429, text="Too Many Requests")
    with pytest.raises(RateLimitError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 429
    assert "Rate limit exceeded" in str(exc_info.value)

    # Test 500 Server Error
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=500, text="Internal Server Error")
    with pytest.raises(ServerError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 500
    assert "Server error" in str(exc_info.value)

    # Test 503 Service Unavailable (also covered by ServerError for >= 500)
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=503, text="Service Unavailable")
    with pytest.raises(ServerError) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 503


def test_unexpected_status_raises_for_unknown_codes(mock_request: Callable) -> None:
    """
    Tests that truly unexpected status codes raise UnexpectedStatus.
    """
    client = ApiClient(host="https://api.galileo.ai/", jwt_token="dummy-token")

    # Test 201 Created - unexpected for healthcheck endpoint
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=201, text="Created")
    with pytest.raises(errors.UnexpectedStatus) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 201

    # Test 418 I'm a teapot - truly unexpected
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=418, text="I'm a teapot")
    with pytest.raises(errors.UnexpectedStatus) as exc_info:
        healthcheck_healthcheck_get.sync(client=client)
    assert exc_info.value.status_code == 418
