from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.annotation_trace_selector import AnnotationTraceSelector
    from ..models.bulk_annotation_rating_create import BulkAnnotationRatingCreate
    from ..models.bulk_annotation_rating_delete import BulkAnnotationRatingDelete


T = TypeVar("T", bound="BulkAnnotationRequest")


@_attrs_define
class BulkAnnotationRequest:
    """
    Attributes:
        operations (list[BulkAnnotationRatingCreate | BulkAnnotationRatingDelete]):
        selector (AnnotationTraceSelector): Choose specific traces to apply the bulk operation to.
    """

    operations: list[BulkAnnotationRatingCreate | BulkAnnotationRatingDelete]
    selector: AnnotationTraceSelector
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.bulk_annotation_rating_create import BulkAnnotationRatingCreate

        operations = []
        for operations_item_data in self.operations:
            operations_item: dict[str, Any]
            if isinstance(operations_item_data, BulkAnnotationRatingCreate):
                operations_item = operations_item_data.to_dict()
            else:
                operations_item = operations_item_data.to_dict()

            operations.append(operations_item)

        selector = self.selector.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operations": operations, "selector": selector})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_trace_selector import AnnotationTraceSelector
        from ..models.bulk_annotation_rating_create import BulkAnnotationRatingCreate
        from ..models.bulk_annotation_rating_delete import BulkAnnotationRatingDelete

        d = dict(src_dict)
        operations = []
        _operations = d.pop("operations")
        for operations_item_data in _operations:

            def _parse_operations_item(data: object) -> BulkAnnotationRatingCreate | BulkAnnotationRatingDelete:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    operations_item_type_0 = BulkAnnotationRatingCreate.from_dict(data)

                    return operations_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                operations_item_type_1 = BulkAnnotationRatingDelete.from_dict(data)

                return operations_item_type_1

            operations_item = _parse_operations_item(operations_item_data)

            operations.append(operations_item)

        selector = AnnotationTraceSelector.from_dict(d.pop("selector"))

        bulk_annotation_request = cls(operations=operations, selector=selector)

        bulk_annotation_request.additional_properties = d
        return bulk_annotation_request

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
