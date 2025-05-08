from typing import Optional, Union

from galileo.datasets import Dataset, convert_dataset_row_to_record, get_dataset
from galileo.schema.datasets import DatasetRecord


def load_dataset_and_records(
    dataset: Union[Dataset, list[dict[str, str]], str, None], dataset_id: Optional[str], dataset_name: Optional[str]
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
    match dataset_id, dataset_name, dataset:
        case str(), _, _:
            return get_dataset_and_records(id=dataset_id)
        case _, str(), _:
            return get_dataset_and_records(name=dataset_name)
        case _, _, str():
            return get_dataset_and_records(name=dataset)
        case _, _, Dataset():
            return dataset, get_records_for_dataset(dataset)
        case _, _, list():
            return None, create_rows_from_records(dataset)
        case _:
            raise ValueError("One of dataset, dataset_name, or dataset_id must be provided")


def get_dataset_and_records(
    id: Optional[str] = None, name: Optional[str] = None
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
        raise ValueError("One of id or name must be provided")

    return dataset, get_records_for_dataset(dataset)


def get_records_for_dataset(dataset: Dataset) -> list[DatasetRecord]:
    content = dataset.get_content()
    if not content:
        raise ValueError("dataset has no content")
    return [convert_dataset_row_to_record(row) for row in content.rows]


def create_rows_from_records(records: list[dict[str, str]]) -> list[DatasetRecord]:
    result = []
    for record in records:
        if isinstance(record, dict) and "input" in record:
            result.append(DatasetRecord(**record))
        else:
            result.append(DatasetRecord(input=record))
    return result
