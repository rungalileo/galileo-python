from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.alert_monitor_type import AlertMonitorType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alert_condition import AlertCondition


T = TypeVar("T", bound="CreateAlertConfigurationRequest")


@_attrs_define
class CreateAlertConfigurationRequest:
    """
    Attributes:
        conditions (list['AlertCondition']):
        interval (int):
        created_by (Union[None, Unset, str]):
        project_id (Union[None, Unset, str]):
        schema_version (Union[Unset, AlertMonitorType]):
    """

    conditions: list["AlertCondition"]
    interval: int
    created_by: Union[None, Unset, str] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    schema_version: Union[Unset, AlertMonitorType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conditions = []
        for conditions_item_data in self.conditions:
            conditions_item = conditions_item_data.to_dict()
            conditions.append(conditions_item)

        interval = self.interval

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        schema_version: Union[Unset, str] = UNSET
        if not isinstance(self.schema_version, Unset):
            schema_version = self.schema_version.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"conditions": conditions, "interval": interval})
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.alert_condition import AlertCondition

        d = src_dict.copy()
        conditions = []
        _conditions = d.pop("conditions")
        for conditions_item_data in _conditions:
            conditions_item = AlertCondition.from_dict(conditions_item_data)

            conditions.append(conditions_item)

        interval = d.pop("interval")

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        _schema_version = d.pop("schema_version", UNSET)
        schema_version: Union[Unset, AlertMonitorType]
        if isinstance(_schema_version, Unset):
            schema_version = UNSET
        else:
            schema_version = AlertMonitorType(_schema_version)

        create_alert_configuration_request = cls(
            conditions=conditions,
            interval=interval,
            created_by=created_by,
            project_id=project_id,
            schema_version=schema_version,
        )

        create_alert_configuration_request.additional_properties = d
        return create_alert_configuration_request

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
