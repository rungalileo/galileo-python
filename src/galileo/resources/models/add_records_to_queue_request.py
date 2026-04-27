from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.annotation_queue_records_by_filter_tree import AnnotationQueueRecordsByFilterTree
    from ..models.annotation_queue_records_by_record_i_ds import AnnotationQueueRecordsByRecordIDs


T = TypeVar("T", bound="AddRecordsToQueueRequest")


@_attrs_define
class AddRecordsToQueueRequest:
    """Request to add records to an annotation queue.

    Attributes:
        project_id (str): Project ID containing the records
        run_id (str): Run ID (log stream, experiment, or metrics testing) containing the records
        record_selector (AnnotationQueueRecordsByFilterTree | AnnotationQueueRecordsByRecordIDs): Selector to specify
            which records to add (either by record IDs or filter tree)
    """

    project_id: str
    run_id: str
    record_selector: AnnotationQueueRecordsByFilterTree | AnnotationQueueRecordsByRecordIDs
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_queue_records_by_record_i_ds import AnnotationQueueRecordsByRecordIDs

        project_id = self.project_id

        run_id = self.run_id

        record_selector: dict[str, Any]
        if isinstance(self.record_selector, AnnotationQueueRecordsByRecordIDs):
            record_selector = self.record_selector.to_dict()
        else:
            record_selector = self.record_selector.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "run_id": run_id, "record_selector": record_selector})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_queue_records_by_filter_tree import AnnotationQueueRecordsByFilterTree
        from ..models.annotation_queue_records_by_record_i_ds import AnnotationQueueRecordsByRecordIDs

        d = dict(src_dict)
        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        def _parse_record_selector(
            data: object,
        ) -> AnnotationQueueRecordsByFilterTree | AnnotationQueueRecordsByRecordIDs:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                record_selector_type_0 = AnnotationQueueRecordsByRecordIDs.from_dict(data)

                return record_selector_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            record_selector_type_1 = AnnotationQueueRecordsByFilterTree.from_dict(data)

            return record_selector_type_1

        record_selector = _parse_record_selector(d.pop("record_selector"))

        add_records_to_queue_request = cls(project_id=project_id, run_id=run_id, record_selector=record_selector)

        add_records_to_queue_request.additional_properties = d
        return add_records_to_queue_request

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
