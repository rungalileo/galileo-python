from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.name import Name
    from ..models.playground_dataset import PlaygroundDataset
    from ..models.scorer_config import ScorerConfig


T = TypeVar("T", bound="UpdatePlaygroundRequest")


@_attrs_define
class UpdatePlaygroundRequest:
    """
    Attributes:
        name (Name | None | str | Unset):
        scorers (list[ScorerConfig] | None | Unset): List of Galileo scorers to enable.
        dataset (None | PlaygroundDataset | Unset): Dataset to use for the playground.
    """

    name: Name | None | str | Unset = UNSET
    scorers: list[ScorerConfig] | None | Unset = UNSET
    dataset: None | PlaygroundDataset | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.name import Name
        from ..models.playground_dataset import PlaygroundDataset

        name: dict[str, Any] | None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        elif isinstance(self.name, Name):
            name = self.name.to_dict()
        else:
            name = self.name

        scorers: list[dict[str, Any]] | None | Unset
        if isinstance(self.scorers, Unset):
            scorers = UNSET
        elif isinstance(self.scorers, list):
            scorers = []
            for scorers_type_0_item_data in self.scorers:
                scorers_type_0_item = scorers_type_0_item_data.to_dict()
                scorers.append(scorers_type_0_item)

        else:
            scorers = self.scorers

        dataset: dict[str, Any] | None | Unset
        if isinstance(self.dataset, Unset):
            dataset = UNSET
        elif isinstance(self.dataset, PlaygroundDataset):
            dataset = self.dataset.to_dict()
        else:
            dataset = self.dataset

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if scorers is not UNSET:
            field_dict["scorers"] = scorers
        if dataset is not UNSET:
            field_dict["dataset"] = dataset

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.name import Name
        from ..models.playground_dataset import PlaygroundDataset
        from ..models.scorer_config import ScorerConfig

        d = dict(src_dict)

        def _parse_name(data: object) -> Name | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                name_type_1 = Name.from_dict(data)

                return name_type_1
            except:  # noqa: E722
                pass
            return cast(Name | None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_scorers(data: object) -> list[ScorerConfig] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scorers_type_0 = []
                _scorers_type_0 = data
                for scorers_type_0_item_data in _scorers_type_0:
                    scorers_type_0_item = ScorerConfig.from_dict(scorers_type_0_item_data)

                    scorers_type_0.append(scorers_type_0_item)

                return scorers_type_0
            except:  # noqa: E722
                pass
            return cast(list[ScorerConfig] | None | Unset, data)

        scorers = _parse_scorers(d.pop("scorers", UNSET))

        def _parse_dataset(data: object) -> None | PlaygroundDataset | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                dataset_type_0 = PlaygroundDataset.from_dict(data)

                return dataset_type_0
            except:  # noqa: E722
                pass
            return cast(None | PlaygroundDataset | Unset, data)

        dataset = _parse_dataset(d.pop("dataset", UNSET))

        update_playground_request = cls(name=name, scorers=scorers, dataset=dataset)

        update_playground_request.additional_properties = d
        return update_playground_request

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
