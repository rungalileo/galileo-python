from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_unit import DataUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.histogram import Histogram


T = TypeVar("T", bound="SystemMetricInfo")


@_attrs_define
class SystemMetricInfo:
    """
    Attributes:
        name (str): Unique identifier for the metric
        label (str): Human-readable display name for the metric
        unit (DataUnit | None | Unset): Unit of measurement, if any
        values (list[float] | Unset): Raw metric values used to compute statistics and histograms
        mean (float | None | Unset): Arithmetic mean of the metric values
        median (float | None | Unset): Median (50th percentile) of the metric values
        p5 (float | None | Unset): 5th percentile of the metric values
        p25 (float | None | Unset): 25th percentile (first quartile) of the metric values
        p75 (float | None | Unset): 75th percentile (third quartile) of the metric values
        p95 (float | None | Unset): 95th percentile of the metric values
        min_ (float | None | Unset): Minimum value in the metric dataset
        max_ (float | None | Unset): Maximum value in the metric dataset
        histogram (Histogram | None | Unset): Histogram representation of the metric distribution
    """

    name: str
    label: str
    unit: DataUnit | None | Unset = UNSET
    values: list[float] | Unset = UNSET
    mean: float | None | Unset = UNSET
    median: float | None | Unset = UNSET
    p5: float | None | Unset = UNSET
    p25: float | None | Unset = UNSET
    p75: float | None | Unset = UNSET
    p95: float | None | Unset = UNSET
    min_: float | None | Unset = UNSET
    max_: float | None | Unset = UNSET
    histogram: Histogram | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.histogram import Histogram

        name = self.name

        label = self.label

        unit: None | str | Unset
        if isinstance(self.unit, Unset):
            unit = UNSET
        elif isinstance(self.unit, DataUnit):
            unit = self.unit.value
        else:
            unit = self.unit

        values: list[float] | Unset = UNSET
        if not isinstance(self.values, Unset):
            values = self.values

        mean: float | None | Unset
        if isinstance(self.mean, Unset):
            mean = UNSET
        else:
            mean = self.mean

        median: float | None | Unset
        if isinstance(self.median, Unset):
            median = UNSET
        else:
            median = self.median

        p5: float | None | Unset
        if isinstance(self.p5, Unset):
            p5 = UNSET
        else:
            p5 = self.p5

        p25: float | None | Unset
        if isinstance(self.p25, Unset):
            p25 = UNSET
        else:
            p25 = self.p25

        p75: float | None | Unset
        if isinstance(self.p75, Unset):
            p75 = UNSET
        else:
            p75 = self.p75

        p95: float | None | Unset
        if isinstance(self.p95, Unset):
            p95 = UNSET
        else:
            p95 = self.p95

        min_: float | None | Unset
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        max_: float | None | Unset
        if isinstance(self.max_, Unset):
            max_ = UNSET
        else:
            max_ = self.max_

        histogram: dict[str, Any] | None | Unset
        if isinstance(self.histogram, Unset):
            histogram = UNSET
        elif isinstance(self.histogram, Histogram):
            histogram = self.histogram.to_dict()
        else:
            histogram = self.histogram

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "label": label})
        if unit is not UNSET:
            field_dict["unit"] = unit
        if values is not UNSET:
            field_dict["values"] = values
        if mean is not UNSET:
            field_dict["mean"] = mean
        if median is not UNSET:
            field_dict["median"] = median
        if p5 is not UNSET:
            field_dict["p5"] = p5
        if p25 is not UNSET:
            field_dict["p25"] = p25
        if p75 is not UNSET:
            field_dict["p75"] = p75
        if p95 is not UNSET:
            field_dict["p95"] = p95
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if histogram is not UNSET:
            field_dict["histogram"] = histogram

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.histogram import Histogram

        d = dict(src_dict)
        name = d.pop("name")

        label = d.pop("label")

        def _parse_unit(data: object) -> DataUnit | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                unit_type_0 = DataUnit(data)

                return unit_type_0
            except:  # noqa: E722
                pass
            return cast(DataUnit | None | Unset, data)

        unit = _parse_unit(d.pop("unit", UNSET))

        values = cast(list[float], d.pop("values", UNSET))

        def _parse_mean(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        mean = _parse_mean(d.pop("mean", UNSET))

        def _parse_median(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        median = _parse_median(d.pop("median", UNSET))

        def _parse_p5(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p5 = _parse_p5(d.pop("p5", UNSET))

        def _parse_p25(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p25 = _parse_p25(d.pop("p25", UNSET))

        def _parse_p75(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p75 = _parse_p75(d.pop("p75", UNSET))

        def _parse_p95(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        p95 = _parse_p95(d.pop("p95", UNSET))

        def _parse_min_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_max_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_ = _parse_max_(d.pop("max", UNSET))

        def _parse_histogram(data: object) -> Histogram | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                histogram_type_0 = Histogram.from_dict(data)

                return histogram_type_0
            except:  # noqa: E722
                pass
            return cast(Histogram | None | Unset, data)

        histogram = _parse_histogram(d.pop("histogram", UNSET))

        system_metric_info = cls(
            name=name,
            label=label,
            unit=unit,
            values=values,
            mean=mean,
            median=median,
            p5=p5,
            p25=p25,
            p75=p75,
            p95=p95,
            min_=min_,
            max_=max_,
            histogram=histogram,
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
