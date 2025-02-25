from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scorer_config import ScorerConfig


T = TypeVar("T", bound="RunScorerSettingsRequest")


@_attrs_define
class RunScorerSettingsRequest:
    """
    Attributes:
        run_id (str): ID of the run.
        scorers (Union[Unset, list['ScorerConfig']]): List of Galileo scorers to enable.
    """

    run_id: str
    scorers: Union[Unset, list["ScorerConfig"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        scorers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.scorers, Unset):
            scorers = []
            for scorers_item_data in self.scorers:
                scorers_item = scorers_item_data.to_dict()
                scorers.append(scorers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"run_id": run_id})
        if scorers is not UNSET:
            field_dict["scorers"] = scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.scorer_config import ScorerConfig

        d = src_dict.copy()
        run_id = d.pop("run_id")

        scorers = []
        _scorers = d.pop("scorers", UNSET)
        for scorers_item_data in _scorers or []:
            scorers_item = ScorerConfig.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        run_scorer_settings_request = cls(run_id=run_id, scorers=scorers)

        run_scorer_settings_request.additional_properties = d
        return run_scorer_settings_request

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
