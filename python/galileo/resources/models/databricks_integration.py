from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.databricks_integration_extra_type_0 import DatabricksIntegrationExtraType0


T = TypeVar("T", bound="DatabricksIntegration")


@_attrs_define
class DatabricksIntegration:
    """
    Attributes:
        extra (Union['DatabricksIntegrationExtraType0', None, Unset]):
        name (Union[Literal['databricks'], Unset]):  Default: 'databricks'.
    """

    extra: Union["DatabricksIntegrationExtraType0", None, Unset] = UNSET
    name: Union[Literal["databricks"], Unset] = "databricks"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.databricks_integration_extra_type_0 import DatabricksIntegrationExtraType0

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, DatabricksIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if extra is not UNSET:
            field_dict["extra"] = extra
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.databricks_integration_extra_type_0 import DatabricksIntegrationExtraType0

        d = src_dict.copy()

        def _parse_extra(data: object) -> Union["DatabricksIntegrationExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = DatabricksIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["DatabricksIntegrationExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        name = cast(Union[Literal["databricks"], Unset], d.pop("name", UNSET))
        if name != "databricks" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'databricks', got '{name}'")

        databricks_integration = cls(extra=extra, name=name)

        databricks_integration.additional_properties = d
        return databricks_integration

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
