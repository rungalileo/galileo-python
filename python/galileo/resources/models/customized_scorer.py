from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.customized_scorer_name import CustomizedScorerName
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomizedScorer")


@_attrs_define
class CustomizedScorer:
    """
    Attributes:
        scorer_name (CustomizedScorerName):
        model_alias (Union[None, Unset, str]): Model alias to use for scoring.
        num_judges (Union[None, Unset, int]): Number of judges for the scorer.
    """

    scorer_name: CustomizedScorerName
    model_alias: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scorer_name = self.scorer_name.value

        model_alias: Union[None, Unset, str]
        if isinstance(self.model_alias, Unset):
            model_alias = UNSET
        else:
            model_alias = self.model_alias

        num_judges: Union[None, Unset, int]
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"scorer_name": scorer_name})
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        scorer_name = CustomizedScorerName(d.pop("scorer_name"))

        def _parse_model_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_alias = _parse_model_alias(d.pop("model_alias", UNSET))

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        customized_scorer = cls(scorer_name=scorer_name, model_alias=model_alias, num_judges=num_judges)

        customized_scorer.additional_properties = d
        return customized_scorer

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
