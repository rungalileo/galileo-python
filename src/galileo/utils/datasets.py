from typing import TYPE_CHECKING, Any, Optional, Union

from galileo.config import GalileoPythonConfig
from galileo.schema.datasets import DatasetRecord

if TYPE_CHECKING:
    from galileo.datasets import Dataset


def validate_dataset_in_project(
    dataset_id: str, dataset_identifier: str, project_id: str, project_identifier: str, config: GalileoPythonConfig
) -> None:
    from galileo.resources.api.datasets import list_dataset_projects_datasets_dataset_id_projects_get

    projects_response = list_dataset_projects_datasets_dataset_id_projects_get.sync(
        dataset_id=dataset_id, client=config.api_client
    )

    if not projects_response or not hasattr(projects_response, "projects"):
        raise ValueError(f"Dataset '{dataset_identifier}' is not used in project '{project_identifier}'")

    project_ids = [p.id for p in projects_response.projects]
    if project_id not in project_ids:
        raise ValueError(f"Dataset '{dataset_identifier}' is not used in project '{project_identifier}'")


def load_dataset(
    dataset: Union["Dataset", list[Union[dict[str, Any], str]], str, None],
    dataset_id: Optional[str],
    dataset_name: Optional[str],
) -> Optional["Dataset"]:
    """
    Load dataset based on provided parameters.

    Parameters
    ----------
    dataset:
        Dataset object, list of records, or dataset name
    dataset_id:
        ID of the dataset
    dataset_name:
        Name of the dataset

    Returns
    -------
    Dataset object or None

    Raises
    ------
    ValueError
            If no dataset information is provided or dataset doesn't exist
    """
    from galileo.datasets import get_dataset

    if dataset_id:
        return get_dataset(id=dataset_id)
    if dataset_name:
        return get_dataset(name=dataset_name)
    if dataset and isinstance(dataset, str):
        return get_dataset(name=dataset)
    if dataset and not isinstance(dataset, (str, list)):
        # Must be a Dataset object
        return dataset
    if dataset and isinstance(dataset, list):
        return None
    raise ValueError("To load dataset records, dataset, dataset_name, or dataset_id must be provided")


def load_dataset_and_records(
    dataset: Union["Dataset", list[Union[dict[str, Any], str]], str, None],
    dataset_id: Optional[str],
    dataset_name: Optional[str],
) -> tuple[Optional["Dataset"], list[DatasetRecord]]:
    """
    Load dataset and records based on provided parameters.

    Parameters
    ----------
    dataset:
        Dataset object, list of records, or dataset name
    dataset_id:
        ID of the dataset
    dataset_name:
        Name of the dataset

    Returns
    -------
    Tuple containing (Dataset object or None, records list)

    Raises
    ------
    ValueError
            If no dataset information is provided or dataset doesn't exist
    """
    if dataset_id:
        return get_dataset_and_records(id=dataset_id)
    if dataset_name:
        return get_dataset_and_records(name=dataset_name)
    if dataset and isinstance(dataset, str):
        return get_dataset_and_records(name=dataset)
    if dataset and not isinstance(dataset, (str, list)):
        # Must be a Dataset object
        return dataset, get_records_for_dataset(dataset)
    if dataset and isinstance(dataset, list):
        return None, create_rows_from_records(dataset)
    raise ValueError("To load dataset records, dataset, dataset_name, or dataset_id must be provided")


def get_dataset_and_records(
    id: Optional[str] = None, name: Optional[str] = None
) -> tuple["Dataset", list[DatasetRecord]]:
    from galileo.datasets import get_dataset

    if id:
        dataset = get_dataset(id=id)
        if not dataset:
            raise ValueError("Could not find dataset with id " + id)
    elif name:
        dataset = get_dataset(name=name)
        if not dataset:
            raise ValueError("Could not find dataset with name " + name)
    else:
        raise ValueError("Either the dataset id or name must be provided")

    return dataset, get_records_for_dataset(dataset)


def get_records_for_dataset(dataset: "Dataset") -> list[DatasetRecord]:
    from galileo.datasets import convert_dataset_row_to_record

    content = dataset.get_content()
    if not content:
        raise ValueError("dataset has no content")
    return [convert_dataset_row_to_record(row) for row in content.rows]


def create_rows_from_records(records: list[Union[dict[str, Any], str]]) -> list[DatasetRecord]:
    result = []
    for record in records:
        if isinstance(record, dict) and "input" in record:
            result.append(DatasetRecord(**record))
        else:
            result.append(DatasetRecord(input=record))
    return result
