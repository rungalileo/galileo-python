from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.recompute_settings_observe_base import RecomputeSettingsObserveBase
    from ..models.recompute_settings_project import RecomputeSettingsProject
    from ..models.recompute_settings_runs import RecomputeSettingsRuns


T = TypeVar("T", bound="MetricCritiqueJobConfiguration")


@_attrs_define
class MetricCritiqueJobConfiguration:
    """Info necessary to execute a metric critique job.

    Attributes:
        critique_ids (list[str]):
        metric_name (str):
        project_type (Union[Literal['llm_monitor'], Literal['prompt_evaluation']]):
        llm_settings (Union[Unset, PromptRunSettings]): Prompt run settings.
        recompute_settings (Union['RecomputeSettingsObserveBase', 'RecomputeSettingsProject', 'RecomputeSettingsRuns',
            None, Unset]):
    """

    critique_ids: list[str]
    metric_name: str
    project_type: Union[Literal["llm_monitor"], Literal["prompt_evaluation"]]
    llm_settings: Union[Unset, "PromptRunSettings"] = UNSET
    recompute_settings: Union[
        "RecomputeSettingsObserveBase", "RecomputeSettingsProject", "RecomputeSettingsRuns", None, Unset
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.recompute_settings_observe_base import RecomputeSettingsObserveBase
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns

        critique_ids = self.critique_ids

        metric_name = self.metric_name

        project_type: Union[Literal["llm_monitor"], Literal["prompt_evaluation"]]
        project_type = self.project_type

        llm_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.llm_settings, Unset):
            llm_settings = self.llm_settings.to_dict()

        recompute_settings: Union[None, Unset, dict[str, Any]]
        if isinstance(self.recompute_settings, Unset):
            recompute_settings = UNSET
        elif isinstance(self.recompute_settings, RecomputeSettingsRuns):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, RecomputeSettingsProject):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, RecomputeSettingsObserveBase):
            recompute_settings = self.recompute_settings.to_dict()
        else:
            recompute_settings = self.recompute_settings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"critique_ids": critique_ids, "metric_name": metric_name, "project_type": project_type})
        if llm_settings is not UNSET:
            field_dict["llm_settings"] = llm_settings
        if recompute_settings is not UNSET:
            field_dict["recompute_settings"] = recompute_settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.recompute_settings_observe_base import RecomputeSettingsObserveBase
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns

        d = src_dict.copy()
        critique_ids = cast(list[str], d.pop("critique_ids"))

        metric_name = d.pop("metric_name")

        def _parse_project_type(data: object) -> Union[Literal["llm_monitor"], Literal["prompt_evaluation"]]:
            project_type_type_0 = cast(Literal["prompt_evaluation"], data)
            if project_type_type_0 != "prompt_evaluation":
                raise ValueError(
                    f"project_type_type_0 must match const 'prompt_evaluation', got '{project_type_type_0}'"
                )
            return project_type_type_0
            project_type_type_1 = cast(Literal["llm_monitor"], data)
            if project_type_type_1 != "llm_monitor":
                raise ValueError(f"project_type_type_1 must match const 'llm_monitor', got '{project_type_type_1}'")
            return project_type_type_1

        project_type = _parse_project_type(d.pop("project_type"))

        _llm_settings = d.pop("llm_settings", UNSET)
        llm_settings: Union[Unset, PromptRunSettings]
        if isinstance(_llm_settings, Unset):
            llm_settings = UNSET
        else:
            llm_settings = PromptRunSettings.from_dict(_llm_settings)

        def _parse_recompute_settings(
            data: object,
        ) -> Union["RecomputeSettingsObserveBase", "RecomputeSettingsProject", "RecomputeSettingsRuns", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recompute_settings_type_0_type_0 = RecomputeSettingsRuns.from_dict(data)

                return recompute_settings_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recompute_settings_type_0_type_1 = RecomputeSettingsProject.from_dict(data)

                return recompute_settings_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recompute_settings_type_0_type_2 = RecomputeSettingsObserveBase.from_dict(data)

                return recompute_settings_type_0_type_2
            except:  # noqa: E722
                pass
            return cast(
                Union["RecomputeSettingsObserveBase", "RecomputeSettingsProject", "RecomputeSettingsRuns", None, Unset],
                data,
            )

        recompute_settings = _parse_recompute_settings(d.pop("recompute_settings", UNSET))

        metric_critique_job_configuration = cls(
            critique_ids=critique_ids,
            metric_name=metric_name,
            project_type=project_type,
            llm_settings=llm_settings,
            recompute_settings=recompute_settings,
        )

        metric_critique_job_configuration.additional_properties = d
        return metric_critique_job_configuration

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
