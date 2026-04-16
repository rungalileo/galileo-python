from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest

from galileo.jobs import Jobs
from galileo.resources.models import HTTPValidationError, PromptRunSettings, TaskType, ValidationError
from galileo.resources.types import Response


def _make_422_response(msg: str = "Invalid model alias: 'gpt-4o-mini'") -> Response:
    return Response(
        status_code=HTTPStatus(422),
        content=b"{}",
        headers={},
        parsed=HTTPValidationError(
            detail=[ValidationError(loc=["body", "prompt_settings", "model_alias"], msg=msg, type_="value_error")]
        ),
    )


def _make_job_kwargs(**overrides):
    defaults = dict(
        project_id="proj-id",
        name="test-job",
        run_id="run-id",
        dataset_id="ds-id",
        prompt_template_id=None,
        task_type=TaskType.VALUE_16,
        scorers=None,
        prompt_settings=PromptRunSettings(model_alias="gpt-4o-mini"),
    )
    return {**defaults, **overrides}


class TestJobsCreate:
    @patch("galileo.jobs.create_job_jobs_post")
    def test_raises_value_error_with_clear_message_on_invalid_model_alias(self, mock_post: MagicMock) -> None:
        """Jobs.create() with invalid model_alias (HTTP 422) raises ValueError with readable message."""
        # Given: the API returns a 422 with validation error for model_alias
        mock_post.sync_detailed = MagicMock(return_value=_make_422_response())

        # When/Then: ValueError is raised with a human-readable message
        with pytest.raises(ValueError, match="Request validation failed"):
            Jobs().create(**_make_job_kwargs())

    @patch("galileo.jobs.create_job_jobs_post")
    def test_error_message_contains_field_path_and_backend_message(self, mock_post: MagicMock) -> None:
        """The ValueError includes the field path and backend error message."""
        # Given: the API returns a 422 with specific validation detail
        mock_post.sync_detailed = MagicMock(return_value=_make_422_response("Invalid model alias: 'gpt-4o-mini'"))

        # When/Then: the error includes the field path and backend message
        with pytest.raises(ValueError) as exc_info:
            Jobs().create(**_make_job_kwargs())
        msg = str(exc_info.value)
        assert "model_alias" in msg
        assert "gpt-4o-mini" in msg

    @patch("galileo.jobs.create_job_jobs_post")
    def test_does_not_raise_galileo_http_exception(self, mock_post: MagicMock) -> None:
        """Jobs.create() no longer raises the empty GalileoHTTPException on 422."""
        # Given: the API returns a 422 response
        mock_post.sync_detailed = MagicMock(return_value=_make_422_response())

        # When/Then: the raised exception is ValueError, not GalileoHTTPException
        from galileo_core.exceptions.http import GalileoHTTPException

        with pytest.raises(ValueError):
            Jobs().create(**_make_job_kwargs())
        # Ensure GalileoHTTPException is NOT raised
        try:
            Jobs().create(**_make_job_kwargs())
        except GalileoHTTPException:
            pytest.fail("GalileoHTTPException should no longer be raised")
        except ValueError:
            pass  # expected

    @patch("galileo.jobs.create_job_jobs_post")
    def test_raises_value_error_on_unexpected_non_200(self, mock_post: MagicMock) -> None:
        """Jobs.create() raises ValueError with status code for non-422 unexpected responses."""
        # Given: the API returns an unexpected non-200 response with no parsed body
        mock_post.sync_detailed = MagicMock(
            return_value=Response(status_code=HTTPStatus(503), content=b"Service Unavailable", headers={}, parsed=None)
        )

        # When/Then: ValueError is raised with the status code in the message
        with pytest.raises(ValueError, match="503"):
            Jobs().create(**_make_job_kwargs())
