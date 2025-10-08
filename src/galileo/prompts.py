import builtins
import logging
from typing import Optional, Union, overload

from galileo import Message
from galileo.config import GalileoPythonConfig
from galileo.projects import Projects
from galileo.resources.api.prompts import (
    create_global_prompt_template_templates_post,
    delete_global_template_templates_template_id_delete,
    get_global_template_templates_template_id_get,
    get_global_template_version_templates_template_id_versions_version_get,
    query_templates_templates_query_post,
    render_template_render_template_post,
    update_global_template_templates_template_id_patch,
)
from galileo.resources.api.prompts.bulk_delete_global_templates_templates_bulk_delete_delete import (
    sync_detailed as bulk_delete_global_templates_sync_detailed,
)
from galileo.resources.models import (
    BasePromptTemplateResponse,
    BasePromptTemplateVersionResponse,
    BulkDeletePromptTemplatesRequest,
    CreatePromptTemplateWithVersionRequestBody,
    DatasetData,
    HTTPValidationError,
    ListPromptTemplateParams,
    PromptTemplateNameFilter,
    PromptTemplateNameFilterOperator,
    PromptTemplateUsedInProjectFilter,
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


def _resolve_project_id(project_id: Optional[str] = None, project_name: Optional[str] = None) -> Optional[str]:
    """
    Resolve project_name to project_id if needed.

    Parameters
    ----------
    project_id : Optional[str], optional
        The project ID. If provided, returns this directly.
    project_name : Optional[str], optional
        The project name. If provided, looks up the project ID.

    Returns
    -------
    Optional[str]
        The resolved project ID, or None if neither was provided.

    Raises
    ------
    ValueError
        If both project_id and project_name are provided, or if project_name doesn't exist.
    """
    if project_id and project_name:
        raise ValueError("Cannot provide both 'project_id' and 'project_name'")

    if project_name:
        project = Projects().get(name=project_name)
        if not project:
            raise ValueError(f"Project '{project_name}' not found")
        return project.id

    return project_id


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


class GlobalPromptTemplates:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def list(
        self,
        *,
        name_filter: Optional[str] = None,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
        limit: Union[Unset, int] = 100,
        starting_token: int = 0,
    ) -> builtins.list[PromptTemplate]:
        """
        List global prompt templates with optional filtering.

        Parameters
        ----------
        name_filter : Optional[str], optional
            Filter templates by name containing this string. Defaults to None.
        project_id : Optional[str], optional
            Filter templates by project ID. Returns templates used in the specified project. Defaults to None.
        project_name : Optional[str], optional
            Filter templates by project name. Returns templates used in the specified project. Defaults to None.
            Cannot be used together with project_id.
        limit : Union[Unset, int], optional
            Maximum number of templates to return. Defaults to 100.
        starting_token : int, optional
            Starting token for pagination. Defaults to 0.

        Returns
        -------
        list[PromptTemplate]
            List of prompt templates matching the criteria.

        Raises
        ------
        ValueError
            If both project_id and project_name are provided, or if project_name doesn't exist.
        """
        # Resolve project_name to project_id if needed
        resolved_project_id = _resolve_project_id(project_id=project_id, project_name=project_name)

        params = ListPromptTemplateParams()
        filters = []

        if name_filter:
            filters.append(
                PromptTemplateNameFilter(operator=PromptTemplateNameFilterOperator.CONTAINS, value=name_filter)
            )

        if resolved_project_id:
            filters.append(PromptTemplateUsedInProjectFilter(value=resolved_project_id))

        if filters:
            params.filters = filters

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
        """
        Delete a global prompt template by ID or name.

        Parameters
        ----------
        template_id : Optional[str], optional
            The unique identifier of the template to delete. Defaults to None.
        name : Optional[str], optional
            The name of the template to delete. Defaults to None.

        Raises
        ------
        ValueError
            If neither or both template_id and name are provided, or if the template is not found.
        """
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

    def bulk_delete(self, template_ids: builtins.list[str]) -> None:
        """
        Delete multiple global prompt templates in bulk.

        Parameters
        ----------
        template_ids : list[str]
            List of template IDs to delete (max 100).

        Raises
        ------
        PromptTemplateAPIException
            If the API request fails or returns an error.
        ValueError
            If the template_ids list is empty or contains more than 100 items.
        """
        if not template_ids:
            raise ValueError("template_ids list cannot be empty")

        if len(template_ids) > 100:
            raise ValueError("Cannot delete more than 100 templates at once")

        body = BulkDeletePromptTemplatesRequest(template_ids=template_ids)

        _logger.debug(f"Bulk deleting {len(template_ids)} templates")
        response = bulk_delete_global_templates_sync_detailed(client=self.config.api_client, body=body)

        if response.status_code != 200:
            raise PromptTemplateAPIException(response.content.decode("utf-8"))

    def get_version(self, *, template_id: str, version: int) -> Optional[PromptTemplateVersion]:
        _logger.debug(f"Get global template {template_id} version {version}")
        template_version = get_global_template_version_templates_template_id_versions_version_get.sync(
            template_id=template_id, version=version, client=self.config.api_client
        )

        if not template_version or isinstance(template_version, HTTPValidationError):
            return None

        return PromptTemplateVersion(prompt_template_version=template_version)

    def create(
        self,
        name: str,
        template: Union[builtins.list[Message], str],
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> PromptTemplate:
        """
        Create a new global prompt template.

        Parameters
        ----------
        name : str
            The name for the new template.
        template : Union[list[Message], str]
            The template content. Can be either a list of Message objects or a JSON string.
        project_id : Optional[str], optional
            The project ID to associate with this template. Defaults to None.
        project_name : Optional[str], optional
            The project name to associate with this template. Defaults to None.
            Cannot be used together with project_id.

        Returns
        -------
        PromptTemplate
            The created prompt template.

        Raises
        ------
        PromptTemplateAPIException
            If the API request fails or returns an error.
        ValueError
            If both project_id and project_name are provided, or if project_name doesn't exist.
        """
        # Resolve project_name to project_id if needed
        resolved_project_id = _resolve_project_id(project_id=project_id, project_name=project_name)

        body = CreatePromptTemplateWithVersionRequestBody(name=name, template=template)

        _logger.debug(f"Creating global template: {body} with project_id: {resolved_project_id}")
        response = create_global_prompt_template_templates_post.sync_detailed(
            client=self.config.api_client, body=body, project_id=resolved_project_id if resolved_project_id else Unset()
        )

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


@overload
def get_prompt(*, id: str) -> Optional[PromptTemplate]: ...


@overload
def get_prompt(*, name: str) -> Optional[PromptTemplate]: ...


def get_prompt(*, id: Optional[str] = None, name: Optional[str] = None) -> Optional[PromptTemplate]:
    """
    Retrieves a global prompt template.

    You must provide either 'id' or 'name', but not both.

    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to retrieve. Defaults to None.
    name : str, optional
        The name of the template to retrieve. Defaults to None.

    Returns
    -------
    Optional[PromptTemplate]
        The template if found, None otherwise.

    Raises
    ------
    ValueError
        If neither or both 'id' and 'name' are provided.

    Examples
    --------
    >>> # Get global template by ID
    >>> template = get_prompt(id="template-id-123")

    >>> # Get global template by name
    >>> template = get_prompt(name="my-template")
    """
    # Validate template identifier
    if (id is None) and (name is None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if (id is not None) and (name is not None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    # Get global template
    prompt_template = GlobalPromptTemplates().get(template_id=id) if id else GlobalPromptTemplates().get(name=name)  # type: ignore[arg-type]

    if not prompt_template:
        return None

    return PromptTemplate(prompt_template=prompt_template)


@overload
def delete_prompt(*, id: str) -> None: ...


@overload
def delete_prompt(*, name: str) -> None: ...


def delete_prompt(*, id: Optional[str] = None, name: Optional[str] = None) -> None:
    """
    Delete a global prompt template by ID or name.

    You must provide either 'id' or 'name', but not both.

    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to delete. Defaults to None.
    name : str, optional
        The name of the template to delete. Defaults to None.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If neither or both id and name are provided, or if the template is not found.

    Examples
    --------
    >>> # Delete global template by ID
    >>> delete_prompt(id="template-id-123")

    >>> # Delete global template by name
    >>> delete_prompt(name="my-template")
    """
    # Validate template identifier
    if (id is None) and (name is None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if (id is not None) and (name is not None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    # Delete global template
    return GlobalPromptTemplates().delete(template_id=id, name=name)  # type: ignore[call-overload]


def bulk_delete_prompts(template_ids: builtins.list[str]) -> None:
    """
    Delete multiple global prompt templates in bulk.

    This function provides efficient deletion of multiple templates at once.
    Maximum of 100 templates can be deleted in a single call.

    Parameters
    ----------
    template_ids : list[str]
        List of template IDs to delete (max 100).

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the template_ids list is empty or contains more than 100 items.
    PromptTemplateAPIException
        If the API request fails or returns an error.

    Examples
    --------
    >>> # Delete multiple templates by their IDs
    >>> bulk_delete_prompts(["template-id-1", "template-id-2", "template-id-3"])

    >>> # Delete up to 100 templates at once
    >>> template_ids = [template.id for template in get_prompts(limit=100)]
    >>> bulk_delete_prompts(template_ids)
    """
    return GlobalPromptTemplates().bulk_delete(template_ids=template_ids)


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


def _check_name_exists_in_organization(name: str) -> bool:
    """
    Check if a prompt template name exists in the organization.

    Enforces organization-wide uniqueness by checking global templates.

    Parameters
    ----------
    name : str
        The template name to check.

    Returns
    -------
    bool
        True if the name exists, False otherwise.
    """
    # Check global templates
    global_templates = GlobalPromptTemplates().list(name_filter=name, limit=1000)
    return any(template.name == name for template in global_templates)


def _generate_unique_name(base_name: str) -> str:
    """
    Generate a unique template name by appending (N) if the base name exists.

    Ensures organization-wide uniqueness by checking global templates.
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


def create_prompt(
    name: str,
    template: Union[builtins.list[Message], str],
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> PromptTemplate:
    """
    Create a new global prompt template.

    Parameters
    ----------
    name : str
        The name for the new template.
    template : Union[list[Message], str]
        The template content. Can be either a list of Message objects or a JSON string
        representing the message structure.
    project_id : Optional[str], optional
        The project ID to associate with this template. When provided, the template
        will be linked to the specified project. Defaults to None.
    project_name : Optional[str], optional
        The project name to associate with this template. When provided, the template
        will be linked to the specified project. Defaults to None.
        Cannot be used together with project_id.

    Returns
    -------
    PromptTemplate
        The created prompt template.

    Raises
    ------
    PromptTemplateAPIException
        If the API request fails or returns an error.
    ValueError
        If both project_id and project_name are provided, or if project_name doesn't exist.

    Examples
    --------
    >>> # Create a global template
    >>> template = create_prompt(
    ...     name="helpful-assistant",
    ...     template=[Message(role=MessageRole.SYSTEM, content="You are helpful")]
    ... )

    >>> # Create a global template associated with a project by ID
    >>> template = create_prompt(
    ...     name="project-assistant",
    ...     template=[Message(role=MessageRole.SYSTEM, content="You are helpful")],
    ...     project_id="project-123"
    ... )

    >>> # Create a global template associated with a project by name
    >>> template = create_prompt(
    ...     name="project-assistant",
    ...     template=[Message(role=MessageRole.SYSTEM, content="You are helpful")],
    ...     project_name="My Project"
    ... )
    """
    # Generate a unique name to ensure organization-wide uniqueness
    unique_name = _generate_unique_name(name)

    # Create a global template with the unique name and optional project association
    return GlobalPromptTemplates().create(
        name=unique_name, template=template, project_id=project_id, project_name=project_name
    )


def get_prompts(
    name_filter: Optional[str] = None,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
    limit: Union[Unset, int] = 100,
) -> builtins.list[PromptTemplate]:
    """
    List global prompt templates with optional filtering.

    Parameters
    ----------
    name_filter : Optional[str], optional
        Filter templates by name containing this string. Defaults to None (no filtering).
    project_id : Optional[str], optional
        Filter templates by project ID. Returns templates used in the specified project. Defaults to None.
    project_name : Optional[str], optional
        Filter templates by project name. Returns templates used in the specified project. Defaults to None.
        Cannot be used together with project_id.
    limit : Union[Unset, int], optional
        Maximum number of templates to return. Defaults to 100.

    Returns
    -------
    list[PromptTemplate]
        List of prompt templates matching the criteria.

    Raises
    ------
    ValueError
        If both project_id and project_name are provided, or if project_name doesn't exist.

    Examples
    --------
    >>> # List all global templates
    >>> templates = get_prompts()

    >>> # List global templates with names containing "assistant"
    >>> templates = get_prompts(name_filter="assistant")

    >>> # List first 10 global templates
    >>> templates = get_prompts(limit=10)

    >>> # List templates associated with a specific project by ID
    >>> templates = get_prompts(project_id="project-123")

    >>> # List templates associated with a specific project by name
    >>> templates = get_prompts(project_name="My Project")

    >>> # Combine filters
    >>> templates = get_prompts(name_filter="assistant", project_id="project-123", limit=50)
    """
    # List global templates with optional project filtering
    return GlobalPromptTemplates().list(
        name_filter=name_filter, project_id=project_id, project_name=project_name, limit=limit
    )


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
