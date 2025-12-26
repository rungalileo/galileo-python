from typing import Optional
from unittest.mock import ANY, AsyncMock, Mock, patch
from uuid import uuid4

from pytest import mark

from galileo.handlers.langchain.tool import ProtectTool
from galileo.protect import Protect, ainvoke_protect, invoke_protect
from galileo.resources.models.execution_status import ExecutionStatus as APIExecutionStatus
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.protect_request import ProtectRequest as APIRequest
from galileo.resources.models.protect_response import ProtectResponse as APIResponse
from galileo.resources.models.validation_error import ValidationError
from galileo_core.schemas.protect.execution_status import ExecutionStatus
from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.request import Request
from galileo_core.schemas.protect.response import Response
from galileo_core.schemas.protect.rule import Rule, RuleOperator
from galileo_core.schemas.protect.ruleset import Ruleset

A_PROJECT_NAME = "project_name"
A_STAGE_NAME = "stage_name"
A_PROTECT_INPUT = "invoke"


def invoke_response_data() -> dict:
    return {
        "action_result": {"action": "PASSTHROUGH"},
        "stage_metadata": {"stage_id": "stage-uuid-example", "stage_name": "test-stage-example"},
        "text": "Original text from payload",
        "trace_metadata": {
            "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
            "received_at": 1234567890,
            "response_at": 1234567990,
            "execution_time": 100.0,
        },
        "status": ExecutionStatus.not_triggered.upper(),
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
                        "status": ExecutionStatus.not_triggered.upper(),
                        "conditions_results": [],
                    }
                ],
                "status": ExecutionStatus.not_triggered.upper(),
            }
        ],
        "api_version": "1.0.0",
        "headers": {"X-Custom-Header": "TestValue"},
        "metadata": {"request_source": "sdk_test"},
    }


def invoke_response() -> APIResponse:
    return APIResponse.from_dict(invoke_response_data())


@mark.parametrize(
    ("include_project_id", "include_project_name", "include_stage_name", "include_stage_id"),
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
        Payload(input=A_PROTECT_INPUT),
        Payload(output=A_PROTECT_INPUT),
        Payload(input=A_PROTECT_INPUT, output=A_PROTECT_INPUT),
    ],
)
@mark.parametrize("timeout", [5, 60])
@mark.parametrize("metadata", [None, {"key": "value"}])
@mark.parametrize("headers", [None, {"key": "value"}])
@mark.parametrize("stage_version", [None, 1, 2])
@patch("galileo.protect.invoke_protect_invoke_post.asyncio", new_callable=AsyncMock)
class TestAInvoke:
    @mark.asyncio
    async def test_ainvoke_success(
        self,
        mock_invoke_post_async: AsyncMock,
        include_project_id: bool,
        include_project_name: bool,
        include_stage_name: bool,
        include_stage_id: bool,
        payload: Payload,
        timeout: float,
        metadata: dict,
        headers: dict,
        stage_version: Optional[int],
    ) -> None:
        mock_invoke_post_async.return_value = invoke_response()

        current_project_id = uuid4() if include_project_id else None
        current_project_name = A_PROJECT_NAME if include_project_name else None
        current_stage_id = uuid4() if include_stage_id else None
        current_stage_name = A_STAGE_NAME if include_stage_name else None

        result = await ainvoke_protect(
            payload=payload,
            prioritized_rulesets=None,
            project_id=current_project_id,
            project_name=current_project_name,
            stage_id=current_stage_id,
            stage_name=current_stage_name,
            stage_version=stage_version,
            timeout=timeout,
            metadata=metadata,
            headers=headers,
        )

        expected_project_id = str(current_project_id) if current_project_id else None
        expected_stage_id = str(current_stage_id) if current_stage_id else None

        body = Request(
            payload=payload,
            prioritized_rulesets=[],
            project_id=expected_project_id,
            project_name=current_project_name,
            stage_id=expected_stage_id,
            stage_name=current_stage_name,
            stage_version=stage_version,
            timeout=timeout,
            metadata=metadata,
            headers=headers,
        )

        body_dict = body.model_dump(mode="json")
        body_dict["prioritized_rulesets"] = body_dict.pop("rulesets", [])
        expected_body = APIRequest.from_dict(body_dict)

        mock_invoke_post_async.assert_called_once_with(client=ANY, body=expected_body)

        assert isinstance(result, Response)

        response_data = invoke_response_data()
        assert result.text == response_data["text"]
        assert result.status == response_data["status"].lower()
        assert str(result.trace_metadata.id) == response_data["trace_metadata"]["id"]

        for key in ["action_result", "stage_metadata", "metric_results", "ruleset_results", "api_version"]:
            assert key in result.model_extra
            assert result.model_extra[key] == response_data[key]


@mark.parametrize(
    ("include_project_id", "include_project_name", "include_stage_name", "include_stage_id"),
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
        Payload(input=A_PROTECT_INPUT),
        Payload(output=A_PROTECT_INPUT),
        Payload(input=A_PROTECT_INPUT, output=A_PROTECT_INPUT),
    ],
)
@mark.parametrize("timeout", [5, 60])
@mark.parametrize("metadata", [None, {"key": "value"}])
@mark.parametrize("headers", [None, {"key": "value"}])
@mark.parametrize("stage_version", [None, 1, 2])
class TestInvoke:
    @patch("galileo.protect.ainvoke_protect")
    def test_invoke_success(
        self,
        mock_ainvoke_protect: Mock,
        include_project_id: bool,
        include_project_name: bool,
        include_stage_name: bool,
        include_stage_id: bool,
        payload: Payload,
        timeout: float,
        metadata: dict,
        headers: dict,
        stage_version: Optional[int],
    ) -> None:
        with patch("galileo.protect.async_run") as mock_async_run:
            project_id = uuid4() if include_project_id else None
            project_name = A_PROJECT_NAME if include_project_name else None
            stage_id = uuid4() if include_stage_id else None
            stage_name = A_STAGE_NAME if include_stage_name else None

            invoke_protect(
                payload=payload,
                prioritized_rulesets=None,
                project_id=project_id,
                project_name=project_name,
                stage_id=stage_id,
                stage_name=stage_name,
                stage_version=stage_version,
                timeout=timeout,
                metadata=metadata,
                headers=headers,
            )
            mock_async_run.assert_called_once()
            mock_ainvoke_protect.assert_called_once_with(
                payload=payload,
                prioritized_rulesets=None,
                project_id=project_id,
                project_name=project_name,
                stage_id=stage_id,
                stage_name=stage_name,
                stage_version=stage_version,
                timeout=timeout,
                metadata=metadata,
                headers=headers,
            )

    @patch("galileo.protect.invoke_protect_invoke_post.asyncio", new_callable=AsyncMock)
    @mark.asyncio
    async def test_langchain_tool(
        self,
        mock_invoke_post_async: AsyncMock,
        include_project_id: bool,
        include_project_name: bool,
        include_stage_name: bool,
        include_stage_id: bool,
        payload: Payload,
        rulesets: list[Ruleset],
        timeout: float,
        metadata: dict,
        headers: dict,
        stage_version: Optional[int],
    ) -> None:
        mock_invoke_post_async.return_value = invoke_response()

        current_project_id = uuid4() if include_project_id else None
        current_project_name = A_PROJECT_NAME if include_project_name else None
        current_stage_id = uuid4() if include_stage_id else None
        current_stage_name = A_STAGE_NAME if include_stage_name else None

        tool = ProtectTool(
            prioritized_rulesets=rulesets,
            project_id=current_project_id,
            project_name=current_project_name,
            stage_id=current_stage_id,
            stage_name=current_stage_name,
            timeout=timeout,
            stage_version=stage_version,
            # Metadata and headers are not used by the tool since they conflict with the
            # langchain_core tool interface.
            # metadata=metadata,
            # headers=headers,
        )
        response_json = tool.run(payload.model_dump())
        assert isinstance(response_json, str)
        response = Response.model_validate_json(response_json)
        assert response.text is not None
        assert response.status == ExecutionStatus.not_triggered
        assert mock_invoke_post_async.call_count == 1

        response_json = await tool.arun(payload.model_dump())
        assert isinstance(response_json, str)
        response = Response.model_validate_json(response_json)
        assert response.text is not None
        assert response.status == ExecutionStatus.not_triggered
        assert mock_invoke_post_async.call_count == 2


@patch("galileo.protect.invoke_protect_invoke_post.asyncio", new_callable=AsyncMock)
@mark.asyncio
async def test_invoke_with_rulesets(mock_invoke_post_async: Mock) -> None:
    mock_invoke_post_async.return_value = invoke_response()

    rules = [Rule(metric="m1", operator=RuleOperator.eq, target_value="v1")]
    rulesets = [Ruleset(rules=rules)]

    await ainvoke_protect(payload=Payload(input="test input"), prioritized_rulesets=rulesets, stage_id=uuid4())

    mock_invoke_post_async.assert_called_once()
    api_call_args = mock_invoke_post_async.call_args.kwargs
    body = api_call_args["body"]

    assert len(body.prioritized_rulesets) == 1
    api_ruleset = body.prioritized_rulesets[0]

    for i, api_rule in enumerate(api_ruleset.rules):
        expected_rule = rules[i]
        assert api_rule.metric == expected_rule.metric
        assert api_rule.operator.lower() == expected_rule.operator.value.lower()
        assert api_rule.target_value == expected_rule.target_value
    assert "rulesets" not in body.additional_properties


@patch("galileo.protect.invoke_protect_invoke_post.asyncio", new_callable=AsyncMock)
@mark.asyncio
async def test_invoke_api_validation_error(mock_invoke_post_async: Mock) -> None:
    error_detail_item = {"loc": ["body", "payload", "input"], "msg": "Field required", "type": "missing"}
    validation_error = HTTPValidationError(detail=[error_detail_item])
    mock_invoke_post_async.return_value = validation_error

    payload = Payload(input="Test input")

    result = await ainvoke_protect(payload=payload, stage_id=uuid4())
    assert isinstance(result, HTTPValidationError)
    assert result.detail[0]["msg"] == "Field required"

    mock_invoke_post_async.reset_mock()
    mock_invoke_post_async.return_value = validation_error

    class_method_result = await Protect().ainvoke(payload=payload, stage_id=uuid4())
    assert isinstance(class_method_result, HTTPValidationError)
    assert class_method_result.detail[0]["msg"] == "Field required"


@mark.parametrize(
    ("status", "expected"),
    [
        ("not_triggered", "not_triggered"),
        # ("NOT_TRIGGERED", "not_triggered"),
        ("Not_Triggered", "not_triggered"),
        ("NoT_TRiGgErEd", "not_triggered"),
        ("triggered", "triggered"),
        ("TRIGGERED", "triggered"),
    ],
)
def test_execution_status_case_insensitive(status: str, expected: str) -> None:
    """
    Tests that APIExecutionStatus can be initialized
    with strings of various casings.
    """
    parsed_status = APIExecutionStatus(status)
    assert parsed_status.value == expected


def test_string_http_validation_error() -> None:
    """
    Tests that HTTPValidationError correctly parses a 'detail' field
    that is a simple string.
    """
    error_message = "A simple error message from API."
    error_dict = {
        "detail": [{"msg": error_message, "type": "string", "loc": ["api"]}],
        "additional_properties": {"key": "value"},
    }

    validation_error = HTTPValidationError.from_dict(error_dict)

    assert isinstance(validation_error, HTTPValidationError)
    assert len(validation_error.detail) == 1
    assert len(validation_error.additional_properties) == 1
    detail_item = validation_error.detail[0]

    assert isinstance(detail_item, ValidationError)
    assert detail_item.loc == ["api"]
    assert detail_item.msg == error_message
    assert detail_item.type_ == "string"
