from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, TypeAlias

from galileo.datasets import Datasets
from galileo.resources.models.dataset_content import DatasetContent
from galileo.resources.models.dataset_row import DatasetRow
from galileo.resources.models.http_validation_error import HTTPValidationError
from galileo.resources.models.list_dataset_version_response import ListDatasetVersionResponse
from galileo.resources.types import Unset
from galileo.shared.base import StateManagementMixin, SyncState
from galileo.shared.exceptions import ResourceNotFoundError, ValidationError

#: Type alias for clarity: ``get_version_content`` returns the content of a specific
#: dataset version. The underlying auto-generated type is ``DatasetContent``.
DatasetVersionContent: TypeAlias = DatasetContent

logger = logging.getLogger(__name__)


class Dataset(StateManagementMixin):
    """
    Object-centric interface for Galileo datasets.

    This class provides an intuitive way to work with Galileo datasets,
    encapsulating dataset management operations and providing seamless
    integration with dataset content management.

    Attributes
    ----------
        id (str): The unique dataset identifier.
        name (str): The dataset name.
        created_at (datetime.datetime): When the dataset was created.
        updated_at (datetime.datetime): When the dataset was last updated.
        num_rows (int): Number of rows in the dataset.
        column_names (list[str]): Column names in the dataset.
        draft (bool): Whether the dataset is in draft state.

    Examples
    --------
        # Create a new dataset locally, then persist
        dataset = Dataset(
            name="ml-knowledge-evaluation_3",
            content=[
                {"input": "What is machine learning?", "output": "Machine learning ..."},
                {"input": "How does deep learning work?", "output": "Deep learning uses ..."}
            ]
        ).create()

        # Get an existing dataset
        dataset = Dataset.get(name="geography-questions")

        # List all datasets
        datasets = Dataset.list(limit=50)

        # Get dataset content
        content = dataset.get_content()

        # Add rows to dataset
        dataset.add_rows([
            {"input": "Australia", "output": "Oceania"},
            {"input": "Egypt", "output": "Africa"},
        ])

        # Get dataset versions
        versions = dataset.get_versions()

        # Delete dataset
        dataset.delete()
    """

    # Fields that trigger SYNCED → DIRTY on assignment
    _TRACKED_FIELDS: frozenset[str] = frozenset({"name"})

    # Type annotations for instance attributes
    id: str | None
    name: str
    created_at: datetime | None
    updated_at: datetime | None
    num_rows: int | None
    column_names: list[str] | None
    draft: bool | None
    content: list[dict[str, Any]]

    def __str__(self) -> str:
        """String representation of the dataset."""
        return f"Dataset(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the dataset."""
        return f"Dataset(name='{self.name}', id='{self.id}', rows={self.num_rows})"

    def __init__(self, name: str | None = None, content: list[dict[str, Any]] | None = None) -> None:
        """
        Initialize a Dataset instance locally.

        Creates a local dataset object that exists only in memory until .create()
        is called to persist it to the API.

        Args:
            name (Optional[str]): The name of the dataset to create.
            content (Optional[list[dict[str, Any]]]): The content for the dataset.

        Raises
        ------
            ValidationError: If name is not provided.
        """
        super().__init__()
        if name is None:
            raise ValidationError(
                "'name' must be provided to create a dataset. Use Dataset.get() to retrieve an existing dataset."
            )

        # Initialize attributes locally
        self.name = name
        self.content = content or []
        self.id = None
        self.created_at = None
        self.updated_at = None
        self.num_rows = None
        self.column_names = None
        self.draft = None

        # Set initial state
        self._set_state(SyncState.LOCAL_ONLY)

    @classmethod
    def _create_empty(cls) -> Dataset:
        """Internal constructor bypassing __init__ for API hydration."""
        instance = cls.__new__(cls)
        super(Dataset, instance).__init__()
        return instance

    @classmethod
    def _from_api_response(cls, retrieved_dataset: Any) -> Dataset:
        """
        Factory method to create a Dataset instance from an API response.

        Args:
            retrieved_dataset: The dataset data retrieved from the API.

        Returns
        -------
            Dataset: A new Dataset instance populated with the API data.
        """
        instance = cls._create_empty()
        instance.id = retrieved_dataset.id
        instance.name = retrieved_dataset.name
        instance.created_at = retrieved_dataset.created_at
        instance.updated_at = retrieved_dataset.updated_at
        instance.num_rows = retrieved_dataset.num_rows
        instance.column_names = retrieved_dataset.column_names
        instance.draft = retrieved_dataset.draft
        instance.content = []  # Content is not loaded in get()/list(), use get_content() for that
        # Set state to synced since we just retrieved from API
        instance._set_state(SyncState.SYNCED)
        return instance

    def create(self) -> Dataset:
        """
        Persist this dataset to the API.

        Returns
        -------
            Dataset: This dataset instance with updated attributes from the API.

        Raises
        ------
            Exception: If the API call fails.

        Examples
        --------
            dataset = Dataset(name="test", content=[...]).create()
            assert dataset.is_synced()
        """
        try:
            logger.info(f"Dataset.create: name='{self.name}' - started")
            datasets_service = Datasets()
            # Don't pass project_id at all - it defaults to None which is handled correctly
            created_dataset = datasets_service.create(name=self.name, content=self.content)

            # Update attributes from response
            self.id = created_dataset.id
            self.name = created_dataset.name
            self.created_at = created_dataset.created_at
            self.updated_at = created_dataset.updated_at
            self.num_rows = created_dataset.num_rows
            self.column_names = created_dataset.column_names
            self.draft = created_dataset.draft

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.info(f"Dataset.create: id='{self.id}' - completed")
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Dataset.create: name='{self.name}' - failed: {e}")
            raise

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Dataset | None:
        """
        Get an existing dataset by ID or name.

        Args:
            id (Optional[str]): The dataset ID.
            name (Optional[str]): The dataset name.

        Returns
        -------
            Optional[Dataset]: The dataset if found, None otherwise.

        Raises
        ------
            ValueError: If neither or both id and name are provided.

        Examples
        --------
            # Get by name
            dataset = Dataset.get(name="geography-questions")

            # Get by ID
            dataset = Dataset.get(id="dataset-123")
        """
        datasets_service = Datasets()

        # Call service with the appropriate signature based on which parameter is provided
        if id is not None:
            retrieved_dataset = datasets_service.get(id=id)
        elif name is not None:
            retrieved_dataset = datasets_service.get(name=name)
        else:
            raise ValueError("Either 'id' or 'name' must be provided")

        if retrieved_dataset is None:
            return None

        return cls._from_api_response(retrieved_dataset)

    @classmethod
    def list(
        cls, *, limit: Unset | int = 100, project_id: str | None = None, project_name: str | None = None
    ) -> list[Dataset]:
        """
        List all available datasets, optionally filtered by project.

        Args:
            limit (Union[Unset, int]): Maximum number of datasets to return.
            project_id (Optional[str]): Filter datasets used in this project by ID.
            project_name (Optional[str]): Filter datasets used in this project by name.

        Returns
        -------
            list[Dataset]: A list of datasets matching the criteria.

        Examples
        --------
            # List all datasets
            datasets = Dataset.list()
            datasets = Dataset.list(limit=50)

            # List datasets used in a specific project
            datasets = Dataset.list(project_id="project-123")
            datasets = Dataset.list(project_name="My Project")
        """
        datasets_service = Datasets()
        retrieved_datasets = datasets_service.list(limit=limit, project_id=project_id, project_name=project_name)

        return [cls._from_api_response(retrieved_dataset) for retrieved_dataset in retrieved_datasets]

    @classmethod
    def generate(
        cls,
        *,
        prompt: str | None = None,
        instructions: str | None = None,
        examples: list[str] | None = None,  # type: ignore[valid-type]
        count: int = 10,
        data_types: list[str] | None = None,  # type: ignore[valid-type]
        prompt_settings: dict[str, Any] | None = None,
    ) -> list[DatasetRow]:  # type: ignore[valid-type]
        """
        Generate synthetic dataset rows.

        Args:
            prompt (Optional[str]): A description of the assistant's role.
            instructions (Optional[str]): Instructions for the assistant.
            examples (Optional[list[str]]): Examples of user prompts.
            count (int): The number of synthetic examples to generate.
            data_types (Optional[list[str]]): The types of data to generate.
            prompt_settings (Optional[dict[str, Any]]): Settings for the prompt generation.

        Returns
        -------
            list[DatasetRow]: A list of generated dataset rows.

        Examples
        --------
            rows = Dataset.generate(
                prompt="Financial planning assistant...",
                instructions="You are a financial planning assistant...",
                examples=["I want to invest $1000 per month."],
                count=3,
            )
        """
        datasets_service = Datasets()
        return datasets_service.extend(
            prompt=prompt,
            instructions=instructions,
            examples=examples,
            count=count,
            data_types=data_types,
            prompt_settings=prompt_settings,
        )

    def get_content(self) -> DatasetContent | None:
        """
        Get the content of this dataset.

        Returns
        -------
            Optional[DatasetContent]: The dataset content if available.

        Examples
        --------
            dataset = Dataset.get(name="my-dataset")
            content = dataset.get_content()
        """
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot get content for a local-only dataset.")
        datasets_service = Datasets()
        dataset = datasets_service.get(id=self.id)
        if dataset is None:
            return None
        return dataset.get_content()

    def add_rows(self, rows: list[dict[str, Any]]) -> Dataset:  # type: ignore[valid-type]
        """
        Add rows to this dataset (active mutation).

        This method performs an API call and atomically updates the state.

        Args:
            rows (list[dict[str, Any]]): The rows to add to the dataset.

        Returns
        -------
            Dataset: This dataset instance for method chaining.

        Examples
        --------
            dataset.add_rows([
                {"input": "Australia", "output": "Oceania"},
                {"input": "Egypt", "output": "Africa"},
            ])
        """
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot add rows to a local-only dataset.")
        try:
            datasets_service = Datasets()
            dataset = datasets_service.get(id=self.id)
            if dataset is not None:
                dataset.add_rows(rows)
                # Refresh attributes after adding rows
                self.num_rows = dataset.num_rows
                self.updated_at = dataset.updated_at
                # Set state to synced after successful update
                self._set_state(SyncState.SYNCED)
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            raise

    def get_versions(self) -> ListDatasetVersionResponse:
        """
        Get a list of versions for this dataset.

        Returns
        -------
            ListDatasetVersionResponse: The list of dataset versions, including version
                metadata such as version_index, num_rows, column_names, and created_at.
                Access the versions list via the `.versions` attribute.

        Raises
        ------
            ValueError: If the dataset has no ID (local-only state) or if the API
                returns a validation error.
            ResourceNotFoundError: If the dataset is not found on the server.

        Examples
        --------
            dataset = Dataset.get(name="my-dataset")
            versions = dataset.get_versions()
            for v in versions.versions:
                print(v.version_index, v.num_rows)
        """
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot get versions for a local-only dataset.")
        datasets_service = Datasets()
        dataset = datasets_service.get(id=self.id)
        if dataset is None:
            raise ResourceNotFoundError(f"Dataset with id={self.id!r} was not found.")
        result = dataset.get_version_history()
        if isinstance(result, HTTPValidationError):
            raise ValueError(f"Failed to retrieve dataset versions: {result}")
        if result is None:
            raise ValueError("Unexpected empty response from dataset versions API")
        return result

    def get_version_content(self, *, index: int) -> DatasetVersionContent:
        """
        Get the content of a specific version of this dataset.

        Args:
            index (int): The 1-based version index to retrieve. Must be >= 1.

        Returns
        -------
            DatasetVersionContent: The content for the specified version.

        Raises
        ------
            ValueError: If the dataset has no ID (local-only state), if index < 1,
                or if the API returns a validation error or unexpected empty response.
            ResourceNotFoundError: If the dataset is not found on the server.

        Examples
        --------
            dataset = Dataset.get(name="my-dataset")
            content = dataset.get_version_content(index=1)
        """
        if index < 1:
            raise ValueError(f"Version index must be >= 1 (1-based indexing). Got: {index}")
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot get version content for a local-only dataset.")
        datasets_service = Datasets()
        dataset = datasets_service.get(id=self.id)
        if dataset is None:
            raise ResourceNotFoundError(f"Dataset with id={self.id!r} was not found.")
        result = dataset.load_version(index)
        if isinstance(result, HTTPValidationError):
            raise ValueError(f"Failed to retrieve version content: {result}")
        if result is None:
            raise ValueError("Unexpected empty response from version content API")
        return result

    def extend(
        self,
        *,
        prompt: str | None = None,
        instructions: str | None = None,
        examples: list[str] | None = None,  # type: ignore[valid-type]
        count: int = 10,
        data_types: list[str] | None = None,  # type: ignore[valid-type]
        prompt_settings: dict[str, Any] | None = None,
    ) -> list[DatasetRow]:  # type: ignore[valid-type]
        """
        Extend this dataset with synthetically generated data.

        Args:
            prompt (Optional[str]): A description of the assistant's role.
            instructions (Optional[str]): Instructions for the assistant.
            examples (Optional[list[str]]): Examples of user prompts.
            count (int): The number of synthetic examples to generate.
            data_types (Optional[list[str]]): The types of data to generate.
            prompt_settings (Optional[dict[str, Any]]): Settings for the prompt generation.

        Returns
        -------
            list[DatasetRow]: A list of generated dataset rows.

        Examples
        --------
            extended_rows = dataset.extend(
                prompt="Financial planning assistant...",
                instructions="You are a financial planning assistant...",
                examples=["I want to invest $1000 per month."],
                count=3,
            )
        """
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot extend a local-only dataset.")
        datasets_service = Datasets()
        # Call extend on the service, not on the Dataset object
        return datasets_service.extend(
            prompt=prompt,
            instructions=instructions,
            examples=examples,
            count=count,
            data_types=data_types,
            prompt_settings=prompt_settings,
        )

    def delete(self) -> None:
        """
        Delete this dataset.

        Examples
        --------
            dataset = Dataset.get(name="my-dataset")
            dataset.delete()
        """
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot delete a local-only dataset.")
        try:
            logger.info(f"Dataset.delete: name='{self.name}' - started")
            datasets_service = Datasets()
            datasets_service.delete(id=self.id)
            # Set state to deleted after successful deletion
            self._set_state(SyncState.DELETED)
            logger.info(f"Dataset.delete: name='{self.name}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Dataset.delete: name='{self.name}' - failed: {e}")
            raise

    def refresh(self) -> None:
        """
        Refresh this dataset's state from the API.

        Updates all attributes with the latest values from the remote API
        and sets the state to SYNCED.

        Raises
        ------
            Exception: If the API call fails or the dataset no longer exists.

        Examples
        --------
            dataset.refresh()
            assert dataset.is_synced()
        """
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot refresh a local-only dataset.")
        try:
            logger.debug(f"Dataset.refresh: id='{self.id}' - started")
            datasets_service = Datasets()
            retrieved_dataset = datasets_service.get(id=self.id)

            if retrieved_dataset is None:
                raise ValueError(f"Dataset with id '{self.id}' no longer exists")

            # Update all attributes from response
            self.id = retrieved_dataset.id
            self.name = retrieved_dataset.name
            self.created_at = retrieved_dataset.created_at
            self.updated_at = retrieved_dataset.updated_at
            self.num_rows = retrieved_dataset.num_rows
            self.column_names = retrieved_dataset.column_names
            self.draft = retrieved_dataset.draft

            # Set state to synced
            self._set_state(SyncState.SYNCED)
            logger.debug(f"Dataset.refresh: id='{self.id}' - completed")
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error(f"Dataset.refresh: id='{self.id}' - failed: {e}")
            raise

    def save(self) -> Dataset:
        """
        Save changes to this dataset.

        Persists any local changes (name) to the remote API. If the dataset is
        LOCAL_ONLY, delegates to create(). If SYNCED, returns immediately as a
        no-op. Raises ValueError for DELETED or FAILED_SYNC states.

        Returns
        -------
            Dataset: This dataset instance with updated attributes from the API.

        Raises
        ------
            ValueError: If the dataset is in a DELETED or FAILED_SYNC state, or if
                the dataset ID is not set.
            Exception: If the API call fails.

        Examples
        --------
            dataset = Dataset.get(name="my-dataset")
            dataset.name = "renamed-dataset"
            dataset.save()
            assert dataset.is_synced()
        """
        if self._sync_state == SyncState.LOCAL_ONLY:
            return self.create()

        if self._sync_state == SyncState.SYNCED:
            return self

        if self._sync_state == SyncState.DELETED:
            raise ValueError("Cannot save a deleted dataset. The remote resource no longer exists.")

        if self._sync_state == SyncState.FAILED_SYNC:
            raise ValueError(
                "Dataset is in FAILED_SYNC state from a previous operation. "
                "Call refresh() to reload the latest state before retrying."
            )

        # DIRTY state — send update to API
        if self.id is None:
            raise ValueError("Dataset ID is not set. Cannot save without a valid ID.")

        try:
            logger.info("Dataset.save: id='%s' - started", self.id)
            datasets_service = Datasets()
            updated_dataset = datasets_service.update(self.id, name=self.name)

            # Sync fields back from the API response
            self._sync_attrs(
                id=updated_dataset.id,
                name=updated_dataset.name,
                created_at=updated_dataset.created_at,
                updated_at=updated_dataset.updated_at,
                num_rows=updated_dataset.num_rows,
                column_names=updated_dataset.column_names,
                draft=updated_dataset.draft,
            )
            self._set_state(SyncState.SYNCED)
            logger.info("Dataset.save: id='%s' - completed", self.id)
            return self
        except Exception as e:
            self._set_state(SyncState.FAILED_SYNC, error=e)
            logger.error("Dataset.save: id='%s' - failed: %s", self.id, e)
            raise
