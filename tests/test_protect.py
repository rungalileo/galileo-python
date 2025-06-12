from typing import Optional
from unittest.mock import (
    ANY,  # For client assertion
    Mock,
    patch,
)
from uuid import uuid4

from pytest import mark

from galileo.protect import Protect, invoke
from galileo.resources.models.execution_status import ExecutionStatus

# from galileo.resources.models.invoke_response import InvokeRespons
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.payload import Payload
from galileo.resources.models.request import Request  # For constructing expected body
from galileo.resources.models.response import Response

A_PROJECT_NAME = "project_name"
A_STAGE_NAME = "stage_name"
A_PROTECT_INPUT = "invoke"


def invoke_response_data() -> dict:
    return {
        "action_result": {"action": "PASSTHROUGH"},
        "stage_metadata": {"stage_id": "stage-uuid-example", "stage_name": "test-stage-example"},
        "text": "Original text from payload",
        "trace_metadata": {
            "id": "trace-uuid-example",
            "received_at": 1234567890,
            "response_at": 1234567990,
            "execution_time": 100.0,
        },
        "status": ExecutionStatus.NOT_TRIGGERED,
        "metric_results": {"sentiment_score": 0.95, "toxicity_level": 0.1},
        "ruleset_results": [
            {
                "ruleset_id": "ruleset-uuid-example",
                "ruleset_name": "basic-ruleset",
                "action_result": {"action": "PASSTHROUGH"},
                "rule_results": [
                    {
                        "rule_id": "rule-uuid-example",
                        "rule_name": "check-sentiment",
                        "action_result": {"action": "PASSTHROUGH"},
                        "metric_results": {"sentiment_score": 0.95},
                        "status": ExecutionStatus.NOT_TRIGGERED,
                        "conditions_results": [],
                    }
                ],
                "status": ExecutionStatus.NOT_TRIGGERED,
            }
        ],
        "api_version": "1.0.0",
        "headers": {"X-Custom-Header": "TestValue"},
        "metadata": {"request_source": "sdk_test"},
    }


def invoke_response() -> Response:
    return Response.from_dict(invoke_response_data())


@mark.parametrize(
    ["include_project_id", "include_project_name", "include_stage_name", "include_stage_id"],
    [
        (True, True, True, True),
        (True, False, True, True),
        (False, True, True, True),
        (False, False, True, True),
        (True, True, False, True),
        (True, False, False, True),
        (True, True, True, False),
        (True, False, True, False),
        (False, True, False, True),
        (False, False, False, True),
    ],
)
@mark.parametrize(
    "payload",
    [
        Payload(input_=A_PROTECT_INPUT),
        Payload(output=A_PROTECT_INPUT),
        Payload(input_=A_PROTECT_INPUT, output=A_PROTECT_INPUT),
    ],
)
@mark.parametrize("timeout", [5, 60])
@mark.parametrize("metadata", [None, {"key": "value"}])
@mark.parametrize("headers", [None, {"key": "value"}])
@mark.parametrize("stage_version", [None, 1, 2])  # Added stage_version parametrization
@patch("galileo.protect.invoke_v2_protect_invoke_post.sync")
def test_invoke_succeess(
    mock_invoke_post_sync: Mock,
    include_project_id: bool,
    include_project_name: bool,
    include_stage_name: bool,
    include_stage_id: bool,
    payload: Payload,
    # rulesets: list[Ruleset], # This is not parametrized directly, but used in invoke call
    timeout: float,
    metadata: dict,
    headers: dict,
    stage_version: Optional[int],  # Added stage_version parameter
) -> None:
    mock_invoke_post_sync.return_value = invoke_response()

    current_project_id_obj = uuid4() if include_project_id else None
    current_project_name_str = A_PROJECT_NAME if include_project_name else None  # Added for clarity
    current_stage_id_obj = uuid4() if include_stage_id else None
    current_stage_name_str = A_STAGE_NAME if include_stage_name else None

    result = invoke(
        payload=payload,
        prioritized_rulesets=None,  # Using None for this test's focus
        project_id=current_project_id_obj,
        project_name=current_project_name_str,
        stage_id=current_stage_id_obj,
        stage_name=current_stage_name_str,
        stage_version=stage_version,
        timeout=timeout,
        metadata=metadata,
        headers=headers,
    )

    # Construct expected_body based on how Protect.invoke creates its Request object
    expected_project_id_val = str(current_project_id_obj) if current_project_id_obj else None
    expected_stage_id_val = str(current_stage_id_obj) if current_stage_id_obj else None

    expected_body = Request(
        payload=payload,
        prioritized_rulesets=[],  # invoke method passes `prioritized_rulesets or []`
        project_id=expected_project_id_val,
        project_name=current_project_name_str,  # Passed as is (can be None)
        stage_id=expected_stage_id_val,
        stage_name=current_stage_name_str,  # Passed as is (can be None)
        stage_version=stage_version,  # Passed as is (can be None)
        timeout=timeout,  # Passed as is (has a default in invoke signature)
        metadata=metadata,  # Passed as is (can be None)
        headers=headers,  # Passed as is (can be None)
    )

    mock_invoke_post_sync.assert_called_once_with(client=ANY, body=expected_body)

    # TODO fix support for InvokeResponse if we can fix the generated response type parsing while not breaking 1.0 docs functionality
    # maybe we need a discriminator field in the response model or something?
    assert isinstance(result, Response)

    response_data = invoke_response_data()
    assert result.text == response_data["text"]
    assert result.status == response_data["status"]
    assert result.trace_metadata.id == response_data["trace_metadata"]["id"]

    for key in ["action_result", "stage_metadata", "metric_results", "ruleset_results", "api_version"]:
        assert key in result.additional_properties
        assert result.additional_properties[key] == response_data[key]


@patch("galileo.protect.invoke_v2_protect_invoke_post.sync")
def test_invoke_api_validation_error(mock_invoke_post_sync: Mock):
    error_detail_item = {"loc": ["body", "payload", "input"], "msg": "Field required", "type": "missing"}
    validation_error = HTTPValidationError(detail=[error_detail_item])
    mock_invoke_post_sync.return_value = validation_error

    payload = Payload(input_="Test input")

    result = invoke(payload=payload)
    assert isinstance(result, HTTPValidationError)
    assert result.detail[0]["msg"] == "Field required"  # Corrected to use dictionary access

    mock_invoke_post_sync.reset_mock()
    mock_invoke_post_sync.return_value = validation_error

    class_method_result = Protect().invoke(payload=payload)
    assert isinstance(class_method_result, HTTPValidationError)
    assert class_method_result.detail[0]["msg"] == "Field required"  # Corrected to use dictionary access
