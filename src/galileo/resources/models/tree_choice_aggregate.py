from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tree_choice_aggregate_counts import TreeChoiceAggregateCounts


T = TypeVar("T", bound="TreeChoiceAggregate")


@_attrs_define
class TreeChoiceAggregate:
    """
    Attributes:
        counts (TreeChoiceAggregateCounts):
        unrated_count (int):
        feedback_type (Union[Literal['tree_choice'], Unset]):  Default: 'tree_choice'.
    """

    counts: "TreeChoiceAggregateCounts"
    unrated_count: int
    feedback_type: Union[Literal["tree_choice"], Unset] = "tree_choice"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        counts = self.counts.to_dict()

        unrated_count = self.unrated_count

        feedback_type = self.feedback_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"counts": counts, "unrated_count": unrated_count})
        if feedback_type is not UNSET:
            field_dict["feedback_type"] = feedback_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tree_choice_aggregate_counts import TreeChoiceAggregateCounts

        d = dict(src_dict)
        counts = TreeChoiceAggregateCounts.from_dict(d.pop("counts"))

        unrated_count = d.pop("unrated_count")

        feedback_type = cast(Union[Literal["tree_choice"], Unset], d.pop("feedback_type", UNSET))
        if feedback_type != "tree_choice" and not isinstance(feedback_type, Unset):
            raise ValueError(f"feedback_type must match const 'tree_choice', got '{feedback_type}'")

        tree_choice_aggregate = cls(counts=counts, unrated_count=unrated_count, feedback_type=feedback_type)

        tree_choice_aggregate.additional_properties = d
        return tree_choice_aggregate

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
