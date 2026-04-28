from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.content_modality import ContentModality
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.control_result import ControlResult
    from ..models.document import Document
    from ..models.file_content_part import FileContentPart
    from ..models.message import Message
    from ..models.metrics import Metrics
    from ..models.partial_extended_session_record_annotation_aggregates import (
        PartialExtendedSessionRecordAnnotationAggregates,
    )
    from ..models.partial_extended_session_record_annotation_agreement import (
        PartialExtendedSessionRecordAnnotationAgreement,
    )
    from ..models.partial_extended_session_record_annotations import PartialExtendedSessionRecordAnnotations
    from ..models.partial_extended_session_record_dataset_metadata import PartialExtendedSessionRecordDatasetMetadata
    from ..models.partial_extended_session_record_feedback_rating_info import (
        PartialExtendedSessionRecordFeedbackRatingInfo,
    )
    from ..models.partial_extended_session_record_files_type_0 import PartialExtendedSessionRecordFilesType0
    from ..models.partial_extended_session_record_metric_info_type_0 import PartialExtendedSessionRecordMetricInfoType0
    from ..models.partial_extended_session_record_overall_annotation_agreement import (
        PartialExtendedSessionRecordOverallAnnotationAgreement,
    )
    from ..models.partial_extended_session_record_user_metadata import PartialExtendedSessionRecordUserMetadata
    from ..models.text_content_part import TextContentPart


T = TypeVar("T", bound="PartialExtendedSessionRecord")


@_attrs_define
class PartialExtendedSessionRecord:
    """
    Attributes
    ----------
        type_ (Literal['session'] | Unset): Type of the trace, span or session. Default: 'session'.
        input_ (list[FileContentPart | TextContentPart] | list[Message] | str | Unset):  Default: ''.
        redacted_input (list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset): Redacted input of
            the trace or span.
        output (ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str |
            Unset): Output of the trace or span.
        redacted_output (ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str
            | Unset): Redacted output of the trace or span.
        name (str | Unset): Name of the trace, span or session. Default: ''.
        created_at (datetime.datetime | Unset): Timestamp of the trace or span's creation.
        user_metadata (PartialExtendedSessionRecordUserMetadata | Unset): Metadata associated with this trace or span.
        tags (list[str] | Unset): Tags associated with this trace or span.
        status_code (int | None | Unset): Status code of the trace or span. Used for logging failure or error states.
        metrics (Metrics | Unset):
        external_id (None | str | Unset): A user-provided session, trace or span ID.
        dataset_input (None | str | Unset): Input to the dataset associated with this trace
        dataset_output (None | str | Unset): Output from the dataset associated with this trace
        dataset_metadata (PartialExtendedSessionRecordDatasetMetadata | Unset): Metadata from the dataset associated
            with this trace
        id (None | Unset | UUID): Galileo ID of the session
        session_id (None | str | Unset): Galileo ID of the session containing the trace or span or session
        trace_id (None | str | Unset): Galileo ID of the trace containing the span (or the same value as id for a trace)
        project_id (None | Unset | UUID): Galileo ID of the project associated with this trace or span
        run_id (None | Unset | UUID): Galileo ID of the run (log stream or experiment) associated with this trace or
            span
        updated_at (datetime.datetime | None | Unset): Timestamp of the session or trace or span's last update
        has_children (bool | None | Unset): Whether or not this trace or span has child spans
        metrics_batch_id (None | str | Unset): Galileo ID of the metrics batch associated with this trace or span
        session_batch_id (None | str | Unset): Galileo ID of the metrics batch associated with this trace or span
        feedback_rating_info (PartialExtendedSessionRecordFeedbackRatingInfo | Unset): Feedback information related to
            the record
        annotations (PartialExtendedSessionRecordAnnotations | Unset): Annotations keyed by template ID and annotator ID
        file_ids (list[str] | Unset): IDs of files associated with this record
        file_modalities (list[ContentModality] | Unset): Modalities of files associated with this record
        annotation_aggregates (PartialExtendedSessionRecordAnnotationAggregates | Unset): Annotation aggregate
            information keyed by template ID
        annotation_agreement (PartialExtendedSessionRecordAnnotationAgreement | Unset): Annotation agreement scores
            keyed by template ID
        overall_annotation_agreement (PartialExtendedSessionRecordOverallAnnotationAgreement | Unset): Average
            annotation agreement per queue (keyed by queue ID)
        annotation_queue_ids (list[str] | Unset): IDs of annotation queues this record is in
        metric_info (None | PartialExtendedSessionRecordMetricInfoType0 | Unset): Detailed information about the metrics
            associated with this trace or span
        files (None | PartialExtendedSessionRecordFilesType0 | Unset): File metadata keyed by file ID for files
            associated with this record
        previous_session_id (None | str | Unset):
    """

    type_: Literal["session"] | Unset = "session"
    input_: list[FileContentPart | TextContentPart] | list[Message] | str | Unset = ""
    redacted_input: list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset = UNSET
    output: ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset = (
        UNSET
    )
    redacted_output: (
        ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset
    ) = UNSET
    name: str | Unset = ""
    created_at: datetime.datetime | Unset = UNSET
    user_metadata: PartialExtendedSessionRecordUserMetadata | Unset = UNSET
    tags: list[str] | Unset = UNSET
    status_code: int | None | Unset = UNSET
    metrics: Metrics | Unset = UNSET
    external_id: None | str | Unset = UNSET
    dataset_input: None | str | Unset = UNSET
    dataset_output: None | str | Unset = UNSET
    dataset_metadata: PartialExtendedSessionRecordDatasetMetadata | Unset = UNSET
    id: None | Unset | UUID = UNSET
    session_id: None | str | Unset = UNSET
    trace_id: None | str | Unset = UNSET
    project_id: None | Unset | UUID = UNSET
    run_id: None | Unset | UUID = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    has_children: bool | None | Unset = UNSET
    metrics_batch_id: None | str | Unset = UNSET
    session_batch_id: None | str | Unset = UNSET
    feedback_rating_info: PartialExtendedSessionRecordFeedbackRatingInfo | Unset = UNSET
    annotations: PartialExtendedSessionRecordAnnotations | Unset = UNSET
    file_ids: list[str] | Unset = UNSET
    file_modalities: list[ContentModality] | Unset = UNSET
    annotation_aggregates: PartialExtendedSessionRecordAnnotationAggregates | Unset = UNSET
    annotation_agreement: PartialExtendedSessionRecordAnnotationAgreement | Unset = UNSET
    overall_annotation_agreement: PartialExtendedSessionRecordOverallAnnotationAgreement | Unset = UNSET
    annotation_queue_ids: list[str] | Unset = UNSET
    metric_info: None | PartialExtendedSessionRecordMetricInfoType0 | Unset = UNSET
    files: None | PartialExtendedSessionRecordFilesType0 | Unset = UNSET
    previous_session_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.control_result import ControlResult
        from ..models.message import Message
        from ..models.partial_extended_session_record_files_type_0 import PartialExtendedSessionRecordFilesType0
        from ..models.partial_extended_session_record_metric_info_type_0 import (
            PartialExtendedSessionRecordMetricInfoType0,
        )
        from ..models.text_content_part import TextContentPart

        type_ = self.type_

        input_: list[dict[str, Any]] | str | Unset
        if isinstance(self.input_, Unset):
            input_ = UNSET
        elif isinstance(self.input_, list):
            input_ = []
            for input_type_1_item_data in self.input_:
                input_type_1_item = input_type_1_item_data.to_dict()
                input_.append(input_type_1_item)

        elif isinstance(self.input_, list):
            input_ = []
            for input_type_2_item_data in self.input_:
                input_type_2_item: dict[str, Any]
                if isinstance(input_type_2_item_data, TextContentPart):
                    input_type_2_item = input_type_2_item_data.to_dict()
                else:
                    input_type_2_item = input_type_2_item_data.to_dict()

                input_.append(input_type_2_item)

        else:
            input_ = self.input_

        redacted_input: list[dict[str, Any]] | None | str | Unset
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_1_item_data in self.redacted_input:
                redacted_input_type_1_item = redacted_input_type_1_item_data.to_dict()
                redacted_input.append(redacted_input_type_1_item)

        elif isinstance(self.redacted_input, list):
            redacted_input = []
            for redacted_input_type_2_item_data in self.redacted_input:
                redacted_input_type_2_item: dict[str, Any]
                if isinstance(redacted_input_type_2_item_data, TextContentPart):
                    redacted_input_type_2_item = redacted_input_type_2_item_data.to_dict()
                else:
                    redacted_input_type_2_item = redacted_input_type_2_item_data.to_dict()

                redacted_input.append(redacted_input_type_2_item)

        else:
            redacted_input = self.redacted_input

        output: dict[str, Any] | list[dict[str, Any]] | None | str | Unset
        if isinstance(self.output, Unset):
            output = UNSET
        elif isinstance(self.output, Message):
            output = self.output.to_dict()
        elif isinstance(self.output, list):
            output = []
            for output_type_2_item_data in self.output:
                output_type_2_item = output_type_2_item_data.to_dict()
                output.append(output_type_2_item)

        elif isinstance(self.output, list):
            output = []
            for output_type_3_item_data in self.output:
                output_type_3_item: dict[str, Any]
                if isinstance(output_type_3_item_data, TextContentPart):
                    output_type_3_item = output_type_3_item_data.to_dict()
                else:
                    output_type_3_item = output_type_3_item_data.to_dict()

                output.append(output_type_3_item)

        elif isinstance(self.output, ControlResult):
            output = self.output.to_dict()
        else:
            output = self.output

        redacted_output: dict[str, Any] | list[dict[str, Any]] | None | str | Unset
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, Message):
            redacted_output = self.redacted_output.to_dict()
        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_2_item_data in self.redacted_output:
                redacted_output_type_2_item = redacted_output_type_2_item_data.to_dict()
                redacted_output.append(redacted_output_type_2_item)

        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_3_item_data in self.redacted_output:
                redacted_output_type_3_item: dict[str, Any]
                if isinstance(redacted_output_type_3_item_data, TextContentPart):
                    redacted_output_type_3_item = redacted_output_type_3_item_data.to_dict()
                else:
                    redacted_output_type_3_item = redacted_output_type_3_item_data.to_dict()

                redacted_output.append(redacted_output_type_3_item)

        elif isinstance(self.redacted_output, ControlResult):
            redacted_output = self.redacted_output.to_dict()
        else:
            redacted_output = self.redacted_output

        name = self.name

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        user_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user_metadata, Unset):
            user_metadata = self.user_metadata.to_dict()

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        status_code: int | None | Unset
        status_code = UNSET if isinstance(self.status_code, Unset) else self.status_code

        metrics: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metrics, Unset):
            metrics = self.metrics.to_dict()

        external_id: None | str | Unset
        external_id = UNSET if isinstance(self.external_id, Unset) else self.external_id

        dataset_input: None | str | Unset
        dataset_input = UNSET if isinstance(self.dataset_input, Unset) else self.dataset_input

        dataset_output: None | str | Unset
        dataset_output = UNSET if isinstance(self.dataset_output, Unset) else self.dataset_output

        dataset_metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dataset_metadata, Unset):
            dataset_metadata = self.dataset_metadata.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        elif isinstance(self.id, UUID):
            id = str(self.id)
        else:
            id = self.id

        session_id: None | str | Unset
        session_id = UNSET if isinstance(self.session_id, Unset) else self.session_id

        trace_id: None | str | Unset
        trace_id = UNSET if isinstance(self.trace_id, Unset) else self.trace_id

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        elif isinstance(self.project_id, UUID):
            project_id = str(self.project_id)
        else:
            project_id = self.project_id

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        elif isinstance(self.run_id, UUID):
            run_id = str(self.run_id)
        else:
            run_id = self.run_id

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        has_children: bool | None | Unset
        has_children = UNSET if isinstance(self.has_children, Unset) else self.has_children

        metrics_batch_id: None | str | Unset
        metrics_batch_id = UNSET if isinstance(self.metrics_batch_id, Unset) else self.metrics_batch_id

        session_batch_id: None | str | Unset
        session_batch_id = UNSET if isinstance(self.session_batch_id, Unset) else self.session_batch_id

        feedback_rating_info: dict[str, Any] | Unset = UNSET
        if not isinstance(self.feedback_rating_info, Unset):
            feedback_rating_info = self.feedback_rating_info.to_dict()

        annotations: dict[str, Any] | Unset = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = self.annotations.to_dict()

        file_ids: list[str] | Unset = UNSET
        if not isinstance(self.file_ids, Unset):
            file_ids = self.file_ids

        file_modalities: list[str] | Unset = UNSET
        if not isinstance(self.file_modalities, Unset):
            file_modalities = []
            for file_modalities_item_data in self.file_modalities:
                file_modalities_item = file_modalities_item_data.value
                file_modalities.append(file_modalities_item)

        annotation_aggregates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.annotation_aggregates, Unset):
            annotation_aggregates = self.annotation_aggregates.to_dict()

        annotation_agreement: dict[str, Any] | Unset = UNSET
        if not isinstance(self.annotation_agreement, Unset):
            annotation_agreement = self.annotation_agreement.to_dict()

        overall_annotation_agreement: dict[str, Any] | Unset = UNSET
        if not isinstance(self.overall_annotation_agreement, Unset):
            overall_annotation_agreement = self.overall_annotation_agreement.to_dict()

        annotation_queue_ids: list[str] | Unset = UNSET
        if not isinstance(self.annotation_queue_ids, Unset):
            annotation_queue_ids = self.annotation_queue_ids

        metric_info: dict[str, Any] | None | Unset
        if isinstance(self.metric_info, Unset):
            metric_info = UNSET
        elif isinstance(self.metric_info, PartialExtendedSessionRecordMetricInfoType0):
            metric_info = self.metric_info.to_dict()
        else:
            metric_info = self.metric_info

        files: dict[str, Any] | None | Unset
        if isinstance(self.files, Unset):
            files = UNSET
        elif isinstance(self.files, PartialExtendedSessionRecordFilesType0):
            files = self.files.to_dict()
        else:
            files = self.files

        previous_session_id: None | str | Unset
        previous_session_id = UNSET if isinstance(self.previous_session_id, Unset) else self.previous_session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if input_ is not UNSET:
            field_dict["input"] = input_
        if redacted_input is not UNSET:
            field_dict["redacted_input"] = redacted_input
        if output is not UNSET:
            field_dict["output"] = output
        if redacted_output is not UNSET:
            field_dict["redacted_output"] = redacted_output
        if name is not UNSET:
            field_dict["name"] = name
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata
        if tags is not UNSET:
            field_dict["tags"] = tags
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if metrics is not UNSET:
            field_dict["metrics"] = metrics
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if dataset_input is not UNSET:
            field_dict["dataset_input"] = dataset_input
        if dataset_output is not UNSET:
            field_dict["dataset_output"] = dataset_output
        if dataset_metadata is not UNSET:
            field_dict["dataset_metadata"] = dataset_metadata
        if id is not UNSET:
            field_dict["id"] = id
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if trace_id is not UNSET:
            field_dict["trace_id"] = trace_id
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if metrics_batch_id is not UNSET:
            field_dict["metrics_batch_id"] = metrics_batch_id
        if session_batch_id is not UNSET:
            field_dict["session_batch_id"] = session_batch_id
        if feedback_rating_info is not UNSET:
            field_dict["feedback_rating_info"] = feedback_rating_info
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if file_ids is not UNSET:
            field_dict["file_ids"] = file_ids
        if file_modalities is not UNSET:
            field_dict["file_modalities"] = file_modalities
        if annotation_aggregates is not UNSET:
            field_dict["annotation_aggregates"] = annotation_aggregates
        if annotation_agreement is not UNSET:
            field_dict["annotation_agreement"] = annotation_agreement
        if overall_annotation_agreement is not UNSET:
            field_dict["overall_annotation_agreement"] = overall_annotation_agreement
        if annotation_queue_ids is not UNSET:
            field_dict["annotation_queue_ids"] = annotation_queue_ids
        if metric_info is not UNSET:
            field_dict["metric_info"] = metric_info
        if files is not UNSET:
            field_dict["files"] = files
        if previous_session_id is not UNSET:
            field_dict["previous_session_id"] = previous_session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.control_result import ControlResult
        from ..models.document import Document
        from ..models.file_content_part import FileContentPart
        from ..models.message import Message
        from ..models.metrics import Metrics
        from ..models.partial_extended_session_record_annotation_aggregates import (
            PartialExtendedSessionRecordAnnotationAggregates,
        )
        from ..models.partial_extended_session_record_annotation_agreement import (
            PartialExtendedSessionRecordAnnotationAgreement,
        )
        from ..models.partial_extended_session_record_annotations import PartialExtendedSessionRecordAnnotations
        from ..models.partial_extended_session_record_dataset_metadata import (
            PartialExtendedSessionRecordDatasetMetadata,
        )
        from ..models.partial_extended_session_record_feedback_rating_info import (
            PartialExtendedSessionRecordFeedbackRatingInfo,
        )
        from ..models.partial_extended_session_record_files_type_0 import PartialExtendedSessionRecordFilesType0
        from ..models.partial_extended_session_record_metric_info_type_0 import (
            PartialExtendedSessionRecordMetricInfoType0,
        )
        from ..models.partial_extended_session_record_overall_annotation_agreement import (
            PartialExtendedSessionRecordOverallAnnotationAgreement,
        )
        from ..models.partial_extended_session_record_user_metadata import PartialExtendedSessionRecordUserMetadata
        from ..models.text_content_part import TextContentPart

        d = dict(src_dict)
        type_ = cast(Literal["session"] | Unset, d.pop("type", UNSET))
        if type_ != "session" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'session', got '{type_}'")

        def _parse_input_(data: object) -> list[FileContentPart | TextContentPart] | list[Message] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = []
                _input_type_1 = data
                for input_type_1_item_data in _input_type_1:
                    input_type_1_item = Message.from_dict(input_type_1_item_data)

                    input_type_1.append(input_type_1_item)

                return input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_2 = []
                _input_type_2 = data
                for input_type_2_item_data in _input_type_2:

                    def _parse_input_type_2_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    input_type_2_item = _parse_input_type_2_item(input_type_2_item_data)

                    input_type_2.append(input_type_2_item)

                return input_type_2
            except:  # noqa: E722
                pass
            return cast(list[FileContentPart | TextContentPart] | list[Message] | str | Unset, data)

        input_ = _parse_input_(d.pop("input", UNSET))

        def _parse_redacted_input(
            data: object,
        ) -> list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_1 = []
                _redacted_input_type_1 = data
                for redacted_input_type_1_item_data in _redacted_input_type_1:
                    redacted_input_type_1_item = Message.from_dict(redacted_input_type_1_item_data)

                    redacted_input_type_1.append(redacted_input_type_1_item)

                return redacted_input_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_input_type_2 = []
                _redacted_input_type_2 = data
                for redacted_input_type_2_item_data in _redacted_input_type_2:

                    def _parse_redacted_input_type_2_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    redacted_input_type_2_item = _parse_redacted_input_type_2_item(redacted_input_type_2_item_data)

                    redacted_input_type_2.append(redacted_input_type_2_item)

                return redacted_input_type_2
            except:  # noqa: E722
                pass
            return cast(list[FileContentPart | TextContentPart] | list[Message] | None | str | Unset, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        def _parse_output(
            data: object,
        ) -> ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Message.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_2 = []
                _output_type_2 = data
                for output_type_2_item_data in _output_type_2:
                    output_type_2_item = Document.from_dict(output_type_2_item_data)

                    output_type_2.append(output_type_2_item)

                return output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_3 = []
                _output_type_3 = data
                for output_type_3_item_data in _output_type_3:

                    def _parse_output_type_3_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    output_type_3_item = _parse_output_type_3_item(output_type_3_item_data)

                    output_type_3.append(output_type_3_item)

                return output_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ControlResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset,
                data,
            )

        output = _parse_output(d.pop("output", UNSET))

        def _parse_redacted_output(
            data: object,
        ) -> ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Message.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_2 = []
                _redacted_output_type_2 = data
                for redacted_output_type_2_item_data in _redacted_output_type_2:
                    redacted_output_type_2_item = Document.from_dict(redacted_output_type_2_item_data)

                    redacted_output_type_2.append(redacted_output_type_2_item)

                return redacted_output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_3 = []
                _redacted_output_type_3 = data
                for redacted_output_type_3_item_data in _redacted_output_type_3:

                    def _parse_redacted_output_type_3_item(data: object) -> FileContentPart | TextContentPart:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return TextContentPart.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return FileContentPart.from_dict(data)

                    redacted_output_type_3_item = _parse_redacted_output_type_3_item(redacted_output_type_3_item_data)

                    redacted_output_type_3.append(redacted_output_type_3_item)

                return redacted_output_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ControlResult.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                ControlResult | list[Document] | list[FileContentPart | TextContentPart] | Message | None | str | Unset,
                data,
            )

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        created_at = UNSET if isinstance(_created_at, Unset) else isoparse(_created_at)

        _user_metadata = d.pop("user_metadata", UNSET)
        user_metadata: PartialExtendedSessionRecordUserMetadata | Unset
        if isinstance(_user_metadata, Unset):
            user_metadata = UNSET
        else:
            user_metadata = PartialExtendedSessionRecordUserMetadata.from_dict(_user_metadata)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        _metrics = d.pop("metrics", UNSET)
        metrics: Metrics | Unset
        metrics = UNSET if isinstance(_metrics, Unset) else Metrics.from_dict(_metrics)

        def _parse_external_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_dataset_input(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_input = _parse_dataset_input(d.pop("dataset_input", UNSET))

        def _parse_dataset_output(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_output = _parse_dataset_output(d.pop("dataset_output", UNSET))

        _dataset_metadata = d.pop("dataset_metadata", UNSET)
        dataset_metadata: PartialExtendedSessionRecordDatasetMetadata | Unset
        if isinstance(_dataset_metadata, Unset):
            dataset_metadata = UNSET
        else:
            dataset_metadata = PartialExtendedSessionRecordDatasetMetadata.from_dict(_dataset_metadata)

        def _parse_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return UUID(data)

            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_id = _parse_session_id(d.pop("session_id", UNSET))

        def _parse_trace_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        trace_id = _parse_trace_id(d.pop("trace_id", UNSET))

        def _parse_project_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return UUID(data)

            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_run_id(data: object) -> None | Unset | UUID:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return UUID(data)

            except:  # noqa: E722
                pass
            return cast(None | Unset | UUID, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return isoparse(data)

            except:  # noqa: E722
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_has_children(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        def _parse_metrics_batch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metrics_batch_id = _parse_metrics_batch_id(d.pop("metrics_batch_id", UNSET))

        def _parse_session_batch_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        session_batch_id = _parse_session_batch_id(d.pop("session_batch_id", UNSET))

        _feedback_rating_info = d.pop("feedback_rating_info", UNSET)
        feedback_rating_info: PartialExtendedSessionRecordFeedbackRatingInfo | Unset
        if isinstance(_feedback_rating_info, Unset):
            feedback_rating_info = UNSET
        else:
            feedback_rating_info = PartialExtendedSessionRecordFeedbackRatingInfo.from_dict(_feedback_rating_info)

        _annotations = d.pop("annotations", UNSET)
        annotations: PartialExtendedSessionRecordAnnotations | Unset
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = PartialExtendedSessionRecordAnnotations.from_dict(_annotations)

        file_ids = cast(list[str], d.pop("file_ids", UNSET))

        _file_modalities = d.pop("file_modalities", UNSET)
        file_modalities: list[ContentModality] | Unset = UNSET
        if _file_modalities is not UNSET:
            file_modalities = []
            for file_modalities_item_data in _file_modalities:
                file_modalities_item = ContentModality(file_modalities_item_data)

                file_modalities.append(file_modalities_item)

        _annotation_aggregates = d.pop("annotation_aggregates", UNSET)
        annotation_aggregates: PartialExtendedSessionRecordAnnotationAggregates | Unset
        if isinstance(_annotation_aggregates, Unset):
            annotation_aggregates = UNSET
        else:
            annotation_aggregates = PartialExtendedSessionRecordAnnotationAggregates.from_dict(_annotation_aggregates)

        _annotation_agreement = d.pop("annotation_agreement", UNSET)
        annotation_agreement: PartialExtendedSessionRecordAnnotationAgreement | Unset
        if isinstance(_annotation_agreement, Unset):
            annotation_agreement = UNSET
        else:
            annotation_agreement = PartialExtendedSessionRecordAnnotationAgreement.from_dict(_annotation_agreement)

        _overall_annotation_agreement = d.pop("overall_annotation_agreement", UNSET)
        overall_annotation_agreement: PartialExtendedSessionRecordOverallAnnotationAgreement | Unset
        if isinstance(_overall_annotation_agreement, Unset):
            overall_annotation_agreement = UNSET
        else:
            overall_annotation_agreement = PartialExtendedSessionRecordOverallAnnotationAgreement.from_dict(
                _overall_annotation_agreement
            )

        annotation_queue_ids = cast(list[str], d.pop("annotation_queue_ids", UNSET))

        def _parse_metric_info(data: object) -> None | PartialExtendedSessionRecordMetricInfoType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return PartialExtendedSessionRecordMetricInfoType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | PartialExtendedSessionRecordMetricInfoType0 | Unset, data)

        metric_info = _parse_metric_info(d.pop("metric_info", UNSET))

        def _parse_files(data: object) -> None | PartialExtendedSessionRecordFilesType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return PartialExtendedSessionRecordFilesType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | PartialExtendedSessionRecordFilesType0 | Unset, data)

        files = _parse_files(d.pop("files", UNSET))

        def _parse_previous_session_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        previous_session_id = _parse_previous_session_id(d.pop("previous_session_id", UNSET))

        partial_extended_session_record = cls(
            type_=type_,
            input_=input_,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at=created_at,
            user_metadata=user_metadata,
            tags=tags,
            status_code=status_code,
            metrics=metrics,
            external_id=external_id,
            dataset_input=dataset_input,
            dataset_output=dataset_output,
            dataset_metadata=dataset_metadata,
            id=id,
            session_id=session_id,
            trace_id=trace_id,
            project_id=project_id,
            run_id=run_id,
            updated_at=updated_at,
            has_children=has_children,
            metrics_batch_id=metrics_batch_id,
            session_batch_id=session_batch_id,
            feedback_rating_info=feedback_rating_info,
            annotations=annotations,
            file_ids=file_ids,
            file_modalities=file_modalities,
            annotation_aggregates=annotation_aggregates,
            annotation_agreement=annotation_agreement,
            overall_annotation_agreement=overall_annotation_agreement,
            annotation_queue_ids=annotation_queue_ids,
            metric_info=metric_info,
            files=files,
            previous_session_id=previous_session_id,
        )

        partial_extended_session_record.additional_properties = d
        return partial_extended_session_record

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
