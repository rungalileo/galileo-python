from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.recompute_settings_log_stream import RecomputeSettingsLogStream
    from ..models.recompute_settings_observe import RecomputeSettingsObserve
    from ..models.recompute_settings_project import RecomputeSettingsProject
    from ..models.recompute_settings_runs import RecomputeSettingsRuns
    from ..models.scorers_config import ScorersConfig


T = TypeVar("T", bound="CreateComputeScoreRequest")


@_attrs_define
class CreateComputeScoreRequest:
    """
    Attributes:
        scorers_config (ScorersConfig):
        recompute_settings (RecomputeSettingsLogStream | RecomputeSettingsObserve | RecomputeSettingsProject |
            RecomputeSettingsRuns):
    """

    scorers_config: ScorersConfig
    recompute_settings: (
        RecomputeSettingsLogStream | RecomputeSettingsObserve | RecomputeSettingsProject | RecomputeSettingsRuns
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.recompute_settings_observe import RecomputeSettingsObserve
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns

        scorers_config = self.scorers_config.to_dict()

        recompute_settings: dict[str, Any]
        if isinstance(self.recompute_settings, RecomputeSettingsRuns):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, RecomputeSettingsProject):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, RecomputeSettingsObserve):
            recompute_settings = self.recompute_settings.to_dict()
        else:
            recompute_settings = self.recompute_settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"scorers_config": scorers_config, "recompute_settings": recompute_settings})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recompute_settings_log_stream import RecomputeSettingsLogStream
        from ..models.recompute_settings_observe import RecomputeSettingsObserve
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns
        from ..models.scorers_config import ScorersConfig

        d = dict(src_dict)
        scorers_config = ScorersConfig.from_dict(d.pop("scorers_config"))

        def _parse_recompute_settings(
            data: object,
        ) -> RecomputeSettingsLogStream | RecomputeSettingsObserve | RecomputeSettingsProject | RecomputeSettingsRuns:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recompute_settings_type_0 = RecomputeSettingsRuns.from_dict(data)

                return recompute_settings_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recompute_settings_type_1 = RecomputeSettingsProject.from_dict(data)

                return recompute_settings_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recompute_settings_type_2 = RecomputeSettingsObserve.from_dict(data)

                return recompute_settings_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            recompute_settings_type_3 = RecomputeSettingsLogStream.from_dict(data)

            return recompute_settings_type_3

        recompute_settings = _parse_recompute_settings(d.pop("recompute_settings"))

        create_compute_score_request = cls(scorers_config=scorers_config, recompute_settings=recompute_settings)

        create_compute_score_request.additional_properties = d
        return create_compute_score_request

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
