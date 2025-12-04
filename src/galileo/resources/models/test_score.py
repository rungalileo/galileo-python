from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TestScore")


@_attrs_define
class TestScore:
    """
    Attributes
    ----------
        node_type (NodeType):
        score (Union[None, Unset, bool, float, int, str]):
    """

    node_type: NodeType
    score: Union[None, Unset, bool, float, int, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        node_type = self.node_type.value

        score: Union[None, Unset, bool, float, int, str]
        score = UNSET if isinstance(self.score, Unset) else self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"node_type": node_type})
        if score is not UNSET:
            field_dict["score"] = score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        node_type = NodeType(d.pop("node_type"))

        def _parse_score(data: object) -> Union[None, Unset, bool, float, int, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool, float, int, str], data)

        score = _parse_score(d.pop("score", UNSET))

        test_score = cls(node_type=node_type, score=score)

        test_score.additional_properties = d
        return test_score

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
