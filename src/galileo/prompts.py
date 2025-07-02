import builtins
import logging
import warnings
from typing import Optional, Union, overload

from galileo import Message
from galileo.base import BaseClientModel
from galileo.projects import Projects
from galileo.resources.api.prompts import (
    create_global_prompt_template_templates_post,
    create_prompt_template_with_version_projects_project_id_templates_post,
    delete_global_template_templates_template_id_delete,
    get_global_template_templates_template_id_get,
    get_global_template_version_templates_template_id_versions_version_get,
    get_project_templates_projects_project_id_templates_get,
    get_template_from_project_projects_project_id_templates_template_id_get,
    query_templates_templates_query_post,
)
from galileo.resources.models import (
    BasePromptTemplateResponse,
    BasePromptTemplateVersionResponse,
    CreatePromptTemplateWithVersionRequestBody,
    HTTPValidationError,
    ListPromptTemplateParams,
    PromptTemplateNameFilter,
    PromptTemplateNameFilterOperator,
)
from galileo.resources.types import Unset
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
                created_at=prompt_template.created_at,
                creator=prompt_template.creator,
                id=prompt_template.id,
                max_version=prompt_template.max_version,
                name=prompt_template.name,
                selected_version=prompt_template.selected_version,
                selected_version_id=prompt_template.selected_version_id,
                template=prompt_template.template,
                total_versions=prompt_template.total_versions,
                updated_at=prompt_template.updated_at,
                all_versions=prompt_template.all_versions,
                permissions=prompt_template.permissions,
            )
            self.additional_properties = prompt_template.additional_properties.copy()


class PromptTemplateVersion(BasePromptTemplateVersionResponse):
    def __init__(self, prompt_template_version: Union[None, BasePromptTemplateVersionResponse] = None):
        if prompt_template_version is not None:
            super().__init__(
                id=prompt_template_version.id,
                lines_added=prompt_template_version.lines_added,
                lines_edited=prompt_template_version.lines_edited,
                lines_removed=prompt_template_version.lines_removed,
                model_changed=prompt_template_version.model_changed,
                settings=prompt_template_version.settings,
                settings_changed=prompt_template_version.settings_changed,
                template=prompt_template_version.template,
                version=prompt_template_version.version,
                output_type=prompt_template_version.output_type,
                raw=prompt_template_version.raw,
                created_at=prompt_template_version.created_at,
                updated_at=prompt_template_version.updated_at,
            )
            self.additional_properties = prompt_template_version.additional_properties.copy()


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

        body = CreatePromptTemplateWithVersionRequestBody(name=name, template=template)  # type: ignore[arg-type]

        _logger.debug(f"{body}")
        response = create_prompt_template_with_version_projects_project_id_templates_post.sync_detailed(
            project_id=project.id,
            client=self.client,  # type: ignore[arg-type]
            body=body,  # type: ignore[arg-type]
        )

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        return PromptTemplate(prompt_template=response.parsed)


class GlobalPromptTemplates(BaseClientModel):
    def list(
        self, *, name_filter: Optional[str] = None, limit: Union[Unset, int] = 100, starting_token: int = 0
    ) -> list[PromptTemplate]:
        params = ListPromptTemplateParams()
        if name_filter:
            params.filters = [
                PromptTemplateNameFilter(operator=PromptTemplateNameFilterOperator.CONTAINS, value=name_filter)
            ]

        response = query_templates_templates_query_post.sync(
            client=self.client, body=params, limit=limit, starting_token=starting_token
        )

        if not response or isinstance(response, HTTPValidationError):
            return []

        if hasattr(response, "templates") and response.templates:
            return [PromptTemplate(prompt_template=template) for template in response.templates]

        return []

    @overload
    def get(self, *, template_id: str) -> Optional[PromptTemplate]: ...

    @overload
    def get(self, *, name: str) -> Optional[PromptTemplate]: ...

    def get(self, *, template_id: Optional[str] = None, name: Optional[str] = None) -> Optional[PromptTemplate]:
        if (template_id is None) and (name is None):
            raise ValueError("Exactly one of 'template_id' or 'name' must be provided")

        if (template_id is not None) and (name is not None):
            raise ValueError("Exactly one of 'template_id' or 'name' must be provided")

        if template_id:
            _logger.debug(f"Get global template {template_id}")
            template = get_global_template_templates_template_id_get.sync(template_id=template_id, client=self.client)

            if not template or isinstance(template, HTTPValidationError):
                return None

            return PromptTemplate(prompt_template=template)

        if name:
            templates = self.list(name_filter=name, limit=1)
            for template in templates:
                if template.name == name:
                    return template
            return None

        return None

    @overload
    def delete(self, *, template_id: str) -> None: ...

    @overload
    def delete(self, *, name: str) -> None: ...

    def delete(self, *, template_id: Optional[str] = None, name: Optional[str] = None) -> None:
        if (template_id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        if name:
            template = self.get(name=name)
            if not template:
                raise ValueError(f"Global template '{name}' not found")
            template_id = template.id

        if template_id:
            delete_global_template_templates_template_id_delete.sync(client=self.client, template_id=template_id)

    def get_version(self, *, template_id: str, version: int) -> Optional[PromptTemplateVersion]:
        _logger.debug(f"Get global template {template_id} version {version}")
        template_version = get_global_template_version_templates_template_id_versions_version_get.sync(
            template_id=template_id, version=version, client=self.client
        )

        if not template_version or isinstance(template_version, HTTPValidationError):
            return None

        return PromptTemplateVersion(prompt_template_version=template_version)

    def create(self, name: str, template: Union[builtins.list[Message], str]) -> PromptTemplate:
        body = CreatePromptTemplateWithVersionRequestBody(name=name, template=template)

        _logger.debug(f"Creating global template: {body}")
        response = create_global_prompt_template_templates_post.sync_detailed(client=self.client, body=body)

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        return PromptTemplate(prompt_template=response.parsed)


def create_prompt_template(name: str, project: str, messages: Union[list[Message], str]) -> Optional[PromptTemplate]:
    warnings.warn("create_prompt_template is deprecated, use create_prompt instead.", DeprecationWarning, stacklevel=2)
    return PromptTemplates().create(name=name, project_name=project, template=messages)


def get_prompt_template(project: str, name: str) -> Optional[PromptTemplate]:
    warnings.warn("get_prompt_template is deprecated, use get_prompt instead.", DeprecationWarning, stacklevel=2)
    prompt_templates = PromptTemplates().list(project_name=project)
    for prompt_template in prompt_templates:
        if prompt_template.name == name:
            _logger.info(f"Get template {prompt_template}")
            return prompt_template
    _logger.warning(f"Template {name} not found in project {project}")
    return None


def list_prompt_templates(project: str) -> list[PromptTemplate]:
    warnings.warn("list_prompt_templates is deprecated, use get_prompts instead.", DeprecationWarning, stacklevel=2)
    return PromptTemplates().list(project_name=project)


@overload
def get_prompt(*, id: str) -> Optional[PromptTemplateVersion]: ...


@overload
def get_prompt(*, name: str) -> Optional[PromptTemplateVersion]: ...


def get_prompt(
    *, id: Optional[str] = None, name: Optional[str] = None, version: Optional[int] = None
) -> Optional[PromptTemplateVersion]:
    """
    Retrieves a specific global prompt template version.

    You must provide either 'id' or 'name', but not both.
    If 'version' is not provided, the currently selected version is returned.
    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to retrieve. Defaults to None.
    name : str, optional
        The name of the template to retrieve. Defaults to None.
    version : int, optional
        The version number to retrieve. If not provided, the currently selected version is returned. Defaults to None.
    Returns
    -------
    Optional[PromptTemplateVersion]
        The template version if found, None otherwise.
    Raises
    ------
    ValueError
        If neither or both 'id' and 'name' are provided.
    """
    if (id is None) and (name is None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if (id is not None) and (name is not None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if version is not None:
        target_id = id
        if name:
            prompt_template = GlobalPromptTemplates().get(name=name)
            if not prompt_template:
                return None
            target_id = prompt_template.id

        if not target_id:
            raise ValueError("A template id is required to fetch a specific version.")

        return GlobalPromptTemplates().get_version(template_id=target_id, version=version)

    prompt_template = GlobalPromptTemplates().get(template_id=id) if id else GlobalPromptTemplates().get(name=name)  # type: ignore[arg-type]

    if not prompt_template or isinstance(prompt_template.selected_version, Unset):
        return None

    return PromptTemplateVersion(prompt_template_version=prompt_template.selected_version)


@overload
def delete_prompt(*, id: str) -> None: ...


@overload
def delete_prompt(*, name: str) -> None: ...


def delete_prompt(*, id: Optional[str] = None, name: Optional[str] = None) -> None:
    """
    Delete a global prompt template by ID or name.

    Parameters
    ----------
    id : str
        The unique identifier of the template to delete. Defaults to None.
    name : str
        The name of the template to delete. Defaults to None.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If neither or both id and name are provided, or if the template is not found.
    """
    return GlobalPromptTemplates().delete(template_id=id, name=name)  # type: ignore[call-overload]


def create_prompt(name: str, template: Union[list[Message], str]) -> PromptTemplate:
    """
    Create a new global prompt template.

    Parameters
    ----------
    name : str
        The name for the new template.
    template : Union[list[Message], str]
        The template content. Can be either a list of Message objects or a JSON string
        representing the message structure.

    Returns
    -------
    PromptTemplate
        The created prompt template.

    Raises
    ------
    PromptTemplateAPIException
        If the API request fails or returns an error.
    """
    return GlobalPromptTemplates().create(name=name, template=template)


def get_prompts(name_filter: Optional[str] = None, limit: Union[Unset, int] = 100) -> list[PromptTemplate]:
    """
    List global prompt templates with optional filtering.

    Parameters
    ----------
    name_filter : Optional[str], optional
        Filter templates by name containing this string. Defaults to None (no filtering).
    limit : Union[Unset, int], optional
        Maximum number of templates to return. Defaults to 100.

    Returns
    -------
    list[PromptTemplate]
        List of prompt templates matching the criteria.

    Examples
    --------
    >>> # List all global templates
    >>> templates = get_prompts()

    >>> # List templates with names containing "assistant"
    >>> templates = get_prompts(name_filter="assistant")

    >>> # List first 10 templates
    >>> templates = get_prompts(limit=10)
    """
    return GlobalPromptTemplates().list(name_filter=name_filter, limit=limit)
