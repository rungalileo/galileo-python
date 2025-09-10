from typing import Callable

import pytest

from galileo.resources import errors
from galileo.resources.api.health import healthcheck_healthcheck_get
from galileo_core.constants.request_method import RequestMethod
from galileo_core.helpers.api_client import ApiClient


def test_raise_on_unexpected_status_flag(mock_request: Callable):
    """
    Tests that the `raise_on_unexpected_status` flag on ApiClient is respected
    by the generated resource modules.
    """
    # Mock the healthcheck endpoint to return 201 Created, which is a success code
    # that ApiClient will not raise an exception for, but is unexpected by the
    # generated healthcheck client (which only expects 200).
    mock_request(method=RequestMethod.GET, path="/healthcheck", status_code=201, text="Created")

    # Case 1: Flag is True, so we expect an exception for the unexpected 201
    client_with_raise = ApiClient(
        host="https://api.galileo.ai/", jwt_token="dummy-token", raise_on_unexpected_status=True
    )
    with pytest.raises(errors.UnexpectedStatus) as exc_info:
        healthcheck_healthcheck_get.sync(client=client_with_raise)
    assert exc_info.value.status_code == 201
    assert "Created" in str(exc_info.value.content)

    # Case 2: Flag is False, so we expect None (no exception)
    client_without_raise = ApiClient(
        host="https://api.galileo.ai/", jwt_token="dummy-token", raise_on_unexpected_status=False
    )
    result = healthcheck_healthcheck_get.sync(client=client_without_raise)
    assert result is None
