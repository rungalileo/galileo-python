import json
from collections.abc import Iterator
from typing import Any, Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.resources.api.trace.export_records_projects_project_id_export_records_post import (
    sync_detailed as export_records_sync,
)
from galileo.resources.models import (
    LogRecordsBooleanFilter,
    LogRecordsDateFilter,
    LogRecordsExportRequest,
    LogRecordsIDFilter,
    LogRecordsNumberFilter,
    LogRecordsTextFilter,
    RootType,
)


class ExportClient(BaseClientModel):
    def records(
        self,
        project_id: UUID4,
        root_type: RootType,
        log_stream_id: Optional[UUID4] = None,
        experiment_id: Optional[UUID4] = None,
        filters: Optional[
            list[
                Union[
                    LogRecordsBooleanFilter,
                    LogRecordsDateFilter,
                    LogRecordsIDFilter,
                    LogRecordsNumberFilter,
                    LogRecordsTextFilter,
                ]
            ]
        ] = None,
    ) -> Iterator[dict[str, Any]]:
        response = export_records_sync(
            client=self.client,
            project_id=project_id,
            body=LogRecordsExportRequest(
                root_type=root_type, log_stream_id=log_stream_id, experiment_id=experiment_id, filters=filters
            ),
        )
        for line in response.content.iter_lines():
            if line:
                yield json.loads(line)


def export_records(
    project_id: UUID4,
    root_type: RootType,
    log_stream_id: Optional[UUID4] = None,
    experiment_id: Optional[UUID4] = None,
    filters: Optional[
        list[
            Union[
                LogRecordsBooleanFilter,
                LogRecordsDateFilter,
                LogRecordsIDFilter,
                LogRecordsNumberFilter,
                LogRecordsTextFilter,
            ]
        ]
    ] = None,
) -> Iterator[dict[str, Any]]:
    client = ExportClient()
    return client.records(
        project_id=project_id,
        root_type=root_type,
        log_stream_id=log_stream_id,
        experiment_id=experiment_id,
        filters=filters,
    )
