from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_type import ScorerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetricPending")


@_attrs_define
class MetricPending:
    """
    Attributes
    ----------
        status_type (Union[Literal['pending'], Unset]):  Default: 'pending'.
        scorer_type (Union[None, ScorerType, Unset]):
        metric_key_alias (Union[None, Unset, str]):
    """

    status_type: Literal["pending"] | Unset = "pending"
    scorer_type: None | ScorerType | Unset = UNSET
    metric_key_alias: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status_type = self.status_type

        scorer_type: None | Unset | str
        if isinstance(self.scorer_type, Unset):
            scorer_type = UNSET
        elif isinstance(self.scorer_type, ScorerType):
            scorer_type = self.scorer_type.value
        else:
            scorer_type = self.scorer_type

        metric_key_alias: None | Unset | str
        metric_key_alias = UNSET if isinstance(self.metric_key_alias, Unset) else self.metric_key_alias

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status_type is not UNSET:
            field_dict["status_type"] = status_type
        if scorer_type is not UNSET:
            field_dict["scorer_type"] = scorer_type
        if metric_key_alias is not UNSET:
            field_dict["metric_key_alias"] = metric_key_alias

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status_type = cast(Literal["pending"] | Unset, d.pop("status_type", UNSET))
        if status_type != "pending" and not isinstance(status_type, Unset):
            raise ValueError(f"status_type must match const 'pending', got '{status_type}'")

        def _parse_scorer_type(data: object) -> None | ScorerType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ScorerType(data)

            except:  # noqa: E722
                pass
            return cast(None | ScorerType | Unset, data)

        scorer_type = _parse_scorer_type(d.pop("scorer_type", UNSET))

        def _parse_metric_key_alias(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        metric_key_alias = _parse_metric_key_alias(d.pop("metric_key_alias", UNSET))

        metric_pending = cls(status_type=status_type, scorer_type=scorer_type, metric_key_alias=metric_key_alias)

        metric_pending.additional_properties = d
        return metric_pending

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
