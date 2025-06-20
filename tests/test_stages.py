import uuid
from unittest.mock import ANY, Mock, patch

import pytest
from pydantic import UUID4

from galileo.resources.models import HTTPValidationError
from galileo.resources.models.stage_db import StageDB as APIStageDB
from galileo.stages import create_stage, get_stage, pause_stage, resume_stage, update_stage
from galileo_core.schemas.protect.rule import Rule, RuleOperator
from galileo_core.schemas.protect.stage import StageDB, StageType

FIXED_PROJECT_ID = uuid.uuid4()
FIXED_STAGE_ID = uuid.uuid4()


def _api_stage_db_factory(
    *,
    project_id: UUID4 = FIXED_PROJECT_ID,
    stage_id: UUID4 | None = None,
    name: str = "fixture-stage",
    paused: bool = False,
    version: int = 1,
    stage_type: StageType = StageType.local,
) -> APIStageDB:
    """Generate an APIStageDB instance with minimal required fields."""
    data = {
        "id": str(stage_id or uuid.uuid4()),
        "name": name,
        "project_id": str(project_id),
        "type": stage_type.value,
        "paused": paused,
        "version": version,
        "created_by": str(uuid.uuid4()),
        # APIStageDB specific fields that might be required by from_dict
        "created_at": "2024-01-01T00:00:00Z",  # Placeholder
        "updated_at": "2024-01-01T00:00:00Z",  # Placeholder
        "rulesets": [],
        "organization_id": str(uuid.uuid4()),  # Placeholder
    }
    # Ensure all fields required by APIStageDB.from_dict are present
    # This might involve checking the APIStageDB model definition
    # For now, assuming the above are sufficient or optional with defaults
    return APIStageDB.from_dict(data)


def _core_stage_db_factory(
    *,
    project_id: UUID4 = FIXED_PROJECT_ID,
    stage_id: UUID4 | None = None,
    name: str = "fixture-stage",
    paused: bool = False,
    version: int = 1,
    stage_type: StageType = StageType.local,
) -> StageDB:  # Returns galileo_core.StageDB
    """Generate a StageDB instance with minimal required fields."""
    data = {
        "id": str(stage_id or uuid.uuid4()),
        "name": name,
        "project_id": str(project_id),
        "type": stage_type.value,
        "paused": paused,
        "version": version,
        "created_by": str(uuid.uuid4()),
    }
    return StageDB.model_validate(data)


@pytest.fixture(autouse=True)
def _patch_common_modules():
    """Patch common external deps once for the whole module."""
    with patch("galileo.stages.Projects") as proj_patch:
        proj_patch.return_value.get.return_value.id = str(FIXED_PROJECT_ID)
        yield


@patch("galileo.stages.create_stage_v2_projects_project_id_stages_post.sync")
@patch("galileo.stages.ts_name", return_value="auto-name")
def test_create_stage_happy_path(mock_ts_name: Mock, mock_api: Mock):
    """Smoke‑test: minimal args produce StageDB and correct API call."""
    mock_api.return_value = _api_stage_db_factory(name="auto-name")

    stage = create_stage(project_id=FIXED_PROJECT_ID, pause=False)

    mock_api.assert_called_once_with(project_id=str(FIXED_PROJECT_ID), body=ANY, client=ANY)
    assert isinstance(stage, StageDB)
    assert stage.project_id == FIXED_PROJECT_ID


@patch("galileo.stages.create_stage_v2_projects_project_id_stages_post.sync")
def test_create_stage_validation_error(mock_api: Mock):
    """create_stage returns HTTPValidationError untouched."""
    err = HTTPValidationError(detail=[{"msg": "bad", "loc": ["body"], "type": "value_error"}])
    mock_api.return_value = err

    res = create_stage(project_id=FIXED_PROJECT_ID, name="x")
    assert res is err


@patch("galileo.stages.create_stage_v2_projects_project_id_stages_post.sync")
@patch("galileo.stages.ts_name", return_value="ts_auto")
def test_create_stage_generates_name_and_type(mock_ts_name: Mock, mock_api: Mock):
    """No name provided → ts_name used; stage_type override respected."""
    mock_api.return_value = _api_stage_db_factory(name="ts_auto", stage_type=StageType.central, paused=True)

    stage = create_stage(project_id=FIXED_PROJECT_ID, stage_type=StageType.central, pause=True)

    mock_ts_name.assert_called_once_with("stage")
    body = mock_api.call_args.kwargs["body"]
    assert body.name == "ts_auto"
    assert body.type_ == StageType.central
    assert stage.type == StageType.central.value
    assert stage.paused is True


@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
def test_get_stage_by_id(mock_api: Mock):
    # mock_api is for get_stage_projects_project_id_stages_get.sync which returns APIStageDB
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID)

    stage = get_stage(project_id=FIXED_PROJECT_ID, stage_id=FIXED_STAGE_ID)  # This returns core StageDB

    mock_api.assert_called_once_with(
        project_id=str(FIXED_PROJECT_ID), stage_id=str(FIXED_STAGE_ID), stage_name=ANY, client=ANY
    )
    assert isinstance(stage, StageDB)
    assert stage.id == FIXED_STAGE_ID


@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
@patch("galileo.stages.Projects")
def test_get_stage_by_names(mock_projects_cls: Mock, mock_api: Mock):
    proj_inst = Mock()
    proj_inst.get.return_value.id = str(FIXED_PROJECT_ID)
    mock_projects_cls.return_value = proj_inst

    # mock_api is for get_stage_projects_project_id_stages_get.sync which returns APIStageDB
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, name="named-stage")

    stage = get_stage(project_name="proj", stage_name="named-stage")  # This returns core StageDB

    proj_inst.get.assert_called_once_with(name="proj")
    mock_api.assert_called_once_with(
        project_id=str(FIXED_PROJECT_ID), stage_name="named-stage", stage_id=ANY, client=ANY
    )
    assert stage.name == "named-stage"


@patch("galileo.stages.update_stage_projects_project_id_stages_stage_id_post.sync")
@patch("galileo.stages.Stages.get")
def test_update_stage_rulesets(mock_get: Mock, mock_api: Mock):
    """Verify rulesets payload reaches API, version bumps."""
    mock_get.return_value = _core_stage_db_factory(stage_id=FIXED_STAGE_ID)  # Stages.get returns core StageDB
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, version=2)  # API call returns APIStageDB

    rulesets = [Rule(metric="m", operator=RuleOperator.eq, target_value="v")]
    stage = update_stage(project_id=FIXED_PROJECT_ID, stage_id=FIXED_STAGE_ID, prioritized_rulesets=rulesets)

    api_body = mock_api.call_args.kwargs["body"]
    assert len(api_body.prioritized_rulesets) == 1
    # assert api_body.prioritized_rulesets[0].rules == rulesets
    api_rules = api_body.prioritized_rulesets[0].rules
    assert api_rules[0].metric == rulesets[0].metric
    assert api_rules[0].target_value == rulesets[0].target_value
    assert api_rules[0].operator.lower() == rulesets[0].operator
    assert stage.version == 2


@patch("galileo.stages.update_stage_projects_project_id_stages_stage_id_post.sync")
@patch("galileo.stages.Stages.get")
@patch("galileo.stages.Projects")
def test_update_stage_by_names(mock_projects_cls: Mock, mock_get: Mock, mock_api: Mock):
    proj_inst = Mock()
    proj_inst.get.return_value.id = str(FIXED_PROJECT_ID)
    mock_projects_cls.return_value = proj_inst

    mock_get.return_value = _core_stage_db_factory(
        stage_id=FIXED_STAGE_ID, name="named-stage"
    )  # Stages.get returns core StageDB
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, version=3)  # API call returns APIStageDB

    stage = update_stage(project_name="proj", stage_name="named-stage", prioritized_rulesets=[])

    proj_inst.get.assert_called_once_with(name="proj")
    mock_get.assert_called_once_with(project_id=str(FIXED_PROJECT_ID), stage_name="named-stage")
    mock_api.assert_called_once()
    assert stage.version == 3


@pytest.mark.parametrize("pause_flag, api_fn", [(True, pause_stage), (False, resume_stage)])
@patch("galileo.stages.pause_stage_projects_project_id_stages_stage_id_put.sync")
@patch("galileo.stages.Stages.get")
def test_pause_and_resume_by_id(mock_get: Mock, mock_api: Mock, pause_flag, api_fn):
    mock_get.return_value = _core_stage_db_factory(
        stage_id=FIXED_STAGE_ID, paused=not pause_flag
    )  # Stages.get returns core StageDB
    mock_api.return_value = _api_stage_db_factory(
        stage_id=FIXED_STAGE_ID, paused=pause_flag
    )  # API call returns APIStageDB

    stage = api_fn(project_id=FIXED_PROJECT_ID, stage_id=FIXED_STAGE_ID)

    mock_api.assert_called_once_with(
        project_id=str(FIXED_PROJECT_ID), stage_id=str(FIXED_STAGE_ID), pause=pause_flag, client=ANY
    )
    assert stage.paused is pause_flag


@patch("galileo.stages.pause_stage_projects_project_id_stages_stage_id_put.sync")
@patch("galileo.stages.Stages.get")
@patch("galileo.stages.Projects")
def test_pause_stage_by_names(mock_projects_cls: Mock, mock_get: Mock, mock_api: Mock):
    proj_inst = Mock()
    proj_inst.get.return_value.id = str(FIXED_PROJECT_ID)
    mock_projects_cls.return_value = proj_inst

    mock_get.return_value = _core_stage_db_factory(
        stage_id=FIXED_STAGE_ID, name="named-stage", paused=False
    )  # Stages.get returns core StageDB
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, paused=True)  # API call returns APIStageDB

    stage = pause_stage(project_name="proj", stage_name="named-stage")

    proj_inst.get.assert_called_once_with(name="proj")
    mock_get.assert_called_once_with(project_id=str(FIXED_PROJECT_ID), stage_name="named-stage")
    mock_api.assert_called_once_with(
        project_id=str(FIXED_PROJECT_ID), stage_id=str(FIXED_STAGE_ID), pause=True, client=ANY
    )
    assert stage.paused is True
