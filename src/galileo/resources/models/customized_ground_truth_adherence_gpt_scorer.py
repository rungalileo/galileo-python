from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_type_enum import InputTypeEnum
from ..models.luna_input_type_enum import LunaInputTypeEnum
from ..models.luna_output_type_enum import LunaOutputTypeEnum
from ..models.node_type import NodeType
from ..models.output_type_enum import OutputTypeEnum
from ..models.scorer_name import ScorerName
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customized_ground_truth_adherence_gpt_scorer_aggregates_type_0 import (
        CustomizedGroundTruthAdherenceGPTScorerAggregatesType0,
    )
    from ..models.customized_ground_truth_adherence_gpt_scorer_class_name_to_vocab_ix_type_0 import (
        CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0,
    )
    from ..models.customized_ground_truth_adherence_gpt_scorer_class_name_to_vocab_ix_type_1 import (
        CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1,
    )
    from ..models.customized_ground_truth_adherence_gpt_scorer_extra_type_0 import (
        CustomizedGroundTruthAdherenceGPTScorerExtraType0,
    )
    from ..models.ground_truth_adherence_template import GroundTruthAdherenceTemplate
    from ..models.metadata_filter import MetadataFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="CustomizedGroundTruthAdherenceGPTScorer")


@_attrs_define
class CustomizedGroundTruthAdherenceGPTScorer:
    """
    Attributes
    ----------
        aggregate_keys (Union[Unset, list[str]]):
        aggregates (Union['CustomizedGroundTruthAdherenceGPTScorerAggregatesType0', None, Unset]):
        can_copy_to_llm (Union[None, Unset, bool]):
        chainpoll_template (Union[Unset, GroundTruthAdherenceTemplate]):
        class_name_to_vocab_ix (Union['CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0',
            'CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1', None, Unset]):
        cot_enabled (Union[None, Unset, bool]):
        description (Union[None, Unset, str]):
        extra (Union['CustomizedGroundTruthAdherenceGPTScorerExtraType0', None, Unset]):
        filters (Union[None, Unset, list[Union['MetadataFilter', 'NodeNameFilter']]]):
        generated_scorer_id (Union[None, Unset, str]):
        ground_truth (Union[None, Unset, bool]):
        indices (Union[None, Unset, list[int]]):
        input_type (Union[InputTypeEnum, None, Unset]):
        lora_task_id (Union[None, Unset, int]):
        luna_input_type (Union[LunaInputTypeEnum, None, Unset]):
        luna_output_type (Union[LunaOutputTypeEnum, None, Unset]):
        metric_name (Union[None, Unset, str]):
        model_alias (Union[Unset, str]):  Default: 'gpt-4.1-mini'.
        name (Union[Literal['ground_truth_adherence'], Unset]):  Default: 'ground_truth_adherence'.
        num_judges (Union[Unset, int]):  Default: 3.
        output_type (Union[None, OutputTypeEnum, Unset]):
        prompt (Union[None, Unset, str]):
        regex_field (Union[Unset, str]):  Default: ''.
        registered_scorer_id (Union[None, Unset, str]):
        required_scorers (Union[None, Unset, list[str]]):
        scoreable_node_types (Union[None, Unset, list[NodeType]]):
        scorer_name (Union[Literal['_customized_ground_truth_adherence'], Unset]):  Default:
            '_customized_ground_truth_adherence'.
        scores (Union[None, Unset, list[Any]]):
        sub_scorers (Union[Unset, list[ScorerName]]):
    """

    aggregate_keys: Union[Unset, list[str]] = UNSET
    aggregates: Union["CustomizedGroundTruthAdherenceGPTScorerAggregatesType0", None, Unset] = UNSET
    can_copy_to_llm: Union[None, Unset, bool] = UNSET
    chainpoll_template: Union[Unset, "GroundTruthAdherenceTemplate"] = UNSET
    class_name_to_vocab_ix: Union[
        "CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0",
        "CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1",
        None,
        Unset,
    ] = UNSET
    cot_enabled: Union[None, Unset, bool] = UNSET
    description: Union[None, Unset, str] = UNSET
    extra: Union["CustomizedGroundTruthAdherenceGPTScorerExtraType0", None, Unset] = UNSET
    filters: Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]] = UNSET
    generated_scorer_id: Union[None, Unset, str] = UNSET
    ground_truth: Union[None, Unset, bool] = UNSET
    indices: Union[None, Unset, list[int]] = UNSET
    input_type: Union[InputTypeEnum, None, Unset] = UNSET
    lora_task_id: Union[None, Unset, int] = UNSET
    luna_input_type: Union[LunaInputTypeEnum, None, Unset] = UNSET
    luna_output_type: Union[LunaOutputTypeEnum, None, Unset] = UNSET
    metric_name: Union[None, Unset, str] = UNSET
    model_alias: Union[Unset, str] = "gpt-4.1-mini"
    name: Union[Literal["ground_truth_adherence"], Unset] = "ground_truth_adherence"
    num_judges: Union[Unset, int] = 3
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    regex_field: Union[Unset, str] = ""
    registered_scorer_id: Union[None, Unset, str] = UNSET
    required_scorers: Union[None, Unset, list[str]] = UNSET
    scoreable_node_types: Union[None, Unset, list[NodeType]] = UNSET
    scorer_name: Union[Literal["_customized_ground_truth_adherence"], Unset] = "_customized_ground_truth_adherence"
    scores: Union[None, Unset, list[Any]] = UNSET
    sub_scorers: Union[Unset, list[ScorerName]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customized_ground_truth_adherence_gpt_scorer_aggregates_type_0 import (
            CustomizedGroundTruthAdherenceGPTScorerAggregatesType0,
        )
        from ..models.customized_ground_truth_adherence_gpt_scorer_class_name_to_vocab_ix_type_0 import (
            CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0,
        )
        from ..models.customized_ground_truth_adherence_gpt_scorer_class_name_to_vocab_ix_type_1 import (
            CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1,
        )
        from ..models.customized_ground_truth_adherence_gpt_scorer_extra_type_0 import (
            CustomizedGroundTruthAdherenceGPTScorerExtraType0,
        )
        from ..models.node_name_filter import NodeNameFilter

        aggregate_keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.aggregate_keys, Unset):
            aggregate_keys = self.aggregate_keys

        aggregates: Union[None, Unset, dict[str, Any]]
        if isinstance(self.aggregates, Unset):
            aggregates = UNSET
        elif isinstance(self.aggregates, CustomizedGroundTruthAdherenceGPTScorerAggregatesType0):
            aggregates = self.aggregates.to_dict()
        else:
            aggregates = self.aggregates

        can_copy_to_llm: Union[None, Unset, bool]
        can_copy_to_llm = UNSET if isinstance(self.can_copy_to_llm, Unset) else self.can_copy_to_llm

        chainpoll_template: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.chainpoll_template, Unset):
            chainpoll_template = self.chainpoll_template.to_dict()

        class_name_to_vocab_ix: Union[None, Unset, dict[str, Any]]
        if isinstance(self.class_name_to_vocab_ix, Unset):
            class_name_to_vocab_ix = UNSET
        elif isinstance(
            self.class_name_to_vocab_ix,
            (
                CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0,
                CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1,
            ),
        ):
            class_name_to_vocab_ix = self.class_name_to_vocab_ix.to_dict()
        else:
            class_name_to_vocab_ix = self.class_name_to_vocab_ix

        cot_enabled: Union[None, Unset, bool]
        cot_enabled = UNSET if isinstance(self.cot_enabled, Unset) else self.cot_enabled

        description: Union[None, Unset, str]
        description = UNSET if isinstance(self.description, Unset) else self.description

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, CustomizedGroundTruthAdherenceGPTScorerExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

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

        generated_scorer_id: Union[None, Unset, str]
        generated_scorer_id = UNSET if isinstance(self.generated_scorer_id, Unset) else self.generated_scorer_id

        ground_truth: Union[None, Unset, bool]
        ground_truth = UNSET if isinstance(self.ground_truth, Unset) else self.ground_truth

        indices: Union[None, Unset, list[int]]
        if isinstance(self.indices, Unset):
            indices = UNSET
        elif isinstance(self.indices, list):
            indices = self.indices

        else:
            indices = self.indices

        input_type: Union[None, Unset, str]
        if isinstance(self.input_type, Unset):
            input_type = UNSET
        elif isinstance(self.input_type, InputTypeEnum):
            input_type = self.input_type.value
        else:
            input_type = self.input_type

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

        metric_name: Union[None, Unset, str]
        metric_name = UNSET if isinstance(self.metric_name, Unset) else self.metric_name

        model_alias = self.model_alias

        name = self.name

        num_judges = self.num_judges

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, OutputTypeEnum):
            output_type = self.output_type.value
        else:
            output_type = self.output_type

        prompt: Union[None, Unset, str]
        prompt = UNSET if isinstance(self.prompt, Unset) else self.prompt

        regex_field = self.regex_field

        registered_scorer_id: Union[None, Unset, str]
        registered_scorer_id = UNSET if isinstance(self.registered_scorer_id, Unset) else self.registered_scorer_id

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
            scoreable_node_types = []
            for scoreable_node_types_type_0_item_data in self.scoreable_node_types:
                scoreable_node_types_type_0_item = scoreable_node_types_type_0_item_data.value
                scoreable_node_types.append(scoreable_node_types_type_0_item)

        else:
            scoreable_node_types = self.scoreable_node_types

        scorer_name = self.scorer_name

        scores: Union[None, Unset, list[Any]]
        if isinstance(self.scores, Unset):
            scores = UNSET
        elif isinstance(self.scores, list):
            scores = self.scores

        else:
            scores = self.scores

        sub_scorers: Union[Unset, list[str]] = UNSET
        if not isinstance(self.sub_scorers, Unset):
            sub_scorers = []
            for sub_scorers_item_data in self.sub_scorers:
                sub_scorers_item = sub_scorers_item_data.value
                sub_scorers.append(sub_scorers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aggregate_keys is not UNSET:
            field_dict["aggregate_keys"] = aggregate_keys
        if aggregates is not UNSET:
            field_dict["aggregates"] = aggregates
        if can_copy_to_llm is not UNSET:
            field_dict["can_copy_to_llm"] = can_copy_to_llm
        if chainpoll_template is not UNSET:
            field_dict["chainpoll_template"] = chainpoll_template
        if class_name_to_vocab_ix is not UNSET:
            field_dict["class_name_to_vocab_ix"] = class_name_to_vocab_ix
        if cot_enabled is not UNSET:
            field_dict["cot_enabled"] = cot_enabled
        if description is not UNSET:
            field_dict["description"] = description
        if extra is not UNSET:
            field_dict["extra"] = extra
        if filters is not UNSET:
            field_dict["filters"] = filters
        if generated_scorer_id is not UNSET:
            field_dict["generated_scorer_id"] = generated_scorer_id
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if indices is not UNSET:
            field_dict["indices"] = indices
        if input_type is not UNSET:
            field_dict["input_type"] = input_type
        if lora_task_id is not UNSET:
            field_dict["lora_task_id"] = lora_task_id
        if luna_input_type is not UNSET:
            field_dict["luna_input_type"] = luna_input_type
        if luna_output_type is not UNSET:
            field_dict["luna_output_type"] = luna_output_type
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if name is not UNSET:
            field_dict["name"] = name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if regex_field is not UNSET:
            field_dict["regex_field"] = regex_field
        if registered_scorer_id is not UNSET:
            field_dict["registered_scorer_id"] = registered_scorer_id
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if scorer_name is not UNSET:
            field_dict["scorer_name"] = scorer_name
        if scores is not UNSET:
            field_dict["scores"] = scores
        if sub_scorers is not UNSET:
            field_dict["sub_scorers"] = sub_scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.customized_ground_truth_adherence_gpt_scorer_aggregates_type_0 import (
            CustomizedGroundTruthAdherenceGPTScorerAggregatesType0,
        )
        from ..models.customized_ground_truth_adherence_gpt_scorer_class_name_to_vocab_ix_type_0 import (
            CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0,
        )
        from ..models.customized_ground_truth_adherence_gpt_scorer_class_name_to_vocab_ix_type_1 import (
            CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1,
        )
        from ..models.customized_ground_truth_adherence_gpt_scorer_extra_type_0 import (
            CustomizedGroundTruthAdherenceGPTScorerExtraType0,
        )
        from ..models.ground_truth_adherence_template import GroundTruthAdherenceTemplate
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        d = dict(src_dict)
        aggregate_keys = cast(list[str], d.pop("aggregate_keys", UNSET))

        def _parse_aggregates(
            data: object,
        ) -> Union["CustomizedGroundTruthAdherenceGPTScorerAggregatesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomizedGroundTruthAdherenceGPTScorerAggregatesType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CustomizedGroundTruthAdherenceGPTScorerAggregatesType0", None, Unset], data)

        aggregates = _parse_aggregates(d.pop("aggregates", UNSET))

        def _parse_can_copy_to_llm(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        can_copy_to_llm = _parse_can_copy_to_llm(d.pop("can_copy_to_llm", UNSET))

        _chainpoll_template = d.pop("chainpoll_template", UNSET)
        chainpoll_template: Union[Unset, GroundTruthAdherenceTemplate]
        if isinstance(_chainpoll_template, Unset):
            chainpoll_template = UNSET
        else:
            chainpoll_template = GroundTruthAdherenceTemplate.from_dict(_chainpoll_template)

        def _parse_class_name_to_vocab_ix(
            data: object,
        ) -> Union[
            "CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0",
            "CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1",
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
                return CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType0",
                    "CustomizedGroundTruthAdherenceGPTScorerClassNameToVocabIxType1",
                    None,
                    Unset,
                ],
                data,
            )

        class_name_to_vocab_ix = _parse_class_name_to_vocab_ix(d.pop("class_name_to_vocab_ix", UNSET))

        def _parse_cot_enabled(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        cot_enabled = _parse_cot_enabled(d.pop("cot_enabled", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_extra(data: object) -> Union["CustomizedGroundTruthAdherenceGPTScorerExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomizedGroundTruthAdherenceGPTScorerExtraType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CustomizedGroundTruthAdherenceGPTScorerExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

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

        def _parse_generated_scorer_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        generated_scorer_id = _parse_generated_scorer_id(d.pop("generated_scorer_id", UNSET))

        def _parse_ground_truth(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

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

        def _parse_metric_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_name = _parse_metric_name(d.pop("metric_name", UNSET))

        model_alias = d.pop("model_alias", UNSET)

        name = cast(Union[Literal["ground_truth_adherence"], Unset], d.pop("name", UNSET))
        if name != "ground_truth_adherence" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'ground_truth_adherence', got '{name}'")

        num_judges = d.pop("num_judges", UNSET)

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

        def _parse_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        regex_field = d.pop("regex_field", UNSET)

        def _parse_registered_scorer_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        registered_scorer_id = _parse_registered_scorer_id(d.pop("registered_scorer_id", UNSET))

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

        scorer_name = cast(Union[Literal["_customized_ground_truth_adherence"], Unset], d.pop("scorer_name", UNSET))
        if scorer_name != "_customized_ground_truth_adherence" and not isinstance(scorer_name, Unset):
            raise ValueError(f"scorer_name must match const '_customized_ground_truth_adherence', got '{scorer_name}'")

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

        sub_scorers = []
        _sub_scorers = d.pop("sub_scorers", UNSET)
        for sub_scorers_item_data in _sub_scorers or []:
            sub_scorers_item = ScorerName(sub_scorers_item_data)

            sub_scorers.append(sub_scorers_item)

        customized_ground_truth_adherence_gpt_scorer = cls(
            aggregate_keys=aggregate_keys,
            aggregates=aggregates,
            can_copy_to_llm=can_copy_to_llm,
            chainpoll_template=chainpoll_template,
            class_name_to_vocab_ix=class_name_to_vocab_ix,
            cot_enabled=cot_enabled,
            description=description,
            extra=extra,
            filters=filters,
            generated_scorer_id=generated_scorer_id,
            ground_truth=ground_truth,
            indices=indices,
            input_type=input_type,
            lora_task_id=lora_task_id,
            luna_input_type=luna_input_type,
            luna_output_type=luna_output_type,
            metric_name=metric_name,
            model_alias=model_alias,
            name=name,
            num_judges=num_judges,
            output_type=output_type,
            prompt=prompt,
            regex_field=regex_field,
            registered_scorer_id=registered_scorer_id,
            required_scorers=required_scorers,
            scoreable_node_types=scoreable_node_types,
            scorer_name=scorer_name,
            scores=scores,
            sub_scorers=sub_scorers,
        )

        customized_ground_truth_adherence_gpt_scorer.additional_properties = d
        return customized_ground_truth_adherence_gpt_scorer

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
