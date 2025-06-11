from typing import Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.projects import Projects
from galileo.resources.api.protect import (
    create_stage_v2_projects_project_id_stages_post,
    get_stage_projects_project_id_stages_get,
)
from galileo.resources.models import StageDB, StageWithRulesets
from galileo.resources.models.rule import Rule
from galileo.resources.models.stage_type import StageType
from galileo.resources.types import UNSET
from galileo.utils.catch_log import DecorateAllMethods
from galileo.utils.exceptions import APIException
from galileo_core.utils.name import ts_name


class StageAPIException(APIException):
    """Custom exception for Stage API errors."""

    pass


# class Stage(BaseClientModel):
#     """
#     Represents a single Stage instance.
#     Provides methods to interact with a specific stage.
#     """
#     _stage_db: StageDB
#
#     def __init__(self, stage_db: StageDB, client: Optional[GalileoApiClient] = None) -> None:
#         super().__init__(client=client)
#         self._stage_db = stage_db


class Stages(BaseClientModel, DecorateAllMethods):
    """
    Manages collections of Stages.
    Provides methods to create and retrieve stages.
    """

    def create(
        self,
        project_id: Union[str, UUID4],
        name: Optional[str] = None,
        stage_type: StageType = StageType.LOCAL,
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
            StageAPIException: If the API call fails.
            ValueError: If project_id is not provided.
        """
        if not project_id:
            raise ValueError("project_id must be provided for creating a stage.")
        actual_name = name or ts_name("stage")

        payload = StageWithRulesets(
            name=actual_name,
            project_id=str(project_id),
            type_=stage_type,
            paused=pause,
            description=description if description is not None else UNSET,
            prioritized_rulesets=rulesets if rulesets is not None else UNSET,
        )

        response = create_stage_v2_projects_project_id_stages_post.sync(
            project_id=str(project_id), client=self.client, body=payload
        )
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
            StageAPIException: If the API call fails.
            ValueError: If project identifiers or stage identifiers are insufficient or ambiguous.
        """
        actual_project_id_str: Optional[str] = None
        if project_id:
            actual_project_id_str = str(project_id)
        elif project_name:
            project_obj = Projects(client=self.client).get(name=project_name)
            if not project_obj:
                raise ValueError(f"Project with name '{project_name}' not found.")
            actual_project_id_str = str(project_obj.id)
        else:
            raise ValueError("Either project_id or project_name must be provided.")

        if not stage_id and not stage_name:
            raise ValueError("Either stage_id or stage_name must be provided.")
        if stage_id and stage_name:
            # Allowing both might be ambiguous depending on API; for now, let API handle or prefer ID
            # Or raise ValueError("Provide either stage_id or stage_name, not both.")
            pass  # Preferring ID if both are passed, by passing both to API client

        response = get_stage_projects_project_id_stages_get.sync(
            project_id=actual_project_id_str,
            stage_id=str(stage_id) if stage_id else UNSET,
            stage_name=stage_name if stage_name else UNSET,
            client=self.client,
        )
        return response


def create_stage(
    project_id: Union[str, UUID4],
    name: Optional[str] = None,
    stage_type: StageType = StageType.LOCAL,
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
