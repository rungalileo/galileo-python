from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_queue_details_response_annotation_aggregates_by_annotator_type_0 import (
        AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0,
    )
    from ..models.annotation_queue_details_response_annotation_aggregates_type_0 import (
        AnnotationQueueDetailsResponseAnnotationAggregatesType0,
    )


T = TypeVar("T", bound="AnnotationQueueDetailsResponse")


@_attrs_define
class AnnotationQueueDetailsResponse:
    """
    Attributes:
        num_logs_fully_annotated (int | Unset): Count of queue logs that have a rating for every queue template from
            each annotation-capable collaborator with track_progress enabled. Default: 0.
        annotation_aggregates (AnnotationQueueDetailsResponseAnnotationAggregatesType0 | None | Unset): Queue-wide
            aggregates keyed by annotation template UUID. Null when the caller cannot view queue-wide aggregates.
        annotation_aggregates_by_annotator (AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0 | None |
            Unset): Per-user aggregates keyed by annotation-capable collaborator UUID, then annotation template UUID. Null
            when the caller cannot view all per-user aggregates for the queue.
    """

    num_logs_fully_annotated: int | Unset = 0
    annotation_aggregates: AnnotationQueueDetailsResponseAnnotationAggregatesType0 | None | Unset = UNSET
    annotation_aggregates_by_annotator: (
        AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0 | None | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_queue_details_response_annotation_aggregates_by_annotator_type_0 import (
            AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0,
        )
        from ..models.annotation_queue_details_response_annotation_aggregates_type_0 import (
            AnnotationQueueDetailsResponseAnnotationAggregatesType0,
        )

        num_logs_fully_annotated = self.num_logs_fully_annotated

        annotation_aggregates: dict[str, Any] | None | Unset
        if isinstance(self.annotation_aggregates, Unset):
            annotation_aggregates = UNSET
        elif isinstance(self.annotation_aggregates, AnnotationQueueDetailsResponseAnnotationAggregatesType0):
            annotation_aggregates = self.annotation_aggregates.to_dict()
        else:
            annotation_aggregates = self.annotation_aggregates

        annotation_aggregates_by_annotator: dict[str, Any] | None | Unset
        if isinstance(self.annotation_aggregates_by_annotator, Unset):
            annotation_aggregates_by_annotator = UNSET
        elif isinstance(
            self.annotation_aggregates_by_annotator, AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0
        ):
            annotation_aggregates_by_annotator = self.annotation_aggregates_by_annotator.to_dict()
        else:
            annotation_aggregates_by_annotator = self.annotation_aggregates_by_annotator

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if num_logs_fully_annotated is not UNSET:
            field_dict["num_logs_fully_annotated"] = num_logs_fully_annotated
        if annotation_aggregates is not UNSET:
            field_dict["annotation_aggregates"] = annotation_aggregates
        if annotation_aggregates_by_annotator is not UNSET:
            field_dict["annotation_aggregates_by_annotator"] = annotation_aggregates_by_annotator

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_queue_details_response_annotation_aggregates_by_annotator_type_0 import (
            AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0,
        )
        from ..models.annotation_queue_details_response_annotation_aggregates_type_0 import (
            AnnotationQueueDetailsResponseAnnotationAggregatesType0,
        )

        d = dict(src_dict)
        num_logs_fully_annotated = d.pop("num_logs_fully_annotated", UNSET)

        def _parse_annotation_aggregates(
            data: object,
        ) -> AnnotationQueueDetailsResponseAnnotationAggregatesType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                annotation_aggregates_type_0 = AnnotationQueueDetailsResponseAnnotationAggregatesType0.from_dict(data)

                return annotation_aggregates_type_0
            except:  # noqa: E722
                pass
            return cast(AnnotationQueueDetailsResponseAnnotationAggregatesType0 | None | Unset, data)

        annotation_aggregates = _parse_annotation_aggregates(d.pop("annotation_aggregates", UNSET))

        def _parse_annotation_aggregates_by_annotator(
            data: object,
        ) -> AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                annotation_aggregates_by_annotator_type_0 = (
                    AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0.from_dict(data)
                )

                return annotation_aggregates_by_annotator_type_0
            except:  # noqa: E722
                pass
            return cast(AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0 | None | Unset, data)

        annotation_aggregates_by_annotator = _parse_annotation_aggregates_by_annotator(
            d.pop("annotation_aggregates_by_annotator", UNSET)
        )

        annotation_queue_details_response = cls(
            num_logs_fully_annotated=num_logs_fully_annotated,
            annotation_aggregates=annotation_aggregates,
            annotation_aggregates_by_annotator=annotation_aggregates_by_annotator,
        )

        annotation_queue_details_response.additional_properties = d
        return annotation_queue_details_response

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
