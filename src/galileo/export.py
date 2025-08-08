import csv
import json
import logging
from collections.abc import Iterator
from typing import Any, Optional, Union

from pydantic import UUID4

from galileo.base import BaseClientModel
from galileo.resources.api.trace.export_records_projects_project_id_export_records_post import (
    stream_detailed as export_records_stream,
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

logger = logging.getLogger(__name__)


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
        response = export_records_stream(
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

        line_iterator = (line.decode("utf-8") if isinstance(line, bytes) else line for line in response.iter_lines())

        if export_format == LLMExportFormat.JSONL:
            for line in line_iterator:
                if line:
                    yield json.loads(line)
        elif export_format == LLMExportFormat.CSV:
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
    """Exports records from a Galileo project.

    Args:
        project_id: The unique identifier of the project.
        root_type: The type of records to export.
        export_format: The desired format for the exported data.
        log_stream_id: Filter records by a specific run ID.
        experiment_id: Filter records by a specific experiment ID.
        filters: A list of filters to apply to the export.
        column_ids: A list of column IDs to include in the export.
        sort: A sort clause to order the exported records.

    Returns:
        An iterator that yields each record as a dictionary.
    """
    return ExportClient().records(
        project_id=project_id,
        root_type=root_type,
        export_format=export_format,
        log_stream_id=log_stream_id,
        experiment_id=experiment_id,
        filters=filters,
        column_ids=column_ids,
        sort=sort,
    )
