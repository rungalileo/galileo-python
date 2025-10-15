import builtins
import logging
from typing import Optional, Union, overload

from galileo import Message
from galileo.config import GalileoPythonConfig
from galileo.resources.api.prompts import (
    create_global_prompt_template_templates_post,
    delete_global_template_templates_template_id_delete,
    get_global_template_templates_template_id_get,
    get_global_template_version_templates_template_id_versions_version_get,
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
from galileo.utils.projects import resolve_project_id
from galileo.utils.prompts import generate_unique_name

_logger = logging.getLogger(__name__)


class PromptTemplateAPIException(APIException):
    pass


class PromptTemplate(BasePromptTemplateResponse):
    def __init__(self, prompt_template: Union[None, BasePromptTemplateResponse] = None):
        """Initialize a PromptTemplate instance."""
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
        resolved_project_id = resolve_project_id(
            project_id=project_id, project_name=project_name, allow_none=True, validate=False
        )

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
        resolved_project_id = resolve_project_id(
            project_id=project_id, project_name=project_name, allow_none=True, validate=False
        )

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


def get_prompt(
    *,
    id: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> Optional[PromptTemplate]:
    """
    Retrieves a global prompt template.

    You must provide either 'id' or 'name', but not both.

    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to retrieve. Defaults to None.
    name : str, optional
        The name of the template to retrieve. Defaults to None.
    project_id : str, optional
        Use get_prompts(project_id=...) to filter templates by project. Defaults to None.
    project_name : str, optional
        Use get_prompts(project_name=...) to filter templates by project. Defaults to None.

    Returns
    -------
    Optional[PromptTemplate]
        The template if found, None otherwise.

    Raises
    ------
    ValueError
        If neither or both 'id' and 'name' are provided.
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


def delete_prompt(
    *,
    id: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
) -> None:
    """
    Delete a global prompt template by ID or name.

    You must provide either 'id' or 'name', but not both.

    Parameters
    ----------
    id : str, optional
        The unique identifier of the template to delete. Defaults to None.
    name : str, optional
        The name of the template to delete. Defaults to None.
    project_id : str, optional
    project_name : str, optional

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If neither or both id and name are provided, or if the template is not found.
    """

    # Validate template identifier
    if (id is None) and (name is None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    if (id is not None) and (name is not None):
        raise ValueError("Exactly one of 'id' or 'name' must be provided")

    # Delete global template
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


def create_prompt_template(name: str, project: str, messages: builtins.list[Message]) -> PromptTemplate:
    """
    Create a new global prompt template.

    Parameters
    ----------
    name : str
        The name for the new template.
    project : str
        The project name to associate with this template.
    messages : list[Message]
        The template content as a list of Message objects.

    Returns
    -------
    PromptTemplate
        The created prompt template.

    Raises
    ------
    PromptTemplateAPIException
        If the API request fails or returns an error.
    ValueError
        If project doesn't exist.
    """
    return create_prompt(name=name, project_name=project, template=messages)


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
    """
    # Resolve project parameters early (validates and converts project_name to project_id)
    # This will raise ValueError if both are provided or if project_name doesn't exist
    resolved_project_id = resolve_project_id(
        project_id=project_id, project_name=project_name, allow_none=True, validate=False
    )

    # Generate a unique name to ensure organization-wide uniqueness
    unique_name = generate_unique_name(name)

    # Create a global template with the unique name and resolved project_id
    # Pass only project_id to avoid duplicate resolution
    return GlobalPromptTemplates().create(
        name=unique_name, template=template, project_id=resolved_project_id, project_name=None
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
