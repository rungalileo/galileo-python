import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.input_type_enum import InputTypeEnum
from ..models.output_type_enum import OutputTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.create_update_registered_scorer_response import CreateUpdateRegisteredScorerResponse
    from ..models.fine_tuned_scorer_response import FineTunedScorerResponse
    from ..models.generated_scorer_response import GeneratedScorerResponse


T = TypeVar("T", bound="BaseScorerVersionResponse")


@_attrs_define
class BaseScorerVersionResponse:
    """
    Attributes
    ----------
        id (str):
        version (int):
        scorer_id (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        generated_scorer (Union['GeneratedScorerResponse', None, Unset]):
        registered_scorer (Union['CreateUpdateRegisteredScorerResponse', None, Unset]):
        finetuned_scorer (Union['FineTunedScorerResponse', None, Unset]):
        model_name (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        scoreable_node_types (Union[None, Unset, list[str]]):
        cot_enabled (Union[None, Unset, bool]):
        output_type (Union[None, OutputTypeEnum, Unset]):
        input_type (Union[InputTypeEnum, None, Unset]): What type of input to use for model-based scorers
            (sessions_normalized, trace_io_only, etc.).
        chain_poll_template (Union['ChainPollTemplate', None, Unset]):
        allowed_model (Union[None, Unset, bool]):
    """

    id: str
    version: int
    scorer_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    generated_scorer: Union["GeneratedScorerResponse", None, Unset] = UNSET
    registered_scorer: Union["CreateUpdateRegisteredScorerResponse", None, Unset] = UNSET
    finetuned_scorer: Union["FineTunedScorerResponse", None, Unset] = UNSET
    model_name: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    scoreable_node_types: Union[None, Unset, list[str]] = UNSET
    cot_enabled: Union[None, Unset, bool] = UNSET
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    input_type: Union[InputTypeEnum, None, Unset] = UNSET
    chain_poll_template: Union["ChainPollTemplate", None, Unset] = UNSET
    allowed_model: Union[None, Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.create_update_registered_scorer_response import CreateUpdateRegisteredScorerResponse
        from ..models.fine_tuned_scorer_response import FineTunedScorerResponse
        from ..models.generated_scorer_response import GeneratedScorerResponse

        id = self.id

        version = self.version

        scorer_id = self.scorer_id

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        generated_scorer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.generated_scorer, Unset):
            generated_scorer = UNSET
        elif isinstance(self.generated_scorer, GeneratedScorerResponse):
            generated_scorer = self.generated_scorer.to_dict()
        else:
            generated_scorer = self.generated_scorer

        registered_scorer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.registered_scorer, Unset):
            registered_scorer = UNSET
        elif isinstance(self.registered_scorer, CreateUpdateRegisteredScorerResponse):
            registered_scorer = self.registered_scorer.to_dict()
        else:
            registered_scorer = self.registered_scorer

        finetuned_scorer: Union[None, Unset, dict[str, Any]]
        if isinstance(self.finetuned_scorer, Unset):
            finetuned_scorer = UNSET
        elif isinstance(self.finetuned_scorer, FineTunedScorerResponse):
            finetuned_scorer = self.finetuned_scorer.to_dict()
        else:
            finetuned_scorer = self.finetuned_scorer

        model_name: Union[None, Unset, str]
        model_name = UNSET if isinstance(self.model_name, Unset) else self.model_name

        num_judges: Union[None, Unset, int]
        num_judges = UNSET if isinstance(self.num_judges, Unset) else self.num_judges

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        cot_enabled: Union[None, Unset, bool]
        cot_enabled = UNSET if isinstance(self.cot_enabled, Unset) else self.cot_enabled

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

        chain_poll_template: Union[None, Unset, dict[str, Any]]
        if isinstance(self.chain_poll_template, Unset):
            chain_poll_template = UNSET
        elif isinstance(self.chain_poll_template, ChainPollTemplate):
            chain_poll_template = self.chain_poll_template.to_dict()
        else:
            chain_poll_template = self.chain_poll_template

        allowed_model: Union[None, Unset, bool]
        allowed_model = UNSET if isinstance(self.allowed_model, Unset) else self.allowed_model

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "version": version, "scorer_id": scorer_id, "created_at": created_at, "updated_at": updated_at}
        )
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
        if chain_poll_template is not UNSET:
            field_dict["chain_poll_template"] = chain_poll_template
        if allowed_model is not UNSET:
            field_dict["allowed_model"] = allowed_model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.create_update_registered_scorer_response import CreateUpdateRegisteredScorerResponse
        from ..models.fine_tuned_scorer_response import FineTunedScorerResponse
        from ..models.generated_scorer_response import GeneratedScorerResponse

        d = dict(src_dict)
        id = d.pop("id")

        version = d.pop("version")

        scorer_id = d.pop("scorer_id")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_generated_scorer(data: object) -> Union["GeneratedScorerResponse", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return GeneratedScorerResponse.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["GeneratedScorerResponse", None, Unset], data)

        generated_scorer = _parse_generated_scorer(d.pop("generated_scorer", UNSET))

        def _parse_registered_scorer(data: object) -> Union["CreateUpdateRegisteredScorerResponse", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CreateUpdateRegisteredScorerResponse.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CreateUpdateRegisteredScorerResponse", None, Unset], data)

        registered_scorer = _parse_registered_scorer(d.pop("registered_scorer", UNSET))

        def _parse_finetuned_scorer(data: object) -> Union["FineTunedScorerResponse", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return FineTunedScorerResponse.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["FineTunedScorerResponse", None, Unset], data)

        finetuned_scorer = _parse_finetuned_scorer(d.pop("finetuned_scorer", UNSET))

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

        def _parse_cot_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        cot_enabled = _parse_cot_enabled(d.pop("cot_enabled", UNSET))

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

        def _parse_chain_poll_template(data: object) -> Union["ChainPollTemplate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ChainPollTemplate.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ChainPollTemplate", None, Unset], data)

        chain_poll_template = _parse_chain_poll_template(d.pop("chain_poll_template", UNSET))

        def _parse_allowed_model(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        allowed_model = _parse_allowed_model(d.pop("allowed_model", UNSET))

        base_scorer_version_response = cls(
            id=id,
            version=version,
            scorer_id=scorer_id,
            created_at=created_at,
            updated_at=updated_at,
            generated_scorer=generated_scorer,
            registered_scorer=registered_scorer,
            finetuned_scorer=finetuned_scorer,
            model_name=model_name,
            num_judges=num_judges,
            scoreable_node_types=scoreable_node_types,
            cot_enabled=cot_enabled,
            output_type=output_type,
            input_type=input_type,
            chain_poll_template=chain_poll_template,
            allowed_model=allowed_model,
        )

        base_scorer_version_response.additional_properties = d
        return base_scorer_version_response

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
