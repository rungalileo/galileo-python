import builtins
import logging
import warnings
from typing import Optional, Union, overload

from galileo import Message
from galileo.config import GalileoPythonConfig
from galileo.projects import Project, Projects
from galileo.resources.api.projects import get_projects_paginated_projects_paginated_post
from galileo.resources.api.prompts import (
    create_global_prompt_template_templates_post,
    create_prompt_template_with_version_projects_project_id_templates_post,
    delete_global_template_templates_template_id_delete,
    delete_template_projects_project_id_templates_template_id_delete,
    get_global_template_templates_template_id_get,
    get_global_template_version_templates_template_id_versions_version_get,
    get_project_templates_projects_project_id_templates_get,
    get_template_from_project_projects_project_id_templates_template_id_get,
    query_templates_templates_query_post,
    render_template_render_template_post,
    update_global_template_templates_template_id_patch,
)
from galileo.resources.models import (
    BasePromptTemplateResponse,
    BasePromptTemplateVersionResponse,
    CreatePromptTemplateWithVersionRequestBody,
    DatasetData,
    HTTPValidationError,
    ListPromptTemplateParams,
    ProjectCollectionParams,
    ProjectType,
    ProjectTypeFilter,
    ProjectTypeFilterOperator,
    PromptTemplateNameFilter,
    PromptTemplateNameFilterOperator,
    RenderTemplateRequest,
    RenderTemplateResponse,
    StringData,
    UpdatePromptTemplateRequest,
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
                created_by_user=prompt_template.created_by_user,
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
                content_changed=prompt_template_version.content_changed,
                created_at=prompt_template_version.created_at,
                created_by_user=prompt_template_version.created_by_user,
                id=prompt_template_version.id,
                lines_added=prompt_template_version.lines_added,
                lines_edited=prompt_template_version.lines_edited,
                lines_removed=prompt_template_version.lines_removed,
                model_changed=prompt_template_version.model_changed,
                settings=prompt_template_version.settings,
                settings_changed=prompt_template_version.settings_changed,
                template=prompt_template_version.template,
                updated_at=prompt_template_version.updated_at,
                version=prompt_template_version.version,
                output_type=prompt_template_version.output_type,
                raw=prompt_template_version.raw,
            )
            self.additional_properties = prompt_template_version.additional_properties.copy()


class PromptTemplates:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def list(self, project_name: str) -> list[PromptTemplate]:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project {project_name} does not exist")

        templates = get_project_templates_projects_project_id_templates_get.sync(
            # TODO: remove type ignore, when migrated to proper AuthenticatedClient
            project_id=project.id,
            client=self.config.api_client,
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
            client=self.config.api_client,
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
            project_id=project.id, client=self.config.api_client, body=body
        )

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        return PromptTemplate(prompt_template=response.parsed)


class GlobalPromptTemplates:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def list(
        self, *, name_filter: Optional[str] = None, limit: Union[Unset, int] = 100, starting_token: int = 0
    ) -> list[PromptTemplate]:
        params = ListPromptTemplateParams()
        if name_filter:
            params.filters = [
                PromptTemplateNameFilter(operator=PromptTemplateNameFilterOperator.CONTAINS, value=name_filter)
            ]

        response = query_templates_templates_query_post.sync(
            client=self.config.api_client, body=params, limit=limit, starting_token=starting_token
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
            template = get_global_template_templates_template_id_get.sync(
                template_id=template_id, client=self.config.api_client
            )

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
            delete_global_template_templates_template_id_delete.sync(
                client=self.config.api_client, template_id=template_id
            )

    def get_version(self, *, template_id: str, version: int) -> Optional[PromptTemplateVersion]:
        _logger.debug(f"Get global template {template_id} version {version}")
        template_version = get_global_template_version_templates_template_id_versions_version_get.sync(
            template_id=template_id, version=version, client=self.config.api_client
        )

        if not template_version or isinstance(template_version, HTTPValidationError):
            return None

        return PromptTemplateVersion(prompt_template_version=template_version)

    def create(self, name: str, template: Union[builtins.list[Message], str]) -> PromptTemplate:
        body = CreatePromptTemplateWithVersionRequestBody(name=name, template=template)

        _logger.debug(f"Creating global template: {body}")
        response = create_global_prompt_template_templates_post.sync_detailed(client=self.config.api_client, body=body)

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        return PromptTemplate(prompt_template=response.parsed)

    def update(self, *, template_id: str, name: str) -> PromptTemplate:
        """
        Update a global prompt template.

        Parameters
        ----------
        template_id : str
            The ID of the template to update.
        name : str
            The new name for the template.

        Returns
        -------
        PromptTemplate
            The updated prompt template.

        Raises
        ------
        PromptTemplateAPIException
            If the API request fails or returns an error.
        """
        body = UpdatePromptTemplateRequest(name=name)

        _logger.debug(f"Updating global template {template_id}: {body}")
        response = update_global_template_templates_template_id_patch.sync_detailed(
            template_id=template_id, client=self.config.api_client, body=body
        )

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        return PromptTemplate(prompt_template=response.parsed)

    def render_template(
        self,
        *,
        template: str,
        data: Union[DatasetData, StringData],
        starting_token: Union[Unset, int] = 0,
        limit: Union[Unset, int] = 100,
    ) -> RenderTemplateResponse:
        """
        Render a template with provided data.

        Parameters
        ----------
        template : str
            The template string to render.
        data : Union[DatasetData, StringData]
            The data to use for rendering the template. Can be either dataset data or string data.
        starting_token : Union[Unset, int], optional
            Starting token for pagination. Defaults to 0.
        limit : Union[Unset, int], optional
            Maximum number of rendered templates to return. Defaults to 100.

        Returns
        -------
        Optional[RenderTemplateResponse]
            The rendered template response if successful, None otherwise.

        Raises
        ------
        PromptTemplateAPIException
            If the API request fails or returns an error.
        """
        body = RenderTemplateRequest(template=template, data=data)

        _logger.debug(f"Rendering template: {template}")
        response = render_template_render_template_post.sync_detailed(
            client=self.config.api_client, body=body, starting_token=starting_token, limit=limit
        )

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        return response.parsed


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
def get_prompt(*, id: str, project_id: str) -> Optional[PromptTemplate]: ...


@overload
def get_prompt(*, id: str, project_name: str) -> Optional[PromptTemplate]: ...


@overload
def get_prompt(*, id: str) -> Optional[PromptTemplate]: ...


@overload
def get_prompt(*, name: str, project_id: str) -> Optional[PromptTemplate]: ...


@overload
def get_prompt(*, name: str, project_name: str) -> Optional[PromptTemplate]: ...


@overload
def get_prompt(*, name: str) -> Optional[PromptTemplate]: ...


def get_prompt(
    *,
    id: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> Optional[PromptTemplate]:
    """
    Retrieves a prompt template (global or project-specific).

    You must provide either 'id' or 'name', but not both. Optionally provide
    'project_id' or 'project_name' to retrieve a project-specific template.

    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to retrieve. Defaults to None.
    name : str, optional
        The name of the template to retrieve. Defaults to None.
    project_id : str, optional
        The ID of the project to retrieve the template from. If not provided,
        retrieves a global template. Mutually exclusive with project_name.
    project_name : str, optional
        The name of the project to retrieve the template from. If not provided,
        retrieves a global template. Mutually exclusive with project_id.

    Returns
    -------
    Optional[PromptTemplate]
        The template if found, None otherwise.

    Raises
    ------
    ValueError
        If neither or both 'id' and 'name' are provided, if both project_id and
        project_name are provided, or if the specified project does not exist.

    Examples
    --------
    >>> # Get global template by ID
    >>> template = get_prompt(id="template-id-123")

    >>> # Get global template by name
    >>> template = get_prompt(name="my-template")

    >>> # Get project-specific template by ID
    >>> template = get_prompt(id="template-id-123", project_name="My Project")

    >>> # Get project-specific template by name
    >>> template = get_prompt(name="my-template", project_id="project-id-456")
    """
    # Validate template identifier
    if (id is None) and (name is None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if (id is not None) and (name is not None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    # Validate project identifier
    if project_id is not None and project_name is not None:
        raise ValueError("Only one of 'project_id' or 'project_name' can be provided, not both")

    # If a project is specified, get project-specific template
    if project_id is not None or project_name is not None:
        # Get the project to validate it exists
        project = Projects().get(id=project_id, name=project_name)
        if not project:
            identifier = project_id if project_id else project_name
            raise ValueError(f"Project '{identifier}' does not exist")

        if id:
            # Get by template ID
            _logger.debug(f"Get template {id} from project {project.id}")
            template = get_template_from_project_projects_project_id_templates_template_id_get.sync(
                project_id=project.id, template_id=id, client=GalileoPythonConfig.get().api_client
            )

            if not template or isinstance(template, HTTPValidationError):
                return None

            return PromptTemplate(prompt_template=template)
        # Get by template name - need to list all and find by name
        config = GalileoPythonConfig.get()
        templates_response = get_project_templates_projects_project_id_templates_get.sync(
            project_id=project.id, client=config.api_client
        )

        if not templates_response or isinstance(templates_response, HTTPValidationError):
            return None

        for template_data in templates_response:
            if template_data.name == name:
                return PromptTemplate(prompt_template=template_data)
        return None

    # Otherwise, get global template
    prompt_template = GlobalPromptTemplates().get(template_id=id) if id else GlobalPromptTemplates().get(name=name)  # type: ignore[arg-type]

    if not prompt_template:
        return None

    return PromptTemplate(prompt_template=prompt_template)


@overload
def delete_prompt(*, id: str, project_id: str) -> None: ...


@overload
def delete_prompt(*, id: str, project_name: str) -> None: ...


@overload
def delete_prompt(*, id: str) -> None: ...


@overload
def delete_prompt(*, name: str, project_id: str) -> None: ...


@overload
def delete_prompt(*, name: str, project_name: str) -> None: ...


@overload
def delete_prompt(*, name: str) -> None: ...


def delete_prompt(
    *,
    id: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> None:
    """
    Delete a prompt template (global or project-specific) by ID or name.

    You must provide either 'id' or 'name', but not both. Optionally provide
    'project_id' or 'project_name' to delete a project-specific template.

    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to delete. Defaults to None.
    name : str, optional
        The name of the template to delete. Defaults to None.
    project_id : str, optional
        The ID of the project containing the template. If not provided,
        deletes a global template. Mutually exclusive with project_name.
    project_name : str, optional
        The name of the project containing the template. If not provided,
        deletes a global template. Mutually exclusive with project_id.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If neither or both id and name are provided, if both project_id and
        project_name are provided, if the specified project does not exist,
        or if the template is not found.

    Examples
    --------
    >>> # Delete global template by ID
    >>> delete_prompt(id="template-id-123")

    >>> # Delete global template by name
    >>> delete_prompt(name="my-template")

    >>> # Delete project-specific template by ID
    >>> delete_prompt(id="template-id-123", project_name="My Project")

    >>> # Delete project-specific template by name
    >>> delete_prompt(name="my-template", project_id="project-id-456")
    """
    # Validate template identifier
    if (id is None) and (name is None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if (id is not None) and (name is not None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    # Validate project identifier
    if project_id is not None and project_name is not None:
        raise ValueError("Only one of 'project_id' or 'project_name' can be provided, not both")

    # If a project is specified, delete project-specific template
    if project_id is not None or project_name is not None:
        # Get the project to validate it exists
        project = Projects().get(id=project_id, name=project_name)
        if not project:
            identifier = project_id if project_id else project_name
            raise ValueError(f"Project '{identifier}' does not exist")

        # If name is provided, need to get the template ID first
        if name:
            # Get template by name without causing a double project lookup
            config = GalileoPythonConfig.get()
            templates_response = get_project_templates_projects_project_id_templates_get.sync(
                project_id=project.id, client=config.api_client
            )

            if not templates_response or isinstance(templates_response, HTTPValidationError):
                raise ValueError(f"Template '{name}' not found in project '{project.name}'")

            # Find template by name
            template_found = None
            for template_data in templates_response:
                if template_data.name == name:
                    template_found = template_data
                    break

            if not template_found:
                raise ValueError(f"Template '{name}' not found in project '{project.name}'")

            id = template_found.id

        # Delete the template
        _logger.debug(f"Deleting template {id} from project {project.id}")
        delete_template_projects_project_id_templates_template_id_delete.sync(
            project_id=project.id, template_id=id, client=GalileoPythonConfig.get().api_client
        )
        return None

    # Otherwise, delete global template
    return GlobalPromptTemplates().delete(template_id=id, name=name)  # type: ignore[call-overload]


@overload
def update_prompt(*, id: str, new_name: str) -> PromptTemplate: ...


@overload
def update_prompt(*, name: str, new_name: str) -> PromptTemplate: ...


def update_prompt(*, id: Optional[str] = None, name: Optional[str] = None, new_name: str) -> PromptTemplate:
    """
    Update a global prompt template by ID or name.

    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to update. Defaults to None.
    name : str, optional
        The name of the template to update. Defaults to None.
    new_name : str
        The new name for the template.

    Returns
    -------
    PromptTemplate
        The updated prompt template.

    Raises
    ------
    ValueError
        If neither or both id and name are provided, or if the template is not found.
    PromptTemplateAPIException
        If the API request fails or returns an error.

    Examples
    --------
    >>> # Update template by ID
    >>> template = update_prompt(id="template-id-123", new_name="new-name")

    >>> # Update template by existing name
    >>> template = update_prompt(name="old-name", new_name="new-name")
    """
    if (id is None) == (name is None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if id:
        return GlobalPromptTemplates().update(template_id=id, name=new_name)
    if name:
        template = GlobalPromptTemplates().get(name=name)
        if not template:
            raise ValueError(f"Global template '{name}' not found")
        return GlobalPromptTemplates().update(template_id=template.id, name=new_name)
    # Line won't be reached but mypy complains without this
    raise ValueError("Invalid state: neither id nor name is provided")


def _get_all_projects_paginated() -> list[Project]:
    """
    Get all projects using the paginated API.

    This replaces the deprecated get_all_projects_projects_all_get API.
    Fetches all projects across all pages.

    Returns
    -------
    list[Project]
        List of all projects.
    """
    config = GalileoPythonConfig.get()
    projects_list: list[Project] = []

    # Create filter for GEN_AI project type
    project_type_filter = ProjectTypeFilter(
        name="type", operator=ProjectTypeFilterOperator.EQ, value=ProjectType.GEN_AI
    )
    body = ProjectCollectionParams(filters=[project_type_filter])

    starting_token = 0
    limit = 100  # Fetch 100 at a time

    while True:
        try:
            response = get_projects_paginated_projects_paginated_post.sync(
                client=config.api_client, body=body, starting_token=starting_token, limit=limit
            )

            if not response or isinstance(response, HTTPValidationError):
                break

            # Add all projects from this page
            for project_data in response.projects:
                projects_list.append(Project(project=project_data))

            # Check if there are more pages
            if response.next_starting_token is None or isinstance(response.next_starting_token, Unset):
                break

            starting_token = response.next_starting_token

        except Exception as e:
            _logger.warning(f"Error fetching projects page: {e}")
            break

    _logger.debug(f"Fetched {len(projects_list)} projects using paginated API")
    return projects_list


def _check_name_exists_in_organization(name: str) -> bool:
    """
    Check if a prompt template name exists anywhere in the organization.

    Enforces organization-wide uniqueness by checking both global templates and
    all project-specific templates across all accessible projects.

    Parameters
    ----------
    name : str
        The template name to check.

    Returns
    -------
    bool
        True if the name exists anywhere, False otherwise.
    """
    # Check global templates
    global_templates = GlobalPromptTemplates().list(name_filter=name, limit=1000)
    for template in global_templates:
        if template.name == name:
            return True

    # Check all projects using paginated API
    projects = _get_all_projects_paginated()

    _logger.debug(f"Checking {len(projects)} projects for duplicate template name '{name}'")

    for project in projects:
        try:
            # Use the direct API call to avoid double project lookup
            config = GalileoPythonConfig.get()
            templates_response = get_project_templates_projects_project_id_templates_get.sync(
                project_id=project.id, client=config.api_client
            )

            if templates_response and not isinstance(templates_response, HTTPValidationError):
                for template_data in templates_response:
                    if template_data.name == name:
                        return True
        except Exception as e:
            # Skip projects we can't access
            _logger.debug(f"Unable to check templates in project {project.id}: {e}")
            continue

    return False


def _generate_unique_name(base_name: str) -> str:
    """
    Generate a unique template name by appending (N) if the base name exists.

    Ensures organization-wide uniqueness by checking all global and project templates.
    Automatically increments the suffix until a unique name is found.

    Parameters
    ----------
    base_name : str
        The desired template name.

    Returns
    -------
    str
        A unique name. Returns the original name if unique, otherwise appends (1), (2), etc.

    Examples
    --------
    - If "my-template" doesn't exist → returns "my-template"
    - If "my-template" exists → returns "my-template (1)"
    - If "my-template" and "my-template (1)" exist → returns "my-template (2)"
    """
    if not _check_name_exists_in_organization(base_name):
        return base_name

    counter = 1
    while True:
        candidate_name = f"{base_name} ({counter})"
        if not _check_name_exists_in_organization(candidate_name):
            _logger.info(f"Name '{base_name}' already exists. Using '{candidate_name}' instead.")
            return candidate_name
        counter += 1
        # Safety limit to prevent infinite loops
        if counter > 1000:
            raise ValueError(f"Unable to generate unique name for '{base_name}' after 1000 attempts")


@overload
def create_prompt(name: str, template: Union[list[Message], str], *, project_id: str) -> PromptTemplate: ...


@overload
def create_prompt(name: str, template: Union[list[Message], str], *, project_name: str) -> PromptTemplate: ...


@overload
def create_prompt(name: str, template: Union[list[Message], str]) -> PromptTemplate: ...


def create_prompt(
    name: str,
    template: Union[list[Message], str],
    *,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> PromptTemplate:
    """
    Create a new prompt template.

    Creates either a global prompt template (when no project is specified) or a
    project-specific prompt template (when project_id or project_name is provided).

    Parameters
    ----------
    name : str
        The name for the new template.
    template : Union[list[Message], str]
        The template content. Can be either a list of Message objects or a JSON string
        representing the message structure.
    project_id : str, optional
        The ID of the project to associate the template with. If provided, creates a
        project-specific template. Mutually exclusive with project_name.
    project_name : str, optional
        The name of the project to associate the template with. If provided, creates a
        project-specific template. Mutually exclusive with project_id.

    Returns
    -------
    PromptTemplate
        The created prompt template.

    Raises
    ------
    ValueError
        If both project_id and project_name are provided, or if the specified project
        does not exist.
    PromptTemplateAPIException
        If the API request fails or returns an error.

    Examples
    --------
    >>> # Create a global template
    >>> template = create_prompt(
    ...     name="helpful-assistant",
    ...     template=[Message(role=MessageRole.SYSTEM, content="You are helpful")]
    ... )

    >>> # Create a project-specific template by project name
    >>> template = create_prompt(
    ...     name="project-assistant",
    ...     template=[Message(role=MessageRole.SYSTEM, content="You are helpful")],
    ...     project_name="My Project"
    ... )

    >>> # Create a project-specific template by project ID
    >>> template = create_prompt(
    ...     name="project-assistant",
    ...     template=[Message(role=MessageRole.SYSTEM, content="You are helpful")],
    ...     project_id="project-id-123"
    ... )
    """
    # Validate that only one project identifier is provided
    if project_id is not None and project_name is not None:
        raise ValueError("Only one of 'project_id' or 'project_name' can be provided, not both")

    # Generate a unique name to ensure organization-wide uniqueness
    unique_name = _generate_unique_name(name)

    # If a project is specified, create a project-specific template
    if project_id is not None or project_name is not None:
        # Get the project to validate it exists and get its ID
        project = Projects().get(id=project_id, name=project_name)
        if not project:
            identifier = project_id if project_id else project_name
            raise ValueError(f"Project '{identifier}' does not exist")

        # Create the request body with the unique name
        body = CreatePromptTemplateWithVersionRequestBody(name=unique_name, template=template)

        # Make API call directly with the project ID
        config = GalileoPythonConfig.get()
        _logger.debug(f"Creating project template: {body}")
        response = create_prompt_template_with_version_projects_project_id_templates_post.sync_detailed(
            project_id=project.id, client=config.api_client, body=body
        )

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        if not response.parsed or isinstance(response.parsed, HTTPValidationError):
            _logger.error(response)
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

        return PromptTemplate(prompt_template=response.parsed)

    # Otherwise, create a global template with the unique name
    return GlobalPromptTemplates().create(name=unique_name, template=template)


def get_prompts(
    name_filter: Optional[str] = None,
    limit: Union[Unset, int] = 100,
    *,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> list[PromptTemplate]:
    """
    List prompt templates (global or project-specific) with optional filtering.

    Parameters
    ----------
    name_filter : Optional[str], optional
        Filter templates by name containing this string. Defaults to None (no filtering).
    limit : Union[Unset, int], optional
        Maximum number of templates to return. Defaults to 100.
    project_id : str, optional
        The ID of the project to list templates from. If not provided,
        lists global templates. Mutually exclusive with project_name.
    project_name : str, optional
        The name of the project to list templates from. If not provided,
        lists global templates. Mutually exclusive with project_id.

    Returns
    -------
    list[PromptTemplate]
        List of prompt templates matching the criteria.

    Raises
    ------
    ValueError
        If both project_id and project_name are provided, or if the specified
        project does not exist.

    Examples
    --------
    >>> # List all global templates
    >>> templates = get_prompts()

    >>> # List global templates with names containing "assistant"
    >>> templates = get_prompts(name_filter="assistant")

    >>> # List first 10 global templates
    >>> templates = get_prompts(limit=10)

    >>> # List all templates in a project by name
    >>> templates = get_prompts(project_name="My Project")

    >>> # List templates in a project by ID with name filter
    >>> templates = get_prompts(name_filter="assistant", project_id="project-id-123")
    """
    # Validate project identifier
    if project_id is not None and project_name is not None:
        raise ValueError("Only one of 'project_id' or 'project_name' can be provided, not both")

    # If a project is specified, list project-specific templates
    if project_id is not None or project_name is not None:
        # Get the project to validate it exists
        project = Projects().get(id=project_id, name=project_name)
        if not project:
            identifier = project_id if project_id else project_name
            raise ValueError(f"Project '{identifier}' does not exist")

        # List project templates directly using the API
        config = GalileoPythonConfig.get()
        templates_response = get_project_templates_projects_project_id_templates_get.sync(
            project_id=project.id, client=config.api_client
        )

        if not templates_response or isinstance(templates_response, HTTPValidationError):
            return []

        # Convert to PromptTemplate objects
        templates = [PromptTemplate(prompt_template=t) for t in templates_response]

        # Apply name filter if provided
        if name_filter:
            templates = [t for t in templates if name_filter.lower() in t.name.lower()]

        # Apply limit
        if not isinstance(limit, Unset):
            templates = templates[:limit]

        return templates

    # Otherwise, list global templates
    return GlobalPromptTemplates().list(name_filter=name_filter, limit=limit)


def render_template(
    *,
    template: str,
    data: Union[DatasetData, StringData, list[str], str],
    starting_token: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 100,
) -> RenderTemplateResponse:
    """
    Render a template with provided data.

    Parameters
    ----------
    template : str
        The template string to render.
    data : Union[DatasetData, StringData, list[str], str]
        The data to use for rendering the template. Can be:
        - DatasetData: Reference to a dataset
        - StringData: List of input strings
        - list[str]: List of input strings (will be converted to StringData)
        - str: Dataset ID (will be converted to DatasetData)
    starting_token : Union[Unset, int], optional
        Starting token for pagination. Defaults to 0.
    limit : Union[Unset, int], optional
        Maximum number of rendered templates to return. Defaults to 100.

    Returns
    -------
    Optional[RenderTemplateResponse]
        The rendered template response if successful, None otherwise.

    Raises
    ------
    PromptTemplateAPIException
        If the API request fails or returns an error.

    Examples
    --------
    >>> # Render template with string data
    >>> response = render_template(
    ...     template="Hello {{name}}!",
    ...     data=["Alice", "Bob", "Charlie"]
    ... )

    >>> # Render template with dataset
    >>> response = render_template(
    ...     template="Hello {{name}}!",
    ...     data="dataset-id-123"
    ... )
    """
    if isinstance(data, list):
        data = StringData(input_strings=data)
    elif isinstance(data, str):
        data = DatasetData(dataset_id=data)
    else:
        data = data

    return GlobalPromptTemplates().render_template(
        template=template, data=data, starting_token=starting_token, limit=limit
    )
