from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.output_type_enum import OutputTypeEnum
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
        cot_enabled (Union[None, Unset, bool]): Whether to enable chain of thought for this scorer. Defaults to False
            for llm scorers.
        generated_scorer (Union['BaseGeneratedScorerDB', None, Unset]):
        model_name (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        output_type (Union[None, OutputTypeEnum, Unset]): What type of output to use for model-based scorers (llm or
            slm).
        registered_scorer (Union['BaseRegisteredScorerDB', None, Unset]):
        scoreable_node_types (Union[None, Unset, list[str]]): List of node types that can be scored by this scorer.
            Defaults to llm/chat.
    """

    id: str
    version: int
    cot_enabled: Union[None, Unset, bool] = UNSET
    generated_scorer: Union["BaseGeneratedScorerDB", None, Unset] = UNSET
    model_name: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    registered_scorer: Union["BaseRegisteredScorerDB", None, Unset] = UNSET
    scoreable_node_types: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
        from ..models.base_registered_scorer_db import BaseRegisteredScorerDB

        id = self.id

        version = self.version

        cot_enabled: Union[None, Unset, bool]
        if isinstance(self.cot_enabled, Unset):
            cot_enabled = UNSET
        else:
            cot_enabled = self.cot_enabled

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

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, OutputTypeEnum):
            output_type = self.output_type.value
        else:
            output_type = self.output_type

        registered_scorer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.registered_scorer, Unset):
            registered_scorer = UNSET
        elif isinstance(self.registered_scorer, BaseRegisteredScorerDB):
            registered_scorer = self.registered_scorer.to_dict()
        else:
            registered_scorer = self.registered_scorer

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "version": version})
        if cot_enabled is not UNSET:
            field_dict["cot_enabled"] = cot_enabled
        if generated_scorer is not UNSET:
            field_dict["generated_scorer"] = generated_scorer
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if registered_scorer is not UNSET:
            field_dict["registered_scorer"] = registered_scorer
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
        from ..models.base_registered_scorer_db import BaseRegisteredScorerDB

        d = dict(src_dict)
        id = d.pop("id")

        version = d.pop("version")

        def _parse_cot_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        cot_enabled = _parse_cot_enabled(d.pop("cot_enabled", UNSET))

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

        def _parse_output_type(data: object) -> Union[None, OutputTypeEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                output_type_type_0 = OutputTypeEnum(data)

                return output_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, OutputTypeEnum, Unset], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

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

        def _parse_scoreable_node_types(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scoreable_node_types_type_0 = cast(list[str], data)

                return scoreable_node_types_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        base_scorer_version_db = cls(
            id=id,
            version=version,
            cot_enabled=cot_enabled,
            generated_scorer=generated_scorer,
            model_name=model_name,
            num_judges=num_judges,
            output_type=output_type,
            registered_scorer=registered_scorer,
            scoreable_node_types=scoreable_node_types,
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
