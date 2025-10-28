"""Column wrapper for type-safe filtering and sorting."""

from __future__ import annotations

import datetime
from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING, Any

from galileo.__future__.shared.exceptions import ValidationError
from galileo.__future__.shared.filter import date, number, text
from galileo.__future__.shared.sort import sort
from galileo.resources.models import (
    DataType,
    LogRecordsDateFilter,
    LogRecordsNumberFilter,
    LogRecordsSortClause,
    LogRecordsTextFilter,
)
from galileo.resources.types import Unset

if TYPE_CHECKING:
    from galileo.resources.models import ColumnInfo

# Constants for common data type groups
_TEXT_TYPES = (DataType.TEXT, DataType.UUID)
_TEXT_LIST_TYPES = (DataType.TEXT, DataType.UUID, DataType.TAG)
_NUMERIC_TYPES = (DataType.INTEGER, DataType.FLOATING_POINT)
_DATE_TYPES = (DataType.TIMESTAMP,)


def _unwrap_unset(value: Any, default: Any = None) -> Any:
    """Helper to unwrap Unset values."""
    return value if not isinstance(value, Unset) else default


class Column:
    """
    Wrapper for ColumnInfo that provides type-safe filtering and sorting.

    This class validates filter and sort operations based on the column's
    data_type and sortable attributes, ensuring only valid operations are performed.

    Attributes
    ----------
        id (str): The column identifier.
        label (str | None): The display label for the column.
        data_type (DataType | None): The data type of the column.
        filterable (bool): Whether the column can be filtered.
        sortable (bool): Whether the column can be sorted.
        description (str | None): A description of the column.
        category (str): The column category.
        multi_valued (bool): Whether the column contains multiple values.
        allowed_values (list[Any] | None): Allowed values for this column.

    Examples
    --------
        # Access columns from a log stream
        log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

        # Filter and sort using columns
        traces = log_stream.get_traces(
            filters=[
                log_stream.trace_columns["input"].contains("hello"),
                log_stream.trace_columns["created_at"].after("2024-01-01")
            ],
            sort=log_stream.trace_columns["created_at"].descending()
        )
    """

    def __init__(self, column_info: ColumnInfo) -> None:
        """
        Initialize a Column from a ColumnInfo object.

        Args:
            column_info: The ColumnInfo object to wrap.
        """
        self.id = column_info.id
        self.label = _unwrap_unset(column_info.label)
        self.data_type = _unwrap_unset(column_info.data_type)
        self.filterable = _unwrap_unset(column_info.filterable, default=False)
        self.sortable = _unwrap_unset(column_info.sortable, default=False)
        self.description = _unwrap_unset(column_info.description)
        self.category = column_info.category
        self.multi_valued = _unwrap_unset(column_info.multi_valued, default=False)
        self.allowed_values = _unwrap_unset(column_info.allowed_values)

    def __repr__(self) -> str:
        """String representation of the column."""
        parts = [f"Column(id='{self.id}'"]
        if self.label:
            parts.append(f"label='{self.label}'")
        if self.data_type:
            parts.append(f"type='{self.data_type.value}'")
        parts.append(f"filterable={self.filterable}")
        parts.append(f"sortable={self.sortable}")
        return ", ".join(parts) + ")"

    __str__ = __repr__

    def _validate_filterable(self) -> None:
        """Validate that the column is filterable."""
        if not self.filterable:
            raise ValidationError(f"Column '{self.id}' is not filterable.")

    def _validate_sortable(self) -> None:
        """Validate that the column is sortable."""
        if not self.sortable:
            raise ValidationError(f"Column '{self.id}' is not sortable.")

    def _validate_data_type(self, expected_types: tuple[DataType, ...], operation: str) -> None:
        """
        Validate that the column has one of the expected data types.

        Args:
            expected_types: Tuple of acceptable data types for this operation.
            operation: The name of the operation being attempted (for error messages).

        Raises
        ------
            ValidationError: If the column's data type doesn't match expected types.
        """
        if self.data_type is None:
            raise ValidationError(f"Column '{self.id}' has no data type specified. Cannot use {operation} operation.")

        if self.data_type not in expected_types:
            expected_str = ", ".join(dt.value for dt in expected_types)
            raise ValidationError(
                f"Column '{self.id}' has data type '{self.data_type.value}'. "
                f"The {operation} operation requires one of: {expected_str}"
            )

    # Text filter methods
    def equals(self, value: str, case_sensitive: bool = True) -> LogRecordsTextFilter:
        """
        Filter for exact text match.

        Args:
            value: The text value to match.
            case_sensitive: Whether the match should be case-sensitive. Default is True.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a text type.
        """
        self._validate_filterable()
        self._validate_data_type(_TEXT_TYPES, "equals")
        return text(self.id, case_sensitive=case_sensitive).equals(value)

    def not_equals(self, value: str, case_sensitive: bool = True) -> LogRecordsTextFilter:
        """
        Filter for text that does not match.

        Args:
            value: The text value to exclude.
            case_sensitive: Whether the match should be case-sensitive. Default is True.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a text type.
        """
        self._validate_filterable()
        self._validate_data_type(_TEXT_TYPES, "not_equals")
        return text(self.id, case_sensitive=case_sensitive).not_equals(value)

    def contains(self, value: str, case_sensitive: bool = True) -> LogRecordsTextFilter:
        """
        Filter for text that contains a substring.

        Args:
            value: The substring to search for.
            case_sensitive: Whether the search should be case-sensitive. Default is True.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a text type.
        """
        self._validate_filterable()
        self._validate_data_type((DataType.TEXT,), "contains")
        return text(self.id, case_sensitive=case_sensitive).contains(value)

    def one_of(self, values: list[str], case_sensitive: bool = True) -> LogRecordsTextFilter:
        """
        Filter for text that matches any value in a list.

        Args:
            values: List of text values to match.
            case_sensitive: Whether the match should be case-sensitive. Default is True.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a text type.
        """
        self._validate_filterable()
        self._validate_data_type(_TEXT_LIST_TYPES, "one_of")
        return text(self.id, case_sensitive=case_sensitive).one_of(values)

    def not_in(self, values: list[str], case_sensitive: bool = True) -> LogRecordsTextFilter:
        """
        Filter for text that does not match any value in a list.

        Args:
            values: List of text values to exclude.
            case_sensitive: Whether the match should be case-sensitive. Default is True.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a text type.
        """
        self._validate_filterable()
        self._validate_data_type(_TEXT_LIST_TYPES, "not_in")
        return text(self.id, case_sensitive=case_sensitive).not_in(values)

    # Number filter methods
    def greater_than(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers greater than a value.

        Args:
            value: The threshold value (exclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a number type.
        """
        self._validate_filterable()
        self._validate_data_type(_NUMERIC_TYPES, "greater_than")
        return number(self.id).greater_than(value)

    def greater_than_or_equal(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers greater than or equal to a value.

        Args:
            value: The threshold value (inclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a number type.
        """
        self._validate_filterable()
        self._validate_data_type(_NUMERIC_TYPES, "greater_than_or_equal")
        return number(self.id).greater_than_or_equal(value)

    def less_than(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers less than a value.

        Args:
            value: The threshold value (exclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a number type.
        """
        self._validate_filterable()
        self._validate_data_type(_NUMERIC_TYPES, "less_than")
        return number(self.id).less_than(value)

    def less_than_or_equal(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers less than or equal to a value.

        Args:
            value: The threshold value (inclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a number type.
        """
        self._validate_filterable()
        self._validate_data_type(_NUMERIC_TYPES, "less_than_or_equal")
        return number(self.id).less_than_or_equal(value)

    def between(self, min_value: int | float, max_value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers within a range (inclusive).

        Args:
            min_value: The minimum value (inclusive).
            max_value: The maximum value (inclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a number type.
        """
        self._validate_filterable()
        self._validate_data_type(_NUMERIC_TYPES, "between")
        return number(self.id).between(min_value, max_value)

    # Date filter methods
    def before(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates before a value (exclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a timestamp type.
        """
        self._validate_filterable()
        self._validate_data_type(_DATE_TYPES, "before")
        return date(self.id).before(value)

    def after(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates after a value (exclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a timestamp type.
        """
        self._validate_filterable()
        self._validate_data_type(_DATE_TYPES, "after")
        return date(self.id).after(value)

    def on_or_before(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates on or before a value (inclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a timestamp type.
        """
        self._validate_filterable()
        self._validate_data_type(_DATE_TYPES, "on_or_before")
        return date(self.id).on_or_before(value)

    def on_or_after(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates on or after a value (inclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.

        Raises
        ------
            ValidationError: If the column is not filterable or not a timestamp type.
        """
        self._validate_filterable()
        self._validate_data_type(_DATE_TYPES, "on_or_after")
        return date(self.id).on_or_after(value)

    # Sort methods
    def ascending(self) -> LogRecordsSortClause:
        """
        Sort in ascending order.

        Returns
        -------
            LogRecordsSortClause: A configured sort clause.

        Raises
        ------
            ValidationError: If the column is not sortable.
        """
        self._validate_sortable()
        return sort(self.id).ascending()

    def descending(self) -> LogRecordsSortClause:
        """
        Sort in descending order.

        Returns
        -------
            LogRecordsSortClause: A configured sort clause.

        Raises
        ------
            ValidationError: If the column is not sortable.
        """
        self._validate_sortable()
        return sort(self.id).descending()


class ColumnCollection(Mapping[str, Column]):
    """
    A dictionary-like collection of Column objects for easy access by column ID.

    This class provides convenient access to columns using dictionary syntax,
    while also supporting iteration and other collection operations.

    Inherits from `Mapping[str, Column]` to provide a read-only mapping interface.

    Examples
    --------
        log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")

        # Access a column by ID
        input_column = log_stream.trace_columns["input"]

        # Iterate over column IDs
        for column_id in log_stream.trace_columns:
            print(column_id)

        # Iterate over Column objects
        for column in log_stream.trace_columns.values():
            print(column)

        # Check if a column exists
        if "input" in log_stream.trace_columns:
            print("Input column exists")
    """

    def __init__(self, columns: list[Column]) -> None:
        """
        Initialize a ColumnCollection from a list of Column objects.

        Args:
            columns: List of Column objects to include in the collection.
        """
        self._columns: dict[str, Column] = {col.id: col for col in columns}

    def __getitem__(self, column_id: str) -> Column:
        """
        Get a column by its ID.

        Args:
            column_id: The ID of the column to retrieve.

        Returns
        -------
            Column: The requested column.

        Raises
        ------
            KeyError: If the column ID doesn't exist.
        """
        if column_id not in self._columns:
            raise KeyError(f"Column '{column_id}' not found. Available columns: {list(self._columns.keys())}")
        return self._columns[column_id]

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over the column IDs in the collection.

        Note: This returns an iterator of column IDs (keys), following the Mapping protocol.
        To iterate over Column objects, use `collection.values()`.
        """
        return iter(self._columns)

    def __len__(self) -> int:
        """Get the number of columns in the collection."""
        return len(self._columns)

    def __repr__(self) -> str:
        """String representation of the collection."""
        return f"ColumnCollection({len(self._columns)} columns: {list(self._columns.keys())})"

    __str__ = __repr__
