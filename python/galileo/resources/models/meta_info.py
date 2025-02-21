from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MetaInfo")


@_attrs_define
class MetaInfo:
    """Class for describing a metadata column.

    Metadata columns and tabular data columns are similar, but metadata columns

    a meta column is categorical if it is of string/object type with <= 50 unique values a meta column is continuous if
    it is of float/int type

    Thus, a column of string type with > 50 unique values is neither continuous nor categorical in our case.

        Attributes:
            is_categorical (bool):
            is_continuous (bool):
            name (str):
            high_cardinality (Union[None, Unset, bool]):
            max_ (Union[None, Unset, float]):
            mean (Union[None, Unset, float]):
            min_ (Union[None, Unset, float]):
            missing (Union[None, Unset, int]):
            missing_pct (Union[None, Unset, float]):
            negative (Union[None, Unset, int]):
            negative_pct (Union[None, Unset, float]):
            unique_count (Union[None, Unset, int]):
            unique_count_full (Union[None, Unset, int]):
            unique_values (Union[None, Unset, list[Any]]):
            unique_values_full (Union[None, Unset, list[Any]]):
            zeros (Union[None, Unset, int]):
            zeros_pct (Union[None, Unset, float]):
    """

    is_categorical: bool
    is_continuous: bool
    name: str
    high_cardinality: Union[None, Unset, bool] = UNSET
    max_: Union[None, Unset, float] = UNSET
    mean: Union[None, Unset, float] = UNSET
    min_: Union[None, Unset, float] = UNSET
    missing: Union[None, Unset, int] = UNSET
    missing_pct: Union[None, Unset, float] = UNSET
    negative: Union[None, Unset, int] = UNSET
    negative_pct: Union[None, Unset, float] = UNSET
    unique_count: Union[None, Unset, int] = UNSET
    unique_count_full: Union[None, Unset, int] = UNSET
    unique_values: Union[None, Unset, list[Any]] = UNSET
    unique_values_full: Union[None, Unset, list[Any]] = UNSET
    zeros: Union[None, Unset, int] = UNSET
    zeros_pct: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_categorical = self.is_categorical

        is_continuous = self.is_continuous

        name = self.name

        high_cardinality: Union[None, Unset, bool]
        if isinstance(self.high_cardinality, Unset):
            high_cardinality = UNSET
        else:
            high_cardinality = self.high_cardinality

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

        min_: Union[None, Unset, float]
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        missing: Union[None, Unset, int]
        if isinstance(self.missing, Unset):
            missing = UNSET
        else:
            missing = self.missing

        missing_pct: Union[None, Unset, float]
        if isinstance(self.missing_pct, Unset):
            missing_pct = UNSET
        else:
            missing_pct = self.missing_pct

        negative: Union[None, Unset, int]
        if isinstance(self.negative, Unset):
            negative = UNSET
        else:
            negative = self.negative

        negative_pct: Union[None, Unset, float]
        if isinstance(self.negative_pct, Unset):
            negative_pct = UNSET
        else:
            negative_pct = self.negative_pct

        unique_count: Union[None, Unset, int]
        if isinstance(self.unique_count, Unset):
            unique_count = UNSET
        else:
            unique_count = self.unique_count

        unique_count_full: Union[None, Unset, int]
        if isinstance(self.unique_count_full, Unset):
            unique_count_full = UNSET
        else:
            unique_count_full = self.unique_count_full

        unique_values: Union[None, Unset, list[Any]]
        if isinstance(self.unique_values, Unset):
            unique_values = UNSET
        elif isinstance(self.unique_values, list):
            unique_values = self.unique_values

        else:
            unique_values = self.unique_values

        unique_values_full: Union[None, Unset, list[Any]]
        if isinstance(self.unique_values_full, Unset):
            unique_values_full = UNSET
        elif isinstance(self.unique_values_full, list):
            unique_values_full = self.unique_values_full

        else:
            unique_values_full = self.unique_values_full

        zeros: Union[None, Unset, int]
        if isinstance(self.zeros, Unset):
            zeros = UNSET
        else:
            zeros = self.zeros

        zeros_pct: Union[None, Unset, float]
        if isinstance(self.zeros_pct, Unset):
            zeros_pct = UNSET
        else:
            zeros_pct = self.zeros_pct

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"is_categorical": is_categorical, "is_continuous": is_continuous, "name": name})
        if high_cardinality is not UNSET:
            field_dict["high_cardinality"] = high_cardinality
        if max_ is not UNSET:
            field_dict["max"] = max_
        if mean is not UNSET:
            field_dict["mean"] = mean
        if min_ is not UNSET:
            field_dict["min"] = min_
        if missing is not UNSET:
            field_dict["missing"] = missing
        if missing_pct is not UNSET:
            field_dict["missing_pct"] = missing_pct
        if negative is not UNSET:
            field_dict["negative"] = negative
        if negative_pct is not UNSET:
            field_dict["negative_pct"] = negative_pct
        if unique_count is not UNSET:
            field_dict["unique_count"] = unique_count
        if unique_count_full is not UNSET:
            field_dict["unique_count_full"] = unique_count_full
        if unique_values is not UNSET:
            field_dict["unique_values"] = unique_values
        if unique_values_full is not UNSET:
            field_dict["unique_values_full"] = unique_values_full
        if zeros is not UNSET:
            field_dict["zeros"] = zeros
        if zeros_pct is not UNSET:
            field_dict["zeros_pct"] = zeros_pct

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        is_categorical = d.pop("is_categorical")

        is_continuous = d.pop("is_continuous")

        name = d.pop("name")

        def _parse_high_cardinality(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        high_cardinality = _parse_high_cardinality(d.pop("high_cardinality", UNSET))

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

        def _parse_min_(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        min_ = _parse_min_(d.pop("min", UNSET))

        def _parse_missing(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        missing = _parse_missing(d.pop("missing", UNSET))

        def _parse_missing_pct(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        missing_pct = _parse_missing_pct(d.pop("missing_pct", UNSET))

        def _parse_negative(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        negative = _parse_negative(d.pop("negative", UNSET))

        def _parse_negative_pct(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        negative_pct = _parse_negative_pct(d.pop("negative_pct", UNSET))

        def _parse_unique_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        unique_count = _parse_unique_count(d.pop("unique_count", UNSET))

        def _parse_unique_count_full(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        unique_count_full = _parse_unique_count_full(d.pop("unique_count_full", UNSET))

        def _parse_unique_values(data: object) -> Union[None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                unique_values_type_0 = cast(list[Any], data)

                return unique_values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Any]], data)

        unique_values = _parse_unique_values(d.pop("unique_values", UNSET))

        def _parse_unique_values_full(data: object) -> Union[None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                unique_values_full_type_0 = cast(list[Any], data)

                return unique_values_full_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Any]], data)

        unique_values_full = _parse_unique_values_full(d.pop("unique_values_full", UNSET))

        def _parse_zeros(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        zeros = _parse_zeros(d.pop("zeros", UNSET))

        def _parse_zeros_pct(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        zeros_pct = _parse_zeros_pct(d.pop("zeros_pct", UNSET))

        meta_info = cls(
            is_categorical=is_categorical,
            is_continuous=is_continuous,
            name=name,
            high_cardinality=high_cardinality,
            max_=max_,
            mean=mean,
            min_=min_,
            missing=missing,
            missing_pct=missing_pct,
            negative=negative,
            negative_pct=negative_pct,
            unique_count=unique_count,
            unique_count_full=unique_count_full,
            unique_values=unique_values,
            unique_values_full=unique_values_full,
            zeros=zeros,
            zeros_pct=zeros_pct,
        )

        meta_info.additional_properties = d
        return meta_info

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
