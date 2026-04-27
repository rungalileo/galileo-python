from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_scorer_version_response import BaseScorerVersionResponse


T = TypeVar("T", bound="ListScorerVersionsResponse")


@_attrs_define
class ListScorerVersionsResponse:
    """
    Attributes:
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.
        paginated (bool | Unset):  Default: False.
        next_starting_token (int | None | Unset):
        versions (list[BaseScorerVersionResponse] | Unset):
    """

    starting_token: int | Unset = 0
    limit: int | Unset = 100
    paginated: bool | Unset = False
    next_starting_token: int | None | Unset = UNSET
    versions: list[BaseScorerVersionResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        starting_token = self.starting_token

        limit = self.limit

        paginated = self.paginated

        next_starting_token: int | None | Unset
        if isinstance(self.next_starting_token, Unset):
            next_starting_token = UNSET
        else:
            next_starting_token = self.next_starting_token

        versions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for versions_item_data in self.versions:
                versions_item = versions_item_data.to_dict()
                versions.append(versions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_scorer_version_response import BaseScorerVersionResponse

        d = dict(src_dict)
        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        paginated = d.pop("paginated", UNSET)

        def _parse_next_starting_token(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        _versions = d.pop("versions", UNSET)
        versions: list[BaseScorerVersionResponse] | Unset = UNSET
        if _versions is not UNSET:
            versions = []
            for versions_item_data in _versions:
                versions_item = BaseScorerVersionResponse.from_dict(versions_item_data)

                versions.append(versions_item)

        list_scorer_versions_response = cls(
            starting_token=starting_token,
            limit=limit,
            paginated=paginated,
            next_starting_token=next_starting_token,
            versions=versions,
        )

        list_scorer_versions_response.additional_properties = d
        return list_scorer_versions_response

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
