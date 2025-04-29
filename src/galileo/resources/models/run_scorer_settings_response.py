from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scorer_config import ScorerConfig
    from ..models.segment_filter import SegmentFilter


T = TypeVar("T", bound="RunScorerSettingsResponse")


@_attrs_define
class RunScorerSettingsResponse:
    """
    Attributes:
        run_id (str): ID of the run.
        scorers (list['ScorerConfig']):
        segment_filters (Union[None, Unset, list['SegmentFilter']]): List of segment filters to apply to the run.
    """

    run_id: str
    scorers: list["ScorerConfig"]
    segment_filters: Union[None, Unset, list["SegmentFilter"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        scorers = []
        for scorers_item_data in self.scorers:
            scorers_item = scorers_item_data.to_dict()
            scorers.append(scorers_item)

        segment_filters: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.segment_filters, Unset):
            segment_filters = UNSET
        elif isinstance(self.segment_filters, list):
            segment_filters = []
            for segment_filters_type_0_item_data in self.segment_filters:
                segment_filters_type_0_item = segment_filters_type_0_item_data.to_dict()
                segment_filters.append(segment_filters_type_0_item)

        else:
            segment_filters = self.segment_filters

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"run_id": run_id, "scorers": scorers})
        if segment_filters is not UNSET:
            field_dict["segment_filters"] = segment_filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.scorer_config import ScorerConfig
        from ..models.segment_filter import SegmentFilter

        d = src_dict.copy()
        run_id = d.pop("run_id")

        scorers = []
        _scorers = d.pop("scorers")
        for scorers_item_data in _scorers:
            scorers_item = ScorerConfig.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        def _parse_segment_filters(data: object) -> Union[None, Unset, list["SegmentFilter"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                segment_filters_type_0 = []
                _segment_filters_type_0 = data
                for segment_filters_type_0_item_data in _segment_filters_type_0:
                    segment_filters_type_0_item = SegmentFilter.from_dict(segment_filters_type_0_item_data)

                    segment_filters_type_0.append(segment_filters_type_0_item)

                return segment_filters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["SegmentFilter"]], data)

        segment_filters = _parse_segment_filters(d.pop("segment_filters", UNSET))

        run_scorer_settings_response = cls(run_id=run_id, scorers=scorers, segment_filters=segment_filters)

        run_scorer_settings_response.additional_properties = d
        return run_scorer_settings_response

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
