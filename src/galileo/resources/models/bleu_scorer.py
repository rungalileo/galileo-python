from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metadata_filter import MetadataFilter
    from ..models.modality_filter import ModalityFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="BleuScorer")


@_attrs_define
class BleuScorer:
    """
    Attributes
    ----------
        name (Literal['bleu'] | Unset):  Default: 'bleu'.
        filters (list[MetadataFilter | ModalityFilter | NodeNameFilter] | None | Unset): List of filters to apply to the
            scorer.
    """

    name: Literal["bleu"] | Unset = "bleu"
    filters: list[MetadataFilter | ModalityFilter | NodeNameFilter] | None | Unset = UNSET
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metadata_filter import MetadataFilter
        from ..models.modality_filter import ModalityFilter
        from ..models.node_name_filter import NodeNameFilter

        d = dict(src_dict)
        name = cast(Literal["bleu"] | Unset, d.pop("name", UNSET))
        if name != "bleu" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'bleu', got '{name}'")

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

        bleu_scorer = cls(name=name, filters=filters)

        bleu_scorer.additional_properties = d
        return bleu_scorer

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
