from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.playground_snapshot_dataset import PlaygroundSnapshotDataset
    from ..models.playground_snapshot_scorer import PlaygroundSnapshotScorer
    from ..models.user_info import UserInfo


T = TypeVar("T", bound="PlaygroundSnapshotResponse")


@_attrs_define
class PlaygroundSnapshotResponse:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        experiment_id (str):
        created_by_user (None | UserInfo):
        num_rows (int):
        scorers (list[PlaygroundSnapshotScorer]):
        dataset (None | PlaygroundSnapshotDataset):
    """

    id: str
    created_at: datetime.datetime
    experiment_id: str
    created_by_user: None | UserInfo
    num_rows: int
    scorers: list[PlaygroundSnapshotScorer]
    dataset: None | PlaygroundSnapshotDataset
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.playground_snapshot_dataset import PlaygroundSnapshotDataset
        from ..models.user_info import UserInfo

        id = self.id

        created_at = self.created_at.isoformat()

        experiment_id = self.experiment_id

        created_by_user: dict[str, Any] | None
        if isinstance(self.created_by_user, UserInfo):
            created_by_user = self.created_by_user.to_dict()
        else:
            created_by_user = self.created_by_user

        num_rows = self.num_rows

        scorers = []
        for scorers_item_data in self.scorers:
            scorers_item = scorers_item_data.to_dict()
            scorers.append(scorers_item)

        dataset: dict[str, Any] | None
        if isinstance(self.dataset, PlaygroundSnapshotDataset):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "experiment_id": experiment_id,
                "created_by_user": created_by_user,
                "num_rows": num_rows,
                "scorers": scorers,
                "dataset": dataset,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.playground_snapshot_dataset import PlaygroundSnapshotDataset
        from ..models.playground_snapshot_scorer import PlaygroundSnapshotScorer
        from ..models.user_info import UserInfo

        d = dict(src_dict)
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        experiment_id = d.pop("experiment_id")

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

        num_rows = d.pop("num_rows")

        scorers = []
        _scorers = d.pop("scorers")
        for scorers_item_data in _scorers:
            scorers_item = PlaygroundSnapshotScorer.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        def _parse_dataset(data: object) -> None | PlaygroundSnapshotDataset:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_type_0 = PlaygroundSnapshotDataset.from_dict(data)

                return dataset_type_0
            except:  # noqa: E722
                pass
            return cast(None | PlaygroundSnapshotDataset, data)

        dataset = _parse_dataset(d.pop("dataset"))

        playground_snapshot_response = cls(
            id=id,
            created_at=created_at,
            experiment_id=experiment_id,
            created_by_user=created_by_user,
            num_rows=num_rows,
            scorers=scorers,
            dataset=dataset,
        )

        playground_snapshot_response.additional_properties = d
        return playground_snapshot_response

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
