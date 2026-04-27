from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.categorical_prompt_filter_param import CategoricalPromptFilterParam
    from ..models.range_prompt_filter_param import RangePromptFilterParam
    from ..models.value_prompt_filter_param import ValuePromptFilterParam


T = TypeVar("T", bound="PromptFilterParams")


@_attrs_define
class PromptFilterParams:
    """
    Attributes:
        filters (list[CategoricalPromptFilterParam | RangePromptFilterParam | ValuePromptFilterParam] | Unset): A list
            of filters.
    """

    filters: list[CategoricalPromptFilterParam | RangePromptFilterParam | ValuePromptFilterParam] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.range_prompt_filter_param import RangePromptFilterParam
        from ..models.value_prompt_filter_param import ValuePromptFilterParam

        filters: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(filters_item_data, RangePromptFilterParam):
                    filters_item = filters_item_data.to_dict()
                elif isinstance(filters_item_data, ValuePromptFilterParam):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.categorical_prompt_filter_param import CategoricalPromptFilterParam
        from ..models.range_prompt_filter_param import RangePromptFilterParam
        from ..models.value_prompt_filter_param import ValuePromptFilterParam

        d = dict(src_dict)
        _filters = d.pop("filters", UNSET)
        filters: list[CategoricalPromptFilterParam | RangePromptFilterParam | ValuePromptFilterParam] | Unset = UNSET
        if _filters is not UNSET:
            filters = []
            for filters_item_data in _filters:

                def _parse_filters_item(
                    data: object,
                ) -> CategoricalPromptFilterParam | RangePromptFilterParam | ValuePromptFilterParam:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_0 = RangePromptFilterParam.from_dict(data)

                        return filters_item_type_0
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_item_type_1 = ValuePromptFilterParam.from_dict(data)

                        return filters_item_type_1
                    except:  # noqa: E722
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    filters_item_type_2 = CategoricalPromptFilterParam.from_dict(data)

                    return filters_item_type_2

                filters_item = _parse_filters_item(filters_item_data)

                filters.append(filters_item)

        prompt_filter_params = cls(filters=filters)

        prompt_filter_params.additional_properties = d
        return prompt_filter_params

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
