from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
    from ..models.base_registered_scorer_db import BaseRegisteredScorerDB


T = TypeVar("T", bound="BaseScorerVersionDB")


@_attrs_define
class BaseScorerVersionDB:
    """Scorer version from the scorer_versions table.

    Attributes:
        id (str):
        version (int):
        generated_scorer (Union['BaseGeneratedScorerDB', None, Unset]):
        model_name (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        registered_scorer (Union['BaseRegisteredScorerDB', None, Unset]):
    """

    id: str
    version: int
    generated_scorer: Union["BaseGeneratedScorerDB", None, Unset] = UNSET
    model_name: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    registered_scorer: Union["BaseRegisteredScorerDB", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
        from ..models.base_registered_scorer_db import BaseRegisteredScorerDB

        id = self.id

        version = self.version

        generated_scorer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.generated_scorer, Unset):
            generated_scorer = UNSET
        elif isinstance(self.generated_scorer, BaseGeneratedScorerDB):
            generated_scorer = self.generated_scorer.to_dict()
        else:
            generated_scorer = self.generated_scorer

        model_name: Union[None, Unset, str]
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        num_judges: Union[None, Unset, int]
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        registered_scorer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.registered_scorer, Unset):
            registered_scorer = UNSET
        elif isinstance(self.registered_scorer, BaseRegisteredScorerDB):
            registered_scorer = self.registered_scorer.to_dict()
        else:
            registered_scorer = self.registered_scorer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "version": version})
        if generated_scorer is not UNSET:
            field_dict["generated_scorer"] = generated_scorer
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if registered_scorer is not UNSET:
            field_dict["registered_scorer"] = registered_scorer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
        from ..models.base_registered_scorer_db import BaseRegisteredScorerDB

        d = dict(src_dict)
        id = d.pop("id")

        version = d.pop("version")

        def _parse_generated_scorer(data: object) -> Union["BaseGeneratedScorerDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                generated_scorer_type_0 = BaseGeneratedScorerDB.from_dict(data)

                return generated_scorer_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseGeneratedScorerDB", None, Unset], data)

        generated_scorer = _parse_generated_scorer(d.pop("generated_scorer", UNSET))

        def _parse_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        def _parse_registered_scorer(data: object) -> Union["BaseRegisteredScorerDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                registered_scorer_type_0 = BaseRegisteredScorerDB.from_dict(data)

                return registered_scorer_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseRegisteredScorerDB", None, Unset], data)

        registered_scorer = _parse_registered_scorer(d.pop("registered_scorer", UNSET))

        base_scorer_version_db = cls(
            id=id,
            version=version,
            generated_scorer=generated_scorer,
            model_name=model_name,
            num_judges=num_judges,
            registered_scorer=registered_scorer,
        )

        base_scorer_version_db.additional_properties = d
        return base_scorer_version_db

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
