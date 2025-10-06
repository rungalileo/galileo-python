from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_type import ModelType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scorer_defaults import ScorerDefaults


T = TypeVar("T", bound="UpdateScorerRequest")


@_attrs_define
class UpdateScorerRequest:
    """
    Attributes:
        default_version_id (Union[None, Unset, str]):
        defaults (Union['ScorerDefaults', None, Unset]):
        description (Union[None, Unset, str]):
        ground_truth (Union[None, Unset, bool]):
        model_type (Union[ModelType, None, Unset]):
        name (Union[None, Unset, str]):
        tags (Union[None, Unset, list[str]]):
        user_prompt (Union[None, Unset, str]):
    """

    default_version_id: Union[None, Unset, str] = UNSET
    defaults: Union["ScorerDefaults", None, Unset] = UNSET
    description: Union[None, Unset, str] = UNSET
    ground_truth: Union[None, Unset, bool] = UNSET
    model_type: Union[ModelType, None, Unset] = UNSET
    name: Union[None, Unset, str] = UNSET
    tags: Union[None, Unset, list[str]] = UNSET
    user_prompt: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scorer_defaults import ScorerDefaults

        default_version_id: Union[None, Unset, str]
        default_version_id = UNSET if isinstance(self.default_version_id, Unset) else self.default_version_id

        defaults: Union[None, Unset, dict[str, Any]]
        if isinstance(self.defaults, Unset):
            defaults = UNSET
        elif isinstance(self.defaults, ScorerDefaults):
            defaults = self.defaults.to_dict()
        else:
            defaults = self.defaults

        description: Union[None, Unset, str]
        description = UNSET if isinstance(self.description, Unset) else self.description

        ground_truth: Union[None, Unset, bool]
        ground_truth = UNSET if isinstance(self.ground_truth, Unset) else self.ground_truth

        model_type: Union[None, Unset, str]
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        name: Union[None, Unset, str]
        name = UNSET if isinstance(self.name, Unset) else self.name

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        user_prompt: Union[None, Unset, str]
        user_prompt = UNSET if isinstance(self.user_prompt, Unset) else self.user_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_version_id is not UNSET:
            field_dict["default_version_id"] = default_version_id
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if description is not UNSET:
            field_dict["description"] = description
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scorer_defaults import ScorerDefaults

        d = dict(src_dict)

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
                return ScorerDefaults.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ScorerDefaults", None, Unset], data)

        defaults = _parse_defaults(d.pop("defaults", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_ground_truth(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_model_type(data: object) -> Union[ModelType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ModelType(data)

            except:  # noqa: E722
                pass
            return cast(Union[ModelType, None, Unset], data)

        model_type = _parse_model_type(d.pop("model_type", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_user_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        update_scorer_request = cls(
            default_version_id=default_version_id,
            defaults=defaults,
            description=description,
            ground_truth=ground_truth,
            model_type=model_type,
            name=name,
            tags=tags,
            user_prompt=user_prompt,
        )

        update_scorer_request.additional_properties = d
        return update_scorer_request

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
