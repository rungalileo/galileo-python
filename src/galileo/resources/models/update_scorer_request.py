from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_type_enum import InputTypeEnum
from ..models.model_type import ModelType
from ..models.output_type_enum import OutputTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.scorer_defaults import ScorerDefaults


T = TypeVar("T", bound="UpdateScorerRequest")


@_attrs_define
class UpdateScorerRequest:
    """
    Attributes
    ----------
        name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        tags (Union[None, Unset, list[str]]):
        defaults (Union['ScorerDefaults', None, Unset]):
        model_type (Union[ModelType, None, Unset]):
        ground_truth (Union[None, Unset, bool]):
        default_version_id (Union[None, Unset, str]):
        user_prompt (Union[None, Unset, str]):
        scoreable_node_types (Union[None, Unset, list[str]]):
        output_type (Union[None, OutputTypeEnum, Unset]):
        input_type (Union[InputTypeEnum, None, Unset]):
        required_scorers (Union[None, Unset, list[str]]):
    """

    name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    tags: Union[None, Unset, list[str]] = UNSET
    defaults: Union["ScorerDefaults", None, Unset] = UNSET
    model_type: Union[ModelType, None, Unset] = UNSET
    ground_truth: Union[None, Unset, bool] = UNSET
    default_version_id: Union[None, Unset, str] = UNSET
    user_prompt: Union[None, Unset, str] = UNSET
    scoreable_node_types: Union[None, Unset, list[str]] = UNSET
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    input_type: Union[InputTypeEnum, None, Unset] = UNSET
    required_scorers: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scorer_defaults import ScorerDefaults

        name: Union[None, Unset, str]
        name = UNSET if isinstance(self.name, Unset) else self.name

        description: Union[None, Unset, str]
        description = UNSET if isinstance(self.description, Unset) else self.description

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        defaults: Union[None, Unset, dict[str, Any]]
        if isinstance(self.defaults, Unset):
            defaults = UNSET
        elif isinstance(self.defaults, ScorerDefaults):
            defaults = self.defaults.to_dict()
        else:
            defaults = self.defaults

        model_type: Union[None, Unset, str]
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        ground_truth: Union[None, Unset, bool]
        ground_truth = UNSET if isinstance(self.ground_truth, Unset) else self.ground_truth

        default_version_id: Union[None, Unset, str]
        default_version_id = UNSET if isinstance(self.default_version_id, Unset) else self.default_version_id

        user_prompt: Union[None, Unset, str]
        user_prompt = UNSET if isinstance(self.user_prompt, Unset) else self.user_prompt

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, OutputTypeEnum):
            output_type = self.output_type.value
        else:
            output_type = self.output_type

        input_type: Union[None, Unset, str]
        if isinstance(self.input_type, Unset):
            input_type = UNSET
        elif isinstance(self.input_type, InputTypeEnum):
            input_type = self.input_type.value
        else:
            input_type = self.input_type

        required_scorers: Union[None, Unset, list[str]]
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if default_version_id is not UNSET:
            field_dict["default_version_id"] = default_version_id
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if input_type is not UNSET:
            field_dict["input_type"] = input_type
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scorer_defaults import ScorerDefaults

        d = dict(src_dict)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

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

        def _parse_ground_truth(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_default_version_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_version_id = _parse_default_version_id(d.pop("default_version_id", UNSET))

        def _parse_user_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        def _parse_scoreable_node_types(data: object) -> Union[None, Unset, list[str]]:
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

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        def _parse_output_type(data: object) -> Union[None, OutputTypeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return OutputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, OutputTypeEnum, Unset], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        def _parse_input_type(data: object) -> Union[InputTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return InputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[InputTypeEnum, None, Unset], data)

        input_type = _parse_input_type(d.pop("input_type", UNSET))

        def _parse_required_scorers(data: object) -> Union[None, Unset, list[str]]:
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

        required_scorers = _parse_required_scorers(d.pop("required_scorers", UNSET))

        update_scorer_request = cls(
            name=name,
            description=description,
            tags=tags,
            defaults=defaults,
            model_type=model_type,
            ground_truth=ground_truth,
            default_version_id=default_version_id,
            user_prompt=user_prompt,
            scoreable_node_types=scoreable_node_types,
            output_type=output_type,
            input_type=input_type,
            required_scorers=required_scorers,
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
