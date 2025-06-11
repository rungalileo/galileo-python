import uuid
from typing import Optional
from unittest.mock import Mock, patch

import pytest
from pydantic import UUID4

from galileo.projects import Projects  # Added for mocking
from galileo.resources.models import HTTPValidationError, Rule, RuleOperator, StageDB, StageWithRulesets
from galileo.resources.models.stage_type import StageType
from galileo.resources.types import UNSET
from galileo.stages import Stages, create_stage, get_stage  # Added get_stage


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


# --- Tests for get_stage ---


@pytest.mark.parametrize(
    "use_project_name, use_stage_name",
    [
        (False, False),  # project_id, stage_id
        (False, True),  # project_id, stage_name
        (True, False),  # project_name, stage_id
        (True, True),  # project_name, stage_name
    ],
)
@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
@patch("galileo.stages.Projects")  # Patch the Projects class used in stages.py
def test_get_stage_success(
    mock_projects_class: Mock,  # Mock for the Projects class itself
    mock_get_stage_api_sync: Mock,  # Mock for the stage API client
    use_project_name: bool,
    use_stage_name: bool,
):
    fixed_project_id = uuid.uuid4()
    fixed_project_name = "Test Project"
    fixed_stage_id = uuid.uuid4()
    fixed_stage_name = "Test Stage"

    # Setup mock for Projects(...).get(...)
    # The Stages class will instantiate Projects, so we mock the class,
    # then configure the get method on its return_value (the mock instance)
    mock_project_instance = Mock(spec=Projects)  # This is what Projects() will return
    mock_projects_class.return_value = mock_project_instance

    mock_project_data = Mock()  # This is what Projects().get() will return
    mock_project_data.id = fixed_project_id
    mock_project_instance.get.return_value = mock_project_data

    # Setup mock for the stage API call
    expected_stage_db = mock_stage_db_instance(
        project_id=fixed_project_id,
        name=fixed_stage_name,
        stage_type_val=StageType.LOCAL.value,  # Example value
        paused=False,  # Example value
        description="Fetched stage",  # Example value
    )
    mock_get_stage_api_sync.return_value = expected_stage_db

    call_kwargs = {}
    if use_project_name:
        call_kwargs["project_name"] = fixed_project_name
    else:
        call_kwargs["project_id"] = fixed_project_id

    if use_stage_name:
        call_kwargs["stage_name"] = fixed_stage_name
    else:
        call_kwargs["stage_id"] = fixed_stage_id

    # Test with Stages().get()
    stages_instance = Stages()  # This will use the mocked Projects class
    result_class_method = stages_instance.get(**call_kwargs)

    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=fixed_project_name)
        # Ensure the client from stages_instance was passed to Projects constructor
        mock_projects_class.assert_called_with(client=stages_instance.client)
    else:
        mock_project_instance.get.assert_not_called()
        # Projects class might still be instantiated if project_id is given,
        # but its .get() method shouldn't be called for name lookup.
        # If Stages always instantiates Projects, this check might need adjustment
        # or we ensure Projects() is only called if project_name is present.
        # Based on current stages.py, Projects() is only called if project_name is used.

    mock_get_stage_api_sync.assert_called_once()
    api_call_args = mock_get_stage_api_sync.call_args.kwargs
    assert api_call_args["project_id"] == str(fixed_project_id)
    assert api_call_args["stage_id"] == (str(fixed_stage_id) if not use_stage_name else UNSET)
    assert api_call_args["stage_name"] == (fixed_stage_name if use_stage_name else UNSET)
    assert api_call_args["client"] == stages_instance.client

    assert isinstance(result_class_method, StageDB)
    assert result_class_method.project_id == str(fixed_project_id)
    assert result_class_method.name == fixed_stage_name

    # Reset mocks for top-level function call
    mock_projects_class.reset_mock()
    mock_project_instance.reset_mock()  # Reset the instance's call counts etc.
    mock_get_stage_api_sync.reset_mock()

    # Re-configure mocks for the new Stages() instance inside get_stage()
    mock_projects_class.return_value = mock_project_instance
    mock_project_instance.get.return_value = mock_project_data
    mock_get_stage_api_sync.return_value = expected_stage_db

    # Test with top-level get_stage()
    result_func = get_stage(**call_kwargs)

    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=fixed_project_name)
        # Check that Projects was instantiated with a client by the internal Stages()
        # This requires knowing how Stages instantiates Projects.
        # For now, assume it passes its client.
        # The first arg to mock_projects_class.call_args is the Stages instance client
        assert mock_projects_class.call_args.kwargs["client"] is not None

    else:
        mock_project_instance.get.assert_not_called()

    mock_get_stage_api_sync.assert_called_once()
    api_call_args_func = mock_get_stage_api_sync.call_args.kwargs
    assert api_call_args_func["project_id"] == str(fixed_project_id)
    assert api_call_args_func["stage_id"] == (str(fixed_stage_id) if not use_stage_name else UNSET)
    assert api_call_args_func["stage_name"] == (fixed_stage_name if use_stage_name else UNSET)
    # Client for API call comes from the internal Stages() instance.

    assert isinstance(result_func, StageDB)
    assert result_func.project_id == str(fixed_project_id)
    assert result_func.name == fixed_stage_name


@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
@patch("galileo.stages.Projects")
def test_get_stage_api_validation_error(mock_projects_class: Mock, mock_get_stage_api_sync: Mock):
    test_project_id = uuid.uuid4()
    test_stage_id = uuid.uuid4()  # Used when calling with project_id

    error_detail = [{"loc": ["query", "stage_name"], "msg": "invalid name", "type": "value_error"}]
    validation_error = HTTPValidationError(detail=error_detail)
    mock_get_stage_api_sync.return_value = validation_error

    # Configure Projects mock even if not always used, to be safe
    mock_project_instance = Mock(spec=Projects)
    mock_projects_class.return_value = mock_project_instance
    mock_project_data = Mock()
    mock_project_data.id = test_project_id  # Ensure it resolves to the test_project_id if called
    mock_project_instance.get.return_value = mock_project_data

    # Test with Stages().get() - using project_id and stage_id
    result_class_method = Stages().get(project_id=test_project_id, stage_id=test_stage_id)
    assert isinstance(result_class_method, HTTPValidationError)
    assert result_class_method.detail == error_detail
    mock_get_stage_api_sync.assert_called_once()  # Ensure API was called
    mock_project_instance.get.assert_not_called()  # Project name lookup not used

    # Reset and test with top-level get_stage()
    mock_get_stage_api_sync.reset_mock()
    mock_projects_class.reset_mock()  # Reset class mock
    mock_project_instance.reset_mock()  # Reset instance mock

    # Reconfigure mocks
    mock_get_stage_api_sync.return_value = validation_error
    mock_projects_class.return_value = mock_project_instance  # Re-assign mock instance
    mock_project_instance.get.return_value = mock_project_data  # Re-assign project data

    result_func = get_stage(project_id=test_project_id, stage_id=test_stage_id)
    assert isinstance(result_func, HTTPValidationError)
    assert result_func.detail == error_detail
    mock_get_stage_api_sync.assert_called_once()
    mock_project_instance.get.assert_not_called()

    # Test with project_name (should still hit the API validation error)
    mock_get_stage_api_sync.reset_mock()
    mock_projects_class.reset_mock()
    mock_project_instance.reset_mock()

    mock_get_stage_api_sync.return_value = validation_error
    mock_projects_class.return_value = mock_project_instance
    mock_project_instance.get.return_value = mock_project_data  # Project lookup succeeds

    result_func_proj_name = get_stage(project_name="Test Project", stage_name="Invalid Stage")
    assert isinstance(result_func_proj_name, HTTPValidationError)
    assert result_func_proj_name.detail == error_detail
    mock_project_instance.get.assert_called_once_with(name="Test Project")  # Project lookup used
    mock_get_stage_api_sync.assert_called_once()  # API was called
