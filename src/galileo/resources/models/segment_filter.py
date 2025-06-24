from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_filter import MetadataFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="SegmentFilter")


@_attrs_define
class SegmentFilter:
    """
    Attributes:
        sample_rate (float): The fraction of the data to sample. Must be between 0 and 1, inclusive.
        filter_ (Union['MetadataFilter', 'NodeNameFilter', None, Unset]): Filter to apply to the segment. By default
            sample on all data.
        llm_scorers (Union[Unset, bool]): Whether to sample only on LLM scorers. Default: False.
    """

    sample_rate: float
    filter_: Union["MetadataFilter", "NodeNameFilter", None, Unset] = UNSET
    llm_scorers: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        sample_rate = self.sample_rate

        filter_: Union[None, Unset, dict[str, Any]]
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, NodeNameFilter):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, MetadataFilter):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_

        llm_scorers = self.llm_scorers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"sample_rate": sample_rate})
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if llm_scorers is not UNSET:
            field_dict["llm_scorers"] = llm_scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        d = dict(src_dict)
        sample_rate = d.pop("sample_rate")

        def _parse_filter_(data: object) -> Union["MetadataFilter", "NodeNameFilter", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0_type_0 = NodeNameFilter.from_dict(data)

                return filter_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0_type_1 = MetadataFilter.from_dict(data)

                return filter_type_0_type_1
            except:  # noqa: E722
                pass
            return cast(Union["MetadataFilter", "NodeNameFilter", None, Unset], data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        llm_scorers = d.pop("llm_scorers", UNSET)

        segment_filter = cls(sample_rate=sample_rate, filter_=filter_, llm_scorers=llm_scorers)

        segment_filter.additional_properties = d
        return segment_filter

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
