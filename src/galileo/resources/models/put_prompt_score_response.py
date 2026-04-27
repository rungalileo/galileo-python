from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PutPromptScoreResponse")


@_attrs_define
class PutPromptScoreResponse:
    """
    Attributes:
        project_id (str):
        run_id (str):
        job_id (str):
        scorer_name (str):
    """

    project_id: str
    run_id: str
    job_id: str
    scorer_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        run_id = self.run_id

        job_id = self.job_id

        scorer_name = self.scorer_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "run_id": run_id, "job_id": job_id, "scorer_name": scorer_name})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        job_id = d.pop("job_id")

        scorer_name = d.pop("scorer_name")

        put_prompt_score_response = cls(project_id=project_id, run_id=run_id, job_id=job_id, scorer_name=scorer_name)

        put_prompt_score_response.additional_properties = d
        return put_prompt_score_response

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
