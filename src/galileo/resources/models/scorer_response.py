import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.model_type import ModelType
from ..models.scorer_types import ScorerTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_scorer_version_db import BaseScorerVersionDB
    from ..models.scorer_defaults import ScorerDefaults


T = TypeVar("T", bound="ScorerResponse")


@_attrs_define
class ScorerResponse:
    """
    Attributes:
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
        included_fields (Union[Unset, list[str]]): Fields that can be used in the scorer to configure it. i.e. model,
            num_judges, etc. This enables the ui to know which fields a user can configure when they're setting a scorer
        label (Union[Unset, str]):  Default: ''.
        latest_version (Union['BaseScorerVersionDB', None, Unset]):
        model_type (Union[ModelType, None, Unset]):
        updated_at (Union[None, Unset, datetime.datetime]):
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
    included_fields: Union[Unset, list[str]] = UNSET
    label: Union[Unset, str] = ""
    latest_version: Union["BaseScorerVersionDB", None, Unset] = UNSET
    model_type: Union[ModelType, None, Unset] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
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
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        default_version: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default_version, Unset):
            default_version = UNSET
        elif isinstance(self.default_version, BaseScorerVersionDB):
            default_version = self.default_version.to_dict()
        else:
            default_version = self.default_version

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

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        included_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.included_fields, Unset):
            included_fields = self.included_fields

        label = self.label

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

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

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
        if included_fields is not UNSET:
            field_dict["included_fields"] = included_fields
        if label is not UNSET:
            field_dict["label"] = label
        if latest_version is not UNSET:
            field_dict["latest_version"] = latest_version
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

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
                created_at_type_0 = isoparse(data)

                return created_at_type_0
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
                default_version_type_0 = BaseScorerVersionDB.from_dict(data)

                return default_version_type_0
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
                defaults_type_0 = ScorerDefaults.from_dict(data)

                return defaults_type_0
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

        included_fields = cast(list[str], d.pop("included_fields", UNSET))

        label = d.pop("label", UNSET)

        def _parse_latest_version(data: object) -> Union["BaseScorerVersionDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_version_type_0 = BaseScorerVersionDB.from_dict(data)

                return latest_version_type_0
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
                model_type_type_0 = ModelType(data)

                return model_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ModelType, None, Unset], data)

        model_type = _parse_model_type(d.pop("model_type", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

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
            included_fields=included_fields,
            label=label,
            latest_version=latest_version,
            model_type=model_type,
            updated_at=updated_at,
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
