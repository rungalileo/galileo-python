from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
    Attributes
    ----------
        label (str): Human-readable display name for the metric
        name (str): Unique identifier for the metric
        histogram (Union['Histogram', None, Unset]): Histogram representation of the metric distribution
        max_ (Union[None, Unset, float]): Maximum value in the metric dataset
        mean (Union[None, Unset, float]): Arithmetic mean of the metric values
        median (Union[None, Unset, float]): Median (50th percentile) of the metric values
        min_ (Union[None, Unset, float]): Minimum value in the metric dataset
        p25 (Union[None, Unset, float]): 25th percentile (first quartile) of the metric values
        p5 (Union[None, Unset, float]): 5th percentile of the metric values
        p75 (Union[None, Unset, float]): 75th percentile (third quartile) of the metric values
        p95 (Union[None, Unset, float]): 95th percentile of the metric values
        unit (Union[DataUnit, None, Unset]): Unit of measurement, if any
        values (Union[Unset, list[float]]): Raw metric values used to compute statistics and histograms.
    """

    label: str
    name: str
    histogram: Union["Histogram", None, Unset] = UNSET
    max_: Union[None, Unset, float] = UNSET
    mean: Union[None, Unset, float] = UNSET
    median: Union[None, Unset, float] = UNSET
    min_: Union[None, Unset, float] = UNSET
    p25: Union[None, Unset, float] = UNSET
    p5: Union[None, Unset, float] = UNSET
    p75: Union[None, Unset, float] = UNSET
    p95: Union[None, Unset, float] = UNSET
    unit: Union[DataUnit, None, Unset] = UNSET
    values: Union[Unset, list[float]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.histogram import Histogram

        label = self.label

        name = self.name

        histogram: Union[None, Unset, dict[str, Any]]
        if isinstance(self.histogram, Unset):
            histogram = UNSET
        elif isinstance(self.histogram, Histogram):
            histogram = self.histogram.to_dict()
        else:
            histogram = self.histogram

        max_: Union[None, Unset, float]
        max_ = UNSET if isinstance(self.max_, Unset) else self.max_

        mean: Union[None, Unset, float]
        mean = UNSET if isinstance(self.mean, Unset) else self.mean

        median: Union[None, Unset, float]
        median = UNSET if isinstance(self.median, Unset) else self.median

        min_: Union[None, Unset, float]
        min_ = UNSET if isinstance(self.min_, Unset) else self.min_

        p25: Union[None, Unset, float]
        p25 = UNSET if isinstance(self.p25, Unset) else self.p25

        p5: Union[None, Unset, float]
        p5 = UNSET if isinstance(self.p5, Unset) else self.p5

        p75: Union[None, Unset, float]
        p75 = UNSET if isinstance(self.p75, Unset) else self.p75

        p95: Union[None, Unset, float]
        p95 = UNSET if isinstance(self.p95, Unset) else self.p95

        unit: Union[None, Unset, str]
        if isinstance(self.unit, Unset):
            unit = UNSET
        elif isinstance(self.unit, DataUnit):
            unit = self.unit.value
        else:
            unit = self.unit

        values: Union[Unset, list[float]] = UNSET
        if not isinstance(self.values, Unset):
            values = self.values

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"label": label, "name": name})
        if histogram is not UNSET:
            field_dict["histogram"] = histogram
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
        if unit is not UNSET:
            field_dict["unit"] = unit
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.histogram import Histogram

        d = dict(src_dict)
        label = d.pop("label")

        name = d.pop("name")

        def _parse_histogram(data: object) -> Union["Histogram", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Histogram.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["Histogram", None, Unset], data)

        histogram = _parse_histogram(d.pop("histogram", UNSET))

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

        def _parse_unit(data: object) -> Union[DataUnit, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return DataUnit(data)

            except:  # noqa: E722
                pass
            return cast(Union[DataUnit, None, Unset], data)

        unit = _parse_unit(d.pop("unit", UNSET))

        values = cast(list[float], d.pop("values", UNSET))

        system_metric_info = cls(
            label=label,
            name=name,
            histogram=histogram,
            max_=max_,
            mean=mean,
            median=median,
            min_=min_,
            p25=p25,
            p5=p5,
            p75=p75,
            p95=p95,
            unit=unit,
            values=values,
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
