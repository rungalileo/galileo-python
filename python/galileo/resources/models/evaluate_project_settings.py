from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        metric_weights_configuration (Union['EvaluateProjectSettingsMetricWeightsConfigurationType0', None, Unset]):
        scorers_config (Union['ScorersConfig', None, Unset]):
    """

    metric_weights_configuration: Union["EvaluateProjectSettingsMetricWeightsConfigurationType0", None, Unset] = UNSET
    scorers_config: Union["ScorersConfig", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluate_project_settings_metric_weights_configuration_type_0 import (
            EvaluateProjectSettingsMetricWeightsConfigurationType0,
        )
        from ..models.scorers_config import ScorersConfig

        metric_weights_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_weights_configuration, Unset):
            metric_weights_configuration = UNSET
        elif isinstance(self.metric_weights_configuration, EvaluateProjectSettingsMetricWeightsConfigurationType0):
            metric_weights_configuration = self.metric_weights_configuration.to_dict()
        else:
            metric_weights_configuration = self.metric_weights_configuration

        scorers_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.scorers_config, Unset):
            scorers_config = UNSET
        elif isinstance(self.scorers_config, ScorersConfig):
            scorers_config = self.scorers_config.to_dict()
        else:
            scorers_config = self.scorers_config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metric_weights_configuration is not UNSET:
            field_dict["metric_weights_configuration"] = metric_weights_configuration
        if scorers_config is not UNSET:
            field_dict["scorers_config"] = scorers_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.evaluate_project_settings_metric_weights_configuration_type_0 import (
            EvaluateProjectSettingsMetricWeightsConfigurationType0,
        )
        from ..models.scorers_config import ScorersConfig

        d = src_dict.copy()

        def _parse_metric_weights_configuration(
            data: object,
        ) -> Union["EvaluateProjectSettingsMetricWeightsConfigurationType0", None, Unset]:
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
            return cast(Union["EvaluateProjectSettingsMetricWeightsConfigurationType0", None, Unset], data)

        metric_weights_configuration = _parse_metric_weights_configuration(d.pop("metric_weights_configuration", UNSET))

        def _parse_scorers_config(data: object) -> Union["ScorersConfig", None, Unset]:
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
            return cast(Union["ScorersConfig", None, Unset], data)

        scorers_config = _parse_scorers_config(d.pop("scorers_config", UNSET))

        evaluate_project_settings = cls(
            metric_weights_configuration=metric_weights_configuration, scorers_config=scorers_config
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
