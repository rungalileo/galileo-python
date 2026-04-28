from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_type_enum import InputTypeEnum
from ..models.output_type_enum import OutputTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_finetuned_scorer_db import BaseFinetunedScorerDB
    from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
    from ..models.base_registered_scorer_db import BaseRegisteredScorerDB


T = TypeVar("T", bound="BaseScorerVersionDB")


@_attrs_define
class BaseScorerVersionDB:
    """Scorer version from the scorer_versions table.

    Attributes
    ----------
        id (str):
        version (int):
        scorer_id (str):
        generated_scorer (BaseGeneratedScorerDB | None | Unset):
        registered_scorer (BaseRegisteredScorerDB | None | Unset):
        finetuned_scorer (BaseFinetunedScorerDB | None | Unset):
        model_name (None | str | Unset):
        num_judges (int | None | Unset):
        scoreable_node_types (list[str] | None | Unset): List of node types that can be scored by this scorer. Defaults
            to llm/chat.
        cot_enabled (bool | None | Unset): Whether to enable chain of thought for this scorer. Defaults to False for llm
            scorers.
        output_type (None | OutputTypeEnum | Unset): What type of output to use for model-based scorers
            (sessions_normalized, trace_io_only, etc.).
        input_type (InputTypeEnum | None | Unset): What type of input to use for model-based scorers
            (sessions_normalized, trace_io_only, etc.).
    """

    id: str
    version: int
    scorer_id: str
    generated_scorer: BaseGeneratedScorerDB | None | Unset = UNSET
    registered_scorer: BaseRegisteredScorerDB | None | Unset = UNSET
    finetuned_scorer: BaseFinetunedScorerDB | None | Unset = UNSET
    model_name: None | str | Unset = UNSET
    num_judges: int | None | Unset = UNSET
    scoreable_node_types: list[str] | None | Unset = UNSET
    cot_enabled: bool | None | Unset = UNSET
    output_type: None | OutputTypeEnum | Unset = UNSET
    input_type: InputTypeEnum | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_finetuned_scorer_db import BaseFinetunedScorerDB
        from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
        from ..models.base_registered_scorer_db import BaseRegisteredScorerDB

        id = self.id

        version = self.version

        scorer_id = self.scorer_id

        generated_scorer: dict[str, Any] | None | Unset
        if isinstance(self.generated_scorer, Unset):
            generated_scorer = UNSET
        elif isinstance(self.generated_scorer, BaseGeneratedScorerDB):
            generated_scorer = self.generated_scorer.to_dict()
        else:
            generated_scorer = self.generated_scorer

        registered_scorer: dict[str, Any] | None | Unset
        if isinstance(self.registered_scorer, Unset):
            registered_scorer = UNSET
        elif isinstance(self.registered_scorer, BaseRegisteredScorerDB):
            registered_scorer = self.registered_scorer.to_dict()
        else:
            registered_scorer = self.registered_scorer

        finetuned_scorer: dict[str, Any] | None | Unset
        if isinstance(self.finetuned_scorer, Unset):
            finetuned_scorer = UNSET
        elif isinstance(self.finetuned_scorer, BaseFinetunedScorerDB):
            finetuned_scorer = self.finetuned_scorer.to_dict()
        else:
            finetuned_scorer = self.finetuned_scorer

        model_name: None | str | Unset
        model_name = UNSET if isinstance(self.model_name, Unset) else self.model_name

        num_judges: int | None | Unset
        num_judges = UNSET if isinstance(self.num_judges, Unset) else self.num_judges

        scoreable_node_types: list[str] | None | Unset
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        cot_enabled: bool | None | Unset
        cot_enabled = UNSET if isinstance(self.cot_enabled, Unset) else self.cot_enabled

        output_type: None | str | Unset
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, OutputTypeEnum):
            output_type = self.output_type.value
        else:
            output_type = self.output_type

        input_type: None | str | Unset
        if isinstance(self.input_type, Unset):
            input_type = UNSET
        elif isinstance(self.input_type, InputTypeEnum):
            input_type = self.input_type.value
        else:
            input_type = self.input_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "version": version, "scorer_id": scorer_id})
        if generated_scorer is not UNSET:
            field_dict["generated_scorer"] = generated_scorer
        if registered_scorer is not UNSET:
            field_dict["registered_scorer"] = registered_scorer
        if finetuned_scorer is not UNSET:
            field_dict["finetuned_scorer"] = finetuned_scorer
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if cot_enabled is not UNSET:
            field_dict["cot_enabled"] = cot_enabled
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if input_type is not UNSET:
            field_dict["input_type"] = input_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_finetuned_scorer_db import BaseFinetunedScorerDB
        from ..models.base_generated_scorer_db import BaseGeneratedScorerDB
        from ..models.base_registered_scorer_db import BaseRegisteredScorerDB

        d = dict(src_dict)
        id = d.pop("id")

        version = d.pop("version")

        scorer_id = d.pop("scorer_id")

        def _parse_generated_scorer(data: object) -> BaseGeneratedScorerDB | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseGeneratedScorerDB.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(BaseGeneratedScorerDB | None | Unset, data)

        generated_scorer = _parse_generated_scorer(d.pop("generated_scorer", UNSET))

        def _parse_registered_scorer(data: object) -> BaseRegisteredScorerDB | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseRegisteredScorerDB.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(BaseRegisteredScorerDB | None | Unset, data)

        registered_scorer = _parse_registered_scorer(d.pop("registered_scorer", UNSET))

        def _parse_finetuned_scorer(data: object) -> BaseFinetunedScorerDB | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseFinetunedScorerDB.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(BaseFinetunedScorerDB | None | Unset, data)

        finetuned_scorer = _parse_finetuned_scorer(d.pop("finetuned_scorer", UNSET))

        def _parse_model_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        def _parse_num_judges(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        def _parse_scoreable_node_types(data: object) -> list[str] | None | Unset:
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
            return cast(list[str] | None | Unset, data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        def _parse_cot_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        cot_enabled = _parse_cot_enabled(d.pop("cot_enabled", UNSET))

        def _parse_output_type(data: object) -> None | OutputTypeEnum | Unset:
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
            return cast(None | OutputTypeEnum | Unset, data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        def _parse_input_type(data: object) -> InputTypeEnum | None | Unset:
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
            return cast(InputTypeEnum | None | Unset, data)

        input_type = _parse_input_type(d.pop("input_type", UNSET))

        base_scorer_version_db = cls(
            id=id,
            version=version,
            scorer_id=scorer_id,
            generated_scorer=generated_scorer,
            registered_scorer=registered_scorer,
            finetuned_scorer=finetuned_scorer,
            model_name=model_name,
            num_judges=num_judges,
            scoreable_node_types=scoreable_node_types,
            cot_enabled=cot_enabled,
            output_type=output_type,
            input_type=input_type,
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
