import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.alert_monitor_type import AlertMonitorType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alert_condition import AlertCondition


T = TypeVar("T", bound="AlertConfigurationResponse")


@_attrs_define
class AlertConfigurationResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        id (str):
        project_id (str):
        updated_at (datetime.datetime):
        active (Union[None, Unset, bool]):
        alert_sent (Union[None, Unset, bool]):
        conditions (Union[None, Unset, list['AlertCondition']]):
        counter (Union[None, Unset, int]):
        counter_since_last_sent (Union[None, Unset, int]):
        interval (Union[None, Unset, int]):
        last_sent (Union[None, Unset, datetime.datetime]):
        last_triggered (Union[None, Unset, datetime.datetime]):
        processed_by (Union[None, Unset, str]):
        schema_version (Union[AlertMonitorType, None, Unset]):
    """

    created_at: datetime.datetime
    created_by: str
    id: str
    project_id: str
    updated_at: datetime.datetime
    active: Union[None, Unset, bool] = UNSET
    alert_sent: Union[None, Unset, bool] = UNSET
    conditions: Union[None, Unset, list["AlertCondition"]] = UNSET
    counter: Union[None, Unset, int] = UNSET
    counter_since_last_sent: Union[None, Unset, int] = UNSET
    interval: Union[None, Unset, int] = UNSET
    last_sent: Union[None, Unset, datetime.datetime] = UNSET
    last_triggered: Union[None, Unset, datetime.datetime] = UNSET
    processed_by: Union[None, Unset, str] = UNSET
    schema_version: Union[AlertMonitorType, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        id = self.id

        project_id = self.project_id

        updated_at = self.updated_at.isoformat()

        active: Union[None, Unset, bool]
        if isinstance(self.active, Unset):
            active = UNSET
        else:
            active = self.active

        alert_sent: Union[None, Unset, bool]
        if isinstance(self.alert_sent, Unset):
            alert_sent = UNSET
        else:
            alert_sent = self.alert_sent

        conditions: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.conditions, Unset):
            conditions = UNSET
        elif isinstance(self.conditions, list):
            conditions = []
            for conditions_type_0_item_data in self.conditions:
                conditions_type_0_item = conditions_type_0_item_data.to_dict()
                conditions.append(conditions_type_0_item)

        else:
            conditions = self.conditions

        counter: Union[None, Unset, int]
        if isinstance(self.counter, Unset):
            counter = UNSET
        else:
            counter = self.counter

        counter_since_last_sent: Union[None, Unset, int]
        if isinstance(self.counter_since_last_sent, Unset):
            counter_since_last_sent = UNSET
        else:
            counter_since_last_sent = self.counter_since_last_sent

        interval: Union[None, Unset, int]
        if isinstance(self.interval, Unset):
            interval = UNSET
        else:
            interval = self.interval

        last_sent: Union[None, Unset, str]
        if isinstance(self.last_sent, Unset):
            last_sent = UNSET
        elif isinstance(self.last_sent, datetime.datetime):
            last_sent = self.last_sent.isoformat()
        else:
            last_sent = self.last_sent

        last_triggered: Union[None, Unset, str]
        if isinstance(self.last_triggered, Unset):
            last_triggered = UNSET
        elif isinstance(self.last_triggered, datetime.datetime):
            last_triggered = self.last_triggered.isoformat()
        else:
            last_triggered = self.last_triggered

        processed_by: Union[None, Unset, str]
        if isinstance(self.processed_by, Unset):
            processed_by = UNSET
        else:
            processed_by = self.processed_by

        schema_version: Union[None, Unset, str]
        if isinstance(self.schema_version, Unset):
            schema_version = UNSET
        elif isinstance(self.schema_version, AlertMonitorType):
            schema_version = self.schema_version.value
        else:
            schema_version = self.schema_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "id": id,
                "project_id": project_id,
                "updated_at": updated_at,
            }
        )
        if active is not UNSET:
            field_dict["active"] = active
        if alert_sent is not UNSET:
            field_dict["alert_sent"] = alert_sent
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if counter is not UNSET:
            field_dict["counter"] = counter
        if counter_since_last_sent is not UNSET:
            field_dict["counter_since_last_sent"] = counter_since_last_sent
        if interval is not UNSET:
            field_dict["interval"] = interval
        if last_sent is not UNSET:
            field_dict["last_sent"] = last_sent
        if last_triggered is not UNSET:
            field_dict["last_triggered"] = last_triggered
        if processed_by is not UNSET:
            field_dict["processed_by"] = processed_by
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.alert_condition import AlertCondition

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        id = d.pop("id")

        project_id = d.pop("project_id")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_active(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        active = _parse_active(d.pop("active", UNSET))

        def _parse_alert_sent(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        alert_sent = _parse_alert_sent(d.pop("alert_sent", UNSET))

        def _parse_conditions(data: object) -> Union[None, Unset, list["AlertCondition"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                conditions_type_0 = []
                _conditions_type_0 = data
                for conditions_type_0_item_data in _conditions_type_0:
                    conditions_type_0_item = AlertCondition.from_dict(conditions_type_0_item_data)

                    conditions_type_0.append(conditions_type_0_item)

                return conditions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["AlertCondition"]], data)

        conditions = _parse_conditions(d.pop("conditions", UNSET))

        def _parse_counter(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        counter = _parse_counter(d.pop("counter", UNSET))

        def _parse_counter_since_last_sent(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        counter_since_last_sent = _parse_counter_since_last_sent(d.pop("counter_since_last_sent", UNSET))

        def _parse_interval(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        interval = _parse_interval(d.pop("interval", UNSET))

        def _parse_last_sent(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sent_type_0 = isoparse(data)

                return last_sent_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_sent = _parse_last_sent(d.pop("last_sent", UNSET))

        def _parse_last_triggered(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_triggered_type_0 = isoparse(data)

                return last_triggered_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_triggered = _parse_last_triggered(d.pop("last_triggered", UNSET))

        def _parse_processed_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        processed_by = _parse_processed_by(d.pop("processed_by", UNSET))

        def _parse_schema_version(data: object) -> Union[AlertMonitorType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                schema_version_type_0 = AlertMonitorType(data)

                return schema_version_type_0
            except:  # noqa: E722
                pass
            return cast(Union[AlertMonitorType, None, Unset], data)

        schema_version = _parse_schema_version(d.pop("schema_version", UNSET))

        alert_configuration_response = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            project_id=project_id,
            updated_at=updated_at,
            active=active,
            alert_sent=alert_sent,
            conditions=conditions,
            counter=counter,
            counter_since_last_sent=counter_since_last_sent,
            interval=interval,
            last_sent=last_sent,
            last_triggered=last_triggered,
            processed_by=processed_by,
            schema_version=schema_version,
        )

        alert_configuration_response.additional_properties = d
        return alert_configuration_response

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
