from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.playground_dataset import PlaygroundDataset
    from ..models.scorer_config import ScorerConfig
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="PlaygroundResponse")


@_attrs_define
class PlaygroundResponse:
    """
    Attributes:
        id (str):
        name (str):
        created_by_user (None | UserInfo):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        dataset (None | PlaygroundDataset):
        scratch_dataset_id (str):
        scorers (list[ScorerConfig] | None):
    """

    id: str
    name: str
    created_by_user: None | UserInfo
    created_at: datetime.datetime
    updated_at: datetime.datetime
    dataset: None | PlaygroundDataset
    scratch_dataset_id: str
    scorers: list[ScorerConfig] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.playground_dataset import PlaygroundDataset
        from ..models.user_info import UserInfo

        id = self.id

        name = self.name

        created_by_user: dict[str, Any] | None
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        dataset: dict[str, Any] | None
        if isinstance(self.dataset, PlaygroundDataset):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        scratch_dataset_id = self.scratch_dataset_id

        scorers: list[dict[str, Any]] | None
        if isinstance(self.scorers, list):
            scorers = []
            for scorers_type_0_item_data in self.scorers:
                scorers_type_0_item = scorers_type_0_item_data.to_dict()
                scorers.append(scorers_type_0_item)

        else:
            scorers = self.scorers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "created_by_user": created_by_user,
                "created_at": created_at,
                "updated_at": updated_at,
                "dataset": dataset,
                "scratch_dataset_id": scratch_dataset_id,
                "scorers": scorers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.playground_dataset import PlaygroundDataset
        from ..models.scorer_config import ScorerConfig
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        def _parse_created_by_user(data: object) -> None | UserInfo:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                created_by_user_type_0 = UserInfo.from_dict(data)

                return created_by_user_type_0
            except:  # noqa: E722
                pass
            return cast(None | UserInfo, data)

        created_by_user = _parse_created_by_user(d.pop("created_by_user"))

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_dataset(data: object) -> None | PlaygroundDataset:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_type_0 = PlaygroundDataset.from_dict(data)

                return dataset_type_0
            except:  # noqa: E722
                pass
            return cast(None | PlaygroundDataset, data)

        dataset = _parse_dataset(d.pop("dataset"))

        scratch_dataset_id = d.pop("scratch_dataset_id")

        def _parse_scorers(data: object) -> list[ScorerConfig] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scorers_type_0 = []
                _scorers_type_0 = data
                for scorers_type_0_item_data in _scorers_type_0:
                    scorers_type_0_item = ScorerConfig.from_dict(scorers_type_0_item_data)

                    scorers_type_0.append(scorers_type_0_item)

                return scorers_type_0
            except:  # noqa: E722
                pass
            return cast(list[ScorerConfig] | None, data)

        scorers = _parse_scorers(d.pop("scorers"))

        playground_response = cls(
            id=id,
            name=name,
            created_by_user=created_by_user,
            created_at=created_at,
            updated_at=updated_at,
            dataset=dataset,
            scratch_dataset_id=scratch_dataset_id,
            scorers=scorers,
        )

        playground_response.additional_properties = d
        return playground_response

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
