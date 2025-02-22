from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.bulk_feedback_rating_create import BulkFeedbackRatingCreate
    from ..models.bulk_feedback_rating_delete import BulkFeedbackRatingDelete
    from ..models.index_selector import IndexSelector


T = TypeVar("T", bound="BulkFeedbackRequest")


@_attrs_define
class BulkFeedbackRequest:
    """
    Attributes:
        operations (list[Union['BulkFeedbackRatingCreate', 'BulkFeedbackRatingDelete']]):
        selector (IndexSelector): Choose specific indexes to apply the bulk operation to.
    """

    operations: list[Union["BulkFeedbackRatingCreate", "BulkFeedbackRatingDelete"]]
    selector: "IndexSelector"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.bulk_feedback_rating_create import BulkFeedbackRatingCreate

        operations = []
        for operations_item_data in self.operations:
            operations_item: dict[str, Any]
            if isinstance(operations_item_data, BulkFeedbackRatingCreate):
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
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.bulk_feedback_rating_create import BulkFeedbackRatingCreate
        from ..models.bulk_feedback_rating_delete import BulkFeedbackRatingDelete
        from ..models.index_selector import IndexSelector

        d = src_dict.copy()
        operations = []
        _operations = d.pop("operations")
        for operations_item_data in _operations:

            def _parse_operations_item(data: object) -> Union["BulkFeedbackRatingCreate", "BulkFeedbackRatingDelete"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    operations_item_type_0 = BulkFeedbackRatingCreate.from_dict(data)

                    return operations_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                operations_item_type_1 = BulkFeedbackRatingDelete.from_dict(data)

                return operations_item_type_1

            operations_item = _parse_operations_item(operations_item_data)

            operations.append(operations_item)

        selector = IndexSelector.from_dict(d.pop("selector"))

        bulk_feedback_request = cls(operations=operations, selector=selector)

        bulk_feedback_request.additional_properties = d
        return bulk_feedback_request

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
