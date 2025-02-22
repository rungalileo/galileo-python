from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chunk_attribution_utilization_scorer_type import ChunkAttributionUtilizationScorerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_filter import MetadataFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="ChunkAttributionUtilizationScorer")


@_attrs_define
class ChunkAttributionUtilizationScorer:
    """
    Attributes:
        filters (Union[None, Unset, list[Union['MetadataFilter', 'NodeNameFilter']]]): List of filters to apply to the
            scorer.
        model_name (Union[None, Unset, str]): Alias of the model to use for the scorer.
        name (Union[Literal['chunk_attribution_utilization'], Unset]):  Default: 'chunk_attribution_utilization'.
        type_ (Union[Unset, ChunkAttributionUtilizationScorerType]):  Default:
            ChunkAttributionUtilizationScorerType.LUNA.
    """

    filters: Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]] = UNSET
    model_name: Union[None, Unset, str] = UNSET
    name: Union[Literal["chunk_attribution_utilization"], Unset] = "chunk_attribution_utilization"
    type_: Union[Unset, ChunkAttributionUtilizationScorerType] = ChunkAttributionUtilizationScorerType.LUNA
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.node_name_filter import NodeNameFilter

        filters: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.filters, Unset):
            filters = UNSET
        elif isinstance(self.filters, list):
            filters = []
            for filters_type_0_item_data in self.filters:
                filters_type_0_item: dict[str, Any]
                if isinstance(filters_type_0_item_data, NodeNameFilter):
                    filters_type_0_item = filters_type_0_item_data.to_dict()
                else:
                    filters_type_0_item = filters_type_0_item_data.to_dict()

                filters.append(filters_type_0_item)

        else:
            filters = self.filters

        model_name: Union[None, Unset, str]
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        name = self.name

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        d = src_dict.copy()

        def _parse_filters(data: object) -> Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filters_type_0 = []
                _filters_type_0 = data
                for filters_type_0_item_data in _filters_type_0:

                    def _parse_filters_type_0_item(data: object) -> Union["MetadataFilter", "NodeNameFilter"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            filters_type_0_item_type_0 = NodeNameFilter.from_dict(data)

                            return filters_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_type_0_item_type_1 = MetadataFilter.from_dict(data)

                        return filters_type_0_item_type_1

                    filters_type_0_item = _parse_filters_type_0_item(filters_type_0_item_data)

                    filters_type_0.append(filters_type_0_item)

                return filters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]], data)

        filters = _parse_filters(d.pop("filters", UNSET))

        def _parse_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        name = cast(Union[Literal["chunk_attribution_utilization"], Unset], d.pop("name", UNSET))
        if name != "chunk_attribution_utilization" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'chunk_attribution_utilization', got '{name}'")

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, ChunkAttributionUtilizationScorerType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ChunkAttributionUtilizationScorerType(_type_)

        chunk_attribution_utilization_scorer = cls(filters=filters, model_name=model_name, name=name, type_=type_)

        chunk_attribution_utilization_scorer.additional_properties = d
        return chunk_attribution_utilization_scorer

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
