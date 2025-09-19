import builtins
import mimetypes
import time
from typing import Any, Optional, Union, overload

from galileo.config import GalileoPythonConfig
from galileo.resources.api.datasets import (
    create_dataset_datasets_post,
    delete_dataset_datasets_dataset_id_delete,
    extend_dataset_content_datasets_extend_post,
    get_dataset_content_datasets_dataset_id_content_get,
    get_dataset_datasets_dataset_id_get,
    get_dataset_synthetic_extend_status_datasets_extend_dataset_id_get,
    get_dataset_version_content_datasets_dataset_id_versions_version_index_content_get,
    list_datasets_datasets_get,
    query_dataset_versions_datasets_dataset_id_versions_query_post,
    query_datasets_datasets_query_post,
    update_dataset_content_datasets_dataset_id_content_patch,
)
from galileo.resources.models import DatasetRow, ListDatasetVersionParams, ListDatasetVersionResponse
from galileo.resources.models.body_create_dataset_datasets_post import BodyCreateDatasetDatasetsPost
from galileo.resources.models.dataset_append_row import DatasetAppendRow
from galileo.resources.models.dataset_append_row_values import DatasetAppendRowValues
from galileo.resources.models.dataset_content import DatasetContent
from galileo.resources.models.dataset_db import DatasetDB
from galileo.resources.models.dataset_name_filter import DatasetNameFilter
from galileo.resources.models.dataset_name_filter_operator import DatasetNameFilterOperator
from galileo.resources.models.dataset_updated_at_sort import DatasetUpdatedAtSort
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.job_progress import JobProgress
from galileo.resources.models.list_dataset_params import ListDatasetParams
from galileo.resources.models.list_dataset_response import ListDatasetResponse
from galileo.resources.models.prompt_run_settings import PromptRunSettings
from galileo.resources.models.synthetic_data_types import SyntheticDataTypes
from galileo.resources.models.synthetic_dataset_extension_request import SyntheticDatasetExtensionRequest
from galileo.resources.models.synthetic_dataset_extension_response import SyntheticDatasetExtensionResponse
from galileo.resources.models.update_dataset_content_request import UpdateDatasetContentRequest
from galileo.resources.types import File, Unset
from galileo.schema.datasets import DatasetRecord
from galileo.utils.catch_log import DecorateAllMethods
from galileo.utils.exceptions import APIException
from galileo_core.utils.dataset import DatasetType, parse_dataset


class DatasetAPIException(APIException):
    pass


class Dataset(DecorateAllMethods):
    content: Optional[DatasetContent] = None
    config: GalileoPythonConfig

    def __init__(self, dataset_db: DatasetDB) -> None:
        self.dataset = dataset_db
        self.config = GalileoPythonConfig.get()

    def get_content(self) -> Union[None, DatasetContent]:
        """
        Gets and returns the content of the dataset.
        Also refreshes the content of the local dataset instance.

        Returns
        -------
        Union[None, DatasetContent]
            The content of the dataset

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if not self.dataset:
            return None

        content: DatasetContent = get_dataset_content_datasets_dataset_id_content_get.sync(
            client=self.config.api_client, dataset_id=self.dataset.id
        )

        self.content = content

        return content

    def _get_etag(self) -> Optional[str]:
        """
        ETag is returned in response headers of API endpoints of the format /datasets.*contents.*

        This is a required parameter to be passed along with all dataset update requests to ensure
        there isn't a version conflict during updates.
        """
        if not self.dataset:
            return None

        response = get_dataset_content_datasets_dataset_id_content_get.sync_detailed(
            client=self.config.api_client, dataset_id=self.dataset.id
        )

        return response.headers.get("ETag")

    def add_rows(self, row_data: list[dict[str, Any]]) -> "Dataset":
        """
        Adds rows to the dataset.

        Parameters
        ----------
        row_data : List[Dict[str, Any]]
            The rows to add to the dataset.

        Returns
        -------
        Dataset
            The updated dataset with the new rows.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        append_rows: list[DatasetAppendRow] = [
            DatasetAppendRow(values=DatasetAppendRowValues.from_dict(row)) for row in row_data
        ]
        request = UpdateDatasetContentRequest(edits=append_rows)
        response = update_dataset_content_datasets_dataset_id_content_patch.sync(
            client=self.config.api_client, dataset_id=self.dataset.id, body=request, if_match=self._get_etag()
        )
        if isinstance(response, HTTPValidationError):
            raise DatasetAPIException("Request to add new rows to dataset failed.")

        # Refresh the content
        self.get_content()

        return self

    def get_version_history(self) -> Optional[Union[HTTPValidationError, ListDatasetVersionResponse]]:
        list_dataset = query_dataset_versions_datasets_dataset_id_versions_query_post.sync(
            dataset_id=self.dataset.id, client=self.config.api_client, body=ListDatasetVersionParams()
        )
        return list_dataset

    def load_version(self, version_index: int) -> DatasetContent:
        return get_dataset_version_content_datasets_dataset_id_versions_version_index_content_get.sync(
            dataset_id=self.dataset.id, version_index=version_index, client=self.config.api_client
        )

    def __getattr__(self, attr: str) -> Any:
        """
        Delegate attribute access to the underlying DatasetDB instance.
        """
        return getattr(self.dataset, attr)


class Datasets:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def list(self, limit: Union[Unset, int] = 100) -> list[Dataset]:
        """
        Lists all datasets.

        Parameters
        ----------
        limit : Union[Unset, int]
            The maximum number of datasets to return. Default is 100.

        Returns
        -------
        List[Dataset]
            A list of datasets.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        datasets: ListDatasetResponse = list_datasets_datasets_get.sync(client=self.config.api_client, limit=limit)
        return [Dataset(dataset_db=dataset) for dataset in datasets.datasets] if datasets else []

    @overload
    def get(self, *, id: str, with_content: bool = False) -> Optional[Dataset]: ...
    @overload
    @overload
    def get(self, *, name: str, with_content: bool = False) -> Optional[Dataset]: ...
    def get(
        self, *, id: Optional[str] = None, name: Optional[str] = None, with_content: bool = False
    ) -> Optional[Dataset]:
        """
        Retrieves a dataset by id or name (exactly one of `id` or `name` must be provided).

        Parameters
        ----------
        id : str
            The id of the dataset.
        name : str
            The name of the dataset.
        with_content : bool
            Whether to return the content of the dataset. Default is False.

        Returns
        -------
        Dataset
            The dataset.

        Raises
        ------
        ValueError
            If neither or both `id` and `name` are provided.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if (id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        if id:
            dataset_response = get_dataset_datasets_dataset_id_get.sync(client=self.config.api_client, dataset_id=id)
            if not dataset_response:
                return None
            dataset = Dataset(dataset_db=dataset_response)

        elif name:
            filter = DatasetNameFilter(operator=DatasetNameFilterOperator.EQ, value=name)
            params = ListDatasetParams(filters=[filter], sort=DatasetUpdatedAtSort(ascending=False))
            datasets_response: ListDatasetResponse = query_datasets_datasets_query_post.sync(
                client=self.config.api_client, body=params, limit=1
            )

            if not datasets_response or len(datasets_response.datasets) == 0:
                return None

            dataset = Dataset(dataset_db=datasets_response.datasets[0])

        if with_content:
            dataset.get_content()
        return dataset

    @overload
    def delete(self, *, id: str) -> None: ...
    @overload
    def delete(self, *, name: str) -> None: ...
    def delete(self, *, id: Optional[str] = None, name: Optional[str] = None) -> None:
        """
        Deletes a dataset by id or name.

        Parameters
        ----------
        id : str
            The id of the dataset.
        name : str
            The name of the dataset.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if (id is None) == (name is None):
            raise ValueError("Exactly one of 'id' or 'name' must be provided")

        dataset = self.get(id=id, name=name)  # type: ignore[call-overload]

        if not dataset:
            raise ValueError(f"Dataset {name} not found")
        return delete_dataset_datasets_dataset_id_delete.sync(client=self.config.api_client, dataset_id=dataset.id)

    def create(self, name: str, content: DatasetType) -> Dataset:
        """
        Creates a new dataset.

        Parameters
        ----------
        name : str
            The name of the dataset.
        content : DatasetType
            The content of the dataset.

        Returns
        -------
        Dataset
            The created dataset.

        Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

        """
        if isinstance(content, (list, dict)) and len(content) == 0:
            # we want to avoid errors: Invalid CSV data: CSV parse error:
            # Empty CSV file or block: cannot infer number of columns
            content = [{}]
        file_path, dataset_format = parse_dataset(content)
        file = File(
            payload=file_path.open("rb"),
            file_name=name,
            mime_type=mimetypes.guess_type(file_path)[0] or "application/octet-stream",
        )

        body = BodyCreateDatasetDatasetsPost(file=file, name=name)

        detailed_response = create_dataset_datasets_post.sync_detailed(
            client=self.config.api_client, body=body, format_=dataset_format
        )

        if not detailed_response.parsed or isinstance(detailed_response.parsed, HTTPValidationError):
            raise DatasetAPIException(detailed_response.content)

        return Dataset(dataset_db=detailed_response.parsed)

    def extend(
        self,
        *,
        prompt_settings: Optional[dict[str, Any]] = None,
        prompt: Optional[str] = None,
        instructions: Optional[str] = None,
        examples: Optional[builtins.list[str]] = None,
        data_types: Optional[builtins.list[str]] = None,
        count: int = 10,
    ) -> builtins.list[DatasetRow]:
        """
        Extends a dataset with synthetically generated data based on the provided parameters.

        This method initiates a dataset extension job, waits for it to complete by polling its status,
        and then returns the content of the extended dataset.

        Parameters
        ----------
        prompt_settings : Dict[str, Any], optional
            Settings for the prompt generation. Should contain 'model_alias' key.
            Example: {'model_alias': 'GPT-4o mini'}
        prompt : str, optional
            A description of the assistant's role.
        instructions : str, optional
            Instructions for the assistant.
        examples : List[str], optional
            Examples of user prompts.
        data_types : List[str], optional
            The types of data to generate. Possible values are:
            'General Query', 'Prompt Injection', 'Off-Topic Query',
            'Toxic Content in Query', 'Multiple Questions in Query',
            'Sexist Content in Query'.
        count : int, default 10
            The number of synthetic examples to generate.

        Returns
        -------
        List[DatasetRow]
            A list of rows from the extended dataset.

        Raises
        ------
        DatasetAPIException
            If the request to extend the dataset fails.
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.
        """
        # Convert prompt_settings dict to PromptRunSettings if provided
        model_alias = prompt_settings.get("model_alias", "gpt-4.1-mini") if prompt_settings else "gpt-4.1-mini"
        prompt_run_settings = PromptRunSettings(model_alias=model_alias)

        # Convert data_types strings to SyntheticDataTypes enum if provided
        synthetic_data_types = None
        if data_types:
            synthetic_data_types = []
            for data_type in data_types:
                try:
                    synthetic_data_types.append(SyntheticDataTypes(data_type))
                except ValueError:
                    raise ValueError(
                        f"Invalid data_type: {data_type}. Must be one of: {[dt.value for dt in SyntheticDataTypes]}"
                    )

        # Create the extension request
        request = SyntheticDatasetExtensionRequest(
            count=count,
            data_types=synthetic_data_types,
            examples=examples,
            instructions=instructions,
            prompt=prompt,
            prompt_settings=prompt_run_settings,
        )

        # Start the extension job
        response = extend_dataset_content_datasets_extend_post.sync(client=self.config.api_client, body=request)

        if isinstance(response, HTTPValidationError):
            raise DatasetAPIException("Request to extend dataset failed.")

        if not response or not isinstance(response, SyntheticDatasetExtensionResponse):
            raise DatasetAPIException("Invalid response from extend dataset API.")

        dataset_id = response.dataset_id

        # Poll for job completion
        while True:
            job_progress = get_dataset_synthetic_extend_status_datasets_extend_dataset_id_get.sync(
                dataset_id=dataset_id, client=self.config.api_client
            )

            if isinstance(job_progress, HTTPValidationError):
                raise DatasetAPIException("Failed to get dataset extension status.")

            if not job_progress or not isinstance(job_progress, JobProgress):
                raise DatasetAPIException("Invalid job progress response.")

            # Check if job is complete
            if (
                job_progress.steps_completed is not None
                and job_progress.steps_total is not None
                and job_progress.steps_completed == job_progress.steps_total
            ):
                print(f"({job_progress.steps_completed}/{job_progress.steps_total}) {job_progress.progress_message}")
                break

            # Print progress message if available
            if job_progress.progress_message:
                print(f"({job_progress.steps_completed}/{job_progress.steps_total}) {job_progress.progress_message}")

            # Wait 1 second before polling again
            time.sleep(1)

        # Get the final dataset content
        dataset_content = get_dataset_content_datasets_dataset_id_content_get.sync(
            client=self.config.api_client, dataset_id=dataset_id
        )

        if not dataset_content or not dataset_content.rows:
            return []

        return dataset_content.rows


#
# Convenience methods
#


def get_dataset(*, id: Optional[str] = None, name: Optional[str] = None) -> Optional[Dataset]:
    """
    Retrieves a dataset by id or name (exactly one of `id` or `name` must be provided).

    Parameters
    ----------
    id : str
        The id of the dataset.
    name : str
        The name of the dataset.
    with_content : bool
        Whether to return the content of the dataset. Default is False.

    Returns
    -------
    Dataset
        The dataset.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().get(id=id, name=name)  # type: ignore[call-overload]


def list_datasets(limit: Union[Unset, int] = 100) -> list[Dataset]:
    """
    Lists all datasets.

    Parameters
    ----------
    limit : Union[Unset, int]
        The maximum number of datasets to return. Default is 100.

    Returns
    -------
    List[Dataset]
        A list of datasets.

    Raises
        ------
        errors.UnexpectedStatus
            If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException
            If the request takes longer than Client.timeout.

    """
    return Datasets().list(limit=limit)


def delete_dataset(*, id: Optional[str] = None, name: Optional[str] = None) -> None:
    """
    Deletes a dataset by id or name (exactly one of `id` or `name` must be provided).

    Parameters
    ----------
    id : str
        The id of the dataset.
    name : str
        The name of the dataset.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().delete(id=id, name=name)  # type: ignore[call-overload]


def create_dataset(name: str, content: DatasetType) -> Dataset:
    """
    Creates a new dataset.

    Parameters
    ----------
    name : str
        The name of the dataset.
    content : DatasetType
        The content of the dataset.

    Returns
    -------
    Dataset
        The created dataset.

    Raises
    ------
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    """
    return Datasets().create(name=name, content=content)


def get_dataset_version_history(
    *, dataset_name: str = None, dataset_id: str = None
) -> Optional[Union[HTTPValidationError, ListDatasetVersionResponse]]:
    """
    Retrieves a dataset version history by dataset name or dataset id.

    Parameters
    ----------
    dataset_name: str
        The name of the dataset.
    dataset_id: str
        The id of the dataset.

    Returns
    -------
    ListDatasetVersionResponse

    Raises
    ------
    HTTPValidationError
    """
    if dataset_name is not None:
        dataset = Datasets().get(name=dataset_name)
        if dataset is None:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        return dataset.get_version_history()
    elif dataset_id is not None:
        dataset = Datasets().get(id=dataset_id)
        if dataset is None:
            raise ValueError(f"Dataset '{dataset_id}' not found")
        return dataset.get_version_history()
    else:
        raise ValueError("Either dataset_name or dataset_id must be provided.")


def get_dataset_version(
    *, version_index: int, dataset_name: str = None, dataset_id: str = None
) -> Optional[DatasetContent]:
    """
    Retrieves a dataset version by dataset name or dataset id.

    Parameters
    ----------
    version_index : int
        The version of the dataset.

    dataset_name: Optional[str]
        The name of the dataset.

    dataset_id: Optional[str]
        The id of the dataset.

    Returns
    -------
    DatasetContent
    """
    if dataset_name is not None:
        dataset = Datasets().get(name=dataset_name)
        if dataset is None:
            raise ValueError(f"Dataset '{dataset_name}' not found")
        return dataset.load_version(version_index)

    elif dataset_id is not None:
        dataset = Datasets().get(id=dataset_id)
        if dataset is None:
            raise ValueError(f"Dataset '{dataset_id}' not found")
        return dataset.load_version(version_index)
    else:
        raise ValueError("Either dataset_name or dataset_id must be provided.")


def extend_dataset(
    *,
    prompt_settings: Optional[dict[str, Any]] = None,
    prompt: Optional[str] = None,
    instructions: Optional[str] = None,
    examples: Optional[list[str]] = None,
    data_types: Optional[list[str]] = None,
    count: int = 10,
) -> list[DatasetRow]:
    """
    Extends a dataset with synthetically generated data based on the provided parameters.

    This function initiates a dataset extension job, waits for it to complete by polling its status,
    and then returns the content of the extended dataset.

    Parameters
    ----------
    prompt_settings : Dict[str, Any], optional
        Settings for the prompt generation. Should contain 'model_alias' key.
        Example: {'model_alias': 'GPT-4o mini'}
    prompt : str, optional
        A description of the assistant's role.
    instructions : str, optional
        Instructions for the assistant.
    examples : List[str], optional
        Examples of user prompts.
    data_types : List[str], optional
        The types of data to generate. Possible values are:
        'General Query', 'Prompt Injection', 'Off-Topic Query',
        'Toxic Content in Query', 'Multiple Questions in Query',
        'Sexist Content in Query'.
    count : int, default 10
        The number of synthetic examples to generate.

    Returns
    -------
    List[DatasetRow]
        A list of rows from the extended dataset.

    Raises
    ------
    DatasetAPIException
        If the request to extend the dataset fails.
    errors.UnexpectedStatus
        If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    httpx.TimeoutException
        If the request takes longer than Client.timeout.

    Examples
    --------
    >>> extended_dataset = extend_dataset(
    ...     prompt_settings={'model_alias': 'GPT-4o mini'},
    ...     prompt='Financial planning assistant that helps clients design an investment strategy.',
    ...     instructions='You are a financial planning assistant that helps clients design an investment strategy.',
    ...     examples=['I want to invest $1000 per month.'],
    ...     data_types=['Prompt Injection'],
    ...     count=3
    ... )
    >>> print('Extended dataset:', extended_dataset)
    """
    return Datasets().extend(
        prompt_settings=prompt_settings,
        prompt=prompt,
        instructions=instructions,
        examples=examples,
        data_types=data_types,
        count=count,
    )


def convert_dataset_row_to_record(dataset_row: DatasetRow) -> "DatasetRecord":
    values_dict = dataset_row.values_dict.to_dict()

    if "input" not in values_dict or not values_dict["input"]:
        raise ValueError("Dataset row must have input field")

    return DatasetRecord(
        id=dataset_row.row_id,
        input=values_dict["input"],
        output=values_dict["output"] if "output" in values_dict else None,
        metadata=values_dict["metadata"] if "metadata" in values_dict else None,
    )
