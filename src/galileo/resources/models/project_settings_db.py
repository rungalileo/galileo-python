from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alerts_configuration import AlertsConfiguration
    from ..models.customized_scorer import CustomizedScorer
    from ..models.generated_scorer_config import GeneratedScorerConfig
    from ..models.project_settings_db_metric_weights_configuration_type_0 import (
        ProjectSettingsDBMetricWeightsConfigurationType0,
    )
    from ..models.registered_scorer import RegisteredScorer
    from ..models.scorers_config import ScorersConfig
    from ..models.scorers_configuration import ScorersConfiguration


T = TypeVar("T", bound="ProjectSettingsDB")


@_attrs_define
class ProjectSettingsDB:
    """
    Attributes:
        project_id (str):
        id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        scorers_config (None | ScorersConfig | Unset):
        metric_weights_configuration (None | ProjectSettingsDBMetricWeightsConfigurationType0 | Unset):
        alerts_configuration (AlertsConfiguration | None | Unset):
        scorers_configuration (None | ScorersConfiguration | Unset):
        registered_scorers_configuration (list[RegisteredScorer] | None | Unset):
        generated_scorers_configuration (list[GeneratedScorerConfig] | None | Unset):
        customized_scorers_configuration (list[CustomizedScorer] | None | Unset):
    """

    project_id: str
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    scorers_config: None | ScorersConfig | Unset = UNSET
    metric_weights_configuration: None | ProjectSettingsDBMetricWeightsConfigurationType0 | Unset = UNSET
    alerts_configuration: AlertsConfiguration | None | Unset = UNSET
    scorers_configuration: None | ScorersConfiguration | Unset = UNSET
    registered_scorers_configuration: list[RegisteredScorer] | None | Unset = UNSET
    generated_scorers_configuration: list[GeneratedScorerConfig] | None | Unset = UNSET
    customized_scorers_configuration: list[CustomizedScorer] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.alerts_configuration import AlertsConfiguration
        from ..models.project_settings_db_metric_weights_configuration_type_0 import (
            ProjectSettingsDBMetricWeightsConfigurationType0,
        )
        from ..models.scorers_config import ScorersConfig
        from ..models.scorers_configuration import ScorersConfiguration

        project_id = self.project_id

        id = self.id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

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
        elif isinstance(self.metric_weights_configuration, ProjectSettingsDBMetricWeightsConfigurationType0):
            metric_weights_configuration = self.metric_weights_configuration.to_dict()
        else:
            metric_weights_configuration = self.metric_weights_configuration

        alerts_configuration: dict[str, Any] | None | Unset
        if isinstance(self.alerts_configuration, Unset):
            alerts_configuration = UNSET
        elif isinstance(self.alerts_configuration, AlertsConfiguration):
            alerts_configuration = self.alerts_configuration.to_dict()
        else:
            alerts_configuration = self.alerts_configuration

        scorers_configuration: dict[str, Any] | None | Unset
        if isinstance(self.scorers_configuration, Unset):
            scorers_configuration = UNSET
        elif isinstance(self.scorers_configuration, ScorersConfiguration):
            scorers_configuration = self.scorers_configuration.to_dict()
        else:
            scorers_configuration = self.scorers_configuration

        registered_scorers_configuration: list[dict[str, Any]] | None | Unset
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

        generated_scorers_configuration: list[dict[str, Any]] | None | Unset
        if isinstance(self.generated_scorers_configuration, Unset):
            generated_scorers_configuration = UNSET
        elif isinstance(self.generated_scorers_configuration, list):
            generated_scorers_configuration = []
            for generated_scorers_configuration_type_0_item_data in self.generated_scorers_configuration:
                generated_scorers_configuration_type_0_item = generated_scorers_configuration_type_0_item_data.to_dict()
                generated_scorers_configuration.append(generated_scorers_configuration_type_0_item)

        else:
            generated_scorers_configuration = self.generated_scorers_configuration

        customized_scorers_configuration: list[dict[str, Any]] | None | Unset
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "id": id, "created_at": created_at, "updated_at": updated_at})
        if scorers_config is not UNSET:
            field_dict["scorers_config"] = scorers_config
        if metric_weights_configuration is not UNSET:
            field_dict["metric_weights_configuration"] = metric_weights_configuration
        if alerts_configuration is not UNSET:
            field_dict["alerts_configuration"] = alerts_configuration
        if scorers_configuration is not UNSET:
            field_dict["scorers_configuration"] = scorers_configuration
        if registered_scorers_configuration is not UNSET:
            field_dict["registered_scorers_configuration"] = registered_scorers_configuration
        if generated_scorers_configuration is not UNSET:
            field_dict["generated_scorers_configuration"] = generated_scorers_configuration
        if customized_scorers_configuration is not UNSET:
            field_dict["customized_scorers_configuration"] = customized_scorers_configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.alerts_configuration import AlertsConfiguration
        from ..models.customized_scorer import CustomizedScorer
        from ..models.generated_scorer_config import GeneratedScorerConfig
        from ..models.project_settings_db_metric_weights_configuration_type_0 import (
            ProjectSettingsDBMetricWeightsConfigurationType0,
        )
        from ..models.registered_scorer import RegisteredScorer
        from ..models.scorers_config import ScorersConfig
        from ..models.scorers_configuration import ScorersConfiguration

        d = dict(src_dict)
        project_id = d.pop("project_id")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

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
        ) -> None | ProjectSettingsDBMetricWeightsConfigurationType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_weights_configuration_type_0 = ProjectSettingsDBMetricWeightsConfigurationType0.from_dict(data)

                return metric_weights_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(None | ProjectSettingsDBMetricWeightsConfigurationType0 | Unset, data)

        metric_weights_configuration = _parse_metric_weights_configuration(d.pop("metric_weights_configuration", UNSET))

        def _parse_alerts_configuration(data: object) -> AlertsConfiguration | None | Unset:
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
            return cast(AlertsConfiguration | None | Unset, data)

        alerts_configuration = _parse_alerts_configuration(d.pop("alerts_configuration", UNSET))

        def _parse_scorers_configuration(data: object) -> None | ScorersConfiguration | Unset:
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
            return cast(None | ScorersConfiguration | Unset, data)

        scorers_configuration = _parse_scorers_configuration(d.pop("scorers_configuration", UNSET))

        def _parse_registered_scorers_configuration(data: object) -> list[RegisteredScorer] | None | Unset:
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
            return cast(list[RegisteredScorer] | None | Unset, data)

        registered_scorers_configuration = _parse_registered_scorers_configuration(
            d.pop("registered_scorers_configuration", UNSET)
        )

        def _parse_generated_scorers_configuration(data: object) -> list[GeneratedScorerConfig] | None | Unset:
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
            return cast(list[GeneratedScorerConfig] | None | Unset, data)

        generated_scorers_configuration = _parse_generated_scorers_configuration(
            d.pop("generated_scorers_configuration", UNSET)
        )

        def _parse_customized_scorers_configuration(data: object) -> list[CustomizedScorer] | None | Unset:
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
            return cast(list[CustomizedScorer] | None | Unset, data)

        customized_scorers_configuration = _parse_customized_scorers_configuration(
            d.pop("customized_scorers_configuration", UNSET)
        )

        project_settings_db = cls(
            project_id=project_id,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            scorers_config=scorers_config,
            metric_weights_configuration=metric_weights_configuration,
            alerts_configuration=alerts_configuration,
            scorers_configuration=scorers_configuration,
            registered_scorers_configuration=registered_scorers_configuration,
            generated_scorers_configuration=generated_scorers_configuration,
            customized_scorers_configuration=customized_scorers_configuration,
        )

        project_settings_db.additional_properties = d
        return project_settings_db

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
