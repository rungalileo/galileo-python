import logging
import random
from time import sleep
from typing import Optional

from pydantic import UUID4
from tqdm.auto import tqdm

from galileo.base import BaseClientModel
from galileo.resources.api.jobs import (
    get_job_jobs_job_id_get,
    get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get,
)
from galileo.resources.models import JobDB
from galileo_core.constants.job import JobStatus

_logger = logging.getLogger(__name__)


class Jobs(BaseClientModel):  # , DecorateAllMethods):
    def get(self, job_id: UUID4) -> JobDB:
        response = get_job_jobs_job_id_get.sync(client=self.client, job_id=str(job_id))
        if not isinstance(response, JobDB):
            raise ValueError(f"Failed to get job status for job {job_id}. Response: {response}")
        return response

    def get_scorer_jobs(self, project_id: UUID4, run_id: UUID4) -> list[JobDB]:
        response = get_jobs_for_project_run_projects_project_id_runs_run_id_jobs_get.sync(
            client=self.client, project_id=str(project_id), run_id=str(run_id)
        )
        print(f"get_scorer_jobs response: {response}")
        if not isinstance(response, list):
            _logger.warning(f"Failed to get scorer jobs for project {project_id}, run {run_id}. Response: {response}")
            return []
        # TODO keep the same enum filter for RunDefaults?
        # from rungalileo.schemas.content.jobs import JobName
        # JobName.log_stream_scorer / JobName.log_stream_run
        return [job for job in response if job.job_name == "log_stream_scorer"]  # RunDefaults.prompt_scorer_job_name]


def scorer_jobs_status(project_id: Optional[UUID4] = None, run_id: Optional[UUID4] = None) -> None:
    jobs_client = Jobs()
    scorer_jobs = jobs_client.get_scorer_jobs(project_id=project_id, run_id=run_id)
    for job in scorer_jobs:
        scorer_name = "scorer"
        # TODO No request data in the job? PQ expected it always
        if (
            "request_data" in job
            and "prompt_scorer_settings" in job.request_data
            and "scorer_name" in job.request_data["prompt_scorer_settings"]
        ):
            scorer_name = job.request_data["prompt_scorer_settings"]["scorer_name"]

        if JobStatus.is_incomplete(job.status):
            print(f"{scorer_name.lstrip('_')}: Computing 🚧")
        elif JobStatus.is_failed(job.status):
            print(f"{scorer_name.lstrip('_')}: Failed ❌, error was: {job.error_message}")
        else:
            # TODO do we expect scorer_name to be "scorer"?
            print(f"{scorer_name.lstrip('_')}: Done ✅")


def job_progress(job_id: UUID4, project_id: UUID4, run_id: UUID4) -> UUID4:
    jobs_client = Jobs()
    job_status = jobs_client.get(job_id)
    backoff = random.random()

    if JobStatus.is_incomplete(job_status.status):
        job_progress_bar = tqdm(total=job_status.steps_total, position=0, leave=True, desc=job_status.progress_message)
        while JobStatus.is_incomplete(job_status.status):
            sleep(backoff)
            job_status = jobs_client.get(job_id)
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
