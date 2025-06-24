from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_type import ModelType
from ..models.scorer_types import ScorerTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scorer_defaults import ScorerDefaults


T = TypeVar("T", bound="CreateScorerRequest")


@_attrs_define
class CreateScorerRequest:
    """
    Attributes:
        name (str):
        scorer_type (ScorerTypes):
        default_version_id (Union[None, Unset, str]):
        defaults (Union['ScorerDefaults', None, Unset]):
        description (Union[Unset, str]):  Default: ''.
        model_type (Union[ModelType, None, Unset]):
        tags (Union[Unset, list[str]]):
    """

    name: str
    scorer_type: ScorerTypes
    default_version_id: Union[None, Unset, str] = UNSET
    defaults: Union["ScorerDefaults", None, Unset] = UNSET
    description: Union[Unset, str] = ""
    model_type: Union[ModelType, None, Unset] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scorer_defaults import ScorerDefaults

        name = self.name

        scorer_type = self.scorer_type.value

        default_version_id: Union[None, Unset, str]
        if isinstance(self.default_version_id, Unset):
            default_version_id = UNSET
        else:
            default_version_id = self.default_version_id

        defaults: Union[None, Unset, dict[str, Any]]
        if isinstance(self.defaults, Unset):
            defaults = UNSET
        elif isinstance(self.defaults, ScorerDefaults):
            defaults = self.defaults.to_dict()
        else:
            defaults = self.defaults

        description = self.description

        model_type: Union[None, Unset, str]
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "scorer_type": scorer_type})
        if default_version_id is not UNSET:
            field_dict["default_version_id"] = default_version_id
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if description is not UNSET:
            field_dict["description"] = description
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scorer_defaults import ScorerDefaults

        d = dict(src_dict)
        name = d.pop("name")

        scorer_type = ScorerTypes(d.pop("scorer_type"))

        def _parse_default_version_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_version_id = _parse_default_version_id(d.pop("default_version_id", UNSET))

        def _parse_defaults(data: object) -> Union["ScorerDefaults", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                defaults_type_0 = ScorerDefaults.from_dict(data)

                return defaults_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ScorerDefaults", None, Unset], data)

        defaults = _parse_defaults(d.pop("defaults", UNSET))

        description = d.pop("description", UNSET)

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

        tags = cast(list[str], d.pop("tags", UNSET))

        create_scorer_request = cls(
            name=name,
            scorer_type=scorer_type,
            default_version_id=default_version_id,
            defaults=defaults,
            description=description,
            model_type=model_type,
            tags=tags,
        )

        create_scorer_request.additional_properties = d
        return create_scorer_request

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
