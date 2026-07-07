from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.write_health_score_request_secondary_type_0 import WriteHealthScoreRequestSecondaryType0


T = TypeVar("T", bound="WriteHealthScoreRequest")


@_attrs_define
class WriteHealthScoreRequest:
    """
    Attributes:
        dataset_id (str):
        health_score_type (str):
        score (float):
        secondary (Union['WriteHealthScoreRequestSecondaryType0', None, Unset]):
    """

    dataset_id: str
    health_score_type: str
    score: float
    secondary: Union["WriteHealthScoreRequestSecondaryType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.write_health_score_request_secondary_type_0 import WriteHealthScoreRequestSecondaryType0

        dataset_id = self.dataset_id

        health_score_type = self.health_score_type

        score = self.score

        secondary: Union[None, Unset, dict[str, Any]]
        if isinstance(self.secondary, Unset):
            secondary = UNSET
        elif isinstance(self.secondary, WriteHealthScoreRequestSecondaryType0):
            secondary = self.secondary.to_dict()
        else:
            secondary = self.secondary

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"dataset_id": dataset_id, "health_score_type": health_score_type, "score": score})
        if secondary is not UNSET:
            field_dict["secondary"] = secondary

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.write_health_score_request_secondary_type_0 import WriteHealthScoreRequestSecondaryType0

        d = dict(src_dict)
        dataset_id = d.pop("dataset_id")

        health_score_type = d.pop("health_score_type")

        score = d.pop("score")

        def _parse_secondary(data: object) -> Union["WriteHealthScoreRequestSecondaryType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                secondary_type_0 = WriteHealthScoreRequestSecondaryType0.from_dict(data)

                return secondary_type_0
            except:  # noqa: E722
                pass
            return cast(Union["WriteHealthScoreRequestSecondaryType0", None, Unset], data)

        secondary = _parse_secondary(d.pop("secondary", UNSET))

        write_health_score_request = cls(
            dataset_id=dataset_id, health_score_type=health_score_type, score=score, secondary=secondary
        )

        write_health_score_request.additional_properties = d
        return write_health_score_request

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
