from unittest.mock import patch, Mock

from galileo.datasets import get_dataset_version
from galileo.resources.models import DatasetDB


def dataset_response():
    return DatasetDB(

    )


@patch("galileo.datasets.get_dataset_datasets_dataset_id_get")
def test_get_dataset_version(get_dataset_datasets_dataset_id_get: Mock):
    get_dataset_datasets_dataset_id_get.sync = Mock(return_value=dataset_response())
    ds_version = get_dataset_version(1, dataset_name="test")
    assert ds_version == ""

