"""
Dataset class for the Galileo Future API.

This module provides an object-centric interface for managing Galileo datasets,
offering a more intuitive alternative to the service-based functions.
"""

from __future__ import annotations

from typing import Any

from galileo.datasets import Dataset as LegacyDataset
from galileo.datasets import delete_dataset as service_delete_dataset
from galileo.datasets import extend_dataset as service_extend_dataset
from galileo.datasets import get_dataset as service_get_dataset
from galileo.datasets import get_dataset_version as service_get_dataset_version
from galileo.datasets import get_dataset_version_history as service_get_dataset_version_history
from galileo.datasets import list_datasets as service_list_datasets
from galileo.resources.models.dataset_content import DatasetContent
from galileo.resources.models.dataset_row import DatasetRow
from galileo.resources.types import Unset


class Dataset:
    """
    Object-centric interface for Galileo datasets.

    This class provides an intuitive way to work with Galileo datasets,
    encapsulating dataset management operations and providing seamless
    integration with dataset content management.

    Attributes:
        id (str): The unique dataset identifier.
        name (str): The dataset name.
        created_at (datetime.datetime): When the dataset was created.
        updated_at (datetime.datetime): When the dataset was last updated.
        num_rows (int): Number of rows in the dataset.
        column_names (list[str]): Column names in the dataset.
        draft (bool): Whether the dataset is in draft state.

    Examples:
        # Create a new dataset
        dataset = Dataset(
            name="ml-knowledge-evaluation_3",
            content=[
                {"input": "What is machine learning?", "output": "Machine learning ..."},
                {"input": "How does deep learning work?", "output": "Deep learning uses ..."}
            ]
        )

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

        # Get version history
        history = dataset.get_version_history()

        # Delete dataset
        dataset.delete()
    """

    def __init__(
        self,
        name: str | None = None,
        content: list[dict[str, Any]] | None = None,
        *,
        _legacy_dataset: LegacyDataset | None = None,
    ) -> None:
        """
        Initialize a Dataset instance.

        When called with name and content, this creates a new dataset.
        To get an existing dataset, use Dataset.get() instead.

        Args:
            name (Optional[str]): The name of the dataset to create.
            content (Optional[list[dict[str, Any]]]): The content for the dataset.
            _legacy_dataset (Optional[LegacyDataset]): Internal parameter for
                wrapping existing dataset instances.
        """
        if _legacy_dataset is not None:
            # Initialize from existing legacy dataset
            self._legacy_dataset = _legacy_dataset
            self.id = _legacy_dataset.id
            self.name = _legacy_dataset.name
            self.created_at = _legacy_dataset.created_at
            self.updated_at = _legacy_dataset.updated_at
            self.num_rows = _legacy_dataset.num_rows
            self.column_names = _legacy_dataset.column_names
            self.draft = _legacy_dataset.draft
        elif name is not None:
            # Create a new dataset
            from galileo.datasets import Datasets

            datasets_service = Datasets()
            self._legacy_dataset = datasets_service.create(name=name, content=content or [])
            self.id = self._legacy_dataset.id
            self.name = self._legacy_dataset.name
            self.created_at = self._legacy_dataset.created_at
            self.updated_at = self._legacy_dataset.updated_at
            self.num_rows = self._legacy_dataset.num_rows
            self.column_names = self._legacy_dataset.column_names
            self.draft = self._legacy_dataset.draft
        else:
            raise ValueError(
                "Either 'name' must be provided to create a dataset, "
                "or use Dataset.get() to retrieve an existing dataset"
            )

    @classmethod
    def get(cls, *, id: str | None = None, name: str | None = None) -> Dataset | None:
        """
        Get an existing dataset by ID or name.

        Args:
            id (Optional[str]): The dataset ID.
            name (Optional[str]): The dataset name.

        Returns:
            Optional[Dataset]: The dataset if found, None otherwise.

        Raises:
            ValueError: If neither or both id and name are provided.

        Examples:
            # Get by name
            dataset = Dataset.get(name="geography-questions")

            # Get by ID
            dataset = Dataset.get(id="dataset-123")
        """
        legacy_dataset = service_get_dataset(id=id, name=name)
        if legacy_dataset is None:
            return None
        return cls(_legacy_dataset=legacy_dataset)

    @classmethod
    def list(cls, *, limit: Unset | int = 100) -> list[Dataset]:
        """
        List all available datasets.

        Args:
            limit (Union[Unset, int]): Maximum number of datasets to return.

        Returns:
            list[Dataset]: A list of all datasets.

        Examples:
            datasets = Dataset.list()
            datasets = Dataset.list(limit=50)
        """
        legacy_datasets = service_list_datasets(limit=limit)
        return [cls(_legacy_dataset=legacy_dataset) for legacy_dataset in legacy_datasets]

    @classmethod
    def generate(
        cls,
        *,
        prompt: str | None = None,
        instructions: str | None = None,
        examples: list[str] | None = None,  # type: ignore[valid-type]
        count: int = 10,
        data_types: list[str] | None = None,  # type: ignore[valid-type]
        prompt_settings: dict[str, Any] | None = None,  # type: ignore[valid-type]
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

        Returns:
            list[DatasetRow]: A list of generated dataset rows.

        Examples:
            rows = Dataset.generate(
                prompt="Financial planning assistant...",
                instructions="You are a financial planning assistant...",
                examples=["I want to invest $1000 per month."],
                count=3,
            )
        """
        return service_extend_dataset(
            prompt=prompt,
            instructions=instructions,
            examples=examples,
            count=count,
            data_types=data_types,
            prompt_settings=prompt_settings,
        )

    def save(self) -> None:
        """
        Save the dataset (remove draft state for synthetic datasets).

        Note: This method is TBD - implementation depends on how draft state removal is handled.
        """
        # TODO: Implement save functionality to remove draft state
        # This will depend on the API endpoint for removing draft state
        raise NotImplementedError(
            "Save functionality is not yet implemented. "
            "This depends on the API endpoint for removing draft state from synthetic datasets."
        )

    def get_content(self) -> DatasetContent | None:
        """
        Get the content of this dataset.

        Returns:
            Optional[DatasetContent]: The dataset content if available.

        Examples:
            dataset = Dataset.get(name="my-dataset")
            content = dataset.get_content()
        """
        return self._legacy_dataset.get_content()

    def add_rows(self, rows: list[dict[str, Any]]) -> Dataset:  # type: ignore[valid-type]
        """
        Add rows to this dataset.

        Args:
            rows (list[dict[str, Any]]): The rows to add to the dataset.

        Returns:
            Dataset: This dataset instance for method chaining.

        Examples:
            dataset.add_rows([
                {"input": "Australia", "output": "Oceania"},
                {"input": "Egypt", "output": "Africa"},
            ])
        """
        self._legacy_dataset.add_rows(rows)
        # Refresh attributes after adding rows
        self.num_rows = self._legacy_dataset.num_rows
        self.updated_at = self._legacy_dataset.updated_at
        return self

    def get_version_history(self) -> list[dict[str, Any]]:  # type: ignore[valid-type]
        """
        Get the version history of this dataset.

        Returns:
            list[dict[str, Any]]: The version history of the dataset.

        Examples:
            dataset = Dataset.get(name="my-dataset")
            history = dataset.get_version_history()
        """
        return service_get_dataset_version_history(dataset_name=self.name)

    def get_version(self, *, index: int) -> DatasetContent | None:
        """
        Get a specific version of this dataset.

        Args:
            index (int): The version index to retrieve.

        Returns:
            Optional[DatasetContent]: The dataset content for the specified version.

        Examples:
            dataset = Dataset.get(name="my-dataset")
            version = dataset.get_version(index=0)
        """
        return service_get_dataset_version(version_index=index, dataset_name=self.name)

    def extend(
        self,
        *,
        prompt: str | None = None,
        instructions: str | None = None,
        examples: list[str] | None = None,  # type: ignore[valid-type]
        count: int = 10,
        data_types: list[str] | None = None,  # type: ignore[valid-type]
        prompt_settings: dict[str, Any] | None = None,  # type: ignore[valid-type]
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

        Returns:
            list[DatasetRow]: A list of generated dataset rows.

        Examples:
            extended_rows = dataset.extend(
                prompt="Financial planning assistant...",
                instructions="You are a financial planning assistant...",
                examples=["I want to invest $1000 per month."],
                count=3,
            )
        """
        return self._legacy_dataset.extend(
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

        Examples:
            dataset = Dataset.get(name="my-dataset")
            dataset.delete()
        """
        service_delete_dataset(name=self.name)

    def __str__(self) -> str:
        """String representation of the dataset."""
        return f"Dataset(name='{self.name}', id='{self.id}')"

    def __repr__(self) -> str:
        """Detailed string representation of the dataset."""
        return f"Dataset(name='{self.name}', id='{self.id}', rows={self.num_rows})"
