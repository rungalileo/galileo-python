from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from galileo.resources.models.validation_error import ValidationError

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.validation_error import ValidationError


T = TypeVar("T", bound="BaseScorerVersionResponse")


@_attrs_define
class HTTPValidationError:
    """
    Attributes:
        detail (Union[Unset, list['ValidationError']]):
    """

    detail: Union[Unset, list["ValidationError"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.detail, Unset):
            detail = []
            for detail_item_data in self.detail:
                detail_item = detail_item_data.to_dict()
                detail.append(detail_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _detail = d.pop("detail", UNSET)
        if _detail is not UNSET and _detail is not None:
            # Use list comprehension for bulk parse
            detail = [ValidationError.from_dict(item) for item in _detail]
        else:
            detail = _detail  # Could be UNSET, None, or empty

        instance = cls(detail=detail)
        instance.additional_properties = d
        return instance

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
