from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionCreateResponse")


@_attrs_define
class SessionCreateResponse:
    """
    Attributes:
        id (str): Session id associated with the session.
        name (Union[None, str]): Name of the session.
        project_id (str): Project id associated with the session.
        project_name (str): Project name associated with the session.
        external_id (Union[None, Unset, str]): External id of the session.
        previous_session_id (Union[None, Unset, str]): Id of the previous session.
    """

    id: str
    name: Union[None, str]
    project_id: str
    project_name: str
    external_id: Union[None, Unset, str] = UNSET
    previous_session_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name: Union[None, str]
        name = self.name

        project_id = self.project_id

        project_name = self.project_name

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        previous_session_id: Union[None, Unset, str]
        if isinstance(self.previous_session_id, Unset):
            previous_session_id = UNSET
        else:
            previous_session_id = self.previous_session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "name": name, "project_id": project_id, "project_name": project_name})
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if previous_session_id is not UNSET:
            field_dict["previous_session_id"] = previous_session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_previous_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        previous_session_id = _parse_previous_session_id(d.pop("previous_session_id", UNSET))

        session_create_response = cls(
            id=id,
            name=name,
            project_id=project_id,
            project_name=project_name,
            external_id=external_id,
            previous_session_id=previous_session_id,
        )

        session_create_response.additional_properties = d
        return session_create_response

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
