import uuid
from typing import Optional
from unittest.mock import Mock, patch

import pytest
from pydantic import UUID4

from galileo.resources.models import HTTPValidationError, Rule, RuleOperator, StageDB, StageWithRulesets
from galileo.resources.models.stage_type import StageType
from galileo.resources.types import UNSET
from galileo.stages import Stages, create_stage


def mock_stage_db_data(
    project_id: UUID4,
    name: str,
    stage_type_val: str,
    paused: bool,
    description: Optional[str] = None,
    prioritized_rulesets: Optional[list] = None,
    version: int = 1,
    created_by: str = "test_user",
) -> dict:
    data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "project_id": str(project_id),
        "type": stage_type_val,  # Corrected key from "type_" to "type"
        "paused": paused,
        "version": version,
        "created_by": created_by,
    }
    if description is not None:
        data["description"] = description
    if prioritized_rulesets is not None:
        data["prioritized_rulesets"] = prioritized_rulesets
    return data


def mock_stage_db_instance(
    project_id: UUID4,
    name: str,
    stage_type_val: str,
    paused: bool,
    description: Optional[str] = None,
    version: int = 1,
    created_by: str = "test_user",
) -> StageDB:
    return StageDB.from_dict(
        mock_stage_db_data(
            project_id=project_id,
            name=name,
            stage_type_val=stage_type_val,
            paused=paused,
            description=description,
            version=version,
            created_by=created_by,
        )
    )


@pytest.mark.parametrize("input_name, expected_name_in_payload_type", [(None, str), ("My Specific Stage", str)])
@pytest.mark.parametrize(
    "input_stage_type, expected_stage_type_val",
    [(None, StageType.LOCAL.value), (StageType.CENTRAL, StageType.CENTRAL.value)],
)
@pytest.mark.parametrize("input_pause", [True, False])
@pytest.mark.parametrize(
    "input_rulesets", [None, [Rule(metric="placeholder_metric", operator=RuleOperator.EQ, target_value="target")]]
)
@pytest.mark.parametrize("input_description", [None, "A test stage description"])
@patch("galileo.stages.create_stage_v2_projects_project_id_stages_post.sync")
@patch("galileo.stages.ts_name")
def test_create_stage_success(
    mock_ts_name: Mock,
    mock_api_sync: Mock,
    input_name: Optional[str],
    expected_name_in_payload_type: type,
    input_stage_type: Optional[StageType],
    expected_stage_type_val: str,
    input_pause: bool,
    input_rulesets: Optional[list[Rule]],
    input_description: Optional[str],
):
    test_project_id = uuid.uuid4()
    default_ts_name = "stage_default_ts_name"
    mock_ts_name.return_value = default_ts_name

    effective_name = input_name or default_ts_name

    mock_api_sync.return_value = mock_stage_db_instance(
        project_id=test_project_id,
        name=effective_name,
        stage_type_val=expected_stage_type_val,
        paused=input_pause,
        description=input_description,
    )

    args = {"project_id": test_project_id, "pause": input_pause}
    if input_name is not None:
        args["name"] = input_name
    if input_stage_type is not None:
        args["stage_type"] = input_stage_type
    if input_rulesets is not None:
        args["rulesets"] = input_rulesets
    if input_description is not None:
        args["description"] = input_description

    result = create_stage(**args)

    mock_api_sync.assert_called_once()
    call_args = mock_api_sync.call_args
    assert call_args.kwargs["project_id"] == str(test_project_id)

    payload_sent: StageWithRulesets = call_args.kwargs["body"]
    assert isinstance(payload_sent.name, expected_name_in_payload_type)
    if input_name:
        assert payload_sent.name == input_name
    else:
        assert payload_sent.name == default_ts_name  # Check ts_name was used
        mock_ts_name.assert_called_once_with("stage")

    assert payload_sent.project_id == str(test_project_id)
    assert payload_sent.type_ == expected_stage_type_val
    assert payload_sent.paused == input_pause
    if input_description is None:
        assert payload_sent.description is UNSET
    else:
        assert payload_sent.description == input_description
    if input_rulesets is None:
        assert payload_sent.prioritized_rulesets is UNSET
    else:
        assert payload_sent.prioritized_rulesets == input_rulesets

    assert isinstance(result, StageDB)
    assert result.id is not None
    assert result.name == effective_name
    assert result.project_id == str(test_project_id)
    assert result.type_ == expected_stage_type_val
    assert result.paused == input_pause
    if input_description is None:
        assert result.description is UNSET
    else:
        assert result.description == input_description


@patch("galileo.stages.create_stage_v2_projects_project_id_stages_post.sync")
def test_create_stage_api_validation_error(mock_api_sync: Mock):
    test_project_id = uuid.uuid4()
    error_detail = [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]
    validation_error = HTTPValidationError(detail=error_detail)
    mock_api_sync.return_value = validation_error

    result_class_method = Stages().create(project_id=test_project_id, name="test")
    assert isinstance(result_class_method, HTTPValidationError)
    assert result_class_method.detail == error_detail

    # Test with top-level create_stage
    mock_api_sync.reset_mock()
    mock_api_sync.return_value = validation_error

    result_func = create_stage(project_id=test_project_id, name="test")
    assert isinstance(result_func, HTTPValidationError)
    assert result_func.detail == error_detail
