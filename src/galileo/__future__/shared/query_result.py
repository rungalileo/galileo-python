"""Query result wrapper for easy data access and pagination."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, Callable

from galileo.resources.models import LogRecordsQueryResponse
from galileo.resources.types import UNSET

if TYPE_CHECKING:
    from galileo.resources.models import LogRecordsSortClause
    from galileo.schema.filters import FilterType
    from galileo.search import RecordType

logger = logging.getLogger(__name__)


def _flatten_dict(d: dict[str, Any], parent_key: str = "", sep: str = "_") -> dict[str, Any]:
    """
    Flatten a nested dictionary into a single-level dictionary.

    Args:
        d: The dictionary to flatten.
        parent_key: The parent key (used for recursion).
        sep: The separator to use between keys.

    Returns
    -------
        A flattened dictionary.
    """
    items: list[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict) and not isinstance(v, UNSET.__class__):
            # Recursively flatten nested dictionaries
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class QueryResult:
    """
    A list-like wrapper for query results that provides easy access to records and pagination.

    This class makes it simple to work with query results by:
    - Providing list-like indexing and iteration (e.g., result[0], for record in result)
    - Flattening nested record structures into simple dictionaries
    - Exposing pagination metadata (limit, next_starting_token, paginated)
    - Offering a next_page() method to easily fetch subsequent pages

    Attributes
    ----------
        limit (int): The maximum number of records per page.
        next_starting_token (int | None): Token for fetching the next page, or None if this is the last page.
        paginated (bool): Whether pagination is enabled.
        starting_token (int): The starting token used for this page.
        last_row_id (str | None): The ID of the last row in this result set.

    Examples
    --------
        # Basic iteration
        log_stream = LogStream.get(name="Production Logs", project_name="My AI Project")
        result = log_stream.get_spans(limit=10)

        for record in result:
            print(record["id"], record["input"])

        # Index access
        first_record = result[0]
        print(first_record["created_at"])

        # Pagination (in-place - extends the current result)
        if result.has_next_page:
            result.next_page()
            print(f"Now have {len(result)} records after fetching next page")

        # Pagination (with assignment - same object returned)
        result = log_stream.get_spans(limit=10)
        if result.has_next_page:
            result = result.next_page()
            for record in result:
                print(record["id"])

        # Check pagination status
        print(f"Total records in this page: {len(result)}")
        print(f"Has next page: {result.has_next_page}")
    """

    def __init__(
        self,
        response: LogRecordsQueryResponse,
        query_fn: Callable[..., LogRecordsQueryResponse],
        record_type: RecordType,
        filters: list[FilterType] | None = None,
        sort: LogRecordsSortClause | None = None,
    ):
        """
        Initialize a QueryResult wrapper.

        Args:
            response: The raw LogRecordsQueryResponse from the API.
            query_fn: The function to call for pagination (e.g., log_stream.query).
            record_type: The type of records being queried.
            filters: The filters used in the original query.
            sort: The sort clause used in the original query.
        """
        self._response = response
        self._query_fn = query_fn
        self._record_type = record_type
        self._filters = filters
        self._sort = sort
        self._flattened_records: list[dict[str, Any]] | None = None

    @property
    def limit(self) -> int:
        """The maximum number of records per page."""
        limit = self._response.limit
        if isinstance(limit, type(UNSET)) or limit is None:
            return 100
        return limit

    @property
    def next_starting_token(self) -> int | None:
        """Token for fetching the next page, or None if this is the last page."""
        token = self._response.next_starting_token
        if isinstance(token, type(UNSET)) or token is None:
            return None
        return token

    @property
    def paginated(self) -> bool:
        """Whether pagination is enabled."""
        return self._response.paginated if not isinstance(self._response.paginated, type(UNSET)) else False

    @property
    def starting_token(self) -> int:
        """The starting token used for this page."""
        return self._response.starting_token if not isinstance(self._response.starting_token, type(UNSET)) else 0

    @property
    def last_row_id(self) -> str | None:
        """The ID of the last row in this result set."""
        row_id = self._response.last_row_id
        if isinstance(row_id, type(UNSET)) or row_id is None:
            return None
        return row_id

    @property
    def has_next_page(self) -> bool:
        """Whether there is a next page available."""
        return self.next_starting_token is not None

    @property
    def _records(self) -> list[dict[str, Any]]:
        """Get flattened records, caching them for performance."""
        if self._flattened_records is None:
            self._flattened_records = self._flatten_records()
        return self._flattened_records

    def _flatten_records(self) -> list[dict[str, Any]]:
        """Convert response records to flattened dictionaries."""
        if isinstance(self._response.records, type(UNSET)) or self._response.records is None:
            return []

        flattened = []
        for record in self._response.records:
            # Convert record to dict
            record_dict = record.to_dict()
            # Flatten nested structures
            flat_dict = _flatten_dict(record_dict)
            flattened.append(flat_dict)

        return flattened

    def next_page(self) -> QueryResult:
        """
        Fetch the next page and extend current results.

        Returns
        -------
            QueryResult: Returns self with the new records appended.

        Raises
        ------
            ValueError: If there is no next page available.

        Examples
        --------
            # In-place usage (mutates the result)
            result = log_stream.get_spans(limit=10)
            if result.has_next_page:
                result.next_page()
                print(f"Now have {len(result)} records")

            # Assignment usage (same object, supports chaining)
            result = log_stream.get_spans(limit=10)
            if result.has_next_page:
                result = result.next_page()
                for record in result:
                    print(record["id"])
        """
        if not self.has_next_page:
            raise ValueError("No next page available. Check has_next_page before calling next_page().")

        logger.debug(f"QueryResult.next_page: fetching page with starting_token={self.next_starting_token}")

        # Call the query function with the next starting token
        next_response = self._query_fn(
            record_type=self._record_type,
            filters=self._filters,
            sort=self._sort,
            limit=self.limit,
            starting_token=self.next_starting_token,
        )

        # Extend current records with new page
        if not isinstance(next_response.records, type(UNSET)) and next_response.records:
            for record in next_response.records:
                flat_dict = _flatten_dict(record.to_dict())
                self._records.append(flat_dict)

        # Update response metadata
        self._response = next_response
        return self

    def __len__(self) -> int:
        """Return the number of records in this page."""
        return len(self._records)

    def __getitem__(self, index: int | slice) -> dict[str, Any] | list[dict[str, Any]]:
        """
        Get a record by index or slice.

        Args:
            index: The index or slice to retrieve.

        Returns
        -------
            A single record dictionary or a list of record dictionaries.

        Examples
        --------
            result = log_stream.get_spans()
            first = result[0]
            first_ten = result[:10]
        """
        return self._records[index]

    def __iter__(self) -> Iterator[dict[str, Any]]:
        """Iterate over the records in this page."""
        return iter(self._records)

    def __repr__(self) -> str:
        """String representation of the QueryResult."""
        return (
            f"QueryResult(records={len(self)}, limit={self.limit}, "
            f"starting_token={self.starting_token}, has_next_page={self.has_next_page})"
        )

    def to_list(self) -> list[dict[str, Any]]:
        """
        Convert the result to a plain list of dictionaries.

        Returns
        -------
            A list of flattened record dictionaries.

        Examples
        --------
            result = log_stream.get_spans()
            records_list = result.to_list()
        """
        return list(self._records)
