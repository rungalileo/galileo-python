from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.output_type_enum import OutputTypeEnum
from ..models.roll_up_method_display_options import RollUpMethodDisplayOptions
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.bucketed_metric_buckets import BucketedMetricBuckets


T = TypeVar("T", bound="BucketedMetric")


@_attrs_define
class BucketedMetric:
    """
    Attributes
    ----------
        name (str):
        buckets (BucketedMetricBuckets):
        average (Union[None, Unset, float]):
        roll_up_method (Union[None, RollUpMethodDisplayOptions, Unset]):
        data_type (Union[None, OutputTypeEnum, Unset]):
    """

    name: str
    buckets: "BucketedMetricBuckets"
    average: None | Unset | float = UNSET
    roll_up_method: None | RollUpMethodDisplayOptions | Unset = UNSET
    data_type: None | OutputTypeEnum | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        buckets = self.buckets.to_dict()

        average: None | Unset | float
        average = UNSET if isinstance(self.average, Unset) else self.average

        roll_up_method: None | Unset | str
        if isinstance(self.roll_up_method, Unset):
            roll_up_method = UNSET
        elif isinstance(self.roll_up_method, RollUpMethodDisplayOptions):
            roll_up_method = self.roll_up_method.value
        else:
            roll_up_method = self.roll_up_method

        data_type: None | Unset | str
        if isinstance(self.data_type, Unset):
            data_type = UNSET
        elif isinstance(self.data_type, OutputTypeEnum):
            data_type = self.data_type.value
        else:
            data_type = self.data_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "buckets": buckets})
        if average is not UNSET:
            field_dict["average"] = average
        if roll_up_method is not UNSET:
            field_dict["roll_up_method"] = roll_up_method
        if data_type is not UNSET:
            field_dict["data_type"] = data_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bucketed_metric_buckets import BucketedMetricBuckets

        d = dict(src_dict)
        name = d.pop("name")

        buckets = BucketedMetricBuckets.from_dict(d.pop("buckets"))

        def _parse_average(data: object) -> None | Unset | float:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | float, data)

        average = _parse_average(d.pop("average", UNSET))

        def _parse_roll_up_method(data: object) -> None | RollUpMethodDisplayOptions | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return RollUpMethodDisplayOptions(data)

            except:  # noqa: E722
                pass
            return cast(None | RollUpMethodDisplayOptions | Unset, data)

        roll_up_method = _parse_roll_up_method(d.pop("roll_up_method", UNSET))

        def _parse_data_type(data: object) -> None | OutputTypeEnum | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return OutputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(None | OutputTypeEnum | Unset, data)

        data_type = _parse_data_type(d.pop("data_type", UNSET))

        bucketed_metric = cls(
            name=name, buckets=buckets, average=average, roll_up_method=roll_up_method, data_type=data_type
        )

        bucketed_metric.additional_properties = d
        return bucketed_metric

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
