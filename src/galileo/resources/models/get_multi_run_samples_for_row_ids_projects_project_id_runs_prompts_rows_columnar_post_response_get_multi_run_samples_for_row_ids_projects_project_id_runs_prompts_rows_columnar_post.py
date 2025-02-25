from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_prompt_rows_columnar_response import GetPromptRowsColumnarResponse


T = TypeVar(
    "T",
    bound="GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost",
)


@_attrs_define
class GetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPostResponseGetMultiRunSamplesForRowIdsProjectsProjectIdRunsPromptsRowsColumnarPost:
    """ """

    additional_properties: dict[str, "GetPromptRowsColumnarResponse"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_prompt_rows_columnar_response import GetPromptRowsColumnarResponse

        d = src_dict.copy()
        get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_response_get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetPromptRowsColumnarResponse.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_response_get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post.additional_properties = additional_properties
        return get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post_response_get_multi_run_samples_for_row_ids_projects_project_id_runs_prompts_rows_columnar_post

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetPromptRowsColumnarResponse":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GetPromptRowsColumnarResponse") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
