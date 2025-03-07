from galileo.base import BaseClientModel
from galileo.resources.api.jobs import create_job_jobs_post
from galileo.resources.models import CreateJobRequest, TaskType


class Job(BaseClientModel):
    def create(self, project_id: str, name: str, run_id: str, prompt_template_id: str, task_type: TaskType):
        body = CreateJobRequest(
            project_id=project_id,
            job_name=name,
            run_id=run_id,
            prompt_template_version_id=prompt_template_id,
            task_type=task_type,
            # prompt_settings=PromptRunSettings()
        )
        return create_job_jobs_post.sync(client=self.client, body=body)
