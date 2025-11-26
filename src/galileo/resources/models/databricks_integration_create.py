from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatabricksIntegrationCreate")


@_attrs_define
class DatabricksIntegrationCreate:
    """
    Attributes
    ----------
        token (str):
        hostname (str):
        default_catalog_name (Union[None, Unset, str]):
        path (Union[None, Unset, str]):
        llm (Union[Unset, bool]):  Default: False.
        storage (Union[Unset, bool]):  Default: False.
    """

    token: str
    hostname: str
    default_catalog_name: Union[None, Unset, str] = UNSET
    path: Union[None, Unset, str] = UNSET
    llm: Union[Unset, bool] = False
    storage: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        hostname = self.hostname

        default_catalog_name: Union[None, Unset, str]
        default_catalog_name = UNSET if isinstance(self.default_catalog_name, Unset) else self.default_catalog_name

        path: Union[None, Unset, str]
        path = UNSET if isinstance(self.path, Unset) else self.path

        llm = self.llm

        storage = self.storage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"token": token, "hostname": hostname})
        if default_catalog_name is not UNSET:
            field_dict["default_catalog_name"] = default_catalog_name
        if path is not UNSET:
            field_dict["path"] = path
        if llm is not UNSET:
            field_dict["llm"] = llm
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        hostname = d.pop("hostname")

        def _parse_default_catalog_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_catalog_name = _parse_default_catalog_name(d.pop("default_catalog_name", UNSET))

        def _parse_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        path = _parse_path(d.pop("path", UNSET))

        llm = d.pop("llm", UNSET)

        storage = d.pop("storage", UNSET)

        databricks_integration_create = cls(
            token=token,
            hostname=hostname,
            default_catalog_name=default_catalog_name,
            path=path,
            llm=llm,
            storage=storage,
        )

        databricks_integration_create.additional_properties = d
        return databricks_integration_create

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
