import re
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest

from galileo.resources.models import HTTPValidationError, LogRecordsQueryResponse, ValidationError
from galileo.search import get_sessions, get_spans, get_traces

FIXED_PROJECT_ID = str(uuid4())


def _log_records_query_response_factory(records: list) -> LogRecordsQueryResponse:
    return LogRecordsQueryResponse(records=records)


@pytest.mark.parametrize(
    "test_function, patch_target",
    [
        (get_spans, "galileo.search.query_spans_projects_project_id_spans_search_post.sync"),
        (get_traces, "galileo.search.query_traces_projects_project_id_traces_search_post.sync"),
        (get_sessions, "galileo.search.query_sessions_projects_project_id_sessions_search_post.sync"),
    ],
)
class TestSearchHelpers:
    def test_successful_call(self, test_function, patch_target):
        mock_records = [{"id": "1"}, {"id": "2"}]
        mock_response = _log_records_query_response_factory(records=mock_records)

        with patch(patch_target) as mock_api_call:
            mock_api_call.return_value = mock_response
            response = test_function(project_id=FIXED_PROJECT_ID)

            mock_api_call.assert_called_once()
            assert FIXED_PROJECT_ID in mock_api_call.call_args[1]["project_id"]
            assert response == mock_response
            assert response.records == mock_records

    def test_api_failure_raises_value_error(self, test_function, patch_target):
        with patch(patch_target) as mock_api_call:
            mock_api_call.return_value = None
            with pytest.raises(ValueError):
                test_function(project_id=FIXED_PROJECT_ID)

            mock_api_call.assert_called_once()

    def test_http_validation_error_raises_exception(self, test_function, patch_target):
        with patch(patch_target) as mock_api_call:
            detail = [
                ValidationError(loc=["body", "project_id"], msg="value is not a valid uuid", type_="type_error.uuid")
            ]
            mock_api_call.return_value = HTTPValidationError(detail=detail)
            with pytest.raises(ValueError, match=re.escape(str(detail))):
                test_function(project_id=FIXED_PROJECT_ID)

    def test_passes_all_parameters_correctly(self, test_function, patch_target):
        experiment_id = str(uuid4())
        log_stream_id = "test_stream"
        limit = 50
        starting_token = 10
        filters = [Mock()]
        sort = Mock()

        with patch(patch_target) as mock_api_call:
            mock_api_call.return_value = _log_records_query_response_factory(records=[])
            test_function(
                project_id=FIXED_PROJECT_ID,
                experiment_id=experiment_id,
                log_stream_id=log_stream_id,
                filters=filters,
                sort=sort,
                limit=limit,
                starting_token=starting_token,
            )

            mock_api_call.assert_called_once()
            called_kwargs = mock_api_call.call_args[1]
            body = called_kwargs["body"]

            assert called_kwargs["project_id"] == FIXED_PROJECT_ID
            assert body.experiment_id == experiment_id
            assert body.log_stream_id == log_stream_id
            assert body.filters == filters
            assert body.sort == sort
            assert body.limit == limit
            assert body.starting_token == starting_token
