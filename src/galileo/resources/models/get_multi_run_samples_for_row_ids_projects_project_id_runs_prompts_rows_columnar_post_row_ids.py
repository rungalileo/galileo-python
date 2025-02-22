from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds")


@_attrs_define
class GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostRowIds:
    """ """

    additional_properties: dict[str, int] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_row_ids = cls()

        get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_row_ids.additional_properties = d
        return get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_row_ids

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> int:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: int) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
