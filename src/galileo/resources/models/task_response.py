from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TaskResponse")


@_attrs_define
class TaskResponse:
    """Response for the available task-labels of a multi-label model.

    Attributes:
        project_id (str):
        run_id (str):
        tasks (list[str]):
    """

    project_id: str
    run_id: str
    tasks: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        run_id = self.run_id

        tasks = self.tasks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "run_id": run_id, "tasks": tasks})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        tasks = cast(list[str], d.pop("tasks"))

        task_response = cls(project_id=project_id, run_id=run_id, tasks=tasks)

        task_response.additional_properties = d
        return task_response

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
