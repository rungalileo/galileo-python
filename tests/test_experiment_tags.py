"""Tests for experiment tags functionality."""

import datetime
from unittest.mock import patch

import pytest

from galileo.experiment_tags import ExperimentTags, delete_experiment_tag, get_experiment_tags, upsert_experiment_tag
from galileo.resources.models.delete_run_response import DeleteRunResponse
from galileo.resources.models.run_tag_db import RunTagDB


@pytest.fixture
def sample_run_tag():
    """Create a sample RunTagDB for testing."""
    return RunTagDB(
        id="tag_1",
        project_id="project_1",
        run_id="experiment_1",
        key="environment",
        value="production",
        tag_type="user",
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
        created_by="test_user",
    )


@patch(
    "galileo.resources.api.experiment_tags.get_experiment_tags_projects_project_id_experiments_experiment_id_tags_get.sync"
)
def test_get_experiment_tags_success(mock_get_tags, sample_run_tag):
    """Test successfully getting experiment tags."""
    mock_get_tags.return_value = [sample_run_tag]
    result = get_experiment_tags("project_1", "experiment_1")

    assert len(result) == 1
    assert result[0].id == sample_run_tag.id
    assert result[0].key == "environment"
    assert result[0].value == "production"
    mock_get_tags.assert_called_once()


@patch(
    "galileo.resources.api.experiment_tags.get_experiment_tags_projects_project_id_experiments_experiment_id_tags_get.sync"
)
def test_get_experiment_tags_no_tags(mock_get_tags):
    """Test getting experiment tags when experiment has no tags."""
    mock_get_tags.return_value = []
    result = get_experiment_tags("project_1", "experiment_1")
    assert result == []
    mock_get_tags.assert_called_once()


@patch(
    "galileo.resources.api.experiment_tags.get_experiment_tags_projects_project_id_experiments_experiment_id_tags_get.sync"
)
def test_get_experiment_tags_experiment_not_found(mock_get_tags):
    """Test getting experiment tags when experiment is not found."""
    mock_get_tags.return_value = None
    result = get_experiment_tags("project_1", "experiment_1")
    assert result is None
    mock_get_tags.assert_called_once()


@patch(
    "galileo.resources.api.experiment_tags.set_tag_for_experiment_projects_project_id_experiments_experiment_id_tags_post.sync"
)
def test_upsert_experiment_tag_create_new(mock_set_tag, sample_run_tag):
    """Test creating a new tag via upsert."""
    mock_set_tag.return_value = sample_run_tag
    result = upsert_experiment_tag("project_1", "experiment_1", "version", "1.0.0")

    assert result.key == "environment"
    assert result.value == "production"
    assert result.tag_type == "user"
    mock_set_tag.assert_called_once()


@patch(
    "galileo.resources.api.experiment_tags.set_tag_for_experiment_projects_project_id_experiments_experiment_id_tags_post.sync"
)
def test_upsert_experiment_tag_update(mock_set_tag, sample_run_tag):
    """Test updating an existing tag via upsert."""
    mock_set_tag.return_value = sample_run_tag
    result = upsert_experiment_tag("project_1", "experiment_1", "environment", "staging", "system")

    assert result.id == sample_run_tag.id
    assert result.key == "environment"
    assert result.value == "production"
    mock_set_tag.assert_called_once()


@patch(
    "galileo.resources.api.experiment_tags.delete_experiment_tag_projects_project_id_experiments_experiment_id_tags_tag_id_delete.sync"
)
def test_delete_experiment_tag_success(mock_delete_tag):
    """Test successfully deleting a tag."""
    mock_delete_tag.return_value = DeleteRunResponse(message="Tag deleted successfully")
    result = delete_experiment_tag("project_1", "experiment_1", "tag_1")

    assert result["message"] == "Tag deleted successfully"
    assert result["tag_id"] == "tag_1"
    mock_delete_tag.assert_called_once()


@patch(
    "galileo.resources.api.experiment_tags.delete_experiment_tag_projects_project_id_experiments_experiment_id_tags_tag_id_delete.sync"
)
def test_delete_experiment_tag_not_found(mock_delete_tag):
    """Test deleting a tag that doesn't exist."""
    mock_delete_tag.return_value = None

    result = delete_experiment_tag("project_1", "experiment_1", "nonexistent_tag")
    assert result is None

    mock_delete_tag.assert_called_once()


@patch(
    "galileo.resources.api.experiment_tags.get_experiment_tags_projects_project_id_experiments_experiment_id_tags_get.sync"
)
def test_experiment_tags_class_get_tags(mock_get_tags, sample_run_tag):
    """Test ExperimentTags class get_experiment_tags method."""
    mock_get_tags.return_value = [sample_run_tag]

    experiment_tags = ExperimentTags()
    result = experiment_tags.get_experiment_tags("project_1", "experiment_1")

    assert len(result) == 1
    assert result[0].id == sample_run_tag.id
    mock_get_tags.assert_called_once()
