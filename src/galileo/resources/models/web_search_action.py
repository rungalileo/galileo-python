from collections.abc import Mapping
from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WebSearchAction")


@_attrs_define
class WebSearchAction:
    """Action payload for a web search call event.

    Attributes
    ----------
        type_ (Literal['search']): Type of web search action
        query (Union[None, Unset, str]): Search query string
        sources (Union[Any, None, Unset]): Optional provider-specific sources
    """

    type_: Literal["search"]
    query: Union[None, Unset, str] = UNSET
    sources: Union[Any, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        query: Union[None, Unset, str]
        query = UNSET if isinstance(self.query, Unset) else self.query

        sources: Union[Any, None, Unset]
        sources = UNSET if isinstance(self.sources, Unset) else self.sources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"type": type_})
        if query is not UNSET:
            field_dict["query"] = query
        if sources is not UNSET:
            field_dict["sources"] = sources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = cast(Literal["search"], d.pop("type"))
        if type_ != "search":
            raise ValueError(f"type must match const 'search', got '{type_}'")

        def _parse_query(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        query = _parse_query(d.pop("query", UNSET))

        def _parse_sources(data: object) -> Union[Any, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[Any, None, Unset], data)

        sources = _parse_sources(d.pop("sources", UNSET))

        web_search_action = cls(type_=type_, query=query, sources=sources)

        web_search_action.additional_properties = d
        return web_search_action

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
