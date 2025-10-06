import csv
import json
import logging
from collections.abc import Iterator
from typing import Any, Optional

from galileo.config import GalileoPythonConfig
from galileo.resources.api.trace.export_records_projects_project_id_export_records_post import (
    stream_detailed as export_records_stream,
)
from galileo.resources.models import LLMExportFormat, LogRecordsExportRequest, LogRecordsSortClause, RootType
from galileo.schema.filters import FilterType

logger = logging.getLogger(__name__)


class ExportClient:
    config: GalileoPythonConfig

    def __init__(self) -> None:
        self.config = GalileoPythonConfig.get()

    def records(
        self,
        project_id: str,
        root_type: RootType = RootType.SESSION,
        filters: Optional[list[FilterType]] = None,
        sort: LogRecordsSortClause = LogRecordsSortClause(column_id="created_at", ascending=False),
        export_format: LLMExportFormat = LLMExportFormat.JSONL,
        log_stream_id: Optional[str] = None,
        experiment_id: Optional[str] = None,
        column_ids: Optional[list[str]] = None,
        redact: bool = True,
    ) -> Iterator[dict[str, Any]]:
        if filters is None:
            filters = []
        response = export_records_stream(
            client=self.config.api_client,
            project_id=project_id,
            body=LogRecordsExportRequest(
                root_type=root_type,
                export_format=export_format,
                log_stream_id=log_stream_id,
                experiment_id=experiment_id,
                filters=filters,
                column_ids=column_ids,
                sort=sort,
                redact=redact,
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
    project_id: str,
    root_type: RootType = RootType.SESSION,
    filters: Optional[list[FilterType]] = None,
    sort: LogRecordsSortClause = LogRecordsSortClause(column_id="created_at", ascending=False),
    export_format: LLMExportFormat = LLMExportFormat.JSONL,
    log_stream_id: Optional[str] = None,
    experiment_id: Optional[str] = None,
    column_ids: Optional[list[str]] = None,
    redact: bool = True,
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
        redact: Redact sensitive data from the response.

    Returns:
        An iterator that yields each record as a dictionary.
    """
    if filters is None:
        filters = []
    if (log_stream_id is None) == (experiment_id is None):
        raise ValueError("Exactly one of log_stream_id or experiment_id must be provided.")

    return ExportClient().records(
        project_id=project_id,
        root_type=root_type,
        export_format=export_format,
        log_stream_id=log_stream_id,
        experiment_id=experiment_id,
        filters=filters,
        column_ids=column_ids,
        sort=sort,
        redact=redact,
    )
