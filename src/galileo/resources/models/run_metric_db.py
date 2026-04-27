from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

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
        key (str):
        run_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        value (float | None | Unset):
        object_value (FeedbackAggregate | None | Unset):
        epoch (int | Unset):  Default: 0.
        extra (list[Any] | None | RunMetricDBExtraType1 | Unset):
    """

    key: str
    run_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    value: float | None | Unset = UNSET
    object_value: FeedbackAggregate | None | Unset = UNSET
    epoch: int | Unset = 0
    extra: list[Any] | None | RunMetricDBExtraType1 | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.run_metric_db_extra_type_1 import RunMetricDBExtraType1

        key = self.key

        run_id = self.run_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        value: float | None | Unset
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        object_value: dict[str, Any] | None | Unset
        if isinstance(self.object_value, Unset):
            object_value = UNSET
        elif isinstance(self.object_value, FeedbackAggregate):
            object_value = self.object_value.to_dict()
        else:
            object_value = self.object_value

        epoch = self.epoch

        extra: dict[str, Any] | list[Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, list):
            extra = self.extra

        elif isinstance(self.extra, RunMetricDBExtraType1):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"key": key, "run_id": run_id, "created_at": created_at, "updated_at": updated_at})
        if value is not UNSET:
            field_dict["value"] = value
        if object_value is not UNSET:
            field_dict["object_value"] = object_value
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.run_metric_db_extra_type_1 import RunMetricDBExtraType1

        d = dict(src_dict)
        key = d.pop("key")

        run_id = d.pop("run_id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_value(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        value = _parse_value(d.pop("value", UNSET))

        def _parse_object_value(data: object) -> FeedbackAggregate | None | Unset:
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
            return cast(FeedbackAggregate | None | Unset, data)

        object_value = _parse_object_value(d.pop("object_value", UNSET))

        epoch = d.pop("epoch", UNSET)

        def _parse_extra(data: object) -> list[Any] | None | RunMetricDBExtraType1 | Unset:
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
            return cast(list[Any] | None | RunMetricDBExtraType1 | Unset, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        run_metric_db = cls(
            key=key,
            run_id=run_id,
            created_at=created_at,
            updated_at=updated_at,
            value=value,
            object_value=object_value,
            epoch=epoch,
            extra=extra,
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
