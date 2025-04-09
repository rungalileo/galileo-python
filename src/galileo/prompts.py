import builtins
import logging
from typing import Optional, Union

from galileo.base import BaseClientModel
from galileo.projects import Projects
from galileo.resources.api.prompts import (
    create_prompt_template_with_version_projects_project_id_templates_post,
    get_project_templates_projects_project_id_templates_get,
    get_template_from_project_projects_project_id_templates_template_id_get,
)
from galileo.resources.models import (
    BasePromptTemplateResponse,
    CreatePromptTemplateWithVersionRequestBody,
    HTTPValidationError,
    Message,
)
from galileo.utils.exceptions import APIException

_logger = logging.getLogger(__name__)


class PromptTemplateAPIException(APIException):
    pass


class PromptTemplate(BasePromptTemplateResponse):
    def __init__(self, prompt_template: Union[None, BasePromptTemplateResponse] = None):
        """
        Initialize a PromptTemplate instance.

        Parameters
        ----------
        prompt_template : Union[None, BasePromptTemplateResponse], optional
            The prompt template data to initialize from. If None, creates an empty prompt template instance.
            Defaults to None.
        """
        if prompt_template is not None:
            super().__init__(
                all_available_versions=prompt_template.all_available_versions,
                id=prompt_template.id,
                max_version=prompt_template.max_version,
                name=prompt_template.name,
                selected_version=prompt_template.selected_version,
                selected_version_id=prompt_template.selected_version_id,
                template=prompt_template.template,
                total_versions=prompt_template.total_versions,
                all_versions=prompt_template.all_versions,
            )
            self.additional_properties = prompt_template.additional_properties.copy()
            return


class PromptTemplates(BaseClientModel):
    def list(self, project_name: str) -> list[PromptTemplate]:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        templates = get_project_templates_projects_project_id_templates_get.sync(
            # TODO: remove type ignore, when migrated to proper AuthenticatedClient
            project_id=project.id,
            client=self.client,  # type: ignore[arg-type]
        )

        if not templates or isinstance(templates, HTTPValidationError):
            return []

        return [PromptTemplate(prompt_template=prompt_template) for prompt_template in templates]

    def get(self, *, project_name: str, template_id: str) -> Optional[PromptTemplate]:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        _logger.debug(f"Get template {template_id} from project {project.id}")
        template = get_template_from_project_projects_project_id_templates_template_id_get.sync(
            # TODO: remove type ignore, when migrated to proper AuthenticatedClient
            project_id=project.id,
            template_id=template_id,
            client=self.client,  # type: ignore[arg-type]
        )

        if not template or isinstance(template, HTTPValidationError):
            return None

        return PromptTemplate(prompt_template=template)

    def create(
        self, name: str, project_name: str, template: Union[builtins.list[Message], str]
    ) -> Optional[PromptTemplate]:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        body = CreatePromptTemplateWithVersionRequestBody(name=name, template=template)

        _logger.debug(f"{body}")
        response = create_prompt_template_with_version_projects_project_id_templates_post.sync_detailed(
            project_id=project.id,
            client=self.client,  # type: ignore[arg-type]
            body=body,
        )

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content)

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content)

        return PromptTemplate(prompt_template=response.parsed)


def create_prompt_template(name: str, project: str, messages: Union[list["Message"], str]) -> Optional[PromptTemplate]:
    return PromptTemplates().create(name=name, project_name=project, template=messages)


def get_prompt_template(project: str, name: str) -> Optional[PromptTemplate]:
    prompt_templates = PromptTemplates().list(project_name=project)
    for prompt_template in prompt_templates:
        if prompt_template.name == name:
            _logger.info(f"Get template {prompt_template}")
            return prompt_template
    raise ValueError(f"Prompt {name} does not exist")
