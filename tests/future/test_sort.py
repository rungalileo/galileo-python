"""Comprehensive tests for sort builders."""

import pytest

from galileo.__future__.shared.sort import Sort, sort
from galileo.resources.models import LogRecordsSortClause


class TestSort:
    """Test suite for Sort class."""

    @pytest.mark.parametrize("column_id", ["simple", "with_underscore", "with-dash", "with.dot", "123"])
    def test_sort_initialization(self, column_id, reset_configuration: None):
        """Test Sort initialization with various column IDs."""
        assert Sort(column_id).column_id == column_id

    @pytest.mark.parametrize("method_name,expected_asc", [("ascending", True), ("descending", False)])
    def test_sort_direction_methods(self, method_name, expected_asc, reset_configuration: None):
        """Test ascending() and descending() create correct sort clauses."""
        result = getattr(Sort("col"), method_name)()
        assert isinstance(result, LogRecordsSortClause)
        assert result.column_id == "col" and result.ascending == expected_asc


class TestSortFactoryFunction:
    """Test suite for sort() factory function."""

    @pytest.mark.parametrize("col_id", ["input", "score", "created_at"])
    def test_sort_factory(self, col_id, reset_configuration: None):
        """Test sort() factory creates Sort instance and supports chaining."""
        sort_obj = sort(col_id)
        assert isinstance(sort_obj, Sort) and sort_obj.column_id == col_id

        # Test chaining
        asc, desc = sort_obj.ascending(), sort_obj.descending()
        assert all(isinstance(c, LogRecordsSortClause) and c.column_id == col_id for c in [asc, desc])
        assert asc.ascending is True and desc.ascending is False


class TestSortMethodChaining:
    """Test suite for Sort method chaining and reusability."""

    def test_sort_reusability_and_independence(self, reset_configuration: None):
        """Test Sort instances create multiple clauses and remain independent."""
        # Single instance creates multiple clauses
        builder = sort("score")
        asc, desc = builder.ascending(), builder.descending()
        assert asc.column_id == desc.column_id == "score"
        assert asc.ascending is True and desc.ascending is False

        # Multiple instances are independent
        c1, c2 = sort("col_a").ascending(), sort("col_b").descending()
        assert c1.column_id == "col_a" and c2.column_id == "col_b"
        assert c1.ascending is True and c2.ascending is False


class TestSortIntegration:
    """Test suite for Sort with various use cases."""

    @pytest.mark.parametrize(
        "col_id,direction", [("created_at", "desc"), ("score", "desc"), ("cost", "asc"), ("latency", "asc")]
    )
    def test_sort_common_use_cases(self, col_id, direction, reset_configuration: None):
        """Test sort with common columns and typical directions."""
        method = "descending" if direction == "desc" else "ascending"
        clause = getattr(sort(col_id), method)()
        assert clause.column_id == col_id and clause.ascending == (direction == "asc")

    def test_multi_column_sort(self, reset_configuration: None):
        """Test creating sort clauses for multiple columns."""
        clauses = [sort("priority").descending(), sort("created_at").ascending(), sort("name").ascending()]
        assert [c.column_id for c in clauses] == ["priority", "created_at", "name"]
        assert [c.ascending for c in clauses] == [False, True, True]


class TestSortEdgeCases:
    """Test suite for Sort edge cases and special scenarios."""

    @pytest.mark.parametrize("col_id", ["", " ", "a", "very_long_column_name_with_many_underscores"])
    def test_sort_unusual_column_ids(self, col_id, reset_configuration: None):
        """Test Sort handles unusual but valid column IDs."""
        assert sort(col_id).ascending().column_id == col_id

    def test_sort_produces_distinct_objects(self, reset_configuration: None):
        """Test sort methods produce distinct objects with correct properties."""
        builder = sort("col")
        asc1, asc2, desc = builder.ascending(), builder.ascending(), builder.descending()

        # Each call produces new object
        assert asc1 is not asc2 and asc1 is not desc
        # All have same column_id
        assert asc1.column_id == asc2.column_id == desc.column_id == "col"
        # Properties are immutable
        _ = builder.descending()
        assert asc1.ascending is True  # Still True
