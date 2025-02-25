from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatabricksIntegrationCreate")


@_attrs_define
class DatabricksIntegrationCreate:
    """
    Attributes:
        hostname (str):
        token (str):
        default_catalog_name (Union[None, Unset, str]):
        llm (Union[Unset, bool]):  Default: False.
        path (Union[None, Unset, str]):
        storage (Union[Unset, bool]):  Default: False.
    """

    hostname: str
    token: str
    default_catalog_name: Union[None, Unset, str] = UNSET
    llm: Union[Unset, bool] = False
    path: Union[None, Unset, str] = UNSET
    storage: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hostname = self.hostname

        token = self.token

        default_catalog_name: Union[None, Unset, str]
        if isinstance(self.default_catalog_name, Unset):
            default_catalog_name = UNSET
        else:
            default_catalog_name = self.default_catalog_name

        llm = self.llm

        path: Union[None, Unset, str]
        if isinstance(self.path, Unset):
            path = UNSET
        else:
            path = self.path

        storage = self.storage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"hostname": hostname, "token": token})
        if default_catalog_name is not UNSET:
            field_dict["default_catalog_name"] = default_catalog_name
        if llm is not UNSET:
            field_dict["llm"] = llm
        if path is not UNSET:
            field_dict["path"] = path
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        hostname = d.pop("hostname")

        token = d.pop("token")

        def _parse_default_catalog_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_catalog_name = _parse_default_catalog_name(d.pop("default_catalog_name", UNSET))

        llm = d.pop("llm", UNSET)

        def _parse_path(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        path = _parse_path(d.pop("path", UNSET))

        storage = d.pop("storage", UNSET)

        databricks_integration_create = cls(
            hostname=hostname,
            token=token,
            default_catalog_name=default_catalog_name,
            llm=llm,
            path=path,
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
