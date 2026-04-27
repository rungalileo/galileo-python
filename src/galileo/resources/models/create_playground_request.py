from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.name import Name


T = TypeVar("T", bound="CreatePlaygroundRequest")


@_attrs_define
class CreatePlaygroundRequest:
    """
    Attributes:
        name (Name | str):
        run_id (None | str | Unset): Optional run ID to initialize the playground with existing run data.
    """

    name: Name | str
    run_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.name import Name

        name: dict[str, Any] | str
        if isinstance(self.name, Name):
            name = self.name.to_dict()
        else:
            name = self.name

        run_id: None | str | Unset
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        else:
            run_id = self.run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if run_id is not UNSET:
            field_dict["run_id"] = run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.name import Name

        d = dict(src_dict)

        def _parse_name(data: object) -> Name | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                name_type_1 = Name.from_dict(data)

                return name_type_1
            except:  # noqa: E722
                pass
            return cast(Name | str, data)

        name = _parse_name(d.pop("name"))

        def _parse_run_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        create_playground_request = cls(name=name, run_id=run_id)

        create_playground_request.additional_properties = d
        return create_playground_request

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
