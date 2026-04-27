from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_type_options import DataTypeOptions
from ..types import UNSET, Unset

T = TypeVar("T", bound="StepMetric")


@_attrs_define
class StepMetric:
    """
    Attributes:
        name (str):
        value (Any):
        status (None | str | Unset):
        explanation (None | str | Unset):
        rationale (None | str | Unset):
        cost (float | None | Unset):
        model_alias (None | str | Unset):
        num_judges (int | None | Unset):
        display_value (Any | None | Unset):
        data_type (DataTypeOptions | Unset):
    """

    name: str
    value: Any
    status: None | str | Unset = UNSET
    explanation: None | str | Unset = UNSET
    rationale: None | str | Unset = UNSET
    cost: float | None | Unset = UNSET
    model_alias: None | str | Unset = UNSET
    num_judges: int | None | Unset = UNSET
    display_value: Any | None | Unset = UNSET
    data_type: DataTypeOptions | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        value = self.value

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        else:
            status = self.status

        explanation: None | str | Unset
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        rationale: None | str | Unset
        if isinstance(self.rationale, Unset):
            rationale = UNSET
        else:
            rationale = self.rationale

        cost: float | None | Unset
        if isinstance(self.cost, Unset):
            cost = UNSET
        else:
            cost = self.cost

        model_alias: None | str | Unset
        if isinstance(self.model_alias, Unset):
            model_alias = UNSET
        else:
            model_alias = self.model_alias

        num_judges: int | None | Unset
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        display_value: Any | None | Unset
        if isinstance(self.display_value, Unset):
            display_value = UNSET
        else:
            display_value = self.display_value

        data_type: str | Unset = UNSET
        if not isinstance(self.data_type, Unset):
            data_type = self.data_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "value": value})
        if status is not UNSET:
            field_dict["status"] = status
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if rationale is not UNSET:
            field_dict["rationale"] = rationale
        if cost is not UNSET:
            field_dict["cost"] = cost
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if display_value is not UNSET:
            field_dict["display_value"] = display_value
        if data_type is not UNSET:
            field_dict["data_type"] = data_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        value = d.pop("value")

        def _parse_status(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_explanation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        def _parse_rationale(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rationale = _parse_rationale(d.pop("rationale", UNSET))

        def _parse_cost(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        cost = _parse_cost(d.pop("cost", UNSET))

        def _parse_model_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_alias = _parse_model_alias(d.pop("model_alias", UNSET))

        def _parse_num_judges(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        def _parse_display_value(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        display_value = _parse_display_value(d.pop("display_value", UNSET))

        _data_type = d.pop("data_type", UNSET)
        data_type: DataTypeOptions | Unset
        if isinstance(_data_type, Unset):
            data_type = UNSET
        else:
            data_type = DataTypeOptions(_data_type)

        step_metric = cls(
            name=name,
            value=value,
            status=status,
            explanation=explanation,
            rationale=rationale,
            cost=cost,
            model_alias=model_alias,
            num_judges=num_judges,
            display_value=display_value,
            data_type=data_type,
        )

        step_metric.additional_properties = d
        return step_metric

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
