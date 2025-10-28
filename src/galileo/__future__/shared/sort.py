"""Declarative sort builders for SDK queries."""

from __future__ import annotations

from galileo.resources.models import LogRecordsSortClause


class Sort:
    """
    Declarative builder for sort clauses.

    Examples
    --------
        sort("created_at").ascending()
        sort("score").descending()
    """

    def __init__(self, column_id: str):
        """
        Initialize a sort builder for a specific column.

        Args:
            column_id: The ID of the column to sort by.
        """
        self.column_id = column_id

    def ascending(self) -> LogRecordsSortClause:
        """
        Sort in ascending order.

        Returns
        -------
            LogRecordsSortClause: A configured sort clause.
        """
        return LogRecordsSortClause(column_id=self.column_id, ascending=True)

    def descending(self) -> LogRecordsSortClause:
        """
        Sort in descending order.

        Returns
        -------
            LogRecordsSortClause: A configured sort clause.
        """
        return LogRecordsSortClause(column_id=self.column_id, ascending=False)


def sort(column_id: str) -> Sort:
    """
    Create a sort builder.

    Args:
        column_id: The ID of the column to sort by.

    Returns
    -------
        Sort: A sort builder.

    Examples
    --------
        sort("created_at").ascending()
        sort("score").descending()
    """
    return Sort(column_id)
