import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.input_type_enum import InputTypeEnum
from ..models.model_type import ModelType
from ..models.output_type_enum import OutputTypeEnum
from ..models.scorer_types import ScorerTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_scorer_version_db import BaseScorerVersionDB
    from ..models.scorer_defaults import ScorerDefaults


T = TypeVar("T", bound="ScorerResponse")


@_attrs_define
class ScorerResponse:
    """
    Attributes
    ----------
        id (str):
        name (str):
        scorer_type (ScorerTypes):
        tags (list[str]):
        created_at (Union[None, Unset, datetime.datetime]):
        created_by (Union[None, Unset, str]):
        default_version (Union['BaseScorerVersionDB', None, Unset]):
        default_version_id (Union[None, Unset, str]):
        defaults (Union['ScorerDefaults', None, Unset]):
        description (Union[None, Unset, str]):
        ground_truth (Union[None, Unset, bool]):
        included_fields (Union[Unset, list[str]]): Fields that can be used in the scorer to configure it. i.e. model,
            num_judges, etc. This enables the ui to know which fields a user can configure when they're setting a scorer
        input_type (Union[InputTypeEnum, None, Unset]):
        label (Union[None, Unset, str]):  Default: ''.
        latest_version (Union['BaseScorerVersionDB', None, Unset]):
        model_type (Union[ModelType, None, Unset]):
        output_type (Union[None, OutputTypeEnum, Unset]):
        required_scorers (Union[None, Unset, list[str]]):
        scoreable_node_types (Union[None, Unset, list[str]]):
        updated_at (Union[None, Unset, datetime.datetime]):
        user_prompt (Union[None, Unset, str]):
    """

    id: str
    name: str
    scorer_type: ScorerTypes
    tags: list[str]
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    default_version: Union["BaseScorerVersionDB", None, Unset] = UNSET
    default_version_id: Union[None, Unset, str] = UNSET
    defaults: Union["ScorerDefaults", None, Unset] = UNSET
    description: Union[None, Unset, str] = UNSET
    ground_truth: Union[None, Unset, bool] = UNSET
    included_fields: Union[Unset, list[str]] = UNSET
    input_type: Union[InputTypeEnum, None, Unset] = UNSET
    label: Union[None, Unset, str] = ""
    latest_version: Union["BaseScorerVersionDB", None, Unset] = UNSET
    model_type: Union[ModelType, None, Unset] = UNSET
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    required_scorers: Union[None, Unset, list[str]] = UNSET
    scoreable_node_types: Union[None, Unset, list[str]] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    user_prompt: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_scorer_version_db import BaseScorerVersionDB
        from ..models.scorer_defaults import ScorerDefaults

        id = self.id

        name = self.name

        scorer_type = self.scorer_type.value

        tags = self.tags

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        created_by: Union[None, Unset, str]
        created_by = UNSET if isinstance(self.created_by, Unset) else self.created_by

        default_version: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default_version, Unset):
            default_version = UNSET
        elif isinstance(self.default_version, BaseScorerVersionDB):
            default_version = self.default_version.to_dict()
        else:
            default_version = self.default_version

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

        included_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.included_fields, Unset):
            included_fields = self.included_fields

        input_type: Union[None, Unset, str]
        if isinstance(self.input_type, Unset):
            input_type = UNSET
        elif isinstance(self.input_type, InputTypeEnum):
            input_type = self.input_type.value
        else:
            input_type = self.input_type

        label: Union[None, Unset, str]
        label = UNSET if isinstance(self.label, Unset) else self.label

        latest_version: Union[None, Unset, dict[str, Any]]
        if isinstance(self.latest_version, Unset):
            latest_version = UNSET
        elif isinstance(self.latest_version, BaseScorerVersionDB):
            latest_version = self.latest_version.to_dict()
        else:
            latest_version = self.latest_version

        model_type: Union[None, Unset, str]
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, OutputTypeEnum):
            output_type = self.output_type.value
        else:
            output_type = self.output_type

        required_scorers: Union[None, Unset, list[str]]
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        user_prompt: Union[None, Unset, str]
        user_prompt = UNSET if isinstance(self.user_prompt, Unset) else self.user_prompt

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "name": name, "scorer_type": scorer_type, "tags": tags})
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if default_version is not UNSET:
            field_dict["default_version"] = default_version
        if default_version_id is not UNSET:
            field_dict["default_version_id"] = default_version_id
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if description is not UNSET:
            field_dict["description"] = description
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if included_fields is not UNSET:
            field_dict["included_fields"] = included_fields
        if input_type is not UNSET:
            field_dict["input_type"] = input_type
        if label is not UNSET:
            field_dict["label"] = label
        if latest_version is not UNSET:
            field_dict["latest_version"] = latest_version
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_scorer_version_db import BaseScorerVersionDB
        from ..models.scorer_defaults import ScorerDefaults

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        scorer_type = ScorerTypes(d.pop("scorer_type"))

        tags = cast(list[str], d.pop("tags"))

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return isoparse(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_default_version(data: object) -> Union["BaseScorerVersionDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseScorerVersionDB.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["BaseScorerVersionDB", None, Unset], data)

        default_version = _parse_default_version(d.pop("default_version", UNSET))

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

        included_fields = cast(list[str], d.pop("included_fields", UNSET))

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

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_latest_version(data: object) -> Union["BaseScorerVersionDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseScorerVersionDB.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["BaseScorerVersionDB", None, Unset], data)

        latest_version = _parse_latest_version(d.pop("latest_version", UNSET))

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

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return isoparse(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_user_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        scorer_response = cls(
            id=id,
            name=name,
            scorer_type=scorer_type,
            tags=tags,
            created_at=created_at,
            created_by=created_by,
            default_version=default_version,
            default_version_id=default_version_id,
            defaults=defaults,
            description=description,
            ground_truth=ground_truth,
            included_fields=included_fields,
            input_type=input_type,
            label=label,
            latest_version=latest_version,
            model_type=model_type,
            output_type=output_type,
            required_scorers=required_scorers,
            scoreable_node_types=scoreable_node_types,
            updated_at=updated_at,
            user_prompt=user_prompt,
        )

        scorer_response.additional_properties = d
        return scorer_response

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
