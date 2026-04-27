from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.evaluate_project_settings_metric_weights_configuration_type_0 import (
        EvaluateProjectSettingsMetricWeightsConfigurationType0,
    )
    from ..models.scorers_config import ScorersConfig


T = TypeVar("T", bound="EvaluateProjectSettings")


@_attrs_define
class EvaluateProjectSettings:
    """
    Attributes:
        scorers_config (None | ScorersConfig | Unset):
        metric_weights_configuration (EvaluateProjectSettingsMetricWeightsConfigurationType0 | None | Unset):
    """

    scorers_config: None | ScorersConfig | Unset = UNSET
    metric_weights_configuration: EvaluateProjectSettingsMetricWeightsConfigurationType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluate_project_settings_metric_weights_configuration_type_0 import (
            EvaluateProjectSettingsMetricWeightsConfigurationType0,
        )
        from ..models.scorers_config import ScorersConfig

        scorers_config: dict[str, Any] | None | Unset
        if isinstance(self.scorers_config, Unset):
            scorers_config = UNSET
        elif isinstance(self.scorers_config, ScorersConfig):
            scorers_config = self.scorers_config.to_dict()
        else:
            scorers_config = self.scorers_config

        metric_weights_configuration: dict[str, Any] | None | Unset
        if isinstance(self.metric_weights_configuration, Unset):
            metric_weights_configuration = UNSET
        elif isinstance(self.metric_weights_configuration, EvaluateProjectSettingsMetricWeightsConfigurationType0):
            metric_weights_configuration = self.metric_weights_configuration.to_dict()
        else:
            metric_weights_configuration = self.metric_weights_configuration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scorers_config is not UNSET:
            field_dict["scorers_config"] = scorers_config
        if metric_weights_configuration is not UNSET:
            field_dict["metric_weights_configuration"] = metric_weights_configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluate_project_settings_metric_weights_configuration_type_0 import (
            EvaluateProjectSettingsMetricWeightsConfigurationType0,
        )
        from ..models.scorers_config import ScorersConfig

        d = dict(src_dict)

        def _parse_scorers_config(data: object) -> None | ScorersConfig | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scorers_config_type_0 = ScorersConfig.from_dict(data)

                return scorers_config_type_0
            except:  # noqa: E722
                pass
            return cast(None | ScorersConfig | Unset, data)

        scorers_config = _parse_scorers_config(d.pop("scorers_config", UNSET))

        def _parse_metric_weights_configuration(
            data: object,
        ) -> EvaluateProjectSettingsMetricWeightsConfigurationType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_weights_configuration_type_0 = EvaluateProjectSettingsMetricWeightsConfigurationType0.from_dict(
                    data
                )

                return metric_weights_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(EvaluateProjectSettingsMetricWeightsConfigurationType0 | None | Unset, data)

        metric_weights_configuration = _parse_metric_weights_configuration(d.pop("metric_weights_configuration", UNSET))

        evaluate_project_settings = cls(
            scorers_config=scorers_config, metric_weights_configuration=metric_weights_configuration
        )

        evaluate_project_settings.additional_properties = d
        return evaluate_project_settings

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
