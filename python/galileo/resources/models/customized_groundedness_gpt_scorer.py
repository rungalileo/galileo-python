from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.scorer_name import ScorerName
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.customized_groundedness_gpt_scorer_aggregates_type_0 import (
        CustomizedGroundednessGPTScorerAggregatesType0,
    )
    from ..models.customized_groundedness_gpt_scorer_extra_type_0 import CustomizedGroundednessGPTScorerExtraType0
    from ..models.groundedness_template import GroundednessTemplate
    from ..models.metadata_filter import MetadataFilter
    from ..models.node_name_filter import NodeNameFilter
    from ..models.prompt_run_settings import PromptRunSettings


T = TypeVar("T", bound="CustomizedGroundednessGPTScorer")


@_attrs_define
class CustomizedGroundednessGPTScorer:
    """
    Attributes:
        aggregate_keys (Union[Unset, list[str]]):
        aggregates (Union['CustomizedGroundednessGPTScorerAggregatesType0', None, Unset]):
        chainpoll_template (Union[Unset, GroundednessTemplate]): Template for the groundedness metric,
            containing all the info necessary to send the groundedness prompt.
        description (Union[None, Unset, str]):
        extra (Union['CustomizedGroundednessGPTScorerExtraType0', None, Unset]):
        filters (Union[None, Unset, list[Union['MetadataFilter', 'NodeNameFilter']]]):
        generated_scorer_id (Union[None, Unset, str]):
        gpt_settings (Union[Unset, PromptRunSettings]): Prompt run settings.
        indices (Union[None, Unset, list[int]]):
        metric_name (Union[None, Unset, str]):
        model_alias (Union[None, Unset, str]): Model alias to use for scoring.
        name (Union[Literal['context_adherence'], Unset]):  Default: 'context_adherence'.
        num_judges (Union[None, Unset, int]): Number of judges for the scorer.
        regex_field (Union[Unset, str]):  Default: ''.
        registered_scorer_id (Union[None, Unset, str]):
        scorer_name (Union[Literal['_customized_groundedness'], Unset]):  Default: '_customized_groundedness'.
        scores (Union[None, Unset, list[Any]]):
        sub_scorers (Union[Unset, list[ScorerName]]):
    """

    aggregate_keys: Union[Unset, list[str]] = UNSET
    aggregates: Union["CustomizedGroundednessGPTScorerAggregatesType0", None, Unset] = UNSET
    chainpoll_template: Union[Unset, "GroundednessTemplate"] = UNSET
    description: Union[None, Unset, str] = UNSET
    extra: Union["CustomizedGroundednessGPTScorerExtraType0", None, Unset] = UNSET
    filters: Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]] = UNSET
    generated_scorer_id: Union[None, Unset, str] = UNSET
    gpt_settings: Union[Unset, "PromptRunSettings"] = UNSET
    indices: Union[None, Unset, list[int]] = UNSET
    metric_name: Union[None, Unset, str] = UNSET
    model_alias: Union[None, Unset, str] = UNSET
    name: Union[Literal["context_adherence"], Unset] = "context_adherence"
    num_judges: Union[None, Unset, int] = UNSET
    regex_field: Union[Unset, str] = ""
    registered_scorer_id: Union[None, Unset, str] = UNSET
    scorer_name: Union[Literal["_customized_groundedness"], Unset] = "_customized_groundedness"
    scores: Union[None, Unset, list[Any]] = UNSET
    sub_scorers: Union[Unset, list[ScorerName]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.customized_groundedness_gpt_scorer_aggregates_type_0 import (
            CustomizedGroundednessGPTScorerAggregatesType0,
        )
        from ..models.customized_groundedness_gpt_scorer_extra_type_0 import CustomizedGroundednessGPTScorerExtraType0
        from ..models.node_name_filter import NodeNameFilter

        aggregate_keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.aggregate_keys, Unset):
            aggregate_keys = self.aggregate_keys

        aggregates: Union[None, Unset, dict[str, Any]]
        if isinstance(self.aggregates, Unset):
            aggregates = UNSET
        elif isinstance(self.aggregates, CustomizedGroundednessGPTScorerAggregatesType0):
            aggregates = self.aggregates.to_dict()
        else:
            aggregates = self.aggregates

        chainpoll_template: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.chainpoll_template, Unset):
            chainpoll_template = self.chainpoll_template.to_dict()

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, CustomizedGroundednessGPTScorerExtraType0):
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

        gpt_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.gpt_settings, Unset):
            gpt_settings = self.gpt_settings.to_dict()

        indices: Union[None, Unset, list[int]]
        if isinstance(self.indices, Unset):
            indices = UNSET
        elif isinstance(self.indices, list):
            indices = self.indices

        else:
            indices = self.indices

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

        regex_field = self.regex_field

        registered_scorer_id: Union[None, Unset, str]
        if isinstance(self.registered_scorer_id, Unset):
            registered_scorer_id = UNSET
        else:
            registered_scorer_id = self.registered_scorer_id

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
        if gpt_settings is not UNSET:
            field_dict["gpt_settings"] = gpt_settings
        if indices is not UNSET:
            field_dict["indices"] = indices
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if name is not UNSET:
            field_dict["name"] = name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if regex_field is not UNSET:
            field_dict["regex_field"] = regex_field
        if registered_scorer_id is not UNSET:
            field_dict["registered_scorer_id"] = registered_scorer_id
        if scorer_name is not UNSET:
            field_dict["scorer_name"] = scorer_name
        if scores is not UNSET:
            field_dict["scores"] = scores
        if sub_scorers is not UNSET:
            field_dict["sub_scorers"] = sub_scorers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.customized_groundedness_gpt_scorer_aggregates_type_0 import (
            CustomizedGroundednessGPTScorerAggregatesType0,
        )
        from ..models.customized_groundedness_gpt_scorer_extra_type_0 import CustomizedGroundednessGPTScorerExtraType0
        from ..models.groundedness_template import GroundednessTemplate
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter
        from ..models.prompt_run_settings import PromptRunSettings

        d = src_dict.copy()
        aggregate_keys = cast(list[str], d.pop("aggregate_keys", UNSET))

        def _parse_aggregates(data: object) -> Union["CustomizedGroundednessGPTScorerAggregatesType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                aggregates_type_0 = CustomizedGroundednessGPTScorerAggregatesType0.from_dict(data)

                return aggregates_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CustomizedGroundednessGPTScorerAggregatesType0", None, Unset], data)

        aggregates = _parse_aggregates(d.pop("aggregates", UNSET))

        _chainpoll_template = d.pop("chainpoll_template", UNSET)
        chainpoll_template: Union[Unset, GroundednessTemplate]
        if isinstance(_chainpoll_template, Unset):
            chainpoll_template = UNSET
        else:
            chainpoll_template = GroundednessTemplate.from_dict(_chainpoll_template)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_extra(data: object) -> Union["CustomizedGroundednessGPTScorerExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = CustomizedGroundednessGPTScorerExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CustomizedGroundednessGPTScorerExtraType0", None, Unset], data)

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

        _gpt_settings = d.pop("gpt_settings", UNSET)
        gpt_settings: Union[Unset, PromptRunSettings]
        if isinstance(_gpt_settings, Unset):
            gpt_settings = UNSET
        else:
            gpt_settings = PromptRunSettings.from_dict(_gpt_settings)

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

        name = cast(Union[Literal["context_adherence"], Unset], d.pop("name", UNSET))
        if name != "context_adherence" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'context_adherence', got '{name}'")

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        regex_field = d.pop("regex_field", UNSET)

        def _parse_registered_scorer_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        registered_scorer_id = _parse_registered_scorer_id(d.pop("registered_scorer_id", UNSET))

        scorer_name = cast(Union[Literal["_customized_groundedness"], Unset], d.pop("scorer_name", UNSET))
        if scorer_name != "_customized_groundedness" and not isinstance(scorer_name, Unset):
            raise ValueError(f"scorer_name must match const '_customized_groundedness', got '{scorer_name}'")

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

        customized_groundedness_gpt_scorer = cls(
            aggregate_keys=aggregate_keys,
            aggregates=aggregates,
            chainpoll_template=chainpoll_template,
            description=description,
            extra=extra,
            filters=filters,
            generated_scorer_id=generated_scorer_id,
            gpt_settings=gpt_settings,
            indices=indices,
            metric_name=metric_name,
            model_alias=model_alias,
            name=name,
            num_judges=num_judges,
            regex_field=regex_field,
            registered_scorer_id=registered_scorer_id,
            scorer_name=scorer_name,
            scores=scores,
            sub_scorers=sub_scorers,
        )

        customized_groundedness_gpt_scorer.additional_properties = d
        return customized_groundedness_gpt_scorer

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
