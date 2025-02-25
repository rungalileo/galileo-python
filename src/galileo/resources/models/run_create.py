from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        created_by (Union[None, Unset, str]):
        dataset_hash (Union[None, Unset, str]):
        num_samples (Union[None, Unset, int]):
        project_id (Union[None, Unset, str]):
        run_tags (Union[Unset, list['RunTagCreateRequest']]):
        winner (Union[None, Unset, bool]):
    """

    name: str
    task_type: int
    created_by: Union[None, Unset, str] = UNSET
    dataset_hash: Union[None, Unset, str] = UNSET
    num_samples: Union[None, Unset, int] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    run_tags: Union[Unset, list["RunTagCreateRequest"]] = UNSET
    winner: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        task_type = self.task_type

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        dataset_hash: Union[None, Unset, str]
        if isinstance(self.dataset_hash, Unset):
            dataset_hash = UNSET
        else:
            dataset_hash = self.dataset_hash

        num_samples: Union[None, Unset, int]
        if isinstance(self.num_samples, Unset):
            num_samples = UNSET
        else:
            num_samples = self.num_samples

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

        winner: Union[None, Unset, bool]
        if isinstance(self.winner, Unset):
            winner = UNSET
        else:
            winner = self.winner

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "task_type": task_type})
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if dataset_hash is not UNSET:
            field_dict["dataset_hash"] = dataset_hash
        if num_samples is not UNSET:
            field_dict["num_samples"] = num_samples
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if run_tags is not UNSET:
            field_dict["run_tags"] = run_tags
        if winner is not UNSET:
            field_dict["winner"] = winner

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.run_tag_create_request import RunTagCreateRequest

        d = src_dict.copy()
        name = d.pop("name")

        task_type = d.pop("task_type")

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_dataset_hash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_hash = _parse_dataset_hash(d.pop("dataset_hash", UNSET))

        def _parse_num_samples(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_samples = _parse_num_samples(d.pop("num_samples", UNSET))

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
            run_tags_item = RunTagCreateRequest.from_dict(run_tags_item_data)

            run_tags.append(run_tags_item)

        def _parse_winner(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        winner = _parse_winner(d.pop("winner", UNSET))

        run_create = cls(
            name=name,
            task_type=task_type,
            created_by=created_by,
            dataset_hash=dataset_hash,
            num_samples=num_samples,
            project_id=project_id,
            run_tags=run_tags,
            winner=winner,
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
