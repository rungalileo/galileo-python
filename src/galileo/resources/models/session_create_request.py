from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SessionCreateRequest")


@_attrs_define
class SessionCreateRequest:
    """
    Attributes:
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        external_id (Union[None, Unset, str]): External id of the session.
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        name (Union[None, Unset, str]): Name of the session.
        previous_session_id (Union[None, Unset, str]): Id of the previous session.
    """

    experiment_id: Union[None, Unset, str] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    log_stream_id: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    previous_session_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        experiment_id: Union[None, Unset, str]
        if isinstance(self.experiment_id, Unset):
            experiment_id = UNSET
        else:
            experiment_id = self.experiment_id

        external_id: Union[None, Unset, str]
        if isinstance(self.external_id, Unset):
            external_id = UNSET
        else:
            external_id = self.external_id

        log_stream_id: Union[None, Unset, str]
        if isinstance(self.log_stream_id, Unset):
            log_stream_id = UNSET
        else:
            log_stream_id = self.log_stream_id

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        previous_session_id: Union[None, Unset, str]
        if isinstance(self.previous_session_id, Unset):
            previous_session_id = UNSET
        else:
            previous_session_id = self.previous_session_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if name is not UNSET:
            field_dict["name"] = name
        if previous_session_id is not UNSET:
            field_dict["previous_session_id"] = previous_session_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_previous_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        previous_session_id = _parse_previous_session_id(d.pop("previous_session_id", UNSET))

        session_create_request = cls(
            experiment_id=experiment_id,
            external_id=external_id,
            log_stream_id=log_stream_id,
            name=name,
            previous_session_id=previous_session_id,
        )

        session_create_request.additional_properties = d
        return session_create_request

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
