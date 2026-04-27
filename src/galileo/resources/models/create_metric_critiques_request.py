from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_metric_critique_request import CreateMetricCritiqueRequest
    from ..models.metric_critique_recompute_settings_log_stream import MetricCritiqueRecomputeSettingsLogStream
    from ..models.metric_critique_recompute_settings_observe import MetricCritiqueRecomputeSettingsObserve
    from ..models.recompute_settings_project import RecomputeSettingsProject
    from ..models.recompute_settings_runs import RecomputeSettingsRuns


T = TypeVar("T", bound="CreateMetricCritiquesRequest")


@_attrs_define
class CreateMetricCritiquesRequest:
    """
    Attributes:
        critiques (list[CreateMetricCritiqueRequest]):
        metric (str):
        scorer_id (None | str | Unset):
        recompute_settings (MetricCritiqueRecomputeSettingsLogStream | MetricCritiqueRecomputeSettingsObserve | None |
            RecomputeSettingsProject | RecomputeSettingsRuns | Unset):
    """

    critiques: list[CreateMetricCritiqueRequest]
    metric: str
    scorer_id: None | str | Unset = UNSET
    recompute_settings: (
        MetricCritiqueRecomputeSettingsLogStream
        | MetricCritiqueRecomputeSettingsObserve
        | None
        | RecomputeSettingsProject
        | RecomputeSettingsRuns
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_critique_recompute_settings_log_stream import MetricCritiqueRecomputeSettingsLogStream
        from ..models.metric_critique_recompute_settings_observe import MetricCritiqueRecomputeSettingsObserve
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns

        critiques = []
        for critiques_item_data in self.critiques:
            critiques_item = critiques_item_data.to_dict()
            critiques.append(critiques_item)

        metric = self.metric

        scorer_id: None | str | Unset
        if isinstance(self.scorer_id, Unset):
            scorer_id = UNSET
        else:
            scorer_id = self.scorer_id

        recompute_settings: dict[str, Any] | None | Unset
        if isinstance(self.recompute_settings, Unset):
            recompute_settings = UNSET
        elif isinstance(self.recompute_settings, RecomputeSettingsRuns):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, RecomputeSettingsProject):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, MetricCritiqueRecomputeSettingsObserve):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, MetricCritiqueRecomputeSettingsLogStream):
            recompute_settings = self.recompute_settings.to_dict()
        else:
            recompute_settings = self.recompute_settings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"critiques": critiques, "metric": metric})
        if scorer_id is not UNSET:
            field_dict["scorer_id"] = scorer_id
        if recompute_settings is not UNSET:
            field_dict["recompute_settings"] = recompute_settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_metric_critique_request import CreateMetricCritiqueRequest
        from ..models.metric_critique_recompute_settings_log_stream import MetricCritiqueRecomputeSettingsLogStream
        from ..models.metric_critique_recompute_settings_observe import MetricCritiqueRecomputeSettingsObserve
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns

        d = dict(src_dict)
        critiques = []
        _critiques = d.pop("critiques")
        for critiques_item_data in _critiques:
            critiques_item = CreateMetricCritiqueRequest.from_dict(critiques_item_data)

            critiques.append(critiques_item)

        metric = d.pop("metric")

        def _parse_scorer_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scorer_id = _parse_scorer_id(d.pop("scorer_id", UNSET))

        def _parse_recompute_settings(
            data: object,
        ) -> (
            MetricCritiqueRecomputeSettingsLogStream
            | MetricCritiqueRecomputeSettingsObserve
            | None
            | RecomputeSettingsProject
            | RecomputeSettingsRuns
            | Unset
        ):
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
                recompute_settings_type_0_type_2 = MetricCritiqueRecomputeSettingsObserve.from_dict(data)

                return recompute_settings_type_0_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                recompute_settings_type_0_type_3 = MetricCritiqueRecomputeSettingsLogStream.from_dict(data)

                return recompute_settings_type_0_type_3
            except:  # noqa: E722
                pass
            return cast(
                MetricCritiqueRecomputeSettingsLogStream
                | MetricCritiqueRecomputeSettingsObserve
                | None
                | RecomputeSettingsProject
                | RecomputeSettingsRuns
                | Unset,
                data,
            )

        recompute_settings = _parse_recompute_settings(d.pop("recompute_settings", UNSET))

        create_metric_critiques_request = cls(
            critiques=critiques, metric=metric, scorer_id=scorer_id, recompute_settings=recompute_settings
        )

        create_metric_critiques_request.additional_properties = d
        return create_metric_critiques_request

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
