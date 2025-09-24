import logging
import random
from time import sleep

from pydantic import UUID4
from tqdm.auto import tqdm

from galileo.config import GalileoPythonConfig
from galileo.resources.api.jobs import (
    get_job_jobs_job_id_get,
    get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get,
)
from galileo.resources.models import HTTPValidationError, JobDB
from galileo_core.constants.job import JobName, JobStatus
from galileo_core.constants.scorers import Scorers

_logger = logging.getLogger(__name__)


def get_job(job_id: str) -> JobDB:
    config = GalileoPythonConfig.get()

    response = get_job_jobs_job_id_get.sync(client=config.api_client, job_id=str(job_id))

    if isinstance(response, HTTPValidationError):
        raise ValueError(response.detail)
    if not response:
        raise ValueError(f"Failed to get job status for job {job_id}")
    return response


def get_run_scorer_jobs(project_id: str, run_id: str) -> list[JobDB]:
    config = GalileoPythonConfig.get()

    response = get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync(
        client=config.api_client, project_id=str(project_id), run_id=str(run_id)
    )
    if isinstance(response, HTTPValidationError):
        raise ValueError(response.detail)
    if response is None:
        raise ValueError(f"Failed to get scorer jobs for project {project_id}, run {run_id}")

    _logger.debug(f"Scorer jobs: {response}")

    return [job for job in response if job.job_name == JobName.log_stream_scorer]


def scorer_jobs_status(project_id: str, run_id: str) -> None:
    """Gets the status of all scorer jobs for a given project and run.

    Args:
        project_id: The unique identifier of the project.
        run_id: The unique identifier of the run.
    """
    scorer_jobs = get_run_scorer_jobs(project_id, run_id)
    for job in scorer_jobs:
        scorer_name = None
        if "prompt_scorer_settings" in job.request_data and job.request_data["prompt_scorer_settings"]:
            scorer_name = job.request_data["prompt_scorer_settings"]["scorer_name"]
        elif "scorer_config" in job.request_data and job.request_data["scorer_config"]:
            scorer_name = job.request_data["scorer_config"]["name"]

        if not scorer_name:
            _logger.debug(f"Scorer job {job.id} has no scorer name.")
            continue

        try:
            scorer_name = Scorers(scorer_name).name
        except ValueError:
            pass

        _logger.debug(f"Scorer job {job.id} has scorer {scorer_name}.")

        if JobStatus.is_incomplete(job.status):
            print(f"{scorer_name.lstrip('_')}: Computing 🚧")
        elif JobStatus.is_failed(job.status):
            print(f"{scorer_name.lstrip('_')}: Failed ❌, error was: {job.error_message}")
        else:
            print(f"{scorer_name.lstrip('_')}: Done ✅")


def job_progress(job_id: str, project_id: str, run_id: str) -> UUID4:
    """Monitors the progress of a job and displays a progress bar.

    Args:
        job_id: The unique identifier of the job to monitor.
        project_id: The unique identifier of the project.
        run_id: The unique identifier of the run.

    Returns:
        The unique identifier of the completed job.
    """
    job_status = get_job(job_id)
    backoff = random.random()

    if JobStatus.is_incomplete(job_status.status):
        job_progress_bar = tqdm(total=job_status.steps_total, position=0, leave=True, desc=job_status.progress_message)
        while JobStatus.is_incomplete(job_status.status):
            sleep(backoff)
            job_status = get_job(job_id)
            job_progress_bar.set_description(job_status.progress_message)
            job_progress_bar.update(job_status.steps_completed - job_progress_bar.n)
            backoff = random.random()
        job_progress_bar.close()

    _logger.debug(f"Job {job_id} status: {job_status.status}.")
    if JobStatus.is_failed(job_status.status):
        raise ValueError(f"Job failed with error message {job_status.error_message}.") from None

    print("Initial job complete, executing scorers asynchronously. Current status:")
    scorer_jobs_status(project_id=project_id, run_id=run_id)
    return job_status.id
