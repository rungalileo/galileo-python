from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.llm_export_format import LLMExportFormat
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_queue_records_by_filter_tree import AnnotationQueueRecordsByFilterTree
    from ..models.annotation_queue_records_by_record_i_ds import AnnotationQueueRecordsByRecordIDs


T = TypeVar("T", bound="AnnotationQueueExportRequest")


@_attrs_define
class AnnotationQueueExportRequest:
    """Request to export selected annotation queue records.

    Attributes
    ----------
        record_selector (Union['AnnotationQueueRecordsByFilterTree', 'AnnotationQueueRecordsByRecordIDs']): Selector to
            specify which queue records to export (either by record IDs or filter tree)
        column_ids (Union[None, Unset, list[str]]): Column IDs to include in the export. Applies only to CSV exports.
        export_format (Union[Unset, LLMExportFormat]):
        redact (Union[Unset, bool]): Redact sensitive data Default: True.
        file_name (Union[None, Unset, str]): Optional filename for the exported file
        export_computed_metrics_only (Union[Unset, bool]): When true, export only enabled scorer metrics with computed
            values (success or roll_up). For session exports, omit entire sessions unless every enabled metric at session,
            trace, or span level is ready (success, roll_up, or not_applicable). Not supported with export_format=jsonl_flat
            (returns 422); use jsonl or csv instead. Default: False.
    """

    record_selector: Union["AnnotationQueueRecordsByFilterTree", "AnnotationQueueRecordsByRecordIDs"]
    column_ids: None | Unset | list[str] = UNSET
    export_format: Unset | LLMExportFormat = UNSET
    redact: Unset | bool = True
    file_name: None | Unset | str = UNSET
    export_computed_metrics_only: Unset | bool = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_queue_records_by_record_i_ds import AnnotationQueueRecordsByRecordIDs

        record_selector: dict[str, Any]
        if isinstance(self.record_selector, AnnotationQueueRecordsByRecordIDs):
            record_selector = self.record_selector.to_dict()
        else:
            record_selector = self.record_selector.to_dict()

        column_ids: None | Unset | list[str]
        if isinstance(self.column_ids, Unset):
            column_ids = UNSET
        elif isinstance(self.column_ids, list):
            column_ids = self.column_ids

        else:
            column_ids = self.column_ids

        export_format: Unset | str = UNSET
        if not isinstance(self.export_format, Unset):
            export_format = self.export_format.value

        redact = self.redact

        file_name: None | Unset | str
        file_name = UNSET if isinstance(self.file_name, Unset) else self.file_name

        export_computed_metrics_only = self.export_computed_metrics_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"record_selector": record_selector})
        if column_ids is not UNSET:
            field_dict["column_ids"] = column_ids
        if export_format is not UNSET:
            field_dict["export_format"] = export_format
        if redact is not UNSET:
            field_dict["redact"] = redact
        if file_name is not UNSET:
            field_dict["file_name"] = file_name
        if export_computed_metrics_only is not UNSET:
            field_dict["export_computed_metrics_only"] = export_computed_metrics_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_queue_records_by_filter_tree import AnnotationQueueRecordsByFilterTree
        from ..models.annotation_queue_records_by_record_i_ds import AnnotationQueueRecordsByRecordIDs

        d = dict(src_dict)

        def _parse_record_selector(
            data: object,
        ) -> Union["AnnotationQueueRecordsByFilterTree", "AnnotationQueueRecordsByRecordIDs"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueRecordsByRecordIDs.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return AnnotationQueueRecordsByFilterTree.from_dict(data)

        record_selector = _parse_record_selector(d.pop("record_selector"))

        def _parse_column_ids(data: object) -> None | Unset | list[str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(None | Unset | list[str], data)

        column_ids = _parse_column_ids(d.pop("column_ids", UNSET))

        _export_format = d.pop("export_format", UNSET)
        export_format: Unset | LLMExportFormat
        export_format = UNSET if isinstance(_export_format, Unset) else LLMExportFormat(_export_format)

        redact = d.pop("redact", UNSET)

        def _parse_file_name(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        file_name = _parse_file_name(d.pop("file_name", UNSET))

        export_computed_metrics_only = d.pop("export_computed_metrics_only", UNSET)

        annotation_queue_export_request = cls(
            record_selector=record_selector,
            column_ids=column_ids,
            export_format=export_format,
            redact=redact,
            file_name=file_name,
            export_computed_metrics_only=export_computed_metrics_only,
        )

        annotation_queue_export_request.additional_properties = d
        return annotation_queue_export_request

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
