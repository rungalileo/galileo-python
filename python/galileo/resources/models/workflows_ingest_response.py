from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="WorkflowsIngestResponse")


@_attrs_define
class WorkflowsIngestResponse:
    """
    Attributes:
        message (str):
        project_id (str):
        project_name (str):
        records_count (int):
        workflows_count (int):
    """

    message: str
    project_id: str
    project_name: str
    records_count: int
    workflows_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        message = self.message

        project_id = self.project_id

        project_name = self.project_name

        records_count = self.records_count

        workflows_count = self.workflows_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
                "project_id": project_id,
                "project_name": project_name,
                "records_count": records_count,
                "workflows_count": workflows_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        records_count = d.pop("records_count")

        workflows_count = d.pop("workflows_count")

        workflows_ingest_response = cls(
            message=message,
            project_id=project_id,
            project_name=project_name,
            records_count=records_count,
            workflows_count=workflows_count,
        )

        workflows_ingest_response.additional_properties = d
        return workflows_ingest_response

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
