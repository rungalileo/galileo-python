from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_metric_critique_request import CreateMetricCritiqueRequest
    from ..models.recompute_settings_observe import RecomputeSettingsObserve
    from ..models.recompute_settings_project import RecomputeSettingsProject
    from ..models.recompute_settings_runs import RecomputeSettingsRuns


T = TypeVar("T", bound="CreateMetricCritiquesRequest")


@_attrs_define
class CreateMetricCritiquesRequest:
    """
    Attributes:
        critiques (list['CreateMetricCritiqueRequest']):
        metric (str):
        recompute_settings (Union['RecomputeSettingsObserve', 'RecomputeSettingsProject', 'RecomputeSettingsRuns', None,
            Unset]):
    """

    critiques: list["CreateMetricCritiqueRequest"]
    metric: str
    recompute_settings: Union[
        "RecomputeSettingsObserve", "RecomputeSettingsProject", "RecomputeSettingsRuns", None, Unset
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.recompute_settings_observe import RecomputeSettingsObserve
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns

        critiques = []
        for critiques_item_data in self.critiques:
            critiques_item = critiques_item_data.to_dict()
            critiques.append(critiques_item)

        metric = self.metric

        recompute_settings: Union[None, Unset, dict[str, Any]]
        if isinstance(self.recompute_settings, Unset):
            recompute_settings = UNSET
        elif isinstance(self.recompute_settings, RecomputeSettingsRuns):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, RecomputeSettingsProject):
            recompute_settings = self.recompute_settings.to_dict()
        elif isinstance(self.recompute_settings, RecomputeSettingsObserve):
            recompute_settings = self.recompute_settings.to_dict()
        else:
            recompute_settings = self.recompute_settings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"critiques": critiques, "metric": metric})
        if recompute_settings is not UNSET:
            field_dict["recompute_settings"] = recompute_settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_metric_critique_request import CreateMetricCritiqueRequest
        from ..models.recompute_settings_observe import RecomputeSettingsObserve
        from ..models.recompute_settings_project import RecomputeSettingsProject
        from ..models.recompute_settings_runs import RecomputeSettingsRuns

        d = src_dict.copy()
        critiques = []
        _critiques = d.pop("critiques")
        for critiques_item_data in _critiques:
            critiques_item = CreateMetricCritiqueRequest.from_dict(critiques_item_data)

            critiques.append(critiques_item)

        metric = d.pop("metric")

        def _parse_recompute_settings(
            data: object,
        ) -> Union["RecomputeSettingsObserve", "RecomputeSettingsProject", "RecomputeSettingsRuns", None, Unset]:
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
                recompute_settings_type_0_type_2 = RecomputeSettingsObserve.from_dict(data)

                return recompute_settings_type_0_type_2
            except:  # noqa: E722
                pass
            return cast(
                Union["RecomputeSettingsObserve", "RecomputeSettingsProject", "RecomputeSettingsRuns", None, Unset],
                data,
            )

        recompute_settings = _parse_recompute_settings(d.pop("recompute_settings", UNSET))

        create_metric_critiques_request = cls(critiques=critiques, metric=metric, recompute_settings=recompute_settings)

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
