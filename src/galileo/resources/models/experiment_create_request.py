from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_dataset_request import ExperimentDatasetRequest
    from ..models.prompt_run_settings import PromptRunSettings
    from ..models.scorer_config import ScorerConfig


T = TypeVar("T", bound="ExperimentCreateRequest")


@_attrs_define
class ExperimentCreateRequest:
    """
    Attributes
    ----------
        name (str):
        task_type (Literal[16] | Literal[17] | Unset):  Default: 16.
        playground_id (None | str | Unset):
        prompt_template_version_id (None | str | Unset):
        dataset (ExperimentDatasetRequest | None | Unset):
        playground_prompt_id (None | str | Unset):
        prompt_settings (None | PromptRunSettings | Unset):
        scorers (list[ScorerConfig] | Unset):
        trigger (bool | Unset):  Default: False.
    """

    name: str
    task_type: Literal[16] | Literal[17] | Unset = 16
    playground_id: None | str | Unset = UNSET
    prompt_template_version_id: None | str | Unset = UNSET
    dataset: ExperimentDatasetRequest | None | Unset = UNSET
    playground_prompt_id: None | str | Unset = UNSET
    prompt_settings: None | PromptRunSettings | Unset = UNSET
    scorers: list[ScorerConfig] | Unset = UNSET
    trigger: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.experiment_dataset_request import ExperimentDatasetRequest
        from ..models.prompt_run_settings import PromptRunSettings

        name = self.name

        task_type: Literal[16] | Literal[17] | Unset
        task_type = UNSET if isinstance(self.task_type, Unset) else self.task_type

        playground_id: None | str | Unset
        playground_id = UNSET if isinstance(self.playground_id, Unset) else self.playground_id

        prompt_template_version_id: None | str | Unset
        if isinstance(self.prompt_template_version_id, Unset):
            prompt_template_version_id = UNSET
        else:
            prompt_template_version_id = self.prompt_template_version_id

        dataset: dict[str, Any] | None | Unset
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, ExperimentDatasetRequest):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        playground_prompt_id: None | str | Unset
        playground_prompt_id = UNSET if isinstance(self.playground_prompt_id, Unset) else self.playground_prompt_id

        prompt_settings: dict[str, Any] | None | Unset
        if isinstance(self.prompt_settings, Unset):
            prompt_settings = UNSET
        elif isinstance(self.prompt_settings, PromptRunSettings):
            prompt_settings = self.prompt_settings.to_dict()
        else:
            prompt_settings = self.prompt_settings

        scorers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.scorers, Unset):
            scorers = []
            for scorers_item_data in self.scorers:
                scorers_item = scorers_item_data.to_dict()
                scorers.append(scorers_item)

        trigger = self.trigger

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if task_type is not UNSET:
            field_dict["task_type"] = task_type
        if playground_id is not UNSET:
            field_dict["playground_id"] = playground_id
        if prompt_template_version_id is not UNSET:
            field_dict["prompt_template_version_id"] = prompt_template_version_id
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if playground_prompt_id is not UNSET:
            field_dict["playground_prompt_id"] = playground_prompt_id
        if prompt_settings is not UNSET:
            field_dict["prompt_settings"] = prompt_settings
        if scorers is not UNSET:
            field_dict["scorers"] = scorers
        if trigger is not UNSET:
            field_dict["trigger"] = trigger

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.experiment_dataset_request import ExperimentDatasetRequest
        from ..models.prompt_run_settings import PromptRunSettings
        from ..models.scorer_config import ScorerConfig

        d = dict(src_dict)
        name = d.pop("name")

        def _parse_task_type(data: object) -> Literal[16] | Literal[17] | Unset:
            if isinstance(data, Unset):
                return data
            task_type_type_0 = cast(Literal[16], data)
            if task_type_type_0 != 16:
                raise ValueError(f"task_type_type_0 must match const 16, got '{task_type_type_0}'")
            return task_type_type_0
            task_type_type_1 = cast(Literal[17], data)
            if task_type_type_1 != 17:
                raise ValueError(f"task_type_type_1 must match const 17, got '{task_type_type_1}'")
            return task_type_type_1

        task_type = _parse_task_type(d.pop("task_type", UNSET))

        def _parse_playground_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        playground_id = _parse_playground_id(d.pop("playground_id", UNSET))

        def _parse_prompt_template_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt_template_version_id = _parse_prompt_template_version_id(d.pop("prompt_template_version_id", UNSET))

        def _parse_dataset(data: object) -> ExperimentDatasetRequest | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ExperimentDatasetRequest.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(ExperimentDatasetRequest | None | Unset, data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        def _parse_playground_prompt_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        playground_prompt_id = _parse_playground_prompt_id(d.pop("playground_prompt_id", UNSET))

        def _parse_prompt_settings(data: object) -> None | PromptRunSettings | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return PromptRunSettings.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(None | PromptRunSettings | Unset, data)

        prompt_settings = _parse_prompt_settings(d.pop("prompt_settings", UNSET))

        _scorers = d.pop("scorers", UNSET)
        scorers: list[ScorerConfig] | Unset = UNSET
        if _scorers is not UNSET:
            scorers = []
            for scorers_item_data in _scorers:
                scorers_item = ScorerConfig.from_dict(scorers_item_data)

                scorers.append(scorers_item)

        trigger = d.pop("trigger", UNSET)

        experiment_create_request = cls(
            name=name,
            task_type=task_type,
            playground_id=playground_id,
            prompt_template_version_id=prompt_template_version_id,
            dataset=dataset,
            playground_prompt_id=playground_prompt_id,
            prompt_settings=prompt_settings,
            scorers=scorers,
            trigger=trigger,
        )

        experiment_create_request.additional_properties = d
        return experiment_create_request

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
