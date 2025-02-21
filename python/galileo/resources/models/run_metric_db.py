import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.feedback_aggregate import FeedbackAggregate
    from ..models.run_metric_db_extra_type_1 import RunMetricDBExtraType1


T = TypeVar("T", bound="RunMetricDB")


@_attrs_define
class RunMetricDB:
    """
    Attributes:
        created_at (datetime.datetime):
        key (str):
        run_id (str):
        updated_at (datetime.datetime):
        epoch (Union[Unset, int]):  Default: 0.
        extra (Union['RunMetricDBExtraType1', None, Unset, list[Any]]):
        object_value (Union['FeedbackAggregate', None, Unset]):
        value (Union[None, Unset, float]):
    """

    created_at: datetime.datetime
    key: str
    run_id: str
    updated_at: datetime.datetime
    epoch: Union[Unset, int] = 0
    extra: Union["RunMetricDBExtraType1", None, Unset, list[Any]] = UNSET
    object_value: Union["FeedbackAggregate", None, Unset] = UNSET
    value: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.run_metric_db_extra_type_1 import RunMetricDBExtraType1

        created_at = self.created_at.isoformat()

        key = self.key

        run_id = self.run_id

        updated_at = self.updated_at.isoformat()

        epoch = self.epoch

        extra: Union[None, Unset, dict[str, Any], list[Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, list):
            extra = self.extra

        elif isinstance(self.extra, RunMetricDBExtraType1):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        object_value: Union[None, Unset, dict[str, Any]]
        if isinstance(self.object_value, Unset):
            object_value = UNSET
        elif isinstance(self.object_value, FeedbackAggregate):
            object_value = self.object_value.to_dict()
        else:
            object_value = self.object_value

        value: Union[None, Unset, float]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"created_at": created_at, "key": key, "run_id": run_id, "updated_at": updated_at})
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if extra is not UNSET:
            field_dict["extra"] = extra
        if object_value is not UNSET:
            field_dict["object_value"] = object_value
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.run_metric_db_extra_type_1 import RunMetricDBExtraType1

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        key = d.pop("key")

        run_id = d.pop("run_id")

        updated_at = isoparse(d.pop("updated_at"))

        epoch = d.pop("epoch", UNSET)

        def _parse_extra(data: object) -> Union["RunMetricDBExtraType1", None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                extra_type_0 = cast(list[Any], data)

                return extra_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_1 = RunMetricDBExtraType1.from_dict(data)

                return extra_type_1
            except:  # noqa: E722
                pass
            return cast(Union["RunMetricDBExtraType1", None, Unset, list[Any]], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        def _parse_object_value(data: object) -> Union["FeedbackAggregate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                object_value_type_0 = FeedbackAggregate.from_dict(data)

                return object_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FeedbackAggregate", None, Unset], data)

        object_value = _parse_object_value(d.pop("object_value", UNSET))

        def _parse_value(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        value = _parse_value(d.pop("value", UNSET))

        run_metric_db = cls(
            created_at=created_at,
            key=key,
            run_id=run_id,
            updated_at=updated_at,
            epoch=epoch,
            extra=extra,
            object_value=object_value,
            value=value,
        )

        run_metric_db.additional_properties = d
        return run_metric_db

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
