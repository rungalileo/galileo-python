from unittest.mock import Mock, patch
from uuid import uuid4

from pytest import mark

from galileo.protect import Protect, invoke
from galileo.resources.models.execution_status import ExecutionStatus

# from galileo.resources.models.invoke_response import InvokeRespons
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.payload import Payload
from galileo.resources.models.response import Response
from galileo.resources.models.ruleset import Ruleset

A_PROJECT_NAME = "project_name"
A_STAGE_NAME = "stage_name"
A_PROTECT_INPUT = "invoke"


# def invoke_response_data() -> dict:
#     return {
#         "action_result": {"action": "PASSTHROUGH", "modified_text": None, "details": None, "error": None},
#         "stage_metadata": {"stage_id": "stage-uuid-example", "stage_name": "test-stage-example", "ruleset_id": None, "ruleset_name": None, "version": None},
#         "text": "Original text from payload",
#         "trace_metadata": {"id": "trace-uuid-example", "received_at": 1234567890, "response_at": 1234567990, "execution_time": 100.0},
#         "status": ExecutionStatus.NOT_TRIGGERED,
#         "metric_results": {"sentiment_score": 0.95, "toxicity_level": 0.1},
#         "ruleset_results": [
#             {
#                 "ruleset_id": "ruleset-uuid-example",
#                 "ruleset_name": "basic-ruleset",
#                 "action_result": {"action": "PASSTHROUGH", "modified_text": None, "details": None, "error": None},
#                 "rule_results": [
#                     {
#                         "rule_id": "rule-uuid-example",
#                         "rule_name": "check-sentiment",
#                         "action_result": {"action": "PASSTHROUGH", "modified_text": None, "details": None, "error": None},
#                         "metric_results": {"sentiment_score": 0.95},
#                         "status": "NOT_TRIGGERED",
#                         "conditions_results": [],
#                         "error": None
#                     }
#                 ],
#                 "status": "NOT_TRIGGERED",
#                 "error": None
#             }
#         ],
#         "api_version": "1.0.0",
#         "headers": {"X-Custom-Header": "TestValue"},
#         "metadata": {"request_source": "sdk_test"},
#     }


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
@patch("galileo.protect.invoke_protect_invoke_post.sync")
def test_invoke_succeess(
    mock_invoke_post_sync: Mock,
    include_project_id: bool,
    include_project_name: bool,
    include_stage_name: bool,
    include_stage_id: bool,
    payload: Payload,
    rulesets: list[Ruleset],
    timeout: float,
    metadata: dict,
    headers: dict,
) -> None:
    mock_invoke_post_sync.return_value = invoke_response()

    # payload = Payload(input_="Test input for invoke")

    result = invoke(
        # payload=payload,
        # project_id=project_id,
        # stage_name=stage_name
        payload=payload,
        prioritized_rulesets=rulesets,
        project_id=uuid4() if include_project_id else None,
        stage_name=A_STAGE_NAME if include_stage_name else None,
        stage_id=uuid4() if include_stage_id else None,
        timeout=timeout,
        metadata=metadata,
        headers=headers,
    )

    # body = Request(
    #     payload=payload,
    #     prioritized_rulesets=prioritized_rulesets or [],
    #     project_id=str(project_id) if project_id is not None else None,
    #     project_name=project_name,
    #     stage_id=str(stage_id) if stage_id is not None else None,
    #     stage_name=stage_name,
    #     timeout=timeout,
    #     metadata=metadata,
    #     headers=headers,
    # )
    # mock_invoke_post_sync.assert_called_once_with(client=ANY, body=body)
    mock_invoke_post_sync.assert_called_once()

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


@patch("galileo.protect.invoke_protect_invoke_post.sync")
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
    protect_instance = Protect()
    class_method_result = protect_instance.invoke(payload=payload)
    assert isinstance(class_method_result, HTTPValidationError)
    assert class_method_result.detail[0]["msg"] == "Field required"  # Corrected to use dictionary access
