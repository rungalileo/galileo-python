"""Declarative filter builders for SDK queries."""

from __future__ import annotations

import datetime

from dateutil.parser import parse as parse_date

from galileo.resources.models import (
    LogRecordsBooleanFilter,
    LogRecordsDateFilter,
    LogRecordsDateFilterOperator,
    LogRecordsNumberFilter,
    LogRecordsNumberFilterOperator,
    LogRecordsTextFilter,
    LogRecordsTextFilterOperator,
)


class Filter:
    """
    Base class for declarative filter construction.

    This class defines the interface for building type-safe filters
    that can be used with LogStream queries and other SDK operations.
    """

    __slots__ = ("column_id",)

    def __init__(self, column_id: str):
        """
        Initialize a filter for a specific column.

        Args:
            column_id: The ID of the column to filter on.
        """
        self.column_id = column_id


class TextFilter(Filter):
    """
    Builder for text-based filters.

    Supports operators: equals, not_equals, contains, one_of, not_in

    Examples
    --------
        text("input").equals("hello")
        text("status").contains("error")
        text("name").one_of(["Alice", "Bob"])
    """

    __slots__ = ("case_sensitive",)

    def __init__(self, column_id: str, case_sensitive: bool = True):
        """
        Initialize a text filter builder.

        Args:
            column_id: The ID of the column to filter on.
            case_sensitive: Whether the filter should be case-sensitive. Default is True.
        """
        super().__init__(column_id)
        self.case_sensitive = case_sensitive

    def equals(self, value: str) -> LogRecordsTextFilter:
        """
        Filter for exact text match.

        Args:
            value: The text value to match.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.
        """
        return LogRecordsTextFilter(
            column_id=self.column_id,
            operator=LogRecordsTextFilterOperator.EQ,
            value=value,
            case_sensitive=self.case_sensitive,
        )

    def not_equals(self, value: str) -> LogRecordsTextFilter:
        """
        Filter for text that does not match.

        Args:
            value: The text value to exclude.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.
        """
        return LogRecordsTextFilter(
            column_id=self.column_id,
            operator=LogRecordsTextFilterOperator.NE,
            value=value,
            case_sensitive=self.case_sensitive,
        )

    def contains(self, value: str) -> LogRecordsTextFilter:
        """
        Filter for text that contains a substring.

        Args:
            value: The substring to search for.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.
        """
        return LogRecordsTextFilter(
            column_id=self.column_id,
            operator=LogRecordsTextFilterOperator.CONTAINS,
            value=value,
            case_sensitive=self.case_sensitive,
        )

    def one_of(self, values: list[str]) -> LogRecordsTextFilter:
        """
        Filter for text that matches any value in a list.

        Args:
            values: List of text values to match.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.
        """
        return LogRecordsTextFilter(
            column_id=self.column_id,
            operator=LogRecordsTextFilterOperator.ONE_OF,
            value=values,
            case_sensitive=self.case_sensitive,
        )

    def not_in(self, values: list[str]) -> LogRecordsTextFilter:
        """
        Filter for text that does not match any value in a list.

        Args:
            values: List of text values to exclude.

        Returns
        -------
            LogRecordsTextFilter: A configured text filter.
        """
        return LogRecordsTextFilter(
            column_id=self.column_id,
            operator=LogRecordsTextFilterOperator.NOT_IN,
            value=values,
            case_sensitive=self.case_sensitive,
        )


class NumberFilter(Filter):
    """
    Builder for number-based filters.

    Supports operators: equals, not_equals, greater_than, greater_than_or_equal,
                        less_than, less_than_or_equal, between

    Examples
    --------
        number("score").greater_than(0.8)
        number("count").between(10, 100)
        number("rating").equals(5)
    """

    def equals(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for exact number match.

        Args:
            value: The number to match.

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.
        """
        return LogRecordsNumberFilter(column_id=self.column_id, operator=LogRecordsNumberFilterOperator.EQ, value=value)

    def not_equals(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers that don't match.

        Args:
            value: The number to exclude.

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.
        """
        return LogRecordsNumberFilter(column_id=self.column_id, operator=LogRecordsNumberFilterOperator.NE, value=value)

    def greater_than(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers greater than a value.

        Args:
            value: The threshold value (exclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.
        """
        return LogRecordsNumberFilter(column_id=self.column_id, operator=LogRecordsNumberFilterOperator.GT, value=value)

    def greater_than_or_equal(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers greater than or equal to a value.

        Args:
            value: The threshold value (inclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.
        """
        return LogRecordsNumberFilter(
            column_id=self.column_id, operator=LogRecordsNumberFilterOperator.GTE, value=value
        )

    def less_than(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers less than a value.

        Args:
            value: The threshold value (exclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.
        """
        return LogRecordsNumberFilter(column_id=self.column_id, operator=LogRecordsNumberFilterOperator.LT, value=value)

    def less_than_or_equal(self, value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers less than or equal to a value.

        Args:
            value: The threshold value (inclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.
        """
        return LogRecordsNumberFilter(
            column_id=self.column_id, operator=LogRecordsNumberFilterOperator.LTE, value=value
        )

    def between(self, min_value: int | float, max_value: int | float) -> LogRecordsNumberFilter:
        """
        Filter for numbers within a range (inclusive).

        Args:
            min_value: The minimum value (inclusive).
            max_value: The maximum value (inclusive).

        Returns
        -------
            LogRecordsNumberFilter: A configured number filter.
        """
        return LogRecordsNumberFilter(
            column_id=self.column_id, operator=LogRecordsNumberFilterOperator.BETWEEN, value=[min_value, max_value]
        )


class DateFilter(Filter):
    """
    Builder for date-based filters.

    Supports operators: equals, not_equals, before, after, on_or_before, on_or_after

    Examples
    --------
        date("created_at").after("2024-01-01")
        date("updated_at").before(datetime.now())
        date("published_at").on_or_after("2024-01-01")
    """

    def _parse_date(self, value: str | datetime.datetime) -> datetime.datetime:
        """
        Parse a date value into a datetime object.

        Args:
            value: A date string or datetime object.

        Returns
        -------
            datetime.datetime: The parsed datetime.
        """
        if isinstance(value, str):
            return parse_date(value)
        return value

    def equals(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for exact date match.

        Args:
            value: The date to match (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.
        """
        return LogRecordsDateFilter(
            column_id=self.column_id, operator=LogRecordsDateFilterOperator.EQ, value=self._parse_date(value)
        )

    def not_equals(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates that don't match.

        Args:
            value: The date to exclude (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.
        """
        return LogRecordsDateFilter(
            column_id=self.column_id, operator=LogRecordsDateFilterOperator.NE, value=self._parse_date(value)
        )

    def before(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates before a value (exclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.
        """
        return LogRecordsDateFilter(
            column_id=self.column_id, operator=LogRecordsDateFilterOperator.LT, value=self._parse_date(value)
        )

    def after(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates after a value (exclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.
        """
        return LogRecordsDateFilter(
            column_id=self.column_id, operator=LogRecordsDateFilterOperator.GT, value=self._parse_date(value)
        )

    def on_or_before(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates on or before a value (inclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.
        """
        return LogRecordsDateFilter(
            column_id=self.column_id, operator=LogRecordsDateFilterOperator.LTE, value=self._parse_date(value)
        )

    def on_or_after(self, value: str | datetime.datetime) -> LogRecordsDateFilter:
        """
        Filter for dates on or after a value (inclusive).

        Args:
            value: The threshold date (string or datetime).

        Returns
        -------
            LogRecordsDateFilter: A configured date filter.
        """
        return LogRecordsDateFilter(
            column_id=self.column_id, operator=LogRecordsDateFilterOperator.GTE, value=self._parse_date(value)
        )


class BooleanFilter(Filter):
    """
    Builder for boolean-based filters.

    Boolean filters are simple equality checks - there are no operators,
    just matching against true or false values.

    Examples
    --------
        boolean("is_active").is_true()
        boolean("has_error").is_false()
        boolean("enabled").equals(True)
    """

    def equals(self, value: bool) -> LogRecordsBooleanFilter:
        """
        Filter for exact boolean match.

        Args:
            value: The boolean value to match (True or False).

        Returns
        -------
            LogRecordsBooleanFilter: A configured boolean filter.
        """
        return LogRecordsBooleanFilter(column_id=self.column_id, value=value)

    def is_true(self) -> LogRecordsBooleanFilter:
        """
        Filter for boolean columns that are True.

        Returns
        -------
            LogRecordsBooleanFilter: A configured boolean filter for True.
        """
        return LogRecordsBooleanFilter(column_id=self.column_id, value=True)

    def is_false(self) -> LogRecordsBooleanFilter:
        """
        Filter for boolean columns that are False.

        Returns
        -------
            LogRecordsBooleanFilter: A configured boolean filter for False.
        """
        return LogRecordsBooleanFilter(column_id=self.column_id, value=False)


# Builder factory functions
def text(column_id: str, case_sensitive: bool = True) -> TextFilter:
    """
    Create a text filter builder.

    Args:
        column_id: The ID of the column to filter on.
        case_sensitive: Whether the filter should be case-sensitive. Default is True.

    Returns
    -------
        TextFilter: A text filter builder.

    Examples
    --------
        text("input").equals("hello")
        text("status").contains("error", case_sensitive=False)
        text("name").one_of(["Alice", "Bob"])
    """
    return TextFilter(column_id, case_sensitive=case_sensitive)


def number(column_id: str) -> NumberFilter:
    """
    Create a number filter builder.

    Args:
        column_id: The ID of the column to filter on.

    Returns
    -------
        NumberFilter: A number filter builder.

    Examples
    --------
        number("score").greater_than(0.8)
        number("count").between(10, 100)
        number("rating").equals(5)
    """
    return NumberFilter(column_id)


def date(column_id: str) -> DateFilter:
    """
    Create a date filter builder.

    Args:
        column_id: The ID of the column to filter on.

    Returns
    -------
        DateFilter: A date filter builder.

    Examples
    --------
        date("created_at").after("2024-01-01")
        date("updated_at").before(datetime.now())
        date("published_at").on_or_after("2024-01-01")
    """
    return DateFilter(column_id)


def boolean(column_id: str) -> BooleanFilter:
    """
    Create a boolean filter builder.

    Args:
        column_id: The ID of the column to filter on.

    Returns
    -------
        BooleanFilter: A boolean filter builder.

    Examples
    --------
        boolean("is_active").is_true()
        boolean("has_error").is_false()
        boolean("enabled").equals(True)
    """
    return BooleanFilter(column_id)
