"""Experiment Tags functionality for managing tags on experiments."""

import logging
from typing import Union

from galileo.config import GalileoPythonConfig
from galileo.resources.api.experiment_tags import (
    delete_experiment_tag_projects_project_id_experiments_experiment_id_tags_tag_id_delete,
    get_experiment_tags_projects_project_id_experiments_experiment_id_tags_get,
    set_tag_for_experiment_projects_project_id_experiments_experiment_id_tags_post,
)
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.run_tag_create_request import RunTagCreateRequest
from galileo.resources.models.run_tag_db import RunTagDB
from galileo.utils.catch_log import DecorateAllMethods
from galileo.utils.exceptions import APIException

_logger = logging.getLogger(__name__)


class ExperimentTagsAPIException(APIException):
    """Exception raised when experiment tags operations fail."""

    pass


class ExperimentTag(RunTagDB):
    """Wrapper class for experiment tags that provides additional functionality."""

    def __init__(self, experiment_tag: Union[None, RunTagDB] = None):
        """
        Initialize an ExperimentTag instance.

        Parameters
        ----------
        experiment_tag : Union[None, RunTagDB], optional
            The experiment tag data to initialize from. If None, creates an empty instance.
            Defaults to None.
        """
        if experiment_tag is not None:
            super().__init__(
                id=experiment_tag.id,
                project_id=experiment_tag.project_id,
                run_id=experiment_tag.run_id,
                key=experiment_tag.key,
                value=experiment_tag.value,
                tag_type=experiment_tag.tag_type,
                created_at=experiment_tag.created_at,
                updated_at=experiment_tag.updated_at,
                created_by=experiment_tag.created_by,
            )
            self.additional_properties = experiment_tag.additional_properties.copy()


class ExperimentTags(DecorateAllMethods):
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def get_experiment_tags(self, project_id: str, experiment_id: str) -> list[ExperimentTag]:
        """
        Get all tags for a specific experiment.

        Args:
            project_id: The project ID
            experiment_id: The experiment ID

        Returns:
            list[ExperimentTag]: List of tags associated with the experiment

        Raises:
            ExperimentTagsAPIException: If the API call fails
            ValueError: If the experiment is not found
        """
        response = get_experiment_tags_projects_project_id_experiments_experiment_id_tags_get.sync(
            project_id=project_id, experiment_id=experiment_id, client=self.config.api_client
        )

        if isinstance(response, HTTPValidationError):
            raise ExperimentTagsAPIException(f"Failed to get experiment tags: {response.detail}")

        return response

    def upsert_experiment_tag(
        self, project_id: str, experiment_id: str, key: str, value: str, tag_type: str = "generic"
    ) -> ExperimentTag:
        """
        Upsert a tag for a specific experiment.

        Args:
            project_id: The project ID
            experiment_id: The experiment ID
            key: The tag key
            value: The tag value
            tag_type: The type of tag (default: "generic")

        Returns:
            ExperimentTag: The created or updated tag

        Raises:
            ExperimentTagsAPIException: If the API call fails
            ValueError: If the experiment is not found
        """
        request_body = RunTagCreateRequest(key=key, value=value, tag_type=tag_type)

        response = set_tag_for_experiment_projects_project_id_experiments_experiment_id_tags_post.sync(
            project_id=project_id, experiment_id=experiment_id, client=self.config.api_client, body=request_body
        )

        if isinstance(response, HTTPValidationError):
            raise ExperimentTagsAPIException(f"Failed to upsert experiment tag: {response.detail}")

        if not response:
            raise ExperimentTagsAPIException("No response received from API")

        return ExperimentTag(experiment_tag=response)

    def delete_experiment_tag(self, project_id: str, experiment_id: str, tag_id: str) -> dict[str, str]:
        """
        Delete a specific tag from an experiment.

        Args:
            project_id: The project ID
            experiment_id: The experiment ID
            tag_id: The tag ID to delete

        Returns:
            dict[str, str]: Success message

        Raises:
            ExperimentTagsAPIException: If the API call fails
            ValueError: If the experiment or tag is not found
        """
        response = delete_experiment_tag_projects_project_id_experiments_experiment_id_tags_tag_id_delete.sync(
            project_id=project_id, experiment_id=experiment_id, tag_id=tag_id, client=self.config.api_client
        )

        if isinstance(response, HTTPValidationError):
            raise ExperimentTagsAPIException(f"Failed to delete experiment tag: {response.detail}")

        if not response:
            raise ExperimentTagsAPIException("No response received from API")

        return {
            "message": response.message if hasattr(response, "message") else "Tag deleted successfully",
            "tag_id": tag_id,
        }


def get_experiment_tags(project_id: str, experiment_id: str) -> list[ExperimentTag]:
    """
    Get all tags for a specific experiment.

    Args:
        project_id: The project ID
        experiment_id: The experiment ID

    Returns:
        list[ExperimentTag]: List of tags associated with the experiment

    Raises:
        ExperimentTagsAPIException: If the API call fails
        ValueError: If the experiment is not found
    """
    return ExperimentTags().get_experiment_tags(project_id, experiment_id)


def upsert_experiment_tag(
    project_id: str, experiment_id: str, key: str, value: str, tag_type: str = "generic"
) -> ExperimentTag:
    """
    Upsert (create or update) a tag for a specific experiment.

    Args:
        project_id: The project ID
        experiment_id: The experiment ID
        key: The tag key
        value: The tag value
        tag_type: The type of tag (default: "generic")

    Returns:
        ExperimentTag: The created or updated tag

    Raises:
        ExperimentTagsAPIException: If the API call fails
        ValueError: If the experiment is not found
    """
    return ExperimentTags().upsert_experiment_tag(project_id, experiment_id, key, value, tag_type)


def delete_experiment_tag(project_id: str, experiment_id: str, tag_id: str) -> dict[str, str]:
    """
    Delete a specific tag from an experiment.

    Args:
        project_id: The project ID
        experiment_id: The experiment ID
        tag_id: The tag ID to delete

    Returns:
        dict[str, str]: Success message

    Raises:
        ExperimentTagsAPIException: If the API call fails
        ValueError: If the experiment or tag is not found
    """
    return ExperimentTags().delete_experiment_tag(project_id, experiment_id, tag_id)
