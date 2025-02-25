from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alerts_configuration import AlertsConfiguration
    from ..models.customized_scorer import CustomizedScorer
    from ..models.generated_scorer_config import GeneratedScorerConfig
    from ..models.registered_scorer import RegisteredScorer
    from ..models.scorers_config import ScorersConfig
    from ..models.scorers_configuration import ScorersConfiguration


T = TypeVar("T", bound="ObserveProjectSettings")


@_attrs_define
class ObserveProjectSettings:
    """
    Attributes:
        alerts_configuration (Union['AlertsConfiguration', None, Unset]):
        customized_scorers_configuration (Union[None, Unset, list['CustomizedScorer']]):
        generated_scorers_configuration (Union[None, Unset, list['GeneratedScorerConfig']]):
        registered_scorers_configuration (Union[None, Unset, list['RegisteredScorer']]):
        scorers_config (Union['ScorersConfig', None, Unset]):
        scorers_configuration (Union['ScorersConfiguration', None, Unset]):
    """

    alerts_configuration: Union["AlertsConfiguration", None, Unset] = UNSET
    customized_scorers_configuration: Union[None, Unset, list["CustomizedScorer"]] = UNSET
    generated_scorers_configuration: Union[None, Unset, list["GeneratedScorerConfig"]] = UNSET
    registered_scorers_configuration: Union[None, Unset, list["RegisteredScorer"]] = UNSET
    scorers_config: Union["ScorersConfig", None, Unset] = UNSET
    scorers_configuration: Union["ScorersConfiguration", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.alerts_configuration import AlertsConfiguration
        from ..models.scorers_config import ScorersConfig
        from ..models.scorers_configuration import ScorersConfiguration

        alerts_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.alerts_configuration, Unset):
            alerts_configuration = UNSET
        elif isinstance(self.alerts_configuration, AlertsConfiguration):
            alerts_configuration = self.alerts_configuration.to_dict()
        else:
            alerts_configuration = self.alerts_configuration

        customized_scorers_configuration: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.customized_scorers_configuration, Unset):
            customized_scorers_configuration = UNSET
        elif isinstance(self.customized_scorers_configuration, list):
            customized_scorers_configuration = []
            for customized_scorers_configuration_type_0_item_data in self.customized_scorers_configuration:
                customized_scorers_configuration_type_0_item = (
                    customized_scorers_configuration_type_0_item_data.to_dict()
                )
                customized_scorers_configuration.append(customized_scorers_configuration_type_0_item)

        else:
            customized_scorers_configuration = self.customized_scorers_configuration

        generated_scorers_configuration: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.generated_scorers_configuration, Unset):
            generated_scorers_configuration = UNSET
        elif isinstance(self.generated_scorers_configuration, list):
            generated_scorers_configuration = []
            for generated_scorers_configuration_type_0_item_data in self.generated_scorers_configuration:
                generated_scorers_configuration_type_0_item = generated_scorers_configuration_type_0_item_data.to_dict()
                generated_scorers_configuration.append(generated_scorers_configuration_type_0_item)

        else:
            generated_scorers_configuration = self.generated_scorers_configuration

        registered_scorers_configuration: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.registered_scorers_configuration, Unset):
            registered_scorers_configuration = UNSET
        elif isinstance(self.registered_scorers_configuration, list):
            registered_scorers_configuration = []
            for registered_scorers_configuration_type_0_item_data in self.registered_scorers_configuration:
                registered_scorers_configuration_type_0_item = (
                    registered_scorers_configuration_type_0_item_data.to_dict()
                )
                registered_scorers_configuration.append(registered_scorers_configuration_type_0_item)

        else:
            registered_scorers_configuration = self.registered_scorers_configuration

        scorers_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.scorers_config, Unset):
            scorers_config = UNSET
        elif isinstance(self.scorers_config, ScorersConfig):
            scorers_config = self.scorers_config.to_dict()
        else:
            scorers_config = self.scorers_config

        scorers_configuration: Union[None, Unset, dict[str, Any]]
        if isinstance(self.scorers_configuration, Unset):
            scorers_configuration = UNSET
        elif isinstance(self.scorers_configuration, ScorersConfiguration):
            scorers_configuration = self.scorers_configuration.to_dict()
        else:
            scorers_configuration = self.scorers_configuration

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if alerts_configuration is not UNSET:
            field_dict["alerts_configuration"] = alerts_configuration
        if customized_scorers_configuration is not UNSET:
            field_dict["customized_scorers_configuration"] = customized_scorers_configuration
        if generated_scorers_configuration is not UNSET:
            field_dict["generated_scorers_configuration"] = generated_scorers_configuration
        if registered_scorers_configuration is not UNSET:
            field_dict["registered_scorers_configuration"] = registered_scorers_configuration
        if scorers_config is not UNSET:
            field_dict["scorers_config"] = scorers_config
        if scorers_configuration is not UNSET:
            field_dict["scorers_configuration"] = scorers_configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.alerts_configuration import AlertsConfiguration
        from ..models.customized_scorer import CustomizedScorer
        from ..models.generated_scorer_config import GeneratedScorerConfig
        from ..models.registered_scorer import RegisteredScorer
        from ..models.scorers_config import ScorersConfig
        from ..models.scorers_configuration import ScorersConfiguration

        d = src_dict.copy()

        def _parse_alerts_configuration(data: object) -> Union["AlertsConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                alerts_configuration_type_0 = AlertsConfiguration.from_dict(data)

                return alerts_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AlertsConfiguration", None, Unset], data)

        alerts_configuration = _parse_alerts_configuration(d.pop("alerts_configuration", UNSET))

        def _parse_customized_scorers_configuration(data: object) -> Union[None, Unset, list["CustomizedScorer"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                customized_scorers_configuration_type_0 = []
                _customized_scorers_configuration_type_0 = data
                for customized_scorers_configuration_type_0_item_data in _customized_scorers_configuration_type_0:
                    customized_scorers_configuration_type_0_item = CustomizedScorer.from_dict(
                        customized_scorers_configuration_type_0_item_data
                    )

                    customized_scorers_configuration_type_0.append(customized_scorers_configuration_type_0_item)

                return customized_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["CustomizedScorer"]], data)

        customized_scorers_configuration = _parse_customized_scorers_configuration(
            d.pop("customized_scorers_configuration", UNSET)
        )

        def _parse_generated_scorers_configuration(data: object) -> Union[None, Unset, list["GeneratedScorerConfig"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                generated_scorers_configuration_type_0 = []
                _generated_scorers_configuration_type_0 = data
                for generated_scorers_configuration_type_0_item_data in _generated_scorers_configuration_type_0:
                    generated_scorers_configuration_type_0_item = GeneratedScorerConfig.from_dict(
                        generated_scorers_configuration_type_0_item_data
                    )

                    generated_scorers_configuration_type_0.append(generated_scorers_configuration_type_0_item)

                return generated_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["GeneratedScorerConfig"]], data)

        generated_scorers_configuration = _parse_generated_scorers_configuration(
            d.pop("generated_scorers_configuration", UNSET)
        )

        def _parse_registered_scorers_configuration(data: object) -> Union[None, Unset, list["RegisteredScorer"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                registered_scorers_configuration_type_0 = []
                _registered_scorers_configuration_type_0 = data
                for registered_scorers_configuration_type_0_item_data in _registered_scorers_configuration_type_0:
                    registered_scorers_configuration_type_0_item = RegisteredScorer.from_dict(
                        registered_scorers_configuration_type_0_item_data
                    )

                    registered_scorers_configuration_type_0.append(registered_scorers_configuration_type_0_item)

                return registered_scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["RegisteredScorer"]], data)

        registered_scorers_configuration = _parse_registered_scorers_configuration(
            d.pop("registered_scorers_configuration", UNSET)
        )

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

        def _parse_scorers_configuration(data: object) -> Union["ScorersConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scorers_configuration_type_0 = ScorersConfiguration.from_dict(data)

                return scorers_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ScorersConfiguration", None, Unset], data)

        scorers_configuration = _parse_scorers_configuration(d.pop("scorers_configuration", UNSET))

        observe_project_settings = cls(
            alerts_configuration=alerts_configuration,
            customized_scorers_configuration=customized_scorers_configuration,
            generated_scorers_configuration=generated_scorers_configuration,
            registered_scorers_configuration=registered_scorers_configuration,
            scorers_config=scorers_config,
            scorers_configuration=scorers_configuration,
        )

        observe_project_settings.additional_properties = d
        return observe_project_settings

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
