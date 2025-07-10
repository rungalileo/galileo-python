import datetime
import logging
from typing import Optional

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.resources.api.trace import query_metrics_projects_project_id_metrics_search_post
from galileo.resources.models import HTTPValidationError, LogRecordsMetricsQueryRequest, LogRecordsMetricsResponse
from galileo.search import FilterType
from galileo.utils.catch_log import DecorateAllMethods

logger = logging.getLogger(__name__)


class Metrics(BaseClientModel, DecorateAllMethods):
    def query(
        self,
        project_id: UUID4,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        experiment_id: Optional[UUID4] = None,
        log_stream_id: Optional[str] = None,
        filters: Optional[list[FilterType]] = None,
        group_by: Optional[str] = None,
        interval: int = 5,
    ) -> Optional[LogRecordsMetricsResponse]:
        """
        Queries for metrics in a project.
        """
        body = LogRecordsMetricsQueryRequest(
            start_time=start_time,
            end_time=end_time,
            experiment_id=experiment_id,
            log_stream_id=log_stream_id,
            filters=filters,
            group_by=group_by,
            interval=interval,
        )

        response = query_metrics_projects_project_id_metrics_search_post.sync(
            client=self.client, project_id=str(project_id), body=body
        )

        if not isinstance(response, LogRecordsMetricsResponse):
            if isinstance(response, HTTPValidationError):
                logger.error(f"Validation error when querying for metrics: {response}")
            else:
                logger.error(f"Failed to query for metrics. Response: {response}")
            return None

        return response


def get_metrics(
    project_id: UUID4,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    experiment_id: Optional[UUID4] = None,
    log_stream_id: Optional[str] = None,
    filters: Optional[list[FilterType]] = None,
    group_by: Optional[str] = None,
    interval: int = 5,
) -> Optional[LogRecordsMetricsResponse]:
    """
    A helper function to query for metrics in a project.
    """
    metrics_client = Metrics()
    return metrics_client.query(
        project_id=project_id,
        start_time=start_time,
        end_time=end_time,
        experiment_id=experiment_id,
        log_stream_id=log_stream_id,
        filters=filters,
        group_by=group_by,
        interval=interval,
    )
