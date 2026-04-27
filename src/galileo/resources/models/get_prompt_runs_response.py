from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_prompt_run import GetPromptRun


T = TypeVar("T", bound="GetPromptRunsResponse")


@_attrs_define
class GetPromptRunsResponse:
    """
    Attributes:
        starting_token (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.
        paginated (bool | Unset):  Default: False.
        next_starting_token (int | None | Unset):
        runs (list[GetPromptRun] | Unset):
    """

    starting_token: int | Unset = 0
    limit: int | Unset = 100
    paginated: bool | Unset = False
    next_starting_token: int | None | Unset = UNSET
    runs: list[GetPromptRun] | Unset = UNSET
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

        runs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.runs, Unset):
            runs = []
            for runs_item_data in self.runs:
                runs_item = runs_item_data.to_dict()
                runs.append(runs_item)

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
        if runs is not UNSET:
            field_dict["runs"] = runs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.get_prompt_run import GetPromptRun

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

        _runs = d.pop("runs", UNSET)
        runs: list[GetPromptRun] | Unset = UNSET
        if _runs is not UNSET:
            runs = []
            for runs_item_data in _runs:
                runs_item = GetPromptRun.from_dict(runs_item_data)

                runs.append(runs_item)

        get_prompt_runs_response = cls(
            starting_token=starting_token,
            limit=limit,
            paginated=paginated,
            next_starting_token=next_starting_token,
            runs=runs,
        )

        get_prompt_runs_response.additional_properties = d
        return get_prompt_runs_response

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
