from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from galileo.__future__ import Dataset
from galileo.__future__.shared.base import SyncState
from galileo.__future__.shared.exceptions import ValidationError
from galileo.resources.models.dataset_content import DatasetContent


class TestDatasetInitialization:
    """Test suite for Dataset initialization."""

    @pytest.mark.parametrize(
        "name,content,expected_content",
        [
            ("Test Dataset", None, []),
            ("Test Dataset", [{"input": "test", "output": "result"}], [{"input": "test", "output": "result"}]),
        ],
    )
    def test_init_with_name(self, name: str, content: list, expected_content: list, reset_configuration: None) -> None:
        """Test initializing a dataset with a name creates a local-only instance."""
        dataset = Dataset(name=name, content=content)

        assert dataset.name == name
        assert dataset.content == expected_content
        assert dataset.id is None
        assert dataset.sync_state == SyncState.LOCAL_ONLY

    def test_init_without_name_raises_validation_error(self, reset_configuration: None) -> None:
        """Test initializing a dataset without a name raises ValidationError."""
        with pytest.raises(ValidationError, match="'name' must be provided"):
            Dataset(name=None)


class TestDatasetCreate:
    """Test suite for Dataset.create() method."""

    @patch("galileo.__future__.dataset.Datasets")
    def test_create_persists_dataset_to_api(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        """Test create() persists the dataset to the API and updates attributes."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.create.return_value = mock_dataset

        content = [{"input": "test", "output": "result"}]
        dataset = Dataset(name="Test Dataset", content=content).create()

        mock_service.create.assert_called_once_with(name="Test Dataset", content=content)
        assert dataset.id == mock_dataset.id
        assert dataset.is_synced()

    @patch("galileo.__future__.dataset.Datasets")
    def test_create_handles_api_failure(self, mock_datasets_class: MagicMock, reset_configuration: None) -> None:
        """Test create() handles API failures and sets state correctly."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.create.side_effect = Exception("API Error")

        dataset = Dataset(name="Test Dataset")

        with pytest.raises(Exception, match="API Error"):
            dataset.create()

        assert dataset.sync_state == SyncState.FAILED_SYNC


class TestDatasetGet:
    """Test suite for Dataset.get() class method."""

    @pytest.mark.parametrize("lookup_key", ["name", "id"])
    @patch("galileo.__future__.dataset.Datasets")
    def test_get_returns_dataset(
        self, mock_datasets_class: MagicMock, lookup_key: str, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        """Test get() with name or id returns a synced dataset instance."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset

        lookup_value = mock_dataset.id if lookup_key == "id" else mock_dataset.name
        dataset = Dataset.get(**{lookup_key: lookup_value})

        assert dataset is not None
        assert dataset.is_synced()

    @patch("galileo.__future__.dataset.Datasets")
    def test_get_returns_none_when_not_found(self, mock_datasets_class: MagicMock, reset_configuration: None) -> None:
        """Test get() returns None when dataset is not found."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = None

        dataset = Dataset.get(name="Nonexistent Dataset")

        assert dataset is None

    @patch("galileo.__future__.dataset.Datasets")
    def test_get_raises_error_without_id_or_name(
        self, mock_datasets_class: MagicMock, reset_configuration: None
    ) -> None:
        """Test get() raises ValueError when neither id nor name is provided."""
        with pytest.raises(ValueError, match="Either 'id' or 'name' must be provided"):
            Dataset.get()


class TestDatasetList:
    """Test suite for Dataset.list() class method."""

    @patch("galileo.__future__.dataset.Datasets")
    def test_list_returns_all_datasets(self, mock_datasets_class: MagicMock, reset_configuration: None) -> None:
        """Test list() returns a list of synced dataset instances."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service

        # Create 3 mock datasets
        mock_datasets = []
        for i in range(3):
            mock_ds = MagicMock()
            mock_ds.id = str(uuid4())
            mock_ds.name = f"Dataset {i}"
            mock_ds.created_at = MagicMock()
            mock_ds.updated_at = MagicMock()
            mock_ds.num_rows = 10
            mock_ds.column_names = ["input", "output"]
            mock_ds.draft = False
            mock_datasets.append(mock_ds)
        mock_service.list.return_value = mock_datasets

        datasets = Dataset.list()

        assert len(datasets) == 3
        assert all(isinstance(d, Dataset) for d in datasets)
        assert all(d.is_synced() for d in datasets)


class TestDatasetContent:
    """Test suite for dataset content management."""

    @patch("galileo.__future__.dataset.Datasets")
    def test_get_content(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        """Test get_content() returns the dataset content."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_content = MagicMock(spec=DatasetContent)
        mock_dataset.get_content.return_value = mock_content
        mock_service.get.return_value = mock_dataset

        dataset = Dataset.get(id=mock_dataset.id)
        content = dataset.get_content()

        assert content == mock_content
        mock_dataset.get_content.assert_called_once()

    @pytest.mark.parametrize("method_name", ["get_content", "add_rows", "get_version_history", "get_version", "extend"])
    def test_content_methods_raise_error_for_local_only(self, method_name: str, reset_configuration: None) -> None:
        """Test content methods raise ValueError for local-only dataset."""
        dataset = Dataset(name="Test Dataset")

        with pytest.raises(ValueError, match="Dataset ID is not set"):
            if method_name == "add_rows":
                dataset.add_rows([{"input": "test"}])
            elif method_name == "get_version":
                dataset.get_version(index=0)
            elif method_name == "extend":
                dataset.extend(prompt="Test", count=2)
            else:
                getattr(dataset, method_name)()

    @patch("galileo.__future__.dataset.Datasets")
    def test_add_rows(self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock) -> None:
        """Test add_rows() adds rows to the dataset."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_dataset.num_rows = 12
        mock_service.get.return_value = mock_dataset

        dataset = Dataset.get(id=mock_dataset.id)
        new_rows = [{"input": "new test", "output": "new result"}]
        result = dataset.add_rows(new_rows)

        mock_dataset.add_rows.assert_called_once_with(new_rows)
        assert result == dataset  # Verify method chaining
        assert dataset.is_synced()


class TestDatasetDelete:
    """Test suite for Dataset.delete() method."""

    @patch("galileo.__future__.dataset.Datasets")
    def test_delete_removes_dataset(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        """Test delete() removes the dataset."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset

        dataset = Dataset.get(id=mock_dataset.id)
        dataset.delete()

        mock_service.delete.assert_called_once_with(id=mock_dataset.id)
        assert dataset.sync_state == SyncState.DELETED

    def test_delete_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test delete() raises ValueError for local-only dataset."""
        dataset = Dataset(name="Test Dataset")

        with pytest.raises(ValueError, match="Dataset ID is not set"):
            dataset.delete()


class TestDatasetRefresh:
    """Test suite for Dataset.refresh() method."""

    @patch("galileo.__future__.dataset.Datasets")
    def test_refresh_updates_attributes(self, mock_datasets_class: MagicMock, reset_configuration: None) -> None:
        """Test refresh() updates all attributes from the API."""
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service

        dataset_id = str(uuid4())
        initial = MagicMock()
        initial.id = dataset_id
        initial.name = "Test Dataset"
        initial.created_at = MagicMock()
        initial.updated_at = MagicMock()
        initial.num_rows = 10
        initial.column_names = ["input", "output"]
        initial.draft = True

        updated = MagicMock()
        updated.id = dataset_id
        updated.name = "Test Dataset"
        updated.created_at = initial.created_at
        updated.updated_at = MagicMock()
        updated.num_rows = 15
        updated.column_names = ["input", "output"]
        updated.draft = False

        mock_service.get.side_effect = [initial, updated]

        dataset = Dataset.get(id=dataset_id)
        assert dataset.num_rows == 10

        dataset.refresh()

        assert dataset.num_rows == 15
        assert dataset.is_synced()

    def test_refresh_raises_error_for_local_only(self, reset_configuration: None) -> None:
        """Test refresh() raises ValueError for local-only dataset."""
        dataset = Dataset(name="Test Dataset")

        with pytest.raises(ValueError, match="Dataset ID is not set"):
            dataset.refresh()


class TestDatasetSave:
    """Test suite for Dataset.save() method."""

    @patch("galileo.__future__.dataset.Datasets")
    def test_save_local_only_delegates_to_create(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        # Given: a local-only dataset and a mocked create response
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.create.return_value = mock_dataset

        # When: save() is called on a LOCAL_ONLY dataset
        dataset = Dataset(name="Test Dataset")
        result = dataset.save()

        # Then: create() is called and the dataset is synced
        mock_service.create.assert_called_once_with(name="Test Dataset", content=[])
        assert result.id == mock_dataset.id
        assert result.is_synced()

    @patch("galileo.__future__.dataset.Datasets")
    def test_save_synced_is_noop(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        # Given: a synced dataset
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset

        dataset = Dataset.get(id=mock_dataset.id)
        assert dataset.is_synced()

        # When: save() is called
        result = dataset.save()

        # Then: no API update call is made and dataset remains synced
        mock_service.update.assert_not_called()
        assert result is dataset
        assert result.is_synced()

    def test_save_deleted_raises_value_error(self, reset_configuration: None) -> None:
        # Given: a dataset in DELETED state
        dataset = Dataset(name="Test Dataset")
        dataset.id = str(uuid4())
        dataset._set_state(SyncState.DELETED)

        # When/Then: save() raises ValueError
        with pytest.raises(ValueError, match="Cannot save a deleted dataset"):
            dataset.save()

    def test_save_without_id_raises_value_error(self, reset_configuration: None) -> None:
        # Given: a dataset in DIRTY state with no ID
        dataset = Dataset(name="Test Dataset")
        dataset._set_state(SyncState.DIRTY)

        # When/Then: save() raises ValueError because there is no ID to update
        with pytest.raises(ValueError, match="Dataset ID is not set"):
            dataset.save()

    @patch("galileo.__future__.dataset.GalileoPythonConfig")
    @patch("galileo.__future__.dataset.update_dataset_datasets_dataset_id_patch")
    @patch("galileo.__future__.dataset.Datasets")
    def test_save_dirty_calls_update_and_syncs_attributes(
        self,
        mock_datasets_class: MagicMock,
        mock_update_patch: MagicMock,
        mock_config_class: MagicMock,
        reset_configuration: None,
        mock_dataset: MagicMock,
    ) -> None:
        # Given: a synced dataset and a mocked API update response with all synced fields
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset

        updated_at = MagicMock()
        updated_response = MagicMock()
        updated_response.id = mock_dataset.id
        updated_response.name = "Renamed Dataset"
        updated_response.created_at = mock_dataset.created_at
        updated_response.updated_at = updated_at
        updated_response.num_rows = 42
        updated_response.column_names = ["input", "output"]
        updated_response.draft = True

        mock_detailed = MagicMock()
        mock_detailed.status_code = 200
        mock_detailed.parsed = updated_response
        mock_update_patch.sync_detailed.return_value = mock_detailed

        dataset = Dataset.get(id=mock_dataset.id)
        assert dataset.is_synced()

        # When: the name is changed (triggers SYNCED → DIRTY automatically) and save() is called
        dataset.name = "Renamed Dataset"
        assert dataset.is_dirty(), "name change should transition SYNCED → DIRTY"

        result = dataset.save()

        # Then: the direct API call is made and ALL synced fields are updated
        mock_update_patch.sync_detailed.assert_called_once()
        assert result.name == "Renamed Dataset"
        assert result.updated_at == updated_at
        assert result.num_rows == 42
        assert result.column_names == ["input", "output"]
        assert result.draft is True
        assert result.id == mock_dataset.id
        assert result.is_synced()

    @patch("galileo.__future__.dataset.Datasets")
    def test_save_failed_sync_raises_value_error(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        # Given: a dataset in FAILED_SYNC state (e.g., from a prior failed operation)
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset

        dataset = Dataset.get(id=mock_dataset.id)
        dataset._set_state(SyncState.FAILED_SYNC)

        # When/Then: save() raises ValueError directing user to refresh()
        with pytest.raises(ValueError, match="FAILED_SYNC"):
            dataset.save()

    @patch("galileo.__future__.dataset.GalileoPythonConfig")
    @patch("galileo.__future__.dataset.update_dataset_datasets_dataset_id_patch")
    @patch("galileo.__future__.dataset.Datasets")
    def test_save_handles_api_failure(
        self,
        mock_datasets_class: MagicMock,
        mock_update_patch: MagicMock,
        mock_config_class: MagicMock,
        reset_configuration: None,
        mock_dataset: MagicMock,
    ) -> None:
        # Given: a synced dataset that has been dirtied, and an API that raises an error
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset
        mock_update_patch.sync_detailed.side_effect = RuntimeError("API error")

        dataset = Dataset.get(id=mock_dataset.id)
        # Trigger DIRTY via real user flow (name assignment)
        dataset.name = "Trigger Dirty"
        assert dataset.is_dirty()

        # When/Then: the exception propagates and state is FAILED_SYNC
        with pytest.raises(RuntimeError, match="API error"):
            dataset.save()

        assert dataset.sync_state == SyncState.FAILED_SYNC


class TestDatasetDirtyTracking:
    """Test suite for Dataset dirty-tracking via __setattr__."""

    @patch("galileo.__future__.dataset.Datasets")
    def test_dirty_tracking_transitions_on_name_change(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        # Given: a synced dataset
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset

        dataset = Dataset.get(id=mock_dataset.id)
        assert dataset.is_synced()

        # When: the name is changed to a different value
        dataset.name = "A Completely New Name"

        # Then: the state transitions to DIRTY
        assert dataset.is_dirty()
        assert dataset.name == "A Completely New Name"

    @patch("galileo.__future__.dataset.Datasets")
    def test_dirty_tracking_noop_on_same_value(
        self, mock_datasets_class: MagicMock, reset_configuration: None, mock_dataset: MagicMock
    ) -> None:
        # Given: a synced dataset
        mock_service = MagicMock()
        mock_datasets_class.return_value = mock_service
        mock_service.get.return_value = mock_dataset

        dataset = Dataset.get(id=mock_dataset.id)
        original_name = dataset.name
        assert dataset.is_synced()

        # When: the name is assigned the same value
        dataset.name = original_name

        # Then: the state remains SYNCED (same-value assignment is a no-op)
        assert dataset.is_synced()


class TestDatasetMethods:
    """Test suite for other Dataset methods."""

    def test_str_and_repr(self, reset_configuration: None) -> None:
        """Test __str__ and __repr__ return expected formats."""
        dataset = Dataset(name="Test Dataset")
        dataset.id = "test-id-123"
        dataset.num_rows = 42

        assert str(dataset) == "Dataset(name='Test Dataset', id='test-id-123')"
        assert "rows=42" in repr(dataset)
