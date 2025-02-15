import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.task_type import TaskType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.run_tag_db import RunTagDB


T = TypeVar("T", bound="CreateRunResponse")


@_attrs_define
class CreateRunResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        id (str):
        last_updated_by (str):
        num_samples (int):
        updated_at (datetime.datetime):
        winner (bool):
        dataset_hash (Union[None, Unset, str]):
        name (Union[None, Unset, str]):
        project_id (Union[None, Unset, str]):
        run_tags (Union[Unset, list['RunTagDB']]):
        task_type (Union[None, TaskType, Unset]):
    """

    created_at: datetime.datetime
    created_by: str
    id: str
    last_updated_by: str
    num_samples: int
    updated_at: datetime.datetime
    winner: bool
    dataset_hash: Union[None, Unset, str] = UNSET
    name: Union[None, Unset, str] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    run_tags: Union[Unset, list["RunTagDB"]] = UNSET
    task_type: Union[None, TaskType, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        id = self.id

        last_updated_by = self.last_updated_by

        num_samples = self.num_samples

        updated_at = self.updated_at.isoformat()

        winner = self.winner

        dataset_hash: Union[None, Unset, str]
        if isinstance(self.dataset_hash, Unset):
            dataset_hash = UNSET
        else:
            dataset_hash = self.dataset_hash

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        run_tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.run_tags, Unset):
            run_tags = []
            for run_tags_item_data in self.run_tags:
                run_tags_item = run_tags_item_data.to_dict()
                run_tags.append(run_tags_item)

        task_type: Union[None, Unset, int]
        if isinstance(self.task_type, Unset):
            task_type = UNSET
        elif isinstance(self.task_type, TaskType):
            task_type = self.task_type.value
        else:
            task_type = self.task_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "id": id,
                "last_updated_by": last_updated_by,
                "num_samples": num_samples,
                "updated_at": updated_at,
                "winner": winner,
            }
        )
        if dataset_hash is not UNSET:
            field_dict["dataset_hash"] = dataset_hash
        if name is not UNSET:
            field_dict["name"] = name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if run_tags is not UNSET:
            field_dict["run_tags"] = run_tags
        if task_type is not UNSET:
            field_dict["task_type"] = task_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.run_tag_db import RunTagDB

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        id = d.pop("id")

        last_updated_by = d.pop("last_updated_by")

        num_samples = d.pop("num_samples")

        updated_at = isoparse(d.pop("updated_at"))

        winner = d.pop("winner")

        def _parse_dataset_hash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_hash = _parse_dataset_hash(d.pop("dataset_hash", UNSET))

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

        run_tags = []
        _run_tags = d.pop("run_tags", UNSET)
        for run_tags_item_data in _run_tags or []:
            run_tags_item = RunTagDB.from_dict(run_tags_item_data)

            run_tags.append(run_tags_item)

        def _parse_task_type(data: object) -> Union[None, TaskType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, int):
                    raise TypeError()
                task_type_type_0 = TaskType(data)

                return task_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, TaskType, Unset], data)

        task_type = _parse_task_type(d.pop("task_type", UNSET))

        create_run_response = cls(
            created_at=created_at,
            created_by=created_by,
            id=id,
            last_updated_by=last_updated_by,
            num_samples=num_samples,
            updated_at=updated_at,
            winner=winner,
            dataset_hash=dataset_hash,
            name=name,
            project_id=project_id,
            run_tags=run_tags,
            task_type=task_type,
        )

        create_run_response.additional_properties = d
        return create_run_response

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
