import re
from typing import Optional
from unittest.mock import ANY, Mock, patch
from uuid import uuid4

import pytest
from pytest import CaptureFixture

from galileo.job_progress import job_progress, scorer_jobs_status
from galileo.resources.models import HTTPValidationError, JobDB, ValidationError
from galileo_core.constants.job import JobStatus

FIXED_PROJECT_ID = str(uuid4())
FIXED_RUN_ID = str(uuid4())
FIXED_JOB_ID = str(uuid4())


def _job_db_factory(
    *,
    project_id: str = FIXED_PROJECT_ID,
    run_id: str = FIXED_RUN_ID,
    job_id: Optional[str] = None,
    job_name: str = "test-job",
    status: JobStatus = JobStatus.completed,
    request_data: Optional[dict] = None,
    error_message: Optional[str] = None,
    steps_total: int = 100,
    steps_completed: int = 100,
    progress_message: str = "Done",
) -> JobDB:
    data = {
        "id": str(job_id or uuid4()),
        "project_id": str(project_id),
        "run_id": str(run_id),
        "job_name": job_name,
        "status": status.value,
        "request_data": request_data or {},
        "error_message": error_message,
        "steps_total": steps_total,
        "steps_completed": steps_completed,
        "progress_message": progress_message,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "retries": 0,
    }
    return JobDB.from_dict(data)


class TestJobProgress:
    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    @patch("galileo.job_progress.get_job_jobs_job_id_get.sync")
    def test_completed(self, mock_get_job: Mock, mock_get_scorer_jobs: Mock):
        mock_get_job.return_value = _job_db_factory(status=JobStatus.completed)
        mock_get_scorer_jobs.return_value = []

        job_progress(job_id=FIXED_JOB_ID, project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        mock_get_job.assert_called_with(client=ANY, job_id=FIXED_JOB_ID)

    @patch("galileo.job_progress.get_job_jobs_job_id_get.sync")
    def test_failed(self, mock_get_job: Mock):
        mock_get_job.return_value = _job_db_factory(status=JobStatus.failed, error_message="Test error")

        with pytest.raises(ValueError, match="Job failed with error message Test error."):
            job_progress(job_id=FIXED_JOB_ID, project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        mock_get_job.assert_called_with(client=ANY, job_id=FIXED_JOB_ID)

    @patch("galileo.job_progress.get_job_jobs_job_id_get.sync")
    def test_get_job_fails(self, mock_get_job: Mock):
        mock_get_job.return_value = None

        with pytest.raises(ValueError, match=f"Failed to get job status for job {FIXED_JOB_ID}"):
            job_progress(job_id=FIXED_JOB_ID, project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        mock_get_job.assert_called_with(client=ANY, job_id=FIXED_JOB_ID)

    @patch("galileo.job_progress.get_job_jobs_job_id_get.sync")
    def test_get_job_http_validation_error(self, mock_get_job: Mock):
        detail = [ValidationError(loc=["path", "job_id"], msg="value is not a valid uuid", type_="type_error.uuid")]
        mock_get_job.return_value = HTTPValidationError(detail=detail)

        with pytest.raises(ValueError, match=re.escape(str(detail))):
            job_progress(job_id=FIXED_JOB_ID, project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)


class TestScorerJobsStatus:
    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    def test_simple(self, mock_get_jobs: Mock, capsys: CaptureFixture[str]):
        mock_get_jobs.return_value = [
            _job_db_factory(
                job_name="log_stream_scorer",
                status=JobStatus.in_progress,
                request_data={"prompt_scorer_settings": {"scorer_name": "pii"}},
            )
        ]

        scorer_jobs_status(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        captured = capsys.readouterr()
        assert captured.out == "pii: Computing 🚧\n"

    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    def test_skips_prompt_run(self, mock_get_jobs: Mock, capsys: CaptureFixture[str]):
        mock_get_jobs.return_value = [
            _job_db_factory(job_name="log_stream_run"),
            _job_db_factory(
                job_name="log_stream_scorer",
                status=JobStatus.in_progress,
                request_data={"prompt_scorer_settings": {"scorer_name": "pii"}},
            ),
        ]

        scorer_jobs_status(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        captured = capsys.readouterr()
        assert captured.out == "pii: Computing 🚧\n"

    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    def test_no_scorer_jobs(self, mock_get_jobs: Mock, capsys: CaptureFixture[str]):
        mock_get_jobs.return_value = [_job_db_factory(job_name="log_stream_run")]

        scorer_jobs_status(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    def test_one_of_each(self, mock_get_jobs: Mock, capsys: CaptureFixture[str]):
        mock_get_jobs.return_value = [
            _job_db_factory(job_name="log_stream_run"),
            _job_db_factory(
                job_name="log_stream_scorer",
                status=JobStatus.in_progress,
                request_data={"prompt_scorer_settings": {"scorer_name": "pii"}},
            ),
            _job_db_factory(
                job_name="log_stream_scorer",
                status=JobStatus.error,
                error_message="An error occurred.",
                request_data={"prompt_scorer_settings": {"scorer_name": "toxicity"}},
            ),
            _job_db_factory(
                job_name="log_stream_scorer",
                status=JobStatus.completed,
                request_data={"prompt_scorer_settings": {"scorer_name": "chunk_attribution_utilization_plus"}},
            ),
        ]

        scorer_jobs_status(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        captured = capsys.readouterr()
        assert captured.out.split("\n") == [
            "pii: Computing 🚧",
            "toxicity: Failed ❌, error was: An error occurred.",
            "chunk_attribution_utilization_plus: Done ✅",
            "",
        ]

    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    def test_unknown_scorer_name(self, mock_get_jobs: Mock, capsys: CaptureFixture[str]):
        mock_get_jobs.return_value = [
            _job_db_factory(job_name="log_stream_run"),
            _job_db_factory(
                job_name="log_stream_scorer",
                status=JobStatus.in_progress,
                request_data={"prompt_scorer_settings": {"scorer_name": "abc"}},
            ),
        ]

        scorer_jobs_status(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
        captured = capsys.readouterr()
        assert captured.out == "abc: Computing 🚧\n"

    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    def test_get_run_scorer_jobs_fails(self, mock_get_jobs: Mock):
        mock_get_jobs.return_value = None

        with pytest.raises(
            ValueError, match=f"Failed to get scorer jobs for project {FIXED_PROJECT_ID}, run {FIXED_RUN_ID}"
        ):
            scorer_jobs_status(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)

    @patch("galileo.job_progress.get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync")
    def test_get_run_scorer_jobs_http_validation_error(self, mock_get_jobs: Mock):
        detail = [ValidationError(loc=["path", "project_id"], msg="value is not a valid uuid", type_="type_error.uuid")]
        mock_get_jobs.return_value = HTTPValidationError(detail=detail)

        with pytest.raises(ValueError, match=re.escape(str(detail))):
            scorer_jobs_status(project_id=FIXED_PROJECT_ID, run_id=FIXED_RUN_ID)
