import logging

from galileo.config import GalileoPythonConfig
from galileo.resources.api.jobs import create_job_jobs_post
from galileo.resources.models import (
    CreateJobRequest,
    CreateJobResponse,
    HTTPValidationError,
    PromptRunSettings,
    ScorerConfig,
    TaskType,
)
from galileo.utils.exceptions import _format_http_validation_error

_logger = logging.getLogger(__name__)


class Jobs:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def create(
        self,
        project_id: str,
        name: str,
        run_id: str,
        dataset_id: str,
        prompt_template_id: str | None,
        task_type: TaskType,
        scorers: list[ScorerConfig] | None,
        prompt_settings: PromptRunSettings | None,
    ) -> CreateJobResponse:
        create_params: dict = {
            "project_id": project_id,
            "dataset_id": dataset_id,
            "job_name": name,
            "run_id": run_id,
            "task_type": task_type,
            "scorers": scorers,
        }
        if prompt_template_id is not None:
            create_params["prompt_template_version_id"] = prompt_template_id
        if prompt_settings is not None:
            create_params["prompt_settings"] = prompt_settings
        _logger.info(f"create job: {create_params}")
        result = create_job_jobs_post.sync_detailed(
            client=self.config.api_client, body=CreateJobRequest(**create_params)
        )
        if not result.parsed or not isinstance(result.parsed, CreateJobResponse):
            if isinstance(result.parsed, HTTPValidationError):
                raise ValueError(_format_http_validation_error(result.parsed))
            raise ValueError(f"Create job failed (HTTP {result.status_code}): {result.content.decode(errors='ignore')}")
        return result.parsed
