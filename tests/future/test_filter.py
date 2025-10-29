"""Comprehensive tests for filter builders."""

import datetime

import pytest

from galileo.__future__.shared.filter import (
    BooleanFilter,
    DateFilter,
    Filter,
    NumberFilter,
    TextFilter,
    boolean,
    date,
    number,
    text,
)
from galileo.resources.models import (
    LogRecordsDateFilter,
    LogRecordsDateFilterOperator,
    LogRecordsNumberFilter,
    LogRecordsNumberFilterOperator,
    LogRecordsTextFilter,
    LogRecordsTextFilterOperator,
)


class TestFilterBase:
    """Test suite for Filter base class."""

    def test_filter_initialization(self, reset_configuration: None):
        """Test Filter base class stores column_id."""
        filter_obj = Filter("test_column")
        assert filter_obj.column_id == "test_column"


class TestTextFilter:
    """Test suite for TextFilter class."""

    @pytest.mark.parametrize("case_sensitive", [True, False])
    def test_text_filter_initialization(self, case_sensitive, reset_configuration: None):
        """Test TextFilter initialization with case sensitivity."""
        text_filter = TextFilter("input", case_sensitive=case_sensitive)
        assert text_filter.column_id == "input" and text_filter.case_sensitive == case_sensitive

    @pytest.mark.parametrize(
        "method_name,value,case_sensitive,expected_op",
        [
            ("equals", "test", True, LogRecordsTextFilterOperator.EQ),
            ("not_equals", "exclude", False, LogRecordsTextFilterOperator.NE),
            ("contains", "substring", True, LogRecordsTextFilterOperator.CONTAINS),
            ("one_of", ["a", "b"], True, LogRecordsTextFilterOperator.ONE_OF),
            ("one_of", [], False, LogRecordsTextFilterOperator.ONE_OF),
            ("not_in", ["x", "y"], True, LogRecordsTextFilterOperator.NOT_IN),
        ],
    )
    def test_text_filter_methods(self, method_name, value, case_sensitive, expected_op, reset_configuration: None):
        """Test all text filter methods with case sensitivity."""
        text_filter = TextFilter("col", case_sensitive=case_sensitive)
        result = getattr(text_filter, method_name)(value)

        assert isinstance(result, LogRecordsTextFilter)
        assert result.column_id == "col" and result.operator == expected_op
        assert result.value == value and result.case_sensitive == case_sensitive


class TestNumberFilter:
    """Test suite for NumberFilter class."""

    @pytest.mark.parametrize(
        "method_name,value,expected_op",
        [
            ("equals", 42, LogRecordsNumberFilterOperator.EQ),
            ("equals", 0, LogRecordsNumberFilterOperator.EQ),
            ("not_equals", 99.99, LogRecordsNumberFilterOperator.NE),
            ("greater_than", 0.5, LogRecordsNumberFilterOperator.GT),
            ("greater_than_or_equal", 100, LogRecordsNumberFilterOperator.GTE),
            ("less_than", 9.99, LogRecordsNumberFilterOperator.LT),
            ("less_than_or_equal", 4.5, LogRecordsNumberFilterOperator.LTE),
        ],
    )
    def test_number_filter_methods(self, method_name, value, expected_op, reset_configuration: None):
        """Test number filter methods with integers and floats."""
        result = getattr(NumberFilter("metric"), method_name)(value)
        assert isinstance(result, LogRecordsNumberFilter)
        assert result.column_id == "metric" and result.operator == expected_op and result.value == value

    @pytest.mark.parametrize("min_val,max_val", [(0, 100), (-10, 10), (0.0, 1.0)])
    def test_number_filter_between(self, min_val, max_val, reset_configuration: None):
        """Test between method with various ranges."""
        result = NumberFilter("count").between(min_val, max_val)
        assert result.operator == LogRecordsNumberFilterOperator.BETWEEN and result.value == [min_val, max_val]


class TestDateFilter:
    """Test suite for DateFilter class."""

    @pytest.mark.parametrize("input_value", ["2024-01-01", "2024-12-31T23:59:59", datetime.datetime(2024, 6, 15)])
    def test_date_filter_parse_date(self, input_value, reset_configuration: None):
        """Test _parse_date handles string and datetime inputs."""
        result = DateFilter("timestamp")._parse_date(input_value)
        assert isinstance(result, datetime.datetime)

    @pytest.mark.parametrize(
        "method_name,value,expected_op",
        [
            ("equals", "2024-01-01", LogRecordsDateFilterOperator.EQ),
            ("not_equals", datetime.datetime(2024, 12, 31), LogRecordsDateFilterOperator.NE),
            ("before", "2024-06-01", LogRecordsDateFilterOperator.LT),
            ("after", datetime.datetime(2024, 6, 30), LogRecordsDateFilterOperator.GT),
            ("on_or_before", "2024-03-15", LogRecordsDateFilterOperator.LTE),
            ("on_or_after", "2024-09-01", LogRecordsDateFilterOperator.GTE),
        ],
    )
    def test_date_filter_methods(self, method_name, value, expected_op, reset_configuration: None):
        """Test date filter methods with string and datetime inputs."""
        result = getattr(DateFilter("created_at"), method_name)(value)
        assert isinstance(result, LogRecordsDateFilter)
        assert result.column_id == "created_at" and result.operator == expected_op
        assert isinstance(result.value, datetime.datetime)


class TestBooleanFilter:
    """Test suite for BooleanFilter class."""

    def test_boolean_filter_multiple_calls(self, reset_configuration: None):
        """Test creating multiple filters from same filter instance."""
        bool_builder = BooleanFilter("active")
        true_filter = bool_builder.is_true()
        false_filter = bool_builder.is_false()
        equals_filter = bool_builder.equals(True)

        assert all(f.column_id == "active" for f in [true_filter, false_filter, equals_filter])
        assert true_filter.value is True
        assert false_filter.value is False
        assert equals_filter.value is True


class TestFilterFactoryFunctions:
    """Test suite for filter factory functions."""

    def test_factory_functions(self, reset_configuration: None):
        """Test all factory functions create correct filter types."""
        text_filter = text("col", case_sensitive=False)
        assert isinstance(text_filter, TextFilter) and text_filter.case_sensitive is False
        assert text("col").case_sensitive is True  # Default case sensitive

        assert isinstance(number("metric"), NumberFilter)
        assert isinstance(date("timestamp"), DateFilter)
        assert isinstance(boolean("enabled"), BooleanFilter)


class TestFilterChaining:
    """Test suite for filter chaining and method composition."""

    def test_filter_method_chaining(self, reset_configuration: None):
        """Test creating multiple filters from same filter instance."""
        # Text filters
        text_builder = text("status", case_sensitive=False)
        eq_f, ne_f, contains_f = text_builder.equals("a"), text_builder.not_equals("b"), text_builder.contains("c")
        assert all(f.column_id == "status" and f.case_sensitive is False for f in [eq_f, ne_f, contains_f])
        assert [eq_f.operator, ne_f.operator, contains_f.operator] == [
            LogRecordsTextFilterOperator.EQ,
            LogRecordsTextFilterOperator.NE,
            LogRecordsTextFilterOperator.CONTAINS,
        ]

        # Number filters
        num_builder = number("score")
        gt_f, lt_f, between_f = num_builder.greater_than(0.5), num_builder.less_than(1.0), num_builder.between(0.3, 0.9)
        assert all(f.column_id == "score" for f in [gt_f, lt_f, between_f])
        assert [gt_f.operator, lt_f.operator, between_f.operator] == [
            LogRecordsNumberFilterOperator.GT,
            LogRecordsNumberFilterOperator.LT,
            LogRecordsNumberFilterOperator.BETWEEN,
        ]

        # Date filters
        date_builder = date("created_at")
        before_f, after_f = date_builder.before("2024-06-01"), date_builder.after("2024-01-01")
        assert all(f.column_id == "created_at" for f in [before_f, after_f])
        assert [before_f.operator, after_f.operator] == [
            LogRecordsDateFilterOperator.LT,
            LogRecordsDateFilterOperator.GT,
        ]


class TestFilterEdgeCases:
    """Test suite for filter edge cases and special values."""

    @pytest.mark.parametrize("value", ["", " ", "special!@#$%", "你好"])
    def test_text_filter_special_strings(self, value, reset_configuration: None):
        """Test text filters handle empty, whitespace, and special characters."""
        assert text("field").equals(value).value == value

    @pytest.mark.parametrize("value", [0, -0, 1e10, 1e-10, float("inf")])
    def test_number_filter_special_numbers(self, value, reset_configuration: None):
        """Test number filters handle zero, large/small numbers, and infinity."""
        assert number("metric").equals(value).value == value

    def test_filter_edge_cases(self, reset_configuration: None):
        """Test various edge cases for filters."""
        # Empty lists
        assert text("field").one_of([]).value == []
        # Equal min/max for between
        assert number("metric").between(5, 5).value == [5, 5]
        # Various date formats
        for date_str in ["2024-01-01", "2024/01/01", "2024-01-01T12:30:45"]:
            assert isinstance(date("timestamp").after(date_str).value, datetime.datetime)
