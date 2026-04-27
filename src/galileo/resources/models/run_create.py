from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_tag_create_request import RunTagCreateRequest


T = TypeVar("T", bound="RunCreate")


@_attrs_define
class RunCreate:
    """
    Attributes:
        name (str):
        task_type (int):
        project_id (None | str | Unset):
        created_by (None | str | Unset):
        num_samples (int | None | Unset):
        winner (bool | None | Unset):
        dataset_hash (None | str | Unset):
        dataset_version_id (None | str | Unset):
        run_tags (list[RunTagCreateRequest] | Unset):
    """

    name: str
    task_type: int
    project_id: None | str | Unset = UNSET
    created_by: None | str | Unset = UNSET
    num_samples: int | None | Unset = UNSET
    winner: bool | None | Unset = UNSET
    dataset_hash: None | str | Unset = UNSET
    dataset_version_id: None | str | Unset = UNSET
    run_tags: list[RunTagCreateRequest] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        task_type = self.task_type

        project_id: None | str | Unset
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        created_by: None | str | Unset
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        num_samples: int | None | Unset
        if isinstance(self.num_samples, Unset):
            num_samples = UNSET
        else:
            num_samples = self.num_samples

        winner: bool | None | Unset
        if isinstance(self.winner, Unset):
            winner = UNSET
        else:
            winner = self.winner

        dataset_hash: None | str | Unset
        if isinstance(self.dataset_hash, Unset):
            dataset_hash = UNSET
        else:
            dataset_hash = self.dataset_hash

        dataset_version_id: None | str | Unset
        if isinstance(self.dataset_version_id, Unset):
            dataset_version_id = UNSET
        else:
            dataset_version_id = self.dataset_version_id

        run_tags: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.run_tags, Unset):
            run_tags = []
            for run_tags_item_data in self.run_tags:
                run_tags_item = run_tags_item_data.to_dict()
                run_tags.append(run_tags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "task_type": task_type})
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if winner is not UNSET:
            field_dict["winner"] = winner
        if dataset_hash is not UNSET:
            field_dict["dataset_hash"] = dataset_hash
        if dataset_version_id is not UNSET:
            field_dict["dataset_version_id"] = dataset_version_id
        if run_tags is not UNSET:
            field_dict["run_tags"] = run_tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_tag_create_request import RunTagCreateRequest

        d = dict(src_dict)
        name = d.pop("name")

        task_type = d.pop("task_type")

        def _parse_project_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_created_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_num_samples(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_samples = _parse_num_samples(d.pop("num_samples", UNSET))

        def _parse_winner(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        winner = _parse_winner(d.pop("winner", UNSET))

        def _parse_dataset_hash(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_hash = _parse_dataset_hash(d.pop("dataset_hash", UNSET))

        def _parse_dataset_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        dataset_version_id = _parse_dataset_version_id(d.pop("dataset_version_id", UNSET))

        _run_tags = d.pop("run_tags", UNSET)
        run_tags: list[RunTagCreateRequest] | Unset = UNSET
        if _run_tags is not UNSET:
            run_tags = []
            for run_tags_item_data in _run_tags:
                run_tags_item = RunTagCreateRequest.from_dict(run_tags_item_data)

                run_tags.append(run_tags_item)

        run_create = cls(
            name=name,
            task_type=task_type,
            project_id=project_id,
            created_by=created_by,
            num_samples=num_samples,
            winner=winner,
            dataset_hash=dataset_hash,
            dataset_version_id=dataset_version_id,
            run_tags=run_tags,
        )

        run_create.additional_properties = d
        return run_create

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
