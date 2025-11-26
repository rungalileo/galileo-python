import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_type import TaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_tag_db import RunTagDB
    from ..models.user_db import UserDB


T = TypeVar("T", bound="RunDB")


@_attrs_define
class RunDB:
    """
    Attributes
    ----------
        created_by (str):
        num_samples (int):
        winner (bool):
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        last_updated_by (str):
        creator (UserDB):
        logged_splits (list[str]):
        logged_inference_names (list[str]):
        name (Union[None, Unset, str]):
        project_id (Union[None, Unset, str]):
        dataset_hash (Union[None, Unset, str]):
        dataset_version_id (Union[None, Unset, str]):
        task_type (Union[None, TaskType, Unset]):
        run_tags (Union[Unset, list['RunTagDB']]):
        example_content_id (Union[None, Unset, str]):
    """

    created_by: str
    num_samples: int
    winner: bool
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    last_updated_by: str
    creator: "UserDB"
    logged_splits: list[str]
    logged_inference_names: list[str]
    name: Union[None, Unset, str] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    dataset_hash: Union[None, Unset, str] = UNSET
    dataset_version_id: Union[None, Unset, str] = UNSET
    task_type: Union[None, TaskType, Unset] = UNSET
    run_tags: Union[Unset, list["RunTagDB"]] = UNSET
    example_content_id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_by = self.created_by

        num_samples = self.num_samples

        winner = self.winner

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        last_updated_by = self.last_updated_by

        creator = self.creator.to_dict()

        logged_splits = self.logged_splits

        logged_inference_names = self.logged_inference_names

        name: Union[None, Unset, str]
        name = UNSET if isinstance(self.name, Unset) else self.name

        project_id: Union[None, Unset, str]
        project_id = UNSET if isinstance(self.project_id, Unset) else self.project_id

        dataset_hash: Union[None, Unset, str]
        dataset_hash = UNSET if isinstance(self.dataset_hash, Unset) else self.dataset_hash

        dataset_version_id: Union[None, Unset, str]
        dataset_version_id = UNSET if isinstance(self.dataset_version_id, Unset) else self.dataset_version_id

        task_type: Union[None, Unset, int]
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        elif isinstance(self.task_type, TaskType):
            task_type = self.task_type.value
        else:
            task_type = self.task_type

        run_tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.run_tags, Unset):
            run_tags = []
            for run_tags_item_data in self.run_tags:
                run_tags_item = run_tags_item_data.to_dict()
                run_tags.append(run_tags_item)

        example_content_id: Union[None, Unset, str]
        example_content_id = UNSET if isinstance(self.example_content_id, Unset) else self.example_content_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_by": created_by,
                "num_samples": num_samples,
                "winner": winner,
                "id": id,
                "created_at": created_at,
                "updated_at": updated_at,
                "last_updated_by": last_updated_by,
                "creator": creator,
                "logged_splits": logged_splits,
                "logged_inference_names": logged_inference_names,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if dataset_hash is not UNSET:
            field_dict["dataset_hash"] = dataset_hash
        if dataset_version_id is not UNSET:
            field_dict["dataset_version_id"] = dataset_version_id
        if task_type is not UNSET:
            field_dict["task_type"] = task_type
        if run_tags is not UNSET:
            field_dict["run_tags"] = run_tags
        if example_content_id is not UNSET:
            field_dict["example_content_id"] = example_content_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_tag_db import RunTagDB
        from ..models.user_db import UserDB

        d = dict(src_dict)
        created_by = d.pop("created_by")

        num_samples = d.pop("num_samples")

        winner = d.pop("winner")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        last_updated_by = d.pop("last_updated_by")

        creator = UserDB.from_dict(d.pop("creator"))

        logged_splits = cast(list[str], d.pop("logged_splits"))

        logged_inference_names = cast(list[str], d.pop("logged_inference_names"))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_dataset_hash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_hash = _parse_dataset_hash(d.pop("dataset_hash", UNSET))

        def _parse_dataset_version_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_version_id = _parse_dataset_version_id(d.pop("dataset_version_id", UNSET))

        def _parse_task_type(data: object) -> Union[None, TaskType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                return TaskType(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, TaskType, Unset], data)

        task_type = _parse_task_type(d.pop("task_type", UNSET))

        run_tags = []
        _run_tags = d.pop("run_tags", UNSET)
        for run_tags_item_data in _run_tags or []:
            run_tags_item = RunTagDB.from_dict(run_tags_item_data)

            run_tags.append(run_tags_item)

        def _parse_example_content_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        example_content_id = _parse_example_content_id(d.pop("example_content_id", UNSET))

        run_db = cls(
            created_by=created_by,
            num_samples=num_samples,
            winner=winner,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            last_updated_by=last_updated_by,
            creator=creator,
            logged_splits=logged_splits,
            logged_inference_names=logged_inference_names,
            name=name,
            project_id=project_id,
            dataset_hash=dataset_hash,
            dataset_version_id=dataset_version_id,
            task_type=task_type,
            run_tags=run_tags,
            example_content_id=example_content_id,
        )

        run_db.additional_properties = d
        return run_db

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
