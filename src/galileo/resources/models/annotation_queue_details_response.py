from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.annotation_agreement_aggregate import AnnotationAgreementAggregate
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
    Attributes
    ----------
        num_logs_fully_annotated (Union[Unset, int]): Count of queue logs that have a rating for every queue template
            from each annotation-capable collaborator with track_progress enabled. Default: 0.
        annotation_aggregates (Union['AnnotationQueueDetailsResponseAnnotationAggregatesType0', None, Unset]): Queue-
            wide aggregates keyed by annotation template UUID. Null when the caller cannot view queue-wide aggregates.
        annotation_aggregates_by_annotator (Union['AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0',
            None, Unset]): Per-user aggregates keyed by annotation-capable collaborator UUID, then annotation template UUID.
            Null when the caller cannot view all per-user aggregates for the queue.
        overall_annotation_agreement (Union['AnnotationAgreementAggregate', None, Unset]): Queue-wide aggregate of
            record-level overall annotator agreement. Null when the caller cannot view queue-wide aggregates.
    """

    num_logs_fully_annotated: Unset | int = 0
    annotation_aggregates: Union["AnnotationQueueDetailsResponseAnnotationAggregatesType0", None, Unset] = UNSET
    annotation_aggregates_by_annotator: Union[
        "AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0", None, Unset
    ] = UNSET
    overall_annotation_agreement: Union["AnnotationAgreementAggregate", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.annotation_agreement_aggregate import AnnotationAgreementAggregate
        from ..models.annotation_queue_details_response_annotation_aggregates_by_annotator_type_0 import (
            AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0,
        )
        from ..models.annotation_queue_details_response_annotation_aggregates_type_0 import (
            AnnotationQueueDetailsResponseAnnotationAggregatesType0,
        )

        num_logs_fully_annotated = self.num_logs_fully_annotated

        annotation_aggregates: None | Unset | dict[str, Any]
        if isinstance(self.annotation_aggregates, Unset):
            annotation_aggregates = UNSET
        elif isinstance(self.annotation_aggregates, AnnotationQueueDetailsResponseAnnotationAggregatesType0):
            annotation_aggregates = self.annotation_aggregates.to_dict()
        else:
            annotation_aggregates = self.annotation_aggregates

        annotation_aggregates_by_annotator: None | Unset | dict[str, Any]
        if isinstance(self.annotation_aggregates_by_annotator, Unset):
            annotation_aggregates_by_annotator = UNSET
        elif isinstance(
            self.annotation_aggregates_by_annotator, AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0
        ):
            annotation_aggregates_by_annotator = self.annotation_aggregates_by_annotator.to_dict()
        else:
            annotation_aggregates_by_annotator = self.annotation_aggregates_by_annotator

        overall_annotation_agreement: None | Unset | dict[str, Any]
        if isinstance(self.overall_annotation_agreement, Unset):
            overall_annotation_agreement = UNSET
        elif isinstance(self.overall_annotation_agreement, AnnotationAgreementAggregate):
            overall_annotation_agreement = self.overall_annotation_agreement.to_dict()
        else:
            overall_annotation_agreement = self.overall_annotation_agreement

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if num_logs_fully_annotated is not UNSET:
            field_dict["num_logs_fully_annotated"] = num_logs_fully_annotated
        if annotation_aggregates is not UNSET:
            field_dict["annotation_aggregates"] = annotation_aggregates
        if annotation_aggregates_by_annotator is not UNSET:
            field_dict["annotation_aggregates_by_annotator"] = annotation_aggregates_by_annotator
        if overall_annotation_agreement is not UNSET:
            field_dict["overall_annotation_agreement"] = overall_annotation_agreement

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.annotation_agreement_aggregate import AnnotationAgreementAggregate
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
        ) -> Union["AnnotationQueueDetailsResponseAnnotationAggregatesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueDetailsResponseAnnotationAggregatesType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AnnotationQueueDetailsResponseAnnotationAggregatesType0", None, Unset], data)

        annotation_aggregates = _parse_annotation_aggregates(d.pop("annotation_aggregates", UNSET))

        def _parse_annotation_aggregates_by_annotator(
            data: object,
        ) -> Union["AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AnnotationQueueDetailsResponseAnnotationAggregatesByAnnotatorType0", None, Unset], data)

        annotation_aggregates_by_annotator = _parse_annotation_aggregates_by_annotator(
            d.pop("annotation_aggregates_by_annotator", UNSET)
        )

        def _parse_overall_annotation_agreement(data: object) -> Union["AnnotationAgreementAggregate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AnnotationAgreementAggregate.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["AnnotationAgreementAggregate", None, Unset], data)

        overall_annotation_agreement = _parse_overall_annotation_agreement(d.pop("overall_annotation_agreement", UNSET))

        annotation_queue_details_response = cls(
            num_logs_fully_annotated=num_logs_fully_annotated,
            annotation_aggregates=annotation_aggregates,
            annotation_aggregates_by_annotator=annotation_aggregates_by_annotator,
            overall_annotation_agreement=overall_annotation_agreement,
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
