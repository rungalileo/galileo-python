import datetime
from unittest.mock import Mock, patch
from uuid import uuid4

from galileo.metrics import get_metrics
from galileo.resources.models import (
    BucketedMetrics,
    LogRecordsMetricsResponse,
    LogRecordsMetricsResponseAggregateMetrics,
    LogRecordsMetricsResponseBucketedMetrics,
)

FIXED_PROJECT_ID = uuid4()


def _log_records_metrics_response_factory() -> LogRecordsMetricsResponse:
    """Creates a realistic LogRecordsMetricsResponse for testing."""
    now = datetime.datetime.now()
    agg_metrics = LogRecordsMetricsResponseAggregateMetrics()
    agg_metrics["total_cost"] = 15.50
    agg_metrics["total_tokens"] = 2500

    bucketed_metrics_data = LogRecordsMetricsResponseBucketedMetrics()
    bucketed_metrics_data["total_cost"] = [
        BucketedMetrics(start_bucket_time=now, end_bucket_time=now + datetime.timedelta(minutes=5)),
        BucketedMetrics(
            start_bucket_time=now + datetime.timedelta(minutes=5), end_bucket_time=now + datetime.timedelta(minutes=10)
        ),
    ]

    return LogRecordsMetricsResponse(
        aggregate_metrics=agg_metrics, bucketed_metrics=bucketed_metrics_data, group_by_columns=[]
    )


class TestGetMetrics:
    @patch("galileo.metrics.query_metrics_projects_project_id_metrics_search_post.sync")
    def test_successful_call(self, mock_api_call):
        mock_response = _log_records_metrics_response_factory()
        mock_api_call.return_value = mock_response

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)

        response = get_metrics(project_id=FIXED_PROJECT_ID, start_time=start_time, end_time=end_time)

        mock_api_call.assert_called_once()
        assert str(FIXED_PROJECT_ID) in mock_api_call.call_args[1]["project_id"]
        assert response == mock_response

    @patch("galileo.metrics.query_metrics_projects_project_id_metrics_search_post.sync")
    def test_api_failure_returns_none(self, mock_api_call):
        mock_api_call.return_value = None  # Simulate API failure

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)

        response = get_metrics(project_id=FIXED_PROJECT_ID, start_time=start_time, end_time=end_time)

        mock_api_call.assert_called_once()
        assert response is None

    @patch("galileo.metrics.query_metrics_projects_project_id_metrics_search_post.sync")
    def test_passes_all_parameters_correctly(self, mock_api_call):
        mock_api_call.return_value = _log_records_metrics_response_factory()

        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(hours=1)
        experiment_id = uuid4()
        log_stream_id = "test_stream"
        filters = [Mock()]
        group_by = "some_column"
        interval = 10

        get_metrics(
            project_id=FIXED_PROJECT_ID,
            start_time=start_time,
            end_time=end_time,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
            filters=filters,
            group_by=group_by,
            interval=interval,
        )

        mock_api_call.assert_called_once()
        called_kwargs = mock_api_call.call_args[1]
        body = called_kwargs["body"]

        assert called_kwargs["project_id"] == str(FIXED_PROJECT_ID)
        assert body.start_time == start_time
        assert body.end_time == end_time
        assert body.experiment_id == experiment_id
        assert body.log_stream_id == log_stream_id
        assert body.filters == filters
        assert body.group_by == group_by
        assert body.interval == interval
