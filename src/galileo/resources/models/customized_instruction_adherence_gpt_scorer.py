from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_type_enum import InputTypeEnum
from ..models.luna_input_type_enum import LunaInputTypeEnum
from ..models.luna_output_type_enum import LunaOutputTypeEnum
from ..models.node_type import NodeType
from ..models.output_type_enum import OutputTypeEnum
from ..models.roll_up_strategy import RollUpStrategy
from ..models.scorer_name import ScorerName
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customized_instruction_adherence_gpt_scorer_aggregates_type_0 import (
        CustomizedInstructionAdherenceGPTScorerAggregatesType0,
    )
    from ..models.customized_instruction_adherence_gpt_scorer_class_name_to_vocab_ix_type_0 import (
        CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0,
    )
    from ..models.customized_instruction_adherence_gpt_scorer_class_name_to_vocab_ix_type_1 import (
        CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1,
    )
    from ..models.customized_instruction_adherence_gpt_scorer_extra_type_0 import (
        CustomizedInstructionAdherenceGPTScorerExtraType0,
    )
    from ..models.instruction_adherence_template import InstructionAdherenceTemplate
    from ..models.metadata_filter import MetadataFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="CustomizedInstructionAdherenceGPTScorer")


@_attrs_define
class CustomizedInstructionAdherenceGPTScorer:
    """
    Attributes
    ----------
        scorer_name (Union[Literal['_customized_instruction_adherence'], Unset]):  Default:
            '_customized_instruction_adherence'.
        model_alias (Union[Unset, str]):  Default: 'gpt-4.1-mini'.
        num_judges (Union[Unset, int]):  Default: 3.
        name (Union[Literal['instruction_adherence'], Unset]):  Default: 'instruction_adherence'.
        scores (Union[None, Unset, list[Any]]):
        indices (Union[None, Unset, list[int]]):
        aggregates (Union['CustomizedInstructionAdherenceGPTScorerAggregatesType0', None, Unset]):
        aggregate_keys (Union[Unset, list[str]]):
        extra (Union['CustomizedInstructionAdherenceGPTScorerExtraType0', None, Unset]):
        sub_scorers (Union[Unset, list[ScorerName]]):
        filters (Union[None, Unset, list[Union['MetadataFilter', 'NodeNameFilter']]]):
        metric_name (Union[None, Unset, str]):
        description (Union[None, Unset, str]):
        chainpoll_template (Union[Unset, InstructionAdherenceTemplate]):
        default_model_alias (Union[None, Unset, str]):
        ground_truth (Union[None, Unset, bool]):
        regex_field (Union[Unset, str]):  Default: ''.
        registered_scorer_id (Union[None, Unset, str]):
        generated_scorer_id (Union[None, Unset, str]):
        can_copy_to_llm (Union[None, Unset, bool]):
        scoreable_node_types (Union[None, Unset, list[NodeType]]):
        cot_enabled (Union[None, Unset, bool]):
        output_type (Union[None, OutputTypeEnum, Unset]):
        input_type (Union[InputTypeEnum, None, Unset]):
        required_scorers (Union[None, Unset, list[str]]):
        roll_up_strategy (Union[None, RollUpStrategy, Unset]):
        prompt (Union[None, Unset, str]):
        lora_task_id (Union[None, Unset, int]):
        luna_input_type (Union[LunaInputTypeEnum, None, Unset]):
        luna_output_type (Union[LunaOutputTypeEnum, None, Unset]):
        class_name_to_vocab_ix (Union['CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0',
            'CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1', None, Unset]):
        function_explanation_param_name (Union[Unset, str]):  Default: 'explanation'.
    """

    scorer_name: Union[Literal["_customized_instruction_adherence"], Unset] = "_customized_instruction_adherence"
    model_alias: Union[Unset, str] = "gpt-4.1-mini"
    num_judges: Union[Unset, int] = 3
    name: Union[Literal["instruction_adherence"], Unset] = "instruction_adherence"
    scores: Union[None, Unset, list[Any]] = UNSET
    indices: Union[None, Unset, list[int]] = UNSET
    aggregates: Union["CustomizedInstructionAdherenceGPTScorerAggregatesType0", None, Unset] = UNSET
    aggregate_keys: Union[Unset, list[str]] = UNSET
    extra: Union["CustomizedInstructionAdherenceGPTScorerExtraType0", None, Unset] = UNSET
    sub_scorers: Union[Unset, list[ScorerName]] = UNSET
    filters: Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]] = UNSET
    metric_name: Union[None, Unset, str] = UNSET
    description: Union[None, Unset, str] = UNSET
    chainpoll_template: Union[Unset, "InstructionAdherenceTemplate"] = UNSET
    default_model_alias: Union[None, Unset, str] = UNSET
    ground_truth: Union[None, Unset, bool] = UNSET
    regex_field: Union[Unset, str] = ""
    registered_scorer_id: Union[None, Unset, str] = UNSET
    generated_scorer_id: Union[None, Unset, str] = UNSET
    can_copy_to_llm: Union[None, Unset, bool] = UNSET
    scoreable_node_types: Union[None, Unset, list[NodeType]] = UNSET
    cot_enabled: Union[None, Unset, bool] = UNSET
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    input_type: Union[InputTypeEnum, None, Unset] = UNSET
    required_scorers: Union[None, Unset, list[str]] = UNSET
    roll_up_strategy: Union[None, RollUpStrategy, Unset] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    lora_task_id: Union[None, Unset, int] = UNSET
    luna_input_type: Union[LunaInputTypeEnum, None, Unset] = UNSET
    luna_output_type: Union[LunaOutputTypeEnum, None, Unset] = UNSET
    class_name_to_vocab_ix: Union[
        "CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0",
        "CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1",
        None,
        Unset,
    ] = UNSET
    function_explanation_param_name: Union[Unset, str] = "explanation"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customized_instruction_adherence_gpt_scorer_aggregates_type_0 import (
            CustomizedInstructionAdherenceGPTScorerAggregatesType0,
        )
        from ..models.customized_instruction_adherence_gpt_scorer_class_name_to_vocab_ix_type_0 import (
            CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0,
        )
        from ..models.customized_instruction_adherence_gpt_scorer_class_name_to_vocab_ix_type_1 import (
            CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1,
        )
        from ..models.customized_instruction_adherence_gpt_scorer_extra_type_0 import (
            CustomizedInstructionAdherenceGPTScorerExtraType0,
        )
        from ..models.node_name_filter import NodeNameFilter

        scorer_name = self.scorer_name

        model_alias = self.model_alias

        num_judges = self.num_judges

        name = self.name

        scores: Union[None, Unset, list[Any]]
        if isinstance(self.scores, Unset):
            scores = UNSET
        elif isinstance(self.scores, list):
            scores = self.scores

        else:
            scores = self.scores

        indices: Union[None, Unset, list[int]]
        if isinstance(self.indices, Unset):
            indices = UNSET
        elif isinstance(self.indices, list):
            indices = self.indices

        else:
            indices = self.indices

        aggregates: Union[None, Unset, dict[str, Any]]
        if isinstance(self.aggregates, Unset):
            aggregates = UNSET
        elif isinstance(self.aggregates, CustomizedInstructionAdherenceGPTScorerAggregatesType0):
            aggregates = self.aggregates.to_dict()
        else:
            aggregates = self.aggregates

        aggregate_keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.aggregate_keys, Unset):
            aggregate_keys = self.aggregate_keys

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, CustomizedInstructionAdherenceGPTScorerExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        sub_scorers: Union[Unset, list[str]] = UNSET
        if not isinstance(self.sub_scorers, Unset):
            sub_scorers = []
            for sub_scorers_item_data in self.sub_scorers:
                sub_scorers_item = sub_scorers_item_data.value
                sub_scorers.append(sub_scorers_item)

        filters: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.filters, Unset):
            filters = UNSET
        elif isinstance(self.filters, list):
            filters = []
            for filters_type_0_item_data in self.filters:
                filters_type_0_item: dict[str, Any]
                if isinstance(filters_type_0_item_data, NodeNameFilter):
                    filters_type_0_item = filters_type_0_item_data.to_dict()
                else:
                    filters_type_0_item = filters_type_0_item_data.to_dict()

                filters.append(filters_type_0_item)

        else:
            filters = self.filters

        metric_name: Union[None, Unset, str]
        metric_name = UNSET if isinstance(self.metric_name, Unset) else self.metric_name

        description: Union[None, Unset, str]
        description = UNSET if isinstance(self.description, Unset) else self.description

        chainpoll_template: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.chainpoll_template, Unset):
            chainpoll_template = self.chainpoll_template.to_dict()

        default_model_alias: Union[None, Unset, str]
        default_model_alias = UNSET if isinstance(self.default_model_alias, Unset) else self.default_model_alias

        ground_truth: Union[None, Unset, bool]
        ground_truth = UNSET if isinstance(self.ground_truth, Unset) else self.ground_truth

        regex_field = self.regex_field

        registered_scorer_id: Union[None, Unset, str]
        registered_scorer_id = UNSET if isinstance(self.registered_scorer_id, Unset) else self.registered_scorer_id

        generated_scorer_id: Union[None, Unset, str]
        generated_scorer_id = UNSET if isinstance(self.generated_scorer_id, Unset) else self.generated_scorer_id

        can_copy_to_llm: Union[None, Unset, bool]
        can_copy_to_llm = UNSET if isinstance(self.can_copy_to_llm, Unset) else self.can_copy_to_llm

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = []
            for scoreable_node_types_type_0_item_data in self.scoreable_node_types:
                scoreable_node_types_type_0_item = scoreable_node_types_type_0_item_data.value
                scoreable_node_types.append(scoreable_node_types_type_0_item)

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

        required_scorers: Union[None, Unset, list[str]]
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        roll_up_strategy: Union[None, Unset, str]
        if isinstance(self.roll_up_strategy, Unset):
            roll_up_strategy = UNSET
        elif isinstance(self.roll_up_strategy, RollUpStrategy):
            roll_up_strategy = self.roll_up_strategy.value
        else:
            roll_up_strategy = self.roll_up_strategy

        prompt: Union[None, Unset, str]
        prompt = UNSET if isinstance(self.prompt, Unset) else self.prompt

        lora_task_id: Union[None, Unset, int]
        lora_task_id = UNSET if isinstance(self.lora_task_id, Unset) else self.lora_task_id

        luna_input_type: Union[None, Unset, str]
        if isinstance(self.luna_input_type, Unset):
            luna_input_type = UNSET
        elif isinstance(self.luna_input_type, LunaInputTypeEnum):
            luna_input_type = self.luna_input_type.value
        else:
            luna_input_type = self.luna_input_type

        luna_output_type: Union[None, Unset, str]
        if isinstance(self.luna_output_type, Unset):
            luna_output_type = UNSET
        elif isinstance(self.luna_output_type, LunaOutputTypeEnum):
            luna_output_type = self.luna_output_type.value
        else:
            luna_output_type = self.luna_output_type

        class_name_to_vocab_ix: Union[None, Unset, dict[str, Any]]
        if isinstance(self.class_name_to_vocab_ix, Unset):
            class_name_to_vocab_ix = UNSET
        elif isinstance(
            self.class_name_to_vocab_ix,
            (
                CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0,
                CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1,
            ),
        ):
            class_name_to_vocab_ix = self.class_name_to_vocab_ix.to_dict()
        else:
            class_name_to_vocab_ix = self.class_name_to_vocab_ix

        function_explanation_param_name = self.function_explanation_param_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if scorer_name is not UNSET:
            field_dict["scorer_name"] = scorer_name
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if name is not UNSET:
            field_dict["name"] = name
        if scores is not UNSET:
            field_dict["scores"] = scores
        if indices is not UNSET:
            field_dict["indices"] = indices
        if aggregates is not UNSET:
            field_dict["aggregates"] = aggregates
        if aggregate_keys is not UNSET:
            field_dict["aggregate_keys"] = aggregate_keys
        if extra is not UNSET:
            field_dict["extra"] = extra
        if sub_scorers is not UNSET:
            field_dict["sub_scorers"] = sub_scorers
        if filters is not UNSET:
            field_dict["filters"] = filters
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if description is not UNSET:
            field_dict["description"] = description
        if chainpoll_template is not UNSET:
            field_dict["chainpoll_template"] = chainpoll_template
        if default_model_alias is not UNSET:
            field_dict["default_model_alias"] = default_model_alias
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if regex_field is not UNSET:
            field_dict["regex_field"] = regex_field
        if registered_scorer_id is not UNSET:
            field_dict["registered_scorer_id"] = registered_scorer_id
        if generated_scorer_id is not UNSET:
            field_dict["generated_scorer_id"] = generated_scorer_id
        if can_copy_to_llm is not UNSET:
            field_dict["can_copy_to_llm"] = can_copy_to_llm
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if cot_enabled is not UNSET:
            field_dict["cot_enabled"] = cot_enabled
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if input_type is not UNSET:
            field_dict["input_type"] = input_type
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if roll_up_strategy is not UNSET:
            field_dict["roll_up_strategy"] = roll_up_strategy
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if lora_task_id is not UNSET:
            field_dict["lora_task_id"] = lora_task_id
        if luna_input_type is not UNSET:
            field_dict["luna_input_type"] = luna_input_type
        if luna_output_type is not UNSET:
            field_dict["luna_output_type"] = luna_output_type
        if class_name_to_vocab_ix is not UNSET:
            field_dict["class_name_to_vocab_ix"] = class_name_to_vocab_ix
        if function_explanation_param_name is not UNSET:
            field_dict["function_explanation_param_name"] = function_explanation_param_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customized_instruction_adherence_gpt_scorer_aggregates_type_0 import (
            CustomizedInstructionAdherenceGPTScorerAggregatesType0,
        )
        from ..models.customized_instruction_adherence_gpt_scorer_class_name_to_vocab_ix_type_0 import (
            CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0,
        )
        from ..models.customized_instruction_adherence_gpt_scorer_class_name_to_vocab_ix_type_1 import (
            CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1,
        )
        from ..models.customized_instruction_adherence_gpt_scorer_extra_type_0 import (
            CustomizedInstructionAdherenceGPTScorerExtraType0,
        )
        from ..models.instruction_adherence_template import InstructionAdherenceTemplate
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        d = dict(src_dict)
        scorer_name = cast(Union[Literal["_customized_instruction_adherence"], Unset], d.pop("scorer_name", UNSET))
        if scorer_name != "_customized_instruction_adherence" and not isinstance(scorer_name, Unset):
            raise ValueError(f"scorer_name must match const '_customized_instruction_adherence', got '{scorer_name}'")

        model_alias = d.pop("model_alias", UNSET)

        num_judges = d.pop("num_judges", UNSET)

        name = cast(Union[Literal["instruction_adherence"], Unset], d.pop("name", UNSET))
        if name != "instruction_adherence" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'instruction_adherence', got '{name}'")

        def _parse_scores(data: object) -> Union[None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[Any], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Any]], data)

        scores = _parse_scores(d.pop("scores", UNSET))

        def _parse_indices(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[int], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        indices = _parse_indices(d.pop("indices", UNSET))

        def _parse_aggregates(
            data: object,
        ) -> Union["CustomizedInstructionAdherenceGPTScorerAggregatesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomizedInstructionAdherenceGPTScorerAggregatesType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CustomizedInstructionAdherenceGPTScorerAggregatesType0", None, Unset], data)

        aggregates = _parse_aggregates(d.pop("aggregates", UNSET))

        aggregate_keys = cast(list[str], d.pop("aggregate_keys", UNSET))

        def _parse_extra(data: object) -> Union["CustomizedInstructionAdherenceGPTScorerExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomizedInstructionAdherenceGPTScorerExtraType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CustomizedInstructionAdherenceGPTScorerExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        sub_scorers = []
        _sub_scorers = d.pop("sub_scorers", UNSET)
        for sub_scorers_item_data in _sub_scorers or []:
            sub_scorers_item = ScorerName(sub_scorers_item_data)

            sub_scorers.append(sub_scorers_item)

        def _parse_filters(data: object) -> Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filters_type_0 = []
                _filters_type_0 = data
                for filters_type_0_item_data in _filters_type_0:

                    def _parse_filters_type_0_item(data: object) -> Union["MetadataFilter", "NodeNameFilter"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return NodeNameFilter.from_dict(data)

                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        return MetadataFilter.from_dict(data)

                    filters_type_0_item = _parse_filters_type_0_item(filters_type_0_item_data)

                    filters_type_0.append(filters_type_0_item)

                return filters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]], data)

        filters = _parse_filters(d.pop("filters", UNSET))

        def _parse_metric_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_name = _parse_metric_name(d.pop("metric_name", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _chainpoll_template = d.pop("chainpoll_template", UNSET)
        chainpoll_template: Union[Unset, InstructionAdherenceTemplate]
        if isinstance(_chainpoll_template, Unset):
            chainpoll_template = UNSET
        else:
            chainpoll_template = InstructionAdherenceTemplate.from_dict(_chainpoll_template)

        def _parse_default_model_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_model_alias = _parse_default_model_alias(d.pop("default_model_alias", UNSET))

        def _parse_ground_truth(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        regex_field = d.pop("regex_field", UNSET)

        def _parse_registered_scorer_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        registered_scorer_id = _parse_registered_scorer_id(d.pop("registered_scorer_id", UNSET))

        def _parse_generated_scorer_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        generated_scorer_id = _parse_generated_scorer_id(d.pop("generated_scorer_id", UNSET))

        def _parse_can_copy_to_llm(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        can_copy_to_llm = _parse_can_copy_to_llm(d.pop("can_copy_to_llm", UNSET))

        def _parse_scoreable_node_types(data: object) -> Union[None, Unset, list[NodeType]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scoreable_node_types_type_0 = []
                _scoreable_node_types_type_0 = data
                for scoreable_node_types_type_0_item_data in _scoreable_node_types_type_0:
                    scoreable_node_types_type_0_item = NodeType(scoreable_node_types_type_0_item_data)

                    scoreable_node_types_type_0.append(scoreable_node_types_type_0_item)

                return scoreable_node_types_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[NodeType]], data)

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

        def _parse_roll_up_strategy(data: object) -> Union[None, RollUpStrategy, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return RollUpStrategy(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, RollUpStrategy, Unset], data)

        roll_up_strategy = _parse_roll_up_strategy(d.pop("roll_up_strategy", UNSET))

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_lora_task_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        lora_task_id = _parse_lora_task_id(d.pop("lora_task_id", UNSET))

        def _parse_luna_input_type(data: object) -> Union[LunaInputTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LunaInputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[LunaInputTypeEnum, None, Unset], data)

        luna_input_type = _parse_luna_input_type(d.pop("luna_input_type", UNSET))

        def _parse_luna_output_type(data: object) -> Union[LunaOutputTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LunaOutputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[LunaOutputTypeEnum, None, Unset], data)

        luna_output_type = _parse_luna_output_type(d.pop("luna_output_type", UNSET))

        def _parse_class_name_to_vocab_ix(
            data: object,
        ) -> Union[
            "CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0",
            "CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1",
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType0",
                    "CustomizedInstructionAdherenceGPTScorerClassNameToVocabIxType1",
                    None,
                    Unset,
                ],
                data,
            )

        class_name_to_vocab_ix = _parse_class_name_to_vocab_ix(d.pop("class_name_to_vocab_ix", UNSET))

        function_explanation_param_name = d.pop("function_explanation_param_name", UNSET)

        customized_instruction_adherence_gpt_scorer = cls(
            scorer_name=scorer_name,
            model_alias=model_alias,
            num_judges=num_judges,
            name=name,
            scores=scores,
            indices=indices,
            aggregates=aggregates,
            aggregate_keys=aggregate_keys,
            extra=extra,
            sub_scorers=sub_scorers,
            filters=filters,
            metric_name=metric_name,
            description=description,
            chainpoll_template=chainpoll_template,
            default_model_alias=default_model_alias,
            ground_truth=ground_truth,
            regex_field=regex_field,
            registered_scorer_id=registered_scorer_id,
            generated_scorer_id=generated_scorer_id,
            can_copy_to_llm=can_copy_to_llm,
            scoreable_node_types=scoreable_node_types,
            cot_enabled=cot_enabled,
            output_type=output_type,
            input_type=input_type,
            required_scorers=required_scorers,
            roll_up_strategy=roll_up_strategy,
            prompt=prompt,
            lora_task_id=lora_task_id,
            luna_input_type=luna_input_type,
            luna_output_type=luna_output_type,
            class_name_to_vocab_ix=class_name_to_vocab_ix,
            function_explanation_param_name=function_explanation_param_name,
        )

        customized_instruction_adherence_gpt_scorer.additional_properties = d
        return customized_instruction_adherence_gpt_scorer

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
