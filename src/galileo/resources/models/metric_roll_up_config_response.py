from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.categorical_roll_up_method import CategoricalRollUpMethod
from ..models.numeric_roll_up_method import NumericRollUpMethod

T = TypeVar("T", bound="MetricRollUpConfigResponse")


@_attrs_define
class MetricRollUpConfigResponse:
    """Response for a metric roll up configuration.

    Attributes:
        roll_up_methods (list[CategoricalRollUpMethod] | list[NumericRollUpMethod]): List of roll up methods to apply to
            the metric. For numeric scorers we support doing multiple roll up types per metric.
        id (str):
        organization_id (str):
        scorer_id (str):
        metric_name (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    roll_up_methods: list[CategoricalRollUpMethod] | list[NumericRollUpMethod]
    id: str
    organization_id: str
    scorer_id: str
    metric_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        roll_up_methods: list[str]
        if isinstance(self.roll_up_methods, list):
            roll_up_methods = []
            for roll_up_methods_type_0_item_data in self.roll_up_methods:
                roll_up_methods_type_0_item = roll_up_methods_type_0_item_data.value
                roll_up_methods.append(roll_up_methods_type_0_item)

        else:
            roll_up_methods = []
            for roll_up_methods_type_1_item_data in self.roll_up_methods:
                roll_up_methods_type_1_item = roll_up_methods_type_1_item_data.value
                roll_up_methods.append(roll_up_methods_type_1_item)

        id = self.id

        organization_id = self.organization_id

        scorer_id = self.scorer_id

        metric_name = self.metric_name

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "roll_up_methods": roll_up_methods,
                "id": id,
                "organization_id": organization_id,
                "scorer_id": scorer_id,
                "metric_name": metric_name,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_roll_up_methods(data: object) -> list[CategoricalRollUpMethod] | list[NumericRollUpMethod]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                roll_up_methods_type_0 = []
                _roll_up_methods_type_0 = data
                for roll_up_methods_type_0_item_data in _roll_up_methods_type_0:
                    roll_up_methods_type_0_item = NumericRollUpMethod(roll_up_methods_type_0_item_data)

                    roll_up_methods_type_0.append(roll_up_methods_type_0_item)

                return roll_up_methods_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            roll_up_methods_type_1 = []
            _roll_up_methods_type_1 = data
            for roll_up_methods_type_1_item_data in _roll_up_methods_type_1:
                roll_up_methods_type_1_item = CategoricalRollUpMethod(roll_up_methods_type_1_item_data)

                roll_up_methods_type_1.append(roll_up_methods_type_1_item)

            return roll_up_methods_type_1

        roll_up_methods = _parse_roll_up_methods(d.pop("roll_up_methods"))

        id = d.pop("id")

        organization_id = d.pop("organization_id")

        scorer_id = d.pop("scorer_id")

        metric_name = d.pop("metric_name")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        metric_roll_up_config_response = cls(
            roll_up_methods=roll_up_methods,
            id=id,
            organization_id=organization_id,
            scorer_id=scorer_id,
            metric_name=metric_name,
            created_at=created_at,
            updated_at=updated_at,
        )

        metric_roll_up_config_response.additional_properties = d
        return metric_roll_up_config_response

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
