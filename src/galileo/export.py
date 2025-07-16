import csv
import json
from collections.abc import Iterator
from typing import Any, Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.resources.api.trace.export_records_projects_project_id_export_records_post import (
    sync_detailed as export_records_sync,
)
from galileo.resources.models import (
    LLMExportFormat,
    LogRecordsBooleanFilter,
    LogRecordsDateFilter,
    LogRecordsExportRequest,
    LogRecordsIDFilter,
    LogRecordsNumberFilter,
    LogRecordsSortClause,
    LogRecordsTextFilter,
    RootType,
)


class ExportClient(BaseClientModel):
    def records(
        self,
        project_id: UUID4,
        root_type: RootType,
        export_format: LLMExportFormat = LLMExportFormat.JSONL,
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
        column_ids: Optional[list[str]] = None,
        sort: Optional[LogRecordsSortClause] = None,
    ) -> Iterator[dict[str, Any]]:
        response = export_records_sync(
            client=self.client,
            project_id=project_id,
            body=LogRecordsExportRequest(
                root_type=root_type,
                export_format=export_format,
                log_stream_id=log_stream_id,
                experiment_id=experiment_id,
                filters=filters,
                column_ids=column_ids,
                sort=sort,
            ),
        )

        line_iterator = (
            line.decode("utf-8") if isinstance(line, bytes) else line for line in response.content.iter_lines()
        )

        if export_format == LLMExportFormat.JSONL:
            for line in line_iterator:
                if line:
                    yield json.loads(line)
        elif export_format == LLMExportFormat.CSV:
            # The csv module can take an iterator of lines
            reader = csv.DictReader(line_iterator)
            yield from reader


def export_records(
    project_id: UUID4,
    root_type: RootType,
    export_format: LLMExportFormat = LLMExportFormat.JSONL,
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
    column_ids: Optional[list[str]] = None,
    sort: Optional[LogRecordsSortClause] = None,
) -> Iterator[dict[str, Any]]:
    client = ExportClient()
    return client.records(
        project_id=project_id,
        root_type=root_type,
        export_format=export_format,
        log_stream_id=log_stream_id,
        experiment_id=experiment_id,
        filters=filters,
        column_ids=column_ids,
        sort=sort,
    )
