"""Comprehensive tests for Column and ColumnCollection classes."""

import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest

from galileo.__future__.shared.column import Column, ColumnCollection, _unwrap_unset
from galileo.__future__.shared.exceptions import ValidationError
from galileo.resources.models import (
    DataType,
    LogRecordsDateFilter,
    LogRecordsDateFilterOperator,
    LogRecordsNumberFilter,
    LogRecordsNumberFilterOperator,
    LogRecordsSortClause,
    LogRecordsTextFilter,
    LogRecordsTextFilterOperator,
)
from galileo.resources.types import UNSET


def _create_mock_column_info(
    column_id: str = "test_col",
    data_type: Any = UNSET,
    filterable: Any = UNSET,
    sortable: Any = UNSET,
    label: Any = UNSET,
    category: str = "test",
    **kwargs,
) -> MagicMock:
    """Helper to create mock ColumnInfo with minimal boilerplate."""
    mock = MagicMock()
    mock.id = column_id
    mock.data_type = data_type
    mock.filterable = filterable
    mock.sortable = sortable
    mock.label = label
    mock.category = category
    mock.description = kwargs.get("description", UNSET)
    mock.multi_valued = kwargs.get("multi_valued", UNSET)
    mock.allowed_values = kwargs.get("allowed_values", UNSET)
    return mock


class TestUnwrapUnset:
    """Test suite for _unwrap_unset helper function."""

    @pytest.mark.parametrize(
        "value,default,expected",
        [
            (UNSET, None, None),
            (UNSET, "default", "default"),
            ("actual", None, "actual"),
            (42, "default", 42),
            (False, True, False),
            (None, "default", None),
        ],
    )
    def test_unwrap_unset_handles_various_types(self, value, default, expected):
        """Test _unwrap_unset with various value types and defaults."""
        assert _unwrap_unset(value, default) == expected


class TestColumnInitialization:
    """Test suite for Column initialization from ColumnInfo."""

    def test_init_with_all_attributes(self, reset_configuration: None) -> None:
        """Test Column initialization with all attributes and UNSET defaults."""
        # Test with all attributes set
        mock = _create_mock_column_info(
            "test_col", DataType.TEXT, True, True, "Label", description="A test column", allowed_values=["a", "b"]
        )
        col = Column(mock)
        assert col.id == "test_col" and col.data_type == DataType.TEXT
        assert col.filterable and col.sortable and col.label == "Label"

        # Test with UNSET attributes (should use defaults)
        col_unset = Column(_create_mock_column_info("test_col"))
        assert col_unset.filterable is False and col_unset.sortable is False
        assert col_unset.label is None and col_unset.multi_valued is False


class TestColumnRepresentation:
    """Test suite for Column string representations."""

    @pytest.mark.parametrize(
        "label,data_type,filterable,sortable,expected_parts",
        [
            ("Name", DataType.TEXT, True, True, ["id='col1'", "label='Name'", "type='text'"]),
            (None, None, False, False, ["id='col1'", "filterable=False", "sortable=False"]),
        ],
    )
    def test_repr_and_str_formats(
        self, label, data_type, filterable, sortable, expected_parts, reset_configuration: None
    ):
        """Test __repr__ and __str__ include correct attributes."""
        col = Column(_create_mock_column_info("col1", data_type, filterable, sortable, label))
        repr_str = repr(col)
        assert all(part in repr_str for part in expected_parts) and str(col) == repr_str


class TestColumnValidation:
    """Test suite for Column validation methods."""

    @pytest.mark.parametrize("filterable,should_raise", [(True, False), (False, True)])
    def test_validate_filterable(self, filterable, should_raise, reset_configuration: None):
        """Test filterable validation."""
        col = Column(_create_mock_column_info(filterable=filterable))
        if should_raise:
            with pytest.raises(ValidationError, match="not filterable"):
                col._validate_filterable()
        else:
            col._validate_filterable()

    @pytest.mark.parametrize("sortable,should_raise", [(True, False), (False, True)])
    def test_validate_sortable(self, sortable, should_raise, reset_configuration: None):
        """Test sortable validation."""
        col = Column(_create_mock_column_info(sortable=sortable))
        if should_raise:
            with pytest.raises(ValidationError, match="not sortable"):
                col._validate_sortable()
        else:
            col._validate_sortable()

    @pytest.mark.parametrize(
        "data_type,expected_types,should_raise",
        [
            (DataType.TEXT, (DataType.TEXT, DataType.UUID), False),
            (DataType.INTEGER, (DataType.TEXT,), True),
            (None, (DataType.TEXT,), True),
        ],
    )
    def test_validate_data_type(self, data_type, expected_types, should_raise, reset_configuration: None):
        """Test data type validation."""
        col = Column(_create_mock_column_info(data_type=data_type, filterable=True))
        if should_raise:
            with pytest.raises(ValidationError):
                col._validate_data_type(expected_types, "test_op")
        else:
            col._validate_data_type(expected_types, "test_op")


class TestColumnTextFilters:
    """Test suite for Column text filter methods."""

    @pytest.mark.parametrize(
        "method_name,args,expected_op",
        [
            ("equals", ("test",), LogRecordsTextFilterOperator.EQ),
            ("not_equals", ("test",), LogRecordsTextFilterOperator.NE),
            ("contains", ("sub",), LogRecordsTextFilterOperator.CONTAINS),
            ("one_of", (["a", "b"],), LogRecordsTextFilterOperator.ONE_OF),
            ("not_in", (["x"],), LogRecordsTextFilterOperator.NOT_IN),
        ],
    )
    def test_text_filter_methods(self, method_name, args, expected_op, reset_configuration: None):
        """Test all text filter methods create correct filters."""
        col = Column(_create_mock_column_info(data_type=DataType.TEXT, filterable=True))
        result = getattr(col, method_name)(*args)
        assert isinstance(result, LogRecordsTextFilter) and result.operator == expected_op

    def test_text_filters_validation(self, reset_configuration: None):
        """Test text filters validate column properties."""
        # Wrong data type
        col_num = Column(_create_mock_column_info(data_type=DataType.INTEGER, filterable=True))
        with pytest.raises(ValidationError, match="equals.*requires"):
            col_num.equals("test")

        # Not filterable
        col_unfilterable = Column(_create_mock_column_info(data_type=DataType.TEXT, filterable=False))
        with pytest.raises(ValidationError, match="not filterable"):
            col_unfilterable.equals("test")


class TestColumnNumberFilters:
    """Test suite for Column number filter methods."""

    @pytest.mark.parametrize(
        "method_name,args,expected_op",
        [
            ("greater_than", (10,), LogRecordsNumberFilterOperator.GT),
            ("greater_than_or_equal", (20.5,), LogRecordsNumberFilterOperator.GTE),
            ("less_than", (5,), LogRecordsNumberFilterOperator.LT),
            ("less_than_or_equal", (15,), LogRecordsNumberFilterOperator.LTE),
            ("between", (0, 100), LogRecordsNumberFilterOperator.BETWEEN),
        ],
    )
    def test_number_filter_methods(self, method_name, args, expected_op, reset_configuration: None):
        """Test all number filter methods create correct filters."""
        col = Column(_create_mock_column_info(data_type=DataType.INTEGER, filterable=True))
        result = getattr(col, method_name)(*args)
        assert isinstance(result, LogRecordsNumberFilter) and result.operator == expected_op

    def test_number_filters_validation(self, reset_configuration: None):
        """Test number filters validate data type."""
        col_text = Column(_create_mock_column_info(data_type=DataType.TEXT, filterable=True))
        with pytest.raises(ValidationError, match="greater_than.*requires"):
            col_text.greater_than(10)


class TestColumnDateFilters:
    """Test suite for Column date filter methods."""

    @pytest.mark.parametrize(
        "method_name,value,expected_op",
        [
            ("before", "2024-01-01", LogRecordsDateFilterOperator.LT),
            ("after", datetime.datetime(2024, 12, 31), LogRecordsDateFilterOperator.GT),
            ("on_or_before", "2024-06-01", LogRecordsDateFilterOperator.LTE),
            ("on_or_after", "2024-06-01", LogRecordsDateFilterOperator.GTE),
        ],
    )
    def test_date_filter_methods(self, method_name, value, expected_op, reset_configuration: None):
        """Test all date filter methods create correct filters and parse dates."""
        col = Column(_create_mock_column_info(data_type=DataType.TIMESTAMP, filterable=True))
        result = getattr(col, method_name)(value)
        assert isinstance(result, LogRecordsDateFilter) and result.operator == expected_op
        assert isinstance(result.value, datetime.datetime)

    def test_date_filters_validation(self, reset_configuration: None):
        """Test date filters validate data type."""
        col_text = Column(_create_mock_column_info(data_type=DataType.TEXT, filterable=True))
        with pytest.raises(ValidationError, match="before.*requires"):
            col_text.before("2024-01-01")


class TestColumnSortMethods:
    """Test suite for Column sort methods."""

    @pytest.mark.parametrize("method_name,expected_asc", [("ascending", True), ("descending", False)])
    def test_sort_methods(self, method_name, expected_asc, reset_configuration: None):
        """Test sort methods create correct sort clauses."""
        col = Column(_create_mock_column_info(sortable=True))
        result = getattr(col, method_name)()
        assert isinstance(result, LogRecordsSortClause) and result.ascending == expected_asc

    def test_sort_validates_sortable(self, reset_configuration: None):
        """Test sort methods validate sortable property."""
        col = Column(_create_mock_column_info(sortable=False))
        with pytest.raises(ValidationError, match="not sortable"):
            col.ascending()
        with pytest.raises(ValidationError, match="not sortable"):
            col.descending()


class TestColumnCollection:
    """Test suite for ColumnCollection class."""

    def test_collection_operations(self, reset_configuration: None):
        """Test ColumnCollection initialization, access, iteration, and repr."""
        # Create collection with 3 columns
        cols = [Column(_create_mock_column_info(f"col_{i}", label=f"Col {i}")) for i in range(3)]
        coll = ColumnCollection(cols)

        # Test len and membership
        assert len(coll) == 3 and "col_0" in coll and "col_1" in coll

        # Test __getitem__
        assert coll["col_0"].id == "col_0" and coll["col_0"].label == "Col 0"

        # Test KeyError for missing column
        with pytest.raises(KeyError, match="Column 'missing' not found"):
            _ = coll["missing"]

        # Test iteration over keys and values
        assert set(coll) == {"col_0", "col_1", "col_2"}
        assert len(list(coll.values())) == 3 and all(isinstance(c, Column) for c in coll.values())

        # Test repr
        repr_str = repr(coll)
        assert "ColumnCollection" in repr_str and "3 columns" in repr_str
        assert str(coll) == repr_str
