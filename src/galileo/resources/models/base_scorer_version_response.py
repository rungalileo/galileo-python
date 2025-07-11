import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from galileo.resources.models.create_update_registered_scorer_response import \
    CreateUpdateRegisteredScorerResponse
from galileo.resources.models.generated_scorer_response import \
    GeneratedScorerResponse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_update_registered_scorer_response import \
        CreateUpdateRegisteredScorerResponse
    from ..models.generated_scorer_response import GeneratedScorerResponse


T = TypeVar("T", bound="BaseScorerVersionResponse")


@_attrs_define
class BaseScorerVersionResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        id (str):
        updated_at (datetime.datetime):
        version (int):
        generated_scorer (Union['GeneratedScorerResponse', None, Unset]):
        model_name (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        registered_scorer (Union['CreateUpdateRegisteredScorerResponse', None, Unset]):
    """

    created_at: datetime.datetime
    id: str
    updated_at: datetime.datetime
    version: int
    generated_scorer: Union["GeneratedScorerResponse", None, Unset] = UNSET
    model_name: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    registered_scorer: Union["CreateUpdateRegisteredScorerResponse", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.create_update_registered_scorer_response import \
            CreateUpdateRegisteredScorerResponse
        from ..models.generated_scorer_response import GeneratedScorerResponse

        created_at = self.created_at.isoformat()

        id = self.id

        updated_at = self.updated_at.isoformat()

        version = self.version

        generated_scorer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.generated_scorer, Unset):
            generated_scorer = UNSET
        elif isinstance(self.generated_scorer, GeneratedScorerResponse):
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
        elif isinstance(self.registered_scorer, CreateUpdateRegisteredScorerResponse):
            registered_scorer = self.registered_scorer.to_dict()
        else:
            registered_scorer = self.registered_scorer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"created_at": created_at, "id": id, "updated_at": updated_at, "version": version})
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
        d = dict(src_dict)

        # Fast batch pop
        created_at_v = d.pop("created_at", None)
        updated_at_v = d.pop("updated_at", None)
        created_at = _fast_parse_iso(created_at_v)
        updated_at = _fast_parse_iso(updated_at_v)
        id = d.pop("id", "")
        version = d.pop("version", 0)

        gen_scorer = d.pop("generated_scorer", UNSET)
        if gen_scorer is not UNSET and gen_scorer is not None and isinstance(gen_scorer, dict):
            try:
                gen_scorer = GeneratedScorerResponse.from_dict(gen_scorer)
            except Exception:
                pass

        model_name = d.pop("model_name", UNSET)
        num_judges = d.pop("num_judges", UNSET)

        reg_scorer = d.pop("registered_scorer", UNSET)
        if reg_scorer is not UNSET and reg_scorer is not None and isinstance(reg_scorer, dict):
            try:
                reg_scorer = CreateUpdateRegisteredScorerResponse.from_dict(reg_scorer)
            except Exception:
                pass

        instance = cls(
            created_at=created_at,
            id=id,
            updated_at=updated_at,
            version=version,
            generated_scorer=gen_scorer,
            model_name=model_name,
            num_judges=num_judges,
            registered_scorer=reg_scorer,
        )
        instance.additional_properties = d
        return instance

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


def _fast_parse_iso(dt):
    # Fast path for naive ISO, fallback for timezone/edge
    # (avoiding dateutil overhead for simple dates)
    if isinstance(dt, str):
        try:
            if dt.endswith("Z"):
                # Handle common utc-Z
                return isoparse(dt)
            return __import__("datetime").datetime.fromisoformat(dt)
        except Exception:
            return isoparse(dt)
    return dt
