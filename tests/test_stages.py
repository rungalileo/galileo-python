import uuid
from typing import Optional
from unittest.mock import ANY, Mock, patch

import pytest
from pydantic import UUID4

from galileo.projects import Projects
from galileo.resources.models import HTTPValidationError, Rule, RuleOperator, RulesetsMixin, StageDB, StageWithRulesets
from galileo.resources.models.stage_type import StageType
from galileo.resources.types import UNSET
from galileo.stages import create_stage, get_stage, pause_stage, resume_stage, update_stage


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
        "type": stage_type_val,
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


@pytest.mark.parametrize("name", [None, "my stage"])
@pytest.mark.parametrize(
    "stage_type, expected_stage_type_val", [(None, StageType.LOCAL.value), (StageType.CENTRAL, StageType.CENTRAL.value)]
)
@pytest.mark.parametrize("paused", [True, False])
@pytest.mark.parametrize("rulesets", [None, [Rule(metric="metric", operator=RuleOperator.EQ, target_value="target")]])
@pytest.mark.parametrize("description", [None, "my description"])
@patch("galileo.stages.create_stage_v2_projects_project_id_stages_post.sync")
@patch("galileo.stages.ts_name")
def test_create_stage_success(
    mock_ts_name: Mock,
    mock_api_sync: Mock,
    name: Optional[str],
    stage_type: Optional[StageType],
    expected_stage_type_val: str,
    paused: bool,
    rulesets: Optional[list[Rule]],
    description: Optional[str],
):
    test_project_id = uuid.uuid4()
    default_ts_name = "stage_default_ts_name"
    mock_ts_name.return_value = default_ts_name

    effective_name = name or default_ts_name

    mock_api_sync.return_value = mock_stage_db_instance(
        project_id=test_project_id,
        name=effective_name,
        stage_type_val=expected_stage_type_val,
        paused=paused,
        description=description,
    )

    # create stage
    args = {"project_id": test_project_id, "pause": paused}
    if name is not None:
        args["name"] = name
    if stage_type is not None:
        args["stage_type"] = stage_type
    if rulesets is not None:
        args["rulesets"] = rulesets
    if description is not None:
        args["description"] = description

    result = create_stage(**args)

    mock_api_sync.assert_called_once()
    call_args = mock_api_sync.call_args
    assert call_args.kwargs["project_id"] == str(test_project_id)

    # assert payload
    payload_sent: StageWithRulesets = call_args.kwargs["body"]
    assert isinstance(payload_sent.name, str)
    if name:
        assert payload_sent.name == name
    else:
        assert payload_sent.name == default_ts_name
        mock_ts_name.assert_called_once_with("stage")

    assert payload_sent.project_id == str(test_project_id)
    assert payload_sent.type_ == expected_stage_type_val
    assert payload_sent.paused == paused
    if description is None:
        assert payload_sent.description is UNSET
    else:
        assert payload_sent.description == description
    if rulesets is None:
        assert payload_sent.prioritized_rulesets is UNSET
    else:
        assert payload_sent.prioritized_rulesets == rulesets

    # assert result
    assert isinstance(result, StageDB)
    assert result.id is not None
    assert result.name == effective_name
    assert result.project_id == str(test_project_id)
    assert result.type_ == expected_stage_type_val
    assert result.paused == paused
    if description is None:
        assert result.description is UNSET
    else:
        assert result.description == description


@patch("galileo.stages.create_stage_v2_projects_project_id_stages_post.sync")
def test_create_stage_api_validation_error(mock_api_sync: Mock):
    test_project_id = uuid.uuid4()
    error_detail = [{"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"}]
    validation_error = HTTPValidationError(detail=error_detail)
    mock_api_sync.return_value = validation_error

    # Test with top-level create_stage
    # The direct test of Stages().create() is removed.
    # The call to create_stage() below will instantiate Stages and call its create method.
    result_func = create_stage(project_id=test_project_id, name="test")
    assert isinstance(result_func, HTTPValidationError)
    assert result_func.detail == error_detail
    # We expect the mock_api_sync to have been called once by the create_stage function.
    # If it was reset and called again, this would fail, ensuring we're not double-calling.
    mock_api_sync.assert_called_once()


@pytest.mark.parametrize(
    "use_project_name, use_stage_name", [(False, False), (False, True), (True, False), (True, True)]
)
@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
@patch("galileo.stages.Projects")
def test_get_stage_success(  # Renamed to test_top_level_get_stage_success if we want to be explicit, but not required by user
    mock_projects_class: Mock, mock_get_stage_api_sync: Mock, use_project_name: bool, use_stage_name: bool
):
    fixed_project_id = uuid.uuid4()
    fixed_project_name = "Test Project"
    fixed_stage_id = uuid.uuid4()
    fixed_stage_name = "Test Stage"

    # Setup mock for Projects(...).get(...) for when project_name is used
    mock_project_instance = Mock(spec=Projects)
    mock_projects_class.return_value = mock_project_instance

    mock_project_data = Mock()
    mock_project_data.id = fixed_project_id
    mock_project_instance.get.return_value = mock_project_data

    # Setup mock for the stage API call (get_stage_projects_project_id_stages_get.sync)
    expected_stage_db = mock_stage_db_instance(
        project_id=fixed_project_id,
        name=fixed_stage_name,
        stage_type_val=StageType.LOCAL.value,
        paused=False,
        description="Fetched stage",
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

    # Test with top-level get_stage()
    # The direct test of Stages().get() is removed as per the plan.
    result_func = get_stage(**call_kwargs)

    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=fixed_project_name)
        # Ensure Projects class was instantiated by the get_stage function (which creates a Stages instance)
        mock_projects_class.assert_called_once()
        assert mock_projects_class.call_args.kwargs["client"] is not None
    else:
        mock_project_instance.get.assert_not_called()
        # Projects class might still be instantiated by Stages() even if project_id is given,
        # but its .get() method for name lookup shouldn't be called.
        # If Stages always instantiates Projects, mock_projects_class might have been called.
        # If Stages only instantiates Projects if project_name is used, then it wouldn't be called here.
        # Based on stages.py _get_project_id, Projects() is only called if project_name is used.
        # So, if not use_project_name, mock_projects_class should not have been called for name lookup.
        # However, Stages() itself is always instantiated by get_stage().
        # The mock_projects_class.assert_called_once() above for the use_project_name case is sufficient.

    mock_get_stage_api_sync.assert_called_once()
    api_call_args_func = mock_get_stage_api_sync.call_args.kwargs
    assert api_call_args_func["project_id"] == str(fixed_project_id)
    assert api_call_args_func["stage_id"] == (str(fixed_stage_id) if not use_stage_name else UNSET)
    assert api_call_args_func["stage_name"] == (fixed_stage_name if use_stage_name else UNSET)
    # Client for API call comes from the internal Stages() instance created by get_stage()
    assert api_call_args_func["client"] is not None

    assert isinstance(result_func, StageDB)
    assert result_func.project_id == str(fixed_project_id)
    assert result_func.name == fixed_stage_name


@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
@patch("galileo.stages.Projects")
def test_get_stage_api_validation_error(mock_projects_class: Mock, mock_get_stage_api_sync: Mock):
    test_project_id = uuid.uuid4()
    test_stage_id = uuid.uuid4()

    error_detail = [{"loc": ["query", "stage_name"], "msg": "invalid name", "type": "value_error"}]
    validation_error = HTTPValidationError(detail=error_detail)

    # Configure Projects mock for scenarios where project_name is used
    mock_project_instance = Mock(spec=Projects)
    mock_projects_class.return_value = mock_project_instance
    mock_project_data = Mock()
    mock_project_data.id = test_project_id
    mock_project_instance.get.return_value = mock_project_data

    # Scenario 1: Test with top-level get_stage() using project_id and stage_id
    mock_get_stage_api_sync.return_value = validation_error  # API call returns error

    result_func_ids = get_stage(project_id=test_project_id, stage_id=test_stage_id)
    assert isinstance(result_func_ids, HTTPValidationError)
    assert result_func_ids.detail == error_detail
    mock_get_stage_api_sync.assert_called_once_with(
        project_id=str(test_project_id), stage_id=str(test_stage_id), stage_name=UNSET, client=ANY
    )
    mock_project_instance.get.assert_not_called()  # Project name lookup not used

    # Reset mocks for the next scenario
    mock_get_stage_api_sync.reset_mock()
    mock_projects_class.reset_mock()
    mock_project_instance.reset_mock()

    # Reconfigure Projects mock for the project_name scenario
    mock_projects_class.return_value = mock_project_instance
    mock_project_instance.get.return_value = mock_project_data

    # Scenario 2: Test with top-level get_stage() using project_name and stage_name
    mock_get_stage_api_sync.return_value = validation_error  # API call returns error

    result_func_names = get_stage(project_name="Test Project", stage_name="Invalid Stage")
    assert isinstance(result_func_names, HTTPValidationError)
    assert result_func_names.detail == error_detail

    # Ensure project name lookup happened
    mock_project_instance.get.assert_called_once_with(name="Test Project")
    # Ensure API was called with resolved project_id and provided stage_name
    mock_get_stage_api_sync.assert_called_once_with(
        project_id=str(test_project_id),  # Resolved from project_name
        stage_name="Invalid Stage",
        stage_id=UNSET,
        client=ANY,
    )


@pytest.mark.parametrize(
    "use_project_name, use_stage_name",
    [
        (False, False),  # project_id, stage_id
        (False, True),  # project_id, stage_name
        (True, False),  # project_name, stage_id
        (True, True),  # project_name, stage_name
    ],
)
@patch("galileo.stages.update_stage_projects_project_id_stages_stage_id_post.sync")
@patch("galileo.stages.Stages.get")
@patch("galileo.stages.Projects")
def test_update_stage_success(
    mock_projects_class: Mock,
    mock_stages_get: Mock,  # This mock targets Stages.get, used by update_stage internally
    mock_update_stage_api_sync: Mock,
    use_project_name: bool,
    use_stage_name: bool,
):
    fixed_project_id = uuid.uuid4()
    fixed_project_name = "Test Project Update"
    fixed_stage_id = uuid.uuid4()
    fixed_stage_name = "Test Stage Update"

    input_rulesets = [Rule(metric="test_metric", operator=RuleOperator.GTE, target_value=10.0)]

    # Mock for Projects().get() - used by _get_project_id if project_name is given
    mock_project_instance = Mock(spec=Projects)
    mock_projects_class.return_value = mock_project_instance
    mock_project_data = Mock()
    mock_project_data.id = fixed_project_id
    mock_project_instance.get.return_value = mock_project_data

    # Mock for Stages().get() - used by _get_stage_id if stage_name is given
    # This mock is for the Stages.get method itself, which is called by the Stages instance
    # created within the top-level update_stage function.
    mock_stage_data_for_get = mock_stage_db_instance(
        project_id=fixed_project_id, name=fixed_stage_name, stage_type_val="local", paused=False
    )
    mock_stage_data_for_get.id = fixed_stage_id  # Ensure it resolves to the correct ID
    mock_stages_get.return_value = mock_stage_data_for_get

    # Mock for the actual update API call (update_stage_projects_project_id_stages_stage_id_post.sync)
    expected_updated_stage_db = mock_stage_db_instance(
        project_id=fixed_project_id,
        name=fixed_stage_name,
        stage_type_val=StageType.LOCAL.value,
        paused=False,
        description="Updated stage",
        version=2,
    )
    mock_update_stage_api_sync.return_value = expected_updated_stage_db

    call_kwargs = {"prioritized_rulesets": input_rulesets}
    if use_project_name:
        call_kwargs["project_name"] = fixed_project_name
    else:
        call_kwargs["project_id"] = fixed_project_id

    if use_stage_name:
        call_kwargs["stage_name"] = fixed_stage_name
    else:
        call_kwargs["stage_id"] = fixed_stage_id

    # Test with top-level update_stage()
    # The direct test of Stages().update() is removed.
    result_func = update_stage(**call_kwargs)

    # Assertions for mocks called by the top-level update_stage path
    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=fixed_project_name)
        # Check that Projects was instantiated by the internal Stages()
        mock_projects_class.assert_called_once()
        assert mock_projects_class.call_args.kwargs["client"] is not None
    else:
        mock_project_instance.get.assert_not_called()

    if use_stage_name:
        # Stages.get (mock_stages_get) should have been called by the internal _get_stage_id
        mock_stages_get.assert_called_once_with(project_id=str(fixed_project_id), stage_name=fixed_stage_name)
    else:
        mock_stages_get.assert_not_called()

    mock_update_stage_api_sync.assert_called_once()
    api_call_args_func = mock_update_stage_api_sync.call_args.kwargs
    assert api_call_args_func["project_id"] == str(fixed_project_id)
    assert api_call_args_func["stage_id"] == str(fixed_stage_id)  # Resolved ID
    assert isinstance(api_call_args_func["body"], RulesetsMixin)
    assert api_call_args_func["body"].prioritized_rulesets == input_rulesets
    assert api_call_args_func["client"] is not None  # Client from internal Stages() instance

    assert isinstance(result_func, StageDB)
    assert result_func.version == 2


@patch("galileo.stages.update_stage_projects_project_id_stages_stage_id_post.sync")
@patch("galileo.stages.Stages.get")
@patch("galileo.stages.Projects")
def test_update_stage_api_validation_error(
    mock_projects_class: Mock, mock_stages_get: Mock, mock_update_stage_api_sync: Mock
):
    test_project_id = uuid.uuid4()
    test_stage_id = uuid.uuid4()
    input_rulesets = [Rule(metric="test_metric", operator=RuleOperator.GTE, target_value=10.0)]

    error_detail = [{"loc": ["body", "prioritized_rulesets"], "msg": "invalid ruleset", "type": "value_error"}]
    validation_error = HTTPValidationError(detail=error_detail)

    # Configure Projects mock for name resolution
    mock_project_instance = Mock(spec=Projects)
    mock_projects_class.return_value = mock_project_instance
    mock_project_data = Mock()
    mock_project_data.id = test_project_id
    mock_project_instance.get.return_value = mock_project_data

    # Configure Stages.get mock for stage name resolution
    mock_stage_data_for_get = Mock()
    mock_stage_data_for_get.id = test_stage_id
    mock_stages_get.return_value = mock_stage_data_for_get

    # Scenario 1: Test with top-level update_stage() using project_id and stage_id
    mock_update_stage_api_sync.return_value = validation_error  # API call returns error

    result_func_ids = update_stage(
        project_id=test_project_id, stage_id=test_stage_id, prioritized_rulesets=input_rulesets
    )
    assert isinstance(result_func_ids, HTTPValidationError)
    assert result_func_ids.detail == error_detail

    mock_update_stage_api_sync.assert_called_once()
    api_call_args_ids = mock_update_stage_api_sync.call_args.kwargs
    assert api_call_args_ids["project_id"] == str(test_project_id)
    assert api_call_args_ids["stage_id"] == str(test_stage_id)
    assert isinstance(api_call_args_ids["body"], RulesetsMixin)
    assert api_call_args_ids["body"].prioritized_rulesets == input_rulesets

    mock_project_instance.get.assert_not_called()  # project_id provided
    mock_stages_get.assert_not_called()  # stage_id provided

    # Reset mocks for the next scenario
    mock_update_stage_api_sync.reset_mock()
    mock_projects_class.reset_mock()
    mock_project_instance.reset_mock()
    mock_stages_get.reset_mock()

    # Reconfigure mocks for name resolution
    mock_projects_class.return_value = mock_project_instance
    mock_project_instance.get.return_value = mock_project_data
    mock_stages_get.return_value = mock_stage_data_for_get
    mock_update_stage_api_sync.return_value = validation_error  # API call returns error

    # Scenario 2: Test with top-level update_stage() using project_name and stage_name
    result_func_names = update_stage(
        project_name="Test Project", stage_name="Test Stage", prioritized_rulesets=input_rulesets
    )
    assert isinstance(result_func_names, HTTPValidationError)
    assert result_func_names.detail == error_detail

    mock_project_instance.get.assert_called_once_with(name="Test Project")
    mock_stages_get.assert_called_once_with(project_id=str(test_project_id), stage_name="Test Stage")

    mock_update_stage_api_sync.assert_called_once()
    api_call_args_names = mock_update_stage_api_sync.call_args.kwargs
    assert api_call_args_names["project_id"] == str(test_project_id)  # Resolved from project_name
    assert api_call_args_names["stage_id"] == str(test_stage_id)  # Resolved from stage_name
    assert isinstance(api_call_args_names["body"], RulesetsMixin)
    assert api_call_args_names["body"].prioritized_rulesets == input_rulesets


# --- Tests for pause_stage and resume_stage ---


@pytest.mark.parametrize("pause_flag_to_set", [True, False])  # True for pause, False for resume
@pytest.mark.parametrize(
    "use_project_name, use_stage_name",
    [
        (False, False),  # project_id, stage_id
        (False, True),  # project_id, stage_name
        (True, False),  # project_name, stage_id
        (True, True),  # project_name, stage_name
    ],
)
@patch("galileo.stages.pause_stage_projects_project_id_stages_stage_id_put.sync")
@patch("galileo.stages.Stages.get")  # Mock Stages.get for stage name resolution
@patch("galileo.stages.Projects")  # Mock Projects for project name resolution
def test_set_pause_state_success(
    mock_projects_class: Mock,
    mock_stages_get: Mock,
    mock_pause_api_sync: Mock,
    pause_flag_to_set: bool,
    use_project_name: bool,
    use_stage_name: bool,
):
    fixed_project_id = uuid.uuid4()
    fixed_project_name = "Test PauseResume Project"
    fixed_stage_id = uuid.uuid4()
    fixed_stage_name = "Test PauseResume Stage"

    # Mock for Projects().get()
    mock_project_instance = Mock(spec=Projects)
    mock_projects_class.return_value = mock_project_instance
    mock_project_data = Mock()
    mock_project_data.id = fixed_project_id
    mock_project_instance.get.return_value = mock_project_data

    # Mock for Stages().get() if stage_name is used
    # Simulate the stage's current paused state as opposite of what we're setting it to
    mock_stage_data_for_get = mock_stage_db_instance(
        project_id=fixed_project_id, name=fixed_stage_name, stage_type_val="local", paused=(not pause_flag_to_set)
    )
    mock_stage_data_for_get.id = fixed_stage_id
    mock_stages_get.return_value = mock_stage_data_for_get

    # Mock for the pause/resume API call
    expected_api_result_stage_db = mock_stage_db_instance(
        project_id=fixed_project_id,
        name=fixed_stage_name,
        stage_type_val=StageType.LOCAL.value,
        paused=pause_flag_to_set,  # Expected final state
        description="Stage after pause/resume action",
    )
    mock_pause_api_sync.return_value = expected_api_result_stage_db

    call_kwargs = {}
    if use_project_name:
        call_kwargs["project_name"] = fixed_project_name
    else:
        call_kwargs["project_id"] = fixed_project_id

    if use_stage_name:
        call_kwargs["stage_name"] = fixed_stage_name
    else:
        call_kwargs["stage_id"] = fixed_stage_id

    action_func_top_level = pause_stage if pause_flag_to_set else resume_stage

    # Test with top-level pause_stage() or resume_stage()
    # The direct test of Stages().pause/resume() is removed.
    result_func = action_func_top_level(**call_kwargs)

    # Assertions for mocks called by the top-level function path
    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=fixed_project_name)
        # Ensure Projects class was instantiated by the top-level function (which creates a Stages instance)
        mock_projects_class.assert_called_once()
        assert mock_projects_class.call_args.kwargs["client"] is not None
    else:
        mock_project_instance.get.assert_not_called()

    if use_stage_name:
        mock_stages_get.assert_called_once_with(project_id=str(fixed_project_id), stage_name=fixed_stage_name)
    else:
        mock_stages_get.assert_not_called()

    mock_pause_api_sync.assert_called_once()
    api_call_args_func = mock_pause_api_sync.call_args.kwargs
    assert api_call_args_func["project_id"] == str(fixed_project_id)
    assert api_call_args_func["stage_id"] == str(fixed_stage_id)
    assert api_call_args_func["pause"] == pause_flag_to_set

    assert isinstance(result_func, StageDB)
    assert result_func.paused == pause_flag_to_set


@patch("galileo.stages.pause_stage_projects_project_id_stages_stage_id_put.sync")
@patch("galileo.stages.Stages.get")
@patch("galileo.stages.Projects")
def test_set_pause_state_api_validation_error(
    mock_projects_class: Mock, mock_stages_get: Mock, mock_pause_api_sync: Mock
):
    test_project_id = uuid.uuid4()
    test_stage_id = uuid.uuid4()

    error_detail = [{"loc": ["query", "pause"], "msg": "value could not be parsed", "type": "type_error.bool"}]
    validation_error = HTTPValidationError(detail=error_detail)

    # Configure mocks for project/stage resolution (used by _get_project_id and _get_stage_id)
    mock_project_instance = Mock(spec=Projects)
    mock_projects_class.return_value = mock_project_instance
    mock_project_data = Mock()
    mock_project_data.id = test_project_id
    mock_project_instance.get.return_value = mock_project_data

    mock_stage_data_for_get = Mock()
    mock_stage_data_for_get.id = test_stage_id
    mock_stages_get.return_value = mock_stage_data_for_get

    # Scenario 1: Test with top-level pause_stage()
    mock_pause_api_sync.return_value = validation_error  # API call returns error

    result_func_pause = pause_stage(project_id=test_project_id, stage_id=test_stage_id)
    assert isinstance(result_func_pause, HTTPValidationError)
    assert result_func_pause.detail == error_detail
    # Check that the API call was attempted with pause=True
    mock_pause_api_sync.assert_called_once_with(
        project_id=str(test_project_id),
        stage_id=str(test_stage_id),
        client=ANY,  # Client from internal Stages() instance
        pause=True,
    )
    # Ensure resolution mocks were not called if IDs were provided directly
    mock_project_instance.get.assert_not_called()
    mock_stages_get.assert_not_called()

    # Reset mocks for the next scenario
    mock_pause_api_sync.reset_mock()
    mock_projects_class.reset_mock()
    mock_project_instance.reset_mock()
    mock_stages_get.reset_mock()

    # Reconfigure mocks for name resolution if needed, and API error
    mock_projects_class.return_value = mock_project_instance
    mock_project_instance.get.return_value = mock_project_data
    mock_stages_get.return_value = mock_stage_data_for_get
    mock_pause_api_sync.return_value = validation_error  # API call returns error

    # Scenario 2: Test with top-level resume_stage()
    result_func_resume = resume_stage(project_id=test_project_id, stage_id=test_stage_id)
    assert isinstance(result_func_resume, HTTPValidationError)
    assert result_func_resume.detail == error_detail
    # Check that the API call was attempted with pause=False
    mock_pause_api_sync.assert_called_once_with(
        project_id=str(test_project_id),
        stage_id=str(test_stage_id),
        client=ANY,  # Client from internal Stages() instance
        pause=False,
    )
    mock_project_instance.get.assert_not_called()
    mock_stages_get.assert_not_called()

    # (Optional: Add scenarios testing with project_name/stage_name if desired, similar to other error tests)
