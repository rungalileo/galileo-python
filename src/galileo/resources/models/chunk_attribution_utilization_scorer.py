from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.chunk_attribution_utilization_scorer_type import ChunkAttributionUtilizationScorerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_filter import MetadataFilter
    from ..models.modality_filter import ModalityFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="ChunkAttributionUtilizationScorer")


@_attrs_define
class ChunkAttributionUtilizationScorer:
    """
    Attributes
    ----------
        name (Literal['chunk_attribution_utilization'] | Unset):  Default: 'chunk_attribution_utilization'.
        filters (list[MetadataFilter | ModalityFilter | NodeNameFilter] | None | Unset): List of filters to apply to the
            scorer.
        type_ (ChunkAttributionUtilizationScorerType | Unset):  Default: ChunkAttributionUtilizationScorerType.LUNA.
        model_name (None | str | Unset): Alias of the model to use for the scorer.
    """

    name: Literal["chunk_attribution_utilization"] | Unset = "chunk_attribution_utilization"
    filters: list[MetadataFilter | ModalityFilter | NodeNameFilter] | None | Unset = UNSET
    type_: ChunkAttributionUtilizationScorerType | Unset = ChunkAttributionUtilizationScorerType.LUNA
    model_name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        name = self.name

        filters: list[dict[str, Any]] | None | Unset
        if isinstance(self.filters, Unset):
            filters = UNSET
        elif isinstance(self.filters, list):
            filters = []
            for filters_type_0_item_data in self.filters:
                filters_type_0_item: dict[str, Any]
                if isinstance(filters_type_0_item_data, NodeNameFilter | MetadataFilter):
                    filters_type_0_item = filters_type_0_item_data.to_dict()
                else:
                    filters_type_0_item = filters_type_0_item_data.to_dict()

                filters.append(filters_type_0_item)

        else:
            filters = self.filters

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        model_name: None | str | Unset
        model_name = UNSET if isinstance(self.model_name, Unset) else self.model_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if filters is not UNSET:
            field_dict["filters"] = filters
        if type_ is not UNSET:
            field_dict["type"] = type_
        if model_name is not UNSET:
            field_dict["model_name"] = model_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_filter import MetadataFilter
        from ..models.modality_filter import ModalityFilter
        from ..models.node_name_filter import NodeNameFilter

        d = dict(src_dict)
        name = cast(Literal["chunk_attribution_utilization"] | Unset, d.pop("name", UNSET))
        if name != "chunk_attribution_utilization" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'chunk_attribution_utilization', got '{name}'")

        def _parse_filters(data: object) -> list[MetadataFilter | ModalityFilter | NodeNameFilter] | None | Unset:
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

                    def _parse_filters_type_0_item(data: object) -> MetadataFilter | ModalityFilter | NodeNameFilter:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return NodeNameFilter.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return MetadataFilter.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return ModalityFilter.from_dict(data)

                    filters_type_0_item = _parse_filters_type_0_item(filters_type_0_item_data)

                    filters_type_0.append(filters_type_0_item)

                return filters_type_0
            except:  # noqa: E722
                pass
            return cast(list[MetadataFilter | ModalityFilter | NodeNameFilter] | None | Unset, data)

        filters = _parse_filters(d.pop("filters", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: ChunkAttributionUtilizationScorerType | Unset
        type_ = UNSET if isinstance(_type_, Unset) else ChunkAttributionUtilizationScorerType(_type_)

        def _parse_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        chunk_attribution_utilization_scorer = cls(name=name, filters=filters, type_=type_, model_name=model_name)

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
