from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.query_filter_v1 import QueryFilterV1


T = TypeVar("T", bound="RecomputeSettingsObserve")


@_attrs_define
class RecomputeSettingsObserve:
    """
    Attributes:
        filters (Union[Unset, list['QueryFilterV1']]): The parsed filters that are used to recompute the metric
            critique.
        mode (Union[Literal['observe_filters'], Unset]):  Default: 'observe_filters'.
    """

    filters: Union[Unset, list["QueryFilterV1"]] = UNSET
    mode: Union[Literal["observe_filters"], Unset] = "observe_filters"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        mode = self.mode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.query_filter_v1 import QueryFilterV1

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = QueryFilterV1.from_dict(filters_item_data)

            filters.append(filters_item)

        mode = cast(Union[Literal["observe_filters"], Unset], d.pop("mode", UNSET))
        if mode != "observe_filters" and not isinstance(mode, Unset):
            raise ValueError(f"mode must match const 'observe_filters', got '{mode}'")

        recompute_settings_observe = cls(filters=filters, mode=mode)

        recompute_settings_observe.additional_properties = d
        return recompute_settings_observe

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
