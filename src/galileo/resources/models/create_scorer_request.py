from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
        defaults (Union['ScorerDefaults', None, Unset]):
        description (Union[Unset, str]):  Default: ''.
        tags (Union[Unset, list[str]]):
    """

    name: str
    scorer_type: ScorerTypes
    defaults: Union["ScorerDefaults", None, Unset] = UNSET
    description: Union[Unset, str] = ""
    tags: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.scorer_defaults import ScorerDefaults

        name = self.name

        scorer_type = self.scorer_type.value

        defaults: Union[None, Unset, dict[str, Any]]
        if isinstance(self.defaults, Unset):
            defaults = UNSET
        elif isinstance(self.defaults, ScorerDefaults):
            defaults = self.defaults.to_dict()
        else:
            defaults = self.defaults

        description = self.description

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "scorer_type": scorer_type})
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.scorer_defaults import ScorerDefaults

        d = src_dict.copy()
        name = d.pop("name")

        scorer_type = ScorerTypes(d.pop("scorer_type"))

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

        tags = cast(list[str], d.pop("tags", UNSET))

        create_scorer_request = cls(
            name=name, scorer_type=scorer_type, defaults=defaults, description=description, tags=tags
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
