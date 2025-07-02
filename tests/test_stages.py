import uuid
from typing import Optional
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
    stage_id: Optional[UUID4] = None,
    name: str = "fixture-stage",
    paused: bool = False,
    version: int = 1,
    stage_type: StageType = StageType.local,
) -> APIStageDB:
    data = {
        "id": str(stage_id or uuid.uuid4()),
        "name": name,
        "project_id": str(project_id),
        "type": stage_type.value,
        "paused": paused,
        "version": version,
        "created_by": str(uuid.uuid4()),
    }
    return APIStageDB.from_dict(data)


def _core_stage_db_factory(
    *,
    project_id: UUID4 = FIXED_PROJECT_ID,
    stage_id: Optional[UUID4] = None,
    name: str = "fixture-stage",
    paused: bool = False,
    version: int = 1,
    stage_type: StageType = StageType.local,
) -> StageDB:
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


@patch("galileo.stages.create_stage_projects_project_id_stages_post.sync")
@patch("galileo.stages.ts_name", return_value="auto-name")
def test_create_stage_happy_path(mock_ts_name: Mock, mock_api: Mock):
    """Smoke‑test: minimal args produce StageDB and correct API call."""
    mock_api.return_value = _api_stage_db_factory(name="auto-name")

    stage = create_stage(project_id=FIXED_PROJECT_ID, pause=False)

    mock_api.assert_called_once_with(project_id=str(FIXED_PROJECT_ID), body=ANY, client=ANY)
    assert isinstance(stage, StageDB)
    assert stage.project_id == FIXED_PROJECT_ID


@patch("galileo.stages.create_stage_projects_project_id_stages_post.sync")
def test_create_stage_validation_error(mock_api: Mock):
    """create_stage returns HTTPValidationError untouched."""
    err = HTTPValidationError(detail=[{"msg": "bad", "loc": ["body"], "type": "value_error"}])
    mock_api.return_value = err

    res = create_stage(project_id=FIXED_PROJECT_ID, name="x")
    assert res is err


@patch("galileo.stages.create_stage_projects_project_id_stages_post.sync")
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


@patch("galileo.stages.create_stage_projects_project_id_stages_post.sync")
def test_create_central_stage_with_rulesets(mock_api: Mock):
    rules = [Rule(metric="m1", operator=RuleOperator.eq, target_value="v1")]
    stage_name = "test-central-stage-with-rules"
    mock_api.return_value = _api_stage_db_factory(name=stage_name, stage_type=StageType.central)

    stage_response = create_stage(
        project_id=FIXED_PROJECT_ID, name=stage_name, rulesets=rules, stage_type=StageType.central
    )

    mock_api.assert_called_once()
    api_call_args = mock_api.call_args.kwargs
    body = api_call_args["body"]

    assert stage_response.type == StageType.central
    assert body.name == stage_name
    assert body.type_ == StageType.central.value

    assert len(body.prioritized_rulesets) == 1
    api_ruleset = body.prioritized_rulesets[0]
    for i, api_rule in enumerate(api_ruleset.rules):
        rule = rules[i]
        assert api_rule.metric == rule.metric
        assert api_rule.operator.lower() == rule.operator.value.lower()
        assert api_rule.target_value == rule.target_value
    assert "rulesets" not in body.additional_properties


@patch("galileo.stages.get_stage_projects_project_id_stages_get.sync")
def test_get_stage_by_id(mock_api: Mock):
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID)

    stage = get_stage(project_id=FIXED_PROJECT_ID, stage_id=FIXED_STAGE_ID)

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

    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, name="named-stage")

    stage = get_stage(project_name="proj", stage_name="named-stage")

    proj_inst.get.assert_called_once_with(name="proj")
    mock_api.assert_called_once_with(
        project_id=str(FIXED_PROJECT_ID), stage_name="named-stage", stage_id=ANY, client=ANY
    )
    assert stage.name == "named-stage"


@patch("galileo.stages.update_stage_projects_project_id_stages_stage_id_post.sync")
@patch("galileo.stages.Stages.get")
def test_update_stage_rulesets(mock_get: Mock, mock_api: Mock):
    """Verify rulesets payload reaches API, version bumps."""
    mock_get.return_value = _core_stage_db_factory(stage_id=FIXED_STAGE_ID)
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, version=2)

    rulesets = [Rule(metric="m", operator=RuleOperator.eq, target_value="v")]
    stage = update_stage(project_id=FIXED_PROJECT_ID, stage_id=FIXED_STAGE_ID, prioritized_rulesets=rulesets)

    api_body = mock_api.call_args.kwargs["body"]
    assert len(api_body.prioritized_rulesets) == 1

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

    mock_get.return_value = _core_stage_db_factory(stage_id=FIXED_STAGE_ID, name="named-stage")
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, version=3)

    stage = update_stage(project_name="proj", stage_name="named-stage", prioritized_rulesets=[])

    proj_inst.get.assert_called_once_with(name="proj")
    mock_get.assert_called_once_with(project_id=str(FIXED_PROJECT_ID), stage_name="named-stage")
    mock_api.assert_called_once()
    assert stage.version == 3


@pytest.mark.parametrize("pause_flag, api_fn", [(True, pause_stage), (False, resume_stage)])
@patch("galileo.stages.pause_stage_projects_project_id_stages_stage_id_put.sync")
@patch("galileo.stages.Stages.get")
def test_pause_and_resume_by_id(mock_get: Mock, mock_api: Mock, pause_flag, api_fn):
    mock_get.return_value = _core_stage_db_factory(stage_id=FIXED_STAGE_ID, paused=not pause_flag)
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, paused=pause_flag)

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

    mock_get.return_value = _core_stage_db_factory(stage_id=FIXED_STAGE_ID, name="named-stage", paused=False)
    mock_api.return_value = _api_stage_db_factory(stage_id=FIXED_STAGE_ID, paused=True)

    stage = pause_stage(project_name="proj", stage_name="named-stage")

    proj_inst.get.assert_called_once_with(name="proj")
    mock_get.assert_called_once_with(project_id=str(FIXED_PROJECT_ID), stage_name="named-stage")
    mock_api.assert_called_once_with(
        project_id=str(FIXED_PROJECT_ID), stage_id=str(FIXED_STAGE_ID), pause=True, client=ANY
    )
    assert stage.paused is True
