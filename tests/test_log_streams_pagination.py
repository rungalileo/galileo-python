"""Tests for pagination behavior of the LogStreams service.

Covers:
- `_list_all` paginates across all pages until the API signals no more pages.
- `get(name=...)` finds matches that span beyond the first page.
- `list()` forwards `starting_token` to the underlying paginated endpoint.
"""

from unittest.mock import MagicMock, patch
from uuid import uuid4

from galileo.log_streams import LogStreams
from galileo.resources.models.list_log_stream_response import ListLogStreamResponse
from galileo.resources.models.log_stream_response import LogStreamResponse
from galileo.resources.types import UNSET


def _make_response(*, names: list[str], next_token, paginated: bool) -> ListLogStreamResponse:
    """Build a mock paginated response with the given names and pagination flags."""
    log_streams = [
        LogStreamResponse(
            id=str(uuid4()),
            name=name,
            project_id="proj-1",
            created_at="2023-01-01T00:00:00Z",
            updated_at="2023-01-01T00:00:00Z",
            created_by="test-user",
        )
        for name in names
    ]
    return ListLogStreamResponse(
        log_streams=log_streams, starting_token=0, limit=100, paginated=paginated, next_starting_token=next_token
    )


class TestListAllPagination:
    """Tests for LogStreams._list_all (internal helper)."""

    @patch("galileo.log_streams.list_log_streams_paginated_projects_project_id_log_streams_paginated_get")
    @patch("galileo.log_streams.GalileoPythonConfig")
    def test_list_all_paginates_across_multiple_pages(
        self, mock_config_class: MagicMock, mock_endpoint: MagicMock
    ) -> None:
        # Given: two pages of results
        page_1 = _make_response(names=[f"stream-{i}" for i in range(5)], next_token=5, paginated=True)
        page_2 = _make_response(names=[f"stream-{i}" for i in range(5, 8)], next_token=None, paginated=True)
        mock_endpoint.sync.side_effect = [page_1, page_2]

        # When: _list_all is called
        all_streams = LogStreams()._list_all(project_id="proj-1")

        # Then: every page is fetched and concatenated
        assert len(all_streams) == 8
        assert [ls.name for ls in all_streams] == [f"stream-{i}" for i in range(8)]
        assert mock_endpoint.sync.call_count == 2
        # Second call passes the token from the first response
        assert mock_endpoint.sync.call_args_list[1].kwargs["starting_token"] == 5

    @patch("galileo.log_streams.list_log_streams_paginated_projects_project_id_log_streams_paginated_get")
    @patch("galileo.log_streams.GalileoPythonConfig")
    def test_list_all_stops_when_paginated_false(self, mock_config_class: MagicMock, mock_endpoint: MagicMock) -> None:
        # Given: a single page with paginated=False
        page = _make_response(names=["only-stream"], next_token=42, paginated=False)
        mock_endpoint.sync.return_value = page

        # When: _list_all is called
        all_streams = LogStreams()._list_all(project_id="proj-1")

        # Then: only one fetch happens regardless of next_starting_token
        assert len(all_streams) == 1
        assert mock_endpoint.sync.call_count == 1

    @patch("galileo.log_streams.list_log_streams_paginated_projects_project_id_log_streams_paginated_get")
    @patch("galileo.log_streams.GalileoPythonConfig")
    def test_list_all_stops_when_next_token_is_unset(
        self, mock_config_class: MagicMock, mock_endpoint: MagicMock
    ) -> None:
        # Given: a page with next_starting_token == UNSET
        page = _make_response(names=["a", "b"], next_token=UNSET, paginated=True)
        mock_endpoint.sync.return_value = page

        # When: _list_all is called
        all_streams = LogStreams()._list_all(project_id="proj-1")

        # Then: pagination stops on UNSET token
        assert len(all_streams) == 2
        assert mock_endpoint.sync.call_count == 1


class TestGetByNamePaginates:
    """Tests for LogStreams.get(name=...) finding matches across pages."""

    @patch("galileo.log_streams.list_log_streams_paginated_projects_project_id_log_streams_paginated_get")
    @patch("galileo.log_streams.GalileoPythonConfig")
    def test_get_by_name_finds_match_on_second_page(
        self, mock_config_class: MagicMock, mock_endpoint: MagicMock
    ) -> None:
        # Given: target stream lives on page 2
        page_1 = _make_response(names=[f"stream-{i}" for i in range(3)], next_token=3, paginated=True)
        page_2 = _make_response(names=["target-stream", "other"], next_token=None, paginated=True)
        mock_endpoint.sync.side_effect = [page_1, page_2]

        # When: looking up by name
        result = LogStreams().get(name="target-stream", project_id="proj-1")

        # Then: the match on page 2 is found (would have returned None before this fix)
        assert result is not None
        assert result.name == "target-stream"
        assert mock_endpoint.sync.call_count == 2

    @patch("galileo.log_streams.list_log_streams_paginated_projects_project_id_log_streams_paginated_get")
    @patch("galileo.log_streams.GalileoPythonConfig")
    def test_get_by_name_returns_none_when_missing(
        self, mock_config_class: MagicMock, mock_endpoint: MagicMock
    ) -> None:
        # Given: name does not exist on any page
        page = _make_response(names=["a", "b"], next_token=None, paginated=True)
        mock_endpoint.sync.return_value = page

        # When: looking up a missing name
        result = LogStreams().get(name="nonexistent", project_id="proj-1")

        # Then: returns None
        assert result is None


class TestListForwardsStartingToken:
    """Tests that LogStreams.list forwards starting_token to the paginated endpoint."""

    @patch("galileo.log_streams.list_log_streams_paginated_projects_project_id_log_streams_paginated_get")
    @patch("galileo.log_streams.GalileoPythonConfig")
    def test_list_forwards_starting_token(self, mock_config_class: MagicMock, mock_endpoint: MagicMock) -> None:
        # Given: a single page response
        mock_endpoint.sync.return_value = _make_response(names=["s1"], next_token=None, paginated=True)

        # When: list is called with a custom starting_token
        LogStreams().list(project_id="proj-1", starting_token=200, limit=50)

        # Then: starting_token and limit are passed to the underlying endpoint
        kwargs = mock_endpoint.sync.call_args.kwargs
        assert kwargs["starting_token"] == 200
        assert kwargs["limit"] == 50
        assert kwargs["project_id"] == "proj-1"

    @patch("galileo.log_streams.list_log_streams_paginated_projects_project_id_log_streams_paginated_get")
    @patch("galileo.log_streams.GalileoPythonConfig")
    def test_list_default_starting_token_is_zero(self, mock_config_class: MagicMock, mock_endpoint: MagicMock) -> None:
        # Given: a single page response
        mock_endpoint.sync.return_value = _make_response(names=[], next_token=None, paginated=True)

        # When: list is called without starting_token
        LogStreams().list(project_id="proj-1")

        # Then: starting_token defaults to 0
        kwargs = mock_endpoint.sync.call_args.kwargs
        assert kwargs["starting_token"] == 0
        assert kwargs["limit"] == 100
