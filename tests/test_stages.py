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

FIXED_PROJECT_ID_UUID = uuid.uuid4()
FIXED_PROJECT_ID_STR = str(FIXED_PROJECT_ID_UUID)
FIXED_PROJECT_NAME = "Fixture Test Project"
FIXED_STAGE_ID_UUID = uuid.uuid4()
FIXED_STAGE_ID_STR = str(FIXED_STAGE_ID_UUID)
FIXED_STAGE_NAME = "Fixture Test Stage"


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


@pytest.fixture
def mock_projects_class_with_instance():
    """Mocks galileo.stages.Projects and provides the class patch and a configured instance."""
    with patch("galileo.stages.Projects") as mock_projects_class_patch:
        mock_project_instance = Mock(spec=Projects)
        mock_projects_class_patch.return_value = mock_project_instance

        mock_project_data = Mock()
        mock_project_data.id = FIXED_PROJECT_ID_STR
        mock_project_instance.get.return_value = mock_project_data
        yield mock_projects_class_patch, mock_project_instance, FIXED_PROJECT_ID_STR


@pytest.fixture
def mock_stages_get_method():
    """Mocks the Stages.get method and provides the patch, a fixed stage ID, and project ID."""
    with patch("galileo.stages.Stages.get") as mock_stages_get_method_patch:
        mock_stage_data = mock_stage_db_instance(
            project_id=FIXED_PROJECT_ID_UUID, name=FIXED_STAGE_NAME, stage_type_val=StageType.LOCAL.value, paused=False
        )
        mock_stage_data.id = FIXED_STAGE_ID_STR
        mock_stage_data.project_id = FIXED_PROJECT_ID_STR

        mock_stages_get_method_patch.return_value = mock_stage_data
        yield mock_stages_get_method_patch, FIXED_STAGE_ID_STR, FIXED_PROJECT_ID_STR


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

    result_func = create_stage(project_id=test_project_id, name="test")
    assert isinstance(result_func, HTTPValidationError)
    assert result_func.detail == error_detail
    mock_api_sync.assert_called_once()


@pytest.mark.parametrize(
    "use_project_name, use_stage_name", [(False, False), (False, True), (True, False), (True, True)]
)
@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
def test_get_stage_success(
    mock_get_stage_api_sync: Mock, mock_projects_class_with_instance, use_project_name: bool, use_stage_name: bool
):
    mock_projects_class, mock_project_instance, _ = mock_projects_class_with_instance

    current_test_stage_id_uuid = uuid.uuid4()
    current_test_stage_id_str = str(current_test_stage_id_uuid)
    current_test_stage_name = "Local Test Stage"

    expected_stage_db = mock_stage_db_instance(
        project_id=FIXED_PROJECT_ID_UUID,
        name=current_test_stage_name,
        stage_type_val=StageType.LOCAL.value,
        paused=False,
        description="Fetched stage",
    )
    mock_get_stage_api_sync.return_value = expected_stage_db

    call_kwargs = {}
    if use_project_name:
        call_kwargs["project_name"] = FIXED_PROJECT_NAME
    else:
        call_kwargs["project_id"] = FIXED_PROJECT_ID_UUID

    if use_stage_name:
        call_kwargs["stage_name"] = current_test_stage_name
    else:
        call_kwargs["stage_id"] = current_test_stage_id_uuid

    result_func = get_stage(**call_kwargs)

    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=FIXED_PROJECT_NAME)
        mock_projects_class.assert_called_once()
        assert mock_projects_class.call_args.kwargs["client"] is not None
    else:
        mock_project_instance.get.assert_not_called()

    mock_get_stage_api_sync.assert_called_once()
    api_call_args_func = mock_get_stage_api_sync.call_args.kwargs
    assert api_call_args_func["project_id"] == FIXED_PROJECT_ID_STR
    assert api_call_args_func["stage_id"] == (current_test_stage_id_str if not use_stage_name else UNSET)
    assert api_call_args_func["stage_name"] == (current_test_stage_name if use_stage_name else UNSET)
    assert api_call_args_func["client"] is not None

    assert isinstance(result_func, StageDB)
    assert result_func.project_id == FIXED_PROJECT_ID_STR
    assert result_func.name == current_test_stage_name


@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
def test_get_stage_api_validation_error(mock_get_stage_api_sync: Mock, mock_projects_class_with_instance):
    _, mock_project_instance, fixture_project_id_str = mock_projects_class_with_instance

    local_test_stage_id_uuid = uuid.uuid4()
    local_test_stage_id_str = str(local_test_stage_id_uuid)

    error_detail = [{"loc": ["query", "stage_name"], "msg": "invalid name", "type": "value_error"}]
    validation_error = HTTPValidationError(detail=error_detail)

    mock_get_stage_api_sync.return_value = validation_error

    result_func_ids = get_stage(project_id=FIXED_PROJECT_ID_UUID, stage_id=local_test_stage_id_uuid)
    assert isinstance(result_func_ids, HTTPValidationError)
    assert result_func_ids.detail == error_detail
    mock_get_stage_api_sync.assert_called_once_with(
        project_id=FIXED_PROJECT_ID_STR, stage_id=local_test_stage_id_str, stage_name=UNSET, client=ANY
    )
    mock_project_instance.get.assert_not_called()

    mock_get_stage_api_sync.reset_mock()
    mock_project_instance.get.reset_mock()

    mock_get_stage_api_sync.return_value = validation_error

    result_func_names = get_stage(project_name=FIXED_PROJECT_NAME, stage_name="Invalid Stage For Error Test")
    assert isinstance(result_func_names, HTTPValidationError)
    assert result_func_names.detail == error_detail

    mock_project_instance.get.assert_called_once_with(name=FIXED_PROJECT_NAME)
    mock_get_stage_api_sync.assert_called_once_with(
        project_id=fixture_project_id_str, stage_name="Invalid Stage For Error Test", stage_id=UNSET, client=ANY
    )


@pytest.mark.parametrize(
    "use_project_name, use_stage_name", [(False, False), (False, True), (True, False), (True, True)]
)
@patch("galileo.stages.update_stage_projects_project_id_stages_stage_id_post.sync")
def test_update_stage_success(
    mock_update_stage_api_sync: Mock,
    mock_projects_class_with_instance,
    mock_stages_get_method,
    use_project_name: bool,
    use_stage_name: bool,
):
    mock_projects_class, mock_project_instance, resolved_project_id_str_from_projects_fixture = (
        mock_projects_class_with_instance
    )
    mock_stages_get, resolved_stage_id_str, resolved_project_id_str_from_stages_fixture = mock_stages_get_method

    assert resolved_project_id_str_from_projects_fixture == resolved_project_id_str_from_stages_fixture
    expected_api_project_id_str = resolved_project_id_str_from_projects_fixture
    expected_api_stage_id_str = resolved_stage_id_str

    input_rulesets = [Rule(metric="test_metric", operator=RuleOperator.GTE, target_value=10.0)]

    expected_updated_stage_db = mock_stage_db_instance(
        project_id=uuid.UUID(expected_api_project_id_str),
        name=FIXED_STAGE_NAME,
        stage_type_val=StageType.LOCAL.value,
        paused=False,
        description="Updated stage",
        version=2,
    )
    mock_update_stage_api_sync.return_value = expected_updated_stage_db

    call_kwargs = {"prioritized_rulesets": input_rulesets}
    if use_project_name:
        call_kwargs["project_name"] = FIXED_PROJECT_NAME
    else:
        call_kwargs["project_id"] = FIXED_PROJECT_ID_UUID

    if use_stage_name:
        call_kwargs["stage_name"] = FIXED_STAGE_NAME
    else:
        call_kwargs["stage_id"] = FIXED_STAGE_ID_UUID

    result_func = update_stage(**call_kwargs)

    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=FIXED_PROJECT_NAME)
        mock_projects_class.assert_called_once()
        assert mock_projects_class.call_args.kwargs["client"] is not None
    else:
        mock_project_instance.get.assert_not_called()

    if use_stage_name:
        mock_stages_get.assert_called_once_with(project_id=expected_api_project_id_str, stage_name=FIXED_STAGE_NAME)
    else:
        mock_stages_get.assert_not_called()

    mock_update_stage_api_sync.assert_called_once()
    api_call_args_func = mock_update_stage_api_sync.call_args.kwargs
    assert api_call_args_func["project_id"] == expected_api_project_id_str
    assert api_call_args_func["stage_id"] == expected_api_stage_id_str
    assert isinstance(api_call_args_func["body"], RulesetsMixin)
    assert api_call_args_func["body"].prioritized_rulesets == input_rulesets
    assert api_call_args_func["client"] is not None

    assert isinstance(result_func, StageDB)
    assert result_func.version == 2
    assert result_func.name == FIXED_STAGE_NAME
    assert result_func.project_id == expected_api_project_id_str


@patch("galileo.stages.update_stage_projects_project_id_stages_stage_id_post.sync")
def test_update_stage_api_validation_error(
    mock_update_stage_api_sync: Mock, mock_projects_class_with_instance, mock_stages_get_method
):
    _, mock_project_instance, fixture_project_id_str = mock_projects_class_with_instance
    mock_stages_get_patcher, fixture_stage_id_str, _ = mock_stages_get_method
    input_rulesets = [Rule(metric="test_metric", operator=RuleOperator.GTE, target_value=10.0)]
    error_detail = [{"loc": ["body", "prioritized_rulesets"], "msg": "invalid ruleset", "type": "value_error"}]
    validation_error = HTTPValidationError(detail=error_detail)

    mock_update_stage_api_sync.return_value = validation_error

    result_func_ids = update_stage(
        project_id=FIXED_PROJECT_ID_UUID, stage_id=FIXED_STAGE_ID_UUID, prioritized_rulesets=input_rulesets
    )
    assert isinstance(result_func_ids, HTTPValidationError)
    assert result_func_ids.detail == error_detail

    mock_update_stage_api_sync.assert_called_once()
    api_call_args_ids = mock_update_stage_api_sync.call_args.kwargs
    assert api_call_args_ids["project_id"] == FIXED_PROJECT_ID_STR
    assert api_call_args_ids["stage_id"] == FIXED_STAGE_ID_STR
    assert isinstance(api_call_args_ids["body"], RulesetsMixin)
    assert api_call_args_ids["body"].prioritized_rulesets == input_rulesets

    mock_project_instance.get.assert_not_called()
    mock_stages_get_patcher.assert_not_called()

    mock_update_stage_api_sync.reset_mock()
    mock_project_instance.get.reset_mock()
    mock_stages_get_patcher.reset_mock()

    mock_update_stage_api_sync.return_value = validation_error

    result_func_names = update_stage(
        project_name=FIXED_PROJECT_NAME, stage_name=FIXED_STAGE_NAME, prioritized_rulesets=input_rulesets
    )
    assert isinstance(result_func_names, HTTPValidationError)
    assert result_func_names.detail == error_detail

    mock_project_instance.get.assert_called_once_with(name=FIXED_PROJECT_NAME)
    mock_stages_get_patcher.assert_called_once_with(project_id=fixture_project_id_str, stage_name=FIXED_STAGE_NAME)

    mock_update_stage_api_sync.assert_called_once()
    api_call_args_names = mock_update_stage_api_sync.call_args.kwargs
    assert api_call_args_names["project_id"] == fixture_project_id_str
    assert api_call_args_names["stage_id"] == fixture_stage_id_str
    assert isinstance(api_call_args_names["body"], RulesetsMixin)
    assert api_call_args_names["body"].prioritized_rulesets == input_rulesets


@pytest.mark.parametrize("pause_flag_to_set", [True, False])
@pytest.mark.parametrize(
    "use_project_name, use_stage_name", [(False, False), (False, True), (True, False), (True, True)]
)
@patch("galileo.stages.pause_stage_projects_project_id_stages_stage_id_put.sync")
def test_set_pause_state_success(
    mock_pause_api_sync: Mock,
    mock_projects_class_with_instance,
    mock_stages_get_method,
    pause_flag_to_set: bool,
    use_project_name: bool,
    use_stage_name: bool,
):
    mock_projects_class, mock_project_instance, fixture_project_id_str = mock_projects_class_with_instance
    mock_stages_get_patcher, fixture_stage_id_str, _ = mock_stages_get_method

    expected_api_result_stage_db = mock_stage_db_instance(
        project_id=FIXED_PROJECT_ID_UUID,
        name=FIXED_STAGE_NAME,
        stage_type_val=StageType.LOCAL.value,
        paused=pause_flag_to_set,
        description="Stage after pause/resume action",
    )
    mock_pause_api_sync.return_value = expected_api_result_stage_db

    call_kwargs = {}
    if use_project_name:
        call_kwargs["project_name"] = FIXED_PROJECT_NAME
    else:
        call_kwargs["project_id"] = FIXED_PROJECT_ID_UUID

    if use_stage_name:
        call_kwargs["stage_name"] = FIXED_STAGE_NAME
    else:
        call_kwargs["stage_id"] = FIXED_STAGE_ID_UUID

    action_func_top_level = pause_stage if pause_flag_to_set else resume_stage

    result_func = action_func_top_level(**call_kwargs)

    if use_project_name:
        mock_project_instance.get.assert_called_once_with(name=FIXED_PROJECT_NAME)
        mock_projects_class.assert_called_once()
        assert mock_projects_class.call_args.kwargs["client"] is not None
    else:
        mock_project_instance.get.assert_not_called()

    if use_stage_name:
        mock_stages_get_patcher.assert_called_once_with(project_id=fixture_project_id_str, stage_name=FIXED_STAGE_NAME)
    else:
        mock_stages_get_patcher.assert_not_called()

    mock_pause_api_sync.assert_called_once()
    api_call_args_func = mock_pause_api_sync.call_args.kwargs
    assert api_call_args_func["project_id"] == fixture_project_id_str
    assert api_call_args_func["stage_id"] == fixture_stage_id_str
    assert api_call_args_func["pause"] == pause_flag_to_set
    assert api_call_args_func["client"] is not None

    assert isinstance(result_func, StageDB)
    assert result_func.paused == pause_flag_to_set


@patch("galileo.stages.pause_stage_projects_project_id_stages_stage_id_put.sync")
def test_set_pause_state_api_validation_error(
    mock_pause_api_sync: Mock, mock_projects_class_with_instance, mock_stages_get_method
):
    _, mock_project_instance, _ = mock_projects_class_with_instance
    mock_stages_get_patcher, _, _ = mock_stages_get_method

    error_detail = [{"loc": ["query", "pause"], "msg": "value could not be parsed", "type": "type_error.bool"}]
    validation_error = HTTPValidationError(detail=error_detail)

    mock_pause_api_sync.return_value = validation_error

    result_func_pause = pause_stage(project_id=FIXED_PROJECT_ID_UUID, stage_id=FIXED_STAGE_ID_UUID)
    assert isinstance(result_func_pause, HTTPValidationError)
    assert result_func_pause.detail == error_detail
    mock_pause_api_sync.assert_called_once_with(
        project_id=FIXED_PROJECT_ID_STR, stage_id=FIXED_STAGE_ID_STR, client=ANY, pause=True
    )
    mock_project_instance.get.assert_not_called()
    mock_stages_get_patcher.assert_not_called()

    mock_pause_api_sync.reset_mock()
    mock_project_instance.get.reset_mock()
    mock_stages_get_patcher.reset_mock()

    mock_pause_api_sync.return_value = validation_error

    result_func_resume = resume_stage(project_id=FIXED_PROJECT_ID_UUID, stage_id=FIXED_STAGE_ID_UUID)
    assert isinstance(result_func_resume, HTTPValidationError)
    assert result_func_resume.detail == error_detail
    mock_pause_api_sync.assert_called_once_with(
        project_id=FIXED_PROJECT_ID_STR, stage_id=FIXED_STAGE_ID_STR, client=ANY, pause=False
    )
    mock_project_instance.get.assert_not_called()
    mock_stages_get_patcher.assert_not_called()
