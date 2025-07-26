import logging
from typing import Optional

from galileo.base import BaseClientModel
from galileo.resources.api.jobs import create_job_jobs_post
from galileo.resources.models import CreateJobRequest, CreateJobResponse, PromptRunSettings, ScorerConfig, TaskType
from galileo_core.exceptions.http import GalileoHTTPException

_logger = logging.getLogger(__name__)


class Jobs(BaseClientModel):
    def create(
        self,
        project_id: str,
        name: str,
        run_id: str,
        dataset_id: str,
        prompt_template_id: str,
        task_type: TaskType,
        scorers: Optional[list[ScorerConfig]],
        prompt_settings: PromptRunSettings,
    ) -> CreateJobResponse:
        create_params = dict(
            project_id=project_id,
            dataset_id=dataset_id,
            job_name=name,
            run_id=run_id,
            prompt_settings=prompt_settings,
            prompt_template_version_id=prompt_template_id,
            task_type=task_type,
            scorers=scorers,
        )
        _logger.info(f"create job: {create_params}")
        result = create_job_jobs_post.sync_detailed(client=self.client, body=CreateJobRequest(**create_params))
        if not result.parsed or not isinstance(result.parsed, CreateJobResponse):
            raise GalileoHTTPException(
                message="Create job failed", status_code=result.status_code, response_text=str(result.content)
            )
        return result.parsed
