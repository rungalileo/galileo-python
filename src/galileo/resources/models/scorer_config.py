from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_type import ModelType
from ..models.scorer_types import ScorerTypes
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScorerConfig")


@_attrs_define
class ScorerConfig:
    """Used for configuring a scorer for a scorer job.

    Attributes:
        id (str):
        scorer_type (ScorerTypes):
        model_name (Union[None, Unset, str]):
        model_type (Union[ModelType, None, Unset]): Type of model to use for this scorer. slm maps to luna, and llm maps
            to plus
        num_judges (Union[None, Unset, int]):
    """

    id: str
    scorer_type: ScorerTypes
    model_name: Union[None, Unset, str] = UNSET
    model_type: Union[ModelType, None, Unset] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        scorer_type = self.scorer_type.value

        model_name: Union[None, Unset, str]
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        model_type: Union[None, Unset, str]
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        num_judges: Union[None, Unset, int]
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "scorer_type": scorer_type})
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        scorer_type = ScorerTypes(d.pop("scorer_type"))

        def _parse_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        def _parse_model_type(data: object) -> Union[ModelType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_type_0 = ModelType(data)

                return model_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ModelType, None, Unset], data)

        model_type = _parse_model_type(d.pop("model_type", UNSET))

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        scorer_config = cls(
            id=id, scorer_type=scorer_type, model_name=model_name, model_type=model_type, num_judges=num_judges
        )

        scorer_config.additional_properties = d
        return scorer_config

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
