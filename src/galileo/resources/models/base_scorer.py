from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.node_type import NodeType
from ..models.scorer_name import ScorerName
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_scorer_aggregates_type_0 import BaseScorerAggregatesType0
    from ..models.base_scorer_extra_type_0 import BaseScorerExtraType0
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.metadata_filter import MetadataFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="BaseScorer")


@_attrs_define
class BaseScorer:
    """
    Attributes:
        aggregate_keys (Union[None, Unset, list[str]]):
        aggregates (Union['BaseScorerAggregatesType0', None, Unset]):
        chainpoll_template (Union['ChainPollTemplate', None, Unset]):
        description (Union[None, Unset, str]):
        extra (Union['BaseScorerExtraType0', None, Unset]):
        filters (Union[None, Unset, list[Union['MetadataFilter', 'NodeNameFilter']]]):
        generated_scorer_id (Union[None, Unset, str]):
        indices (Union[None, Unset, list[int]]):
        lora_task_id (Union[None, Unset, int]):
        metric_name (Union[None, Unset, str]):
        model_alias (Union[None, Unset, str]):
        name (Union[Unset, str]):  Default: ''.
        num_judges (Union[None, Unset, int]):
        prompt (Union[None, Unset, str]):
        regex_field (Union[Unset, str]):  Default: ''.
        registered_scorer_id (Union[None, Unset, str]):
        scoreable_node_types (Union[None, Unset, list[NodeType]]):
        scorer_name (Union[Unset, str]):  Default: ''.
        scores (Union[None, Unset, list[Any]]):
        sub_scorers (Union[Unset, list[ScorerName]]):
    """

    aggregate_keys: Union[None, Unset, list[str]] = UNSET
    aggregates: Union["BaseScorerAggregatesType0", None, Unset] = UNSET
    chainpoll_template: Union["ChainPollTemplate", None, Unset] = UNSET
    description: Union[None, Unset, str] = UNSET
    extra: Union["BaseScorerExtraType0", None, Unset] = UNSET
    filters: Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]] = UNSET
    generated_scorer_id: Union[None, Unset, str] = UNSET
    indices: Union[None, Unset, list[int]] = UNSET
    lora_task_id: Union[None, Unset, int] = UNSET
    metric_name: Union[None, Unset, str] = UNSET
    model_alias: Union[None, Unset, str] = UNSET
    name: Union[Unset, str] = ""
    num_judges: Union[None, Unset, int] = UNSET
    prompt: Union[None, Unset, str] = UNSET
    regex_field: Union[Unset, str] = ""
    registered_scorer_id: Union[None, Unset, str] = UNSET
    scoreable_node_types: Union[None, Unset, list[NodeType]] = UNSET
    scorer_name: Union[Unset, str] = ""
    scores: Union[None, Unset, list[Any]] = UNSET
    sub_scorers: Union[Unset, list[ScorerName]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_scorer_aggregates_type_0 import BaseScorerAggregatesType0
        from ..models.base_scorer_extra_type_0 import BaseScorerExtraType0
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.node_name_filter import NodeNameFilter

        aggregate_keys: Union[None, Unset, list[str]]
        if isinstance(self.aggregate_keys, Unset):
            aggregate_keys = UNSET
        elif isinstance(self.aggregate_keys, list):
            aggregate_keys = self.aggregate_keys

        else:
            aggregate_keys = self.aggregate_keys

        aggregates: Union[None, Unset, dict[str, Any]]
        if isinstance(self.aggregates, Unset):
            aggregates = UNSET
        elif isinstance(self.aggregates, BaseScorerAggregatesType0):
            aggregates = self.aggregates.to_dict()
        else:
            aggregates = self.aggregates

        chainpoll_template: Union[None, Unset, dict[str, Any]]
        if isinstance(self.chainpoll_template, Unset):
            chainpoll_template = UNSET
        elif isinstance(self.chainpoll_template, ChainPollTemplate):
            chainpoll_template = self.chainpoll_template.to_dict()
        else:
            chainpoll_template = self.chainpoll_template

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, BaseScorerExtraType0):
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
        if isinstance(self.generated_scorer_id, Unset):
            generated_scorer_id = UNSET
        else:
            generated_scorer_id = self.generated_scorer_id

        indices: Union[None, Unset, list[int]]
        if isinstance(self.indices, Unset):
            indices = UNSET
        elif isinstance(self.indices, list):
            indices = self.indices

        else:
            indices = self.indices

        lora_task_id: Union[None, Unset, int]
        if isinstance(self.lora_task_id, Unset):
            lora_task_id = UNSET
        else:
            lora_task_id = self.lora_task_id

        metric_name: Union[None, Unset, str]
        if isinstance(self.metric_name, Unset):
            metric_name = UNSET
        else:
            metric_name = self.metric_name

        model_alias: Union[None, Unset, str]
        if isinstance(self.model_alias, Unset):
            model_alias = UNSET
        else:
            model_alias = self.model_alias

        name = self.name

        num_judges: Union[None, Unset, int]
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        prompt: Union[None, Unset, str]
        if isinstance(self.prompt, Unset):
            prompt = UNSET
        else:
            prompt = self.prompt

        regex_field = self.regex_field

        registered_scorer_id: Union[None, Unset, str]
        if isinstance(self.registered_scorer_id, Unset):
            registered_scorer_id = UNSET
        else:
            registered_scorer_id = self.registered_scorer_id

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
        if chainpoll_template is not UNSET:
            field_dict["chainpoll_template"] = chainpoll_template
        if description is not UNSET:
            field_dict["description"] = description
        if extra is not UNSET:
            field_dict["extra"] = extra
        if filters is not UNSET:
            field_dict["filters"] = filters
        if generated_scorer_id is not UNSET:
            field_dict["generated_scorer_id"] = generated_scorer_id
        if indices is not UNSET:
            field_dict["indices"] = indices
        if lora_task_id is not UNSET:
            field_dict["lora_task_id"] = lora_task_id
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if name is not UNSET:
            field_dict["name"] = name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if regex_field is not UNSET:
            field_dict["regex_field"] = regex_field
        if registered_scorer_id is not UNSET:
            field_dict["registered_scorer_id"] = registered_scorer_id
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
        from ..models.base_scorer_aggregates_type_0 import BaseScorerAggregatesType0
        from ..models.base_scorer_extra_type_0 import BaseScorerExtraType0
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        d = dict(src_dict)

        def _parse_aggregate_keys(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                aggregate_keys_type_0 = cast(list[str], data)

                return aggregate_keys_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        aggregate_keys = _parse_aggregate_keys(d.pop("aggregate_keys", UNSET))

        def _parse_aggregates(data: object) -> Union["BaseScorerAggregatesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregates_type_0 = BaseScorerAggregatesType0.from_dict(data)

                return aggregates_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseScorerAggregatesType0", None, Unset], data)

        aggregates = _parse_aggregates(d.pop("aggregates", UNSET))

        def _parse_chainpoll_template(data: object) -> Union["ChainPollTemplate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                chainpoll_template_type_0 = ChainPollTemplate.from_dict(data)

                return chainpoll_template_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ChainPollTemplate", None, Unset], data)

        chainpoll_template = _parse_chainpoll_template(d.pop("chainpoll_template", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_extra(data: object) -> Union["BaseScorerExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = BaseScorerExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseScorerExtraType0", None, Unset], data)

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
                            filters_type_0_item_type_0 = NodeNameFilter.from_dict(data)

                            return filters_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_type_0_item_type_1 = MetadataFilter.from_dict(data)

                        return filters_type_0_item_type_1

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

        def _parse_indices(data: object) -> Union[None, Unset, list[int]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                indices_type_0 = cast(list[int], data)

                return indices_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[int]], data)

        indices = _parse_indices(d.pop("indices", UNSET))

        def _parse_lora_task_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        lora_task_id = _parse_lora_task_id(d.pop("lora_task_id", UNSET))

        def _parse_metric_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_name = _parse_metric_name(d.pop("metric_name", UNSET))

        def _parse_model_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_alias = _parse_model_alias(d.pop("model_alias", UNSET))

        name = d.pop("name", UNSET)

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

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

        scorer_name = d.pop("scorer_name", UNSET)

        def _parse_scores(data: object) -> Union[None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scores_type_0 = cast(list[Any], data)

                return scores_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Any]], data)

        scores = _parse_scores(d.pop("scores", UNSET))

        sub_scorers = []
        _sub_scorers = d.pop("sub_scorers", UNSET)
        for sub_scorers_item_data in _sub_scorers or []:
            sub_scorers_item = ScorerName(sub_scorers_item_data)

            sub_scorers.append(sub_scorers_item)

        base_scorer = cls(
            aggregate_keys=aggregate_keys,
            aggregates=aggregates,
            chainpoll_template=chainpoll_template,
            description=description,
            extra=extra,
            filters=filters,
            generated_scorer_id=generated_scorer_id,
            indices=indices,
            lora_task_id=lora_task_id,
            metric_name=metric_name,
            model_alias=model_alias,
            name=name,
            num_judges=num_judges,
            prompt=prompt,
            regex_field=regex_field,
            registered_scorer_id=registered_scorer_id,
            scoreable_node_types=scoreable_node_types,
            scorer_name=scorer_name,
            scores=scores,
            sub_scorers=sub_scorers,
        )

        base_scorer.additional_properties = d
        return base_scorer

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
