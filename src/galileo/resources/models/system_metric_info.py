from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import cast, Union
from typing import Union


T = TypeVar("T", bound="SystemMetricInfo")


@_attrs_define
class SystemMetricInfo:
    """
    Attributes:
        name (str):
        max_ (Union[None, Unset, float]):
        mean (Union[None, Unset, float]):
        median (Union[None, Unset, float]):
        min_ (Union[None, Unset, float]):
        p25 (Union[None, Unset, float]):
        p5 (Union[None, Unset, float]):
        p75 (Union[None, Unset, float]):
        p95 (Union[None, Unset, float]):
        values (Union[Unset, list[float]]):
    """

    name: str
    max_: Union[None, Unset, float] = UNSET
    mean: Union[None, Unset, float] = UNSET
    median: Union[None, Unset, float] = UNSET
    min_: Union[None, Unset, float] = UNSET
    p25: Union[None, Unset, float] = UNSET
    p5: Union[None, Unset, float] = UNSET
    p75: Union[None, Unset, float] = UNSET
    p95: Union[None, Unset, float] = UNSET
    values: Union[Unset, list[float]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        max_: Union[None, Unset, float]
        if isinstance(self.max_, Unset):
            max_ = UNSET
        else:
            max_ = self.max_

        mean: Union[None, Unset, float]
        if isinstance(self.mean, Unset):
            mean = UNSET
        else:
            mean = self.mean

        median: Union[None, Unset, float]
        if isinstance(self.median, Unset):
            median = UNSET
        else:
            median = self.median

        min_: Union[None, Unset, float]
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        p25: Union[None, Unset, float]
        if isinstance(self.p25, Unset):
            p25 = UNSET
        else:
            p25 = self.p25

        p5: Union[None, Unset, float]
        if isinstance(self.p5, Unset):
            p5 = UNSET
        else:
            p5 = self.p5

        p75: Union[None, Unset, float]
        if isinstance(self.p75, Unset):
            p75 = UNSET
        else:
            p75 = self.p75

        p95: Union[None, Unset, float]
        if isinstance(self.p95, Unset):
            p95 = UNSET
        else:
            p95 = self.p95

        values: Union[Unset, list[float]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if max_ is not UNSET:
            field_dict["max"] = max_
        if mean is not UNSET:
            field_dict["mean"] = mean
        if median is not UNSET:
            field_dict["median"] = median
        if min_ is not UNSET:
            field_dict["min"] = min_
        if p25 is not UNSET:
            field_dict["p25"] = p25
        if p5 is not UNSET:
            field_dict["p5"] = p5
        if p75 is not UNSET:
            field_dict["p75"] = p75
        if p95 is not UNSET:
            field_dict["p95"] = p95
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_max_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        max_ = _parse_max_(d.pop("max", UNSET))

        def _parse_mean(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        mean = _parse_mean(d.pop("mean", UNSET))

        def _parse_median(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        median = _parse_median(d.pop("median", UNSET))

        def _parse_min_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_p25(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        p25 = _parse_p25(d.pop("p25", UNSET))

        def _parse_p5(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        p5 = _parse_p5(d.pop("p5", UNSET))

        def _parse_p75(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        p75 = _parse_p75(d.pop("p75", UNSET))

        def _parse_p95(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        p95 = _parse_p95(d.pop("p95", UNSET))

        values = cast(list[float], d.pop("values", UNSET))

        system_metric_info = cls(
            name=name, max_=max_, mean=mean, median=median, min_=min_, p25=p25, p5=p5, p75=p75, p95=p95, values=values
        )

        system_metric_info.additional_properties = d
        return system_metric_info

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
