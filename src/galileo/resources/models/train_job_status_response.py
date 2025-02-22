from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrainJobStatusResponse")


@_attrs_define
class TrainJobStatusResponse:
    """
    Attributes:
        history (list[Any]):
        id (str):
        status (str):
        status_message (str):
        project_id (Union[None, Unset, str]):
        project_name (Union[None, Unset, str]):
        run_id (Union[None, Unset, str]):
        run_name (Union[None, Unset, str]):
    """

    history: list[Any]
    id: str
    status: str
    status_message: str
    project_id: Union[None, Unset, str] = UNSET
    project_name: Union[None, Unset, str] = UNSET
    run_id: Union[None, Unset, str] = UNSET
    run_name: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        history = self.history

        id = self.id

        status = self.status

        status_message = self.status_message

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        project_name: Union[None, Unset, str]
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        run_id: Union[None, Unset, str]
        if isinstance(self.run_id, Unset):
            run_id = UNSET
        else:
            run_id = self.run_id

        run_name: Union[None, Unset, str]
        if isinstance(self.run_name, Unset):
            run_name = UNSET
        else:
            run_name = self.run_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"history": history, "id": id, "status": status, "status_message": status_message})
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if run_name is not UNSET:
            field_dict["run_name"] = run_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        history = cast(list[Any], d.pop("history"))

        id = d.pop("id")

        status = d.pop("status")

        status_message = d.pop("status_message")

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_project_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        def _parse_run_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        run_id = _parse_run_id(d.pop("run_id", UNSET))

        def _parse_run_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        run_name = _parse_run_name(d.pop("run_name", UNSET))

        train_job_status_response = cls(
            history=history,
            id=id,
            status=status,
            status_message=status_message,
            project_id=project_id,
            project_name=project_name,
            run_id=run_id,
            run_name=run_name,
        )

        train_job_status_response.additional_properties = d
        return train_job_status_response

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
