from typing import Any, Optional, Union

from galileo.datasets import Dataset, convert_dataset_row_to_record, get_dataset
from galileo.schema.datasets import DatasetRecord


def load_dataset_and_records(
    dataset: Union[Dataset, list[Union[dict[str, Any], str]], str, None],
    dataset_id: Optional[str],
    dataset_name: Optional[str],
    limit: Optional[int] = None,
) -> tuple[Optional[Dataset], list[DatasetRecord]]:
    """
    Load dataset and records based on provided parameters.

    Args:
        dataset: Dataset object, list of records, or dataset name
        dataset_id: ID of the dataset
        dataset_name: Name of the dataset

    Returns:
        Tuple containing (Dataset object or None, records list)

    Raises:
        ValueError: If no dataset information is provided or dataset doesn't exist
    """
    if dataset_id:
        return get_dataset_and_records(id=dataset_id, limit=limit)
    if dataset_name:
        return get_dataset_and_records(name=dataset_name, limit=limit)
    if dataset and isinstance(dataset, str):
        return get_dataset_and_records(name=dataset, limit=limit)
    if dataset and isinstance(dataset, Dataset):
        return dataset, get_records_for_dataset(dataset, limit=limit)
    if dataset and isinstance(dataset, list):
        return None, create_rows_from_records(dataset)
    raise ValueError("To load dataset records, dataset, dataset_name, or dataset_id must be provided")


def get_dataset_and_records(
    id: Optional[str] = None, name: Optional[str] = None, limit: Optional[int] = None
) -> tuple[Dataset, list[DatasetRecord]]:
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

    return dataset, get_records_for_dataset(dataset, limit=limit)


def get_records_for_dataset(dataset: Dataset, limit: Optional[int] = None) -> list[DatasetRecord]:
    content = dataset.get_content(limit=limit)
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
