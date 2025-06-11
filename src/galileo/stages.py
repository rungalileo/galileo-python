from typing import Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.resources.api.protect import create_stage_v2_projects_project_id_stages_post
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
    Provides methods to create stages.
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
