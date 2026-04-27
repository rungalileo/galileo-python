from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_type import ScorerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricComputing")


@_attrs_define
class MetricComputing:
    """
    Attributes:
        status_type (Literal['computing'] | Unset):  Default: 'computing'.
        scorer_type (None | ScorerType | Unset):
        metric_key_alias (None | str | Unset):
        message (str | Unset):  Default: 'Metric is computing.'.
    """

    status_type: Literal["computing"] | Unset = "computing"
    scorer_type: None | ScorerType | Unset = UNSET
    metric_key_alias: None | str | Unset = UNSET
    message: str | Unset = "Metric is computing."
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status_type = self.status_type

        scorer_type: None | str | Unset
        if isinstance(self.scorer_type, Unset):
            scorer_type = UNSET
        elif isinstance(self.scorer_type, ScorerType):
            scorer_type = self.scorer_type.value
        else:
            scorer_type = self.scorer_type

        metric_key_alias: None | str | Unset
        if isinstance(self.metric_key_alias, Unset):
            metric_key_alias = UNSET
        else:
            metric_key_alias = self.metric_key_alias

        message = self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status_type is not UNSET:
            field_dict["status_type"] = status_type
        if scorer_type is not UNSET:
            field_dict["scorer_type"] = scorer_type
        if metric_key_alias is not UNSET:
            field_dict["metric_key_alias"] = metric_key_alias
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status_type = cast(Literal["computing"] | Unset, d.pop("status_type", UNSET))
        if status_type != "computing" and not isinstance(status_type, Unset):
            raise ValueError(f"status_type must match const 'computing', got '{status_type}'")

        def _parse_scorer_type(data: object) -> None | ScorerType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scorer_type_type_0 = ScorerType(data)

                return scorer_type_type_0
            except:  # noqa: E722
                pass
            return cast(None | ScorerType | Unset, data)

        scorer_type = _parse_scorer_type(d.pop("scorer_type", UNSET))

        def _parse_metric_key_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metric_key_alias = _parse_metric_key_alias(d.pop("metric_key_alias", UNSET))

        message = d.pop("message", UNSET)

        metric_computing = cls(
            status_type=status_type, scorer_type=scorer_type, metric_key_alias=metric_key_alias, message=message
        )

        metric_computing.additional_properties = d
        return metric_computing

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
