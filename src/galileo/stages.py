from typing import Optional, Union

from pydantic import UUID4

from galileo.api_client import GalileoApiClient
from galileo.base import BaseClientModel
from galileo.projects import Projects
from galileo.resources.api.protect import (
    create_stage_v2_projects_project_id_stages_post,
    get_stage_projects_project_id_stages_get,
    pause_stage_projects_project_id_stages_stage_id_put,
    update_stage_projects_project_id_stages_stage_id_post,
)
from galileo.resources.models.rulesets_mixin import RulesetsMixin as APIRulesetsMixin
from galileo.resources.models.stage_db import StageDB as APIStageDB
from galileo.resources.models.stage_with_rulesets import StageWithRulesets as APIStageWithRulesets
from galileo.resources.types import UNSET
from galileo.utils.catch_log import DecorateAllMethods
from galileo_core.schemas.protect.rule import Rule
from galileo_core.schemas.protect.ruleset import Ruleset, RulesetsMixin
from galileo_core.schemas.protect.stage import StageDB, StageType, StageWithRulesets
from galileo_core.utils.name import ts_name


def _get_project_id(
    project_id: Optional[Union[str, UUID4]] = None,
    project_name: Optional[str] = None,
    client: Optional[GalileoApiClient] = None,
) -> Optional[str]:
    """
    Helper function to resolve project ID from either project_id or project_name.
    """
    if project_id:
        return str(project_id)
    elif project_name:
        project = Projects(client=client).get(name=project_name)
        if not project:
            raise ValueError(f"Project with name '{project_name}' not found.")
        return str(project.id)
    else:
        raise ValueError("Either project_id or project_name must be provided.")


def _get_stage_id(
    stage_id: Optional[Union[str, UUID4]] = None,
    stage_name: Optional[str] = None,
    project_id: Optional[Union[str, UUID4]] = None,
    client: Optional[GalileoApiClient] = None,
) -> Optional[str]:
    """
    Helper function to resolve stage ID from either stage_id or stage_name.
    If stage_name is provided, it will look up the stage within the specified project.
    """
    if stage_id:
        return str(stage_id)
    elif stage_name:
        stage = Stages(client=client).get(project_id=project_id, stage_name=stage_name)
        if not stage:
            raise ValueError(f"Stage with name '{stage_name}' not found.")
        return str(stage.id)
    else:
        raise ValueError("Either stage_id or stage_name must be provided.")


class Stages(BaseClientModel, DecorateAllMethods):
    """
    Provides methods to create, retrieve, update, pause, and resume stages.
    """

    def create(
        self,
        project_id: Union[str, UUID4],
        name: Optional[str] = None,
        stage_type: StageType = StageType.local,
        pause: bool = False,
        rulesets: Optional[list[Rule]] = None,
        description: Optional[str] = None,
    ) -> StageDB:
        """
        Creates a new stage.

        Args:
            project_id: The ID of the project.
            name: Name of the stage. Defaults to a timestamped name if None.
            stage_type: Type of the stage. Defaults to StageType.local.
            pause: Whether the stage should be created in a paused state. Defaults to False.
            rulesets: Optional list of rules for the stage.
            description: Optional description for the stage.

        Returns:
            A Stage instance representing the newly created stage.

        Raises:
            ValueError: If project_id is not provided.
        """
        if not project_id:
            raise ValueError("project_id must be provided for creating a stage.")
        actual_name = name or ts_name("stage")

        request = StageWithRulesets(
            name=actual_name,
            project_id=str(project_id),
            type=stage_type,
            paused=pause,
            description=description,
            prioritized_rulesets=[Ruleset(rules=rulesets)] if rulesets else [],
        )

        body = APIStageWithRulesets.from_dict(request.model_dump())

        response = create_stage_v2_projects_project_id_stages_post.sync(
            project_id=str(project_id), client=self.client, body=body
        )

        if isinstance(response, APIStageDB):
            return StageDB.model_validate(response.to_dict())
        return response

    def get(
        self,
        project_id: Optional[Union[str, UUID4]] = None,
        project_name: Optional[str] = None,
        stage_id: Optional[Union[str, UUID4]] = None,
        stage_name: Optional[str] = None,
    ) -> StageDB:
        """
        Retrieves a specific stage by its ID or name, within a given project.

        Args:
            project_id: The ID of the project.
            project_name: The name of the project. If project_id is not provided,
                          this will be used to look up the project.
            stage_id: The ID of the stage to retrieve.
            stage_name: The name of the stage to retrieve. If stage_id is not provided,
                        this will be used (in conjunction with project_id/project_name).

        Returns:
            A StageDB instance representing the fetched stage.

        Raises:
            ValueError: If project identifiers or stage identifiers are insufficient or ambiguous.
        """
        actual_project_id: Optional[str] = _get_project_id(
            project_id=project_id, project_name=project_name, client=self.client
        )

        if not stage_id and not stage_name:
            raise ValueError("Either stage_id or stage_name must be provided.")

        response = get_stage_projects_project_id_stages_get.sync(
            project_id=actual_project_id,
            stage_id=str(stage_id) if stage_id else UNSET,
            stage_name=stage_name if stage_name else UNSET,
            client=self.client,
        )
        if isinstance(response, APIStageDB):
            return StageDB.model_validate(response.to_dict())
        return response

    def update(
        self,
        project_id: Optional[Union[str, UUID4]] = None,
        project_name: Optional[str] = None,
        stage_id: Optional[Union[str, UUID4]] = None,
        stage_name: Optional[str] = None,
        prioritized_rulesets: Optional[list[Rule]] = None,
    ) -> StageDB:
        """
        Updates a stage, typically its rulesets. This creates a new version of the stage.

        Args:
            project_id: The ID of the project.
            project_name: The name of the project.
            stage_id: The ID of the stage to update.
            stage_name: The name of the stage to update.
            prioritized_rulesets: The new list of prioritized rulesets for the stage.
                                  If None, effectively clears rulesets (sends empty list).

        Returns:
            A StageDB instance representing the updated stage.

        Raises:
            ValueError: If project/stage identifiers are insufficient or the stage is not found.
        """
        actual_project_id: Optional[str] = _get_project_id(
            project_id=project_id, project_name=project_name, client=self.client
        )

        actual_stage_id: Optional[str] = _get_stage_id(
            stage_id=stage_id, stage_name=stage_name, project_id=actual_project_id, client=self.client
        )

        rulesets = [Ruleset(rules=prioritized_rulesets)] if prioritized_rulesets else []
        request = RulesetsMixin(prioritized_rulesets=rulesets)
        body = APIRulesetsMixin.from_dict(request.model_dump(by_alias=True))

        response = update_stage_projects_project_id_stages_stage_id_post.sync(
            project_id=actual_project_id, stage_id=actual_stage_id, client=self.client, body=body
        )
        if isinstance(response, APIStageDB):
            return StageDB.model_validate(response.to_dict())
        return response

    def _set_pause_state(
        self,
        pause_flag: bool,
        project_id: Optional[Union[str, UUID4]] = None,
        project_name: Optional[str] = None,
        stage_id: Optional[Union[str, UUID4]] = None,
        stage_name: Optional[str] = None,
    ) -> StageDB:
        """Internal method to set the pause state of a stage."""
        actual_project_id: Optional[str] = _get_project_id(
            project_id=project_id, project_name=project_name, client=self.client
        )

        actual_stage_id: Optional[str] = _get_stage_id(
            stage_id=stage_id, stage_name=stage_name, project_id=actual_project_id, client=self.client
        )

        response = pause_stage_projects_project_id_stages_stage_id_put.sync(
            project_id=actual_project_id, stage_id=actual_stage_id, client=self.client, pause=pause_flag
        )
        if isinstance(response, APIStageDB):
            return StageDB.model_validate(response.to_dict())
        return response

    def pause(
        self,
        project_id: Optional[Union[str, UUID4]] = None,
        project_name: Optional[str] = None,
        stage_id: Optional[Union[str, UUID4]] = None,
        stage_name: Optional[str] = None,
    ) -> StageDB:
        """Pauses a stage."""
        return self._set_pause_state(
            project_id=project_id, project_name=project_name, stage_id=stage_id, stage_name=stage_name, pause_flag=True
        )

    def resume(
        self,
        project_id: Optional[Union[str, UUID4]] = None,
        project_name: Optional[str] = None,
        stage_id: Optional[Union[str, UUID4]] = None,
        stage_name: Optional[str] = None,
    ) -> StageDB:
        """Resumes a paused stage."""
        return self._set_pause_state(
            project_id=project_id, project_name=project_name, stage_id=stage_id, stage_name=stage_name, pause_flag=False
        )


def create_stage(
    project_id: Union[str, UUID4],
    name: Optional[str] = None,
    stage_type: StageType = StageType.local,
    pause: bool = False,
    rulesets: Optional[list[Rule]] = None,
    description: Optional[str] = None,
) -> StageDB:
    """
    Convenience function to create a new stage.

    Args:
        project_id: The ID of the project.
        name: Name of the stage. Defaults to a timestamped name if None.
        stage_type: Type of the stage. Defaults to StageType.local.
        pause: Whether the stage should be created in a paused state. Defaults to False.
        rulesets: Optional list of rules for the stage.
        description: Optional description for the stage.

    Returns:
        A Stage instance representing the newly created stage.
    """
    return Stages().create(
        project_id=project_id, name=name, stage_type=stage_type, pause=pause, rulesets=rulesets, description=description
    )


def get_stage(
    project_id: Optional[Union[str, UUID4]] = None,
    project_name: Optional[str] = None,
    stage_id: Optional[Union[str, UUID4]] = None,
    stage_name: Optional[str] = None,
) -> StageDB:
    """
    Convenience function to retrieve a specific stage by its ID or name.

    Args:
        project_id: The ID of the project.
        project_name: The name of the project.
        stage_id: The ID of the stage.
        stage_name: The name of the stage.

    Returns:
        A StageDB instance representing the fetched stage.
    """
    return Stages().get(project_id=project_id, project_name=project_name, stage_id=stage_id, stage_name=stage_name)


def update_stage(
    project_id: Optional[Union[str, UUID4]] = None,
    project_name: Optional[str] = None,
    stage_id: Optional[Union[str, UUID4]] = None,
    stage_name: Optional[str] = None,
    prioritized_rulesets: Optional[list[Rule]] = None,
) -> StageDB:
    """
    Convenience function to update a stage's rulesets.

    Args:
        project_id: The ID of the project.
        project_name: The name of the project.
        stage_id: The ID of the stage to update.
        stage_name: The name of the stage to update.
        prioritized_rulesets: The new list of prioritized rulesets.

    Returns:
        A StageDB instance representing the updated stage.
    """
    return Stages().update(
        project_id=project_id,
        project_name=project_name,
        stage_id=stage_id,
        stage_name=stage_name,
        prioritized_rulesets=prioritized_rulesets,
    )


def pause_stage(
    project_id: Optional[Union[str, UUID4]] = None,
    project_name: Optional[str] = None,
    stage_id: Optional[Union[str, UUID4]] = None,
    stage_name: Optional[str] = None,
) -> StageDB:
    """
    Convenience function to pause a stage.

    Args:
        project_id: The ID of the project.
        project_name: The name of the project.
        stage_id: The ID of the stage to pause.
        stage_name: The name of the stage to pause.

    Returns:
        A StageDB instance representing the stage with its updated pause state.
    """
    return Stages().pause(project_id=project_id, project_name=project_name, stage_id=stage_id, stage_name=stage_name)


def resume_stage(
    project_id: Optional[Union[str, UUID4]] = None,
    project_name: Optional[str] = None,
    stage_id: Optional[Union[str, UUID4]] = None,
    stage_name: Optional[str] = None,
) -> StageDB:
    """
    Convenience function to resume a paused stage.

    Args:
        project_id: The ID of the project.
        project_name: The name of the project.
        stage_id: The ID of the stage to resume.
        stage_name: The name of the stage to resume.

    Returns:
        A StageDB instance representing the stage with its updated pause state.
    """
    return Stages().resume(project_id=project_id, project_name=project_name, stage_id=stage_id, stage_name=stage_name)
