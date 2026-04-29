from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
    from ..models.chain_poll_template import ChainPollTemplate
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.generated_scorer_configuration import GeneratedScorerConfiguration
    from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
    from ..models.log_records_collection_filter import LogRecordsCollectionFilter
    from ..models.log_records_date_filter import LogRecordsDateFilter
    from ..models.log_records_id_filter import LogRecordsIDFilter
    from ..models.log_records_number_filter import LogRecordsNumberFilter
    from ..models.log_records_sort_clause import LogRecordsSortClause
    from ..models.log_records_text_filter import LogRecordsTextFilter
    from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
    from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter


T = TypeVar("T", bound="ValidateLLMScorerLogRecordRequest")


@_attrs_define
class ValidateLLMScorerLogRecordRequest:
    """Request to validate a new LLM scorer based on a log record.
    This is used to create a new experiment with the copied log records to store the metric testing results.

    Attributes
    ----------
            query (str):
            response (str):
            chain_poll_template (ChainPollTemplate): Template for a chainpoll metric prompt,
                containing all the info necessary to send a chainpoll prompt.
            scorer_configuration (GeneratedScorerConfiguration):
            user_prompt (str):
            starting_token (Union[Unset, int]):  Default: 0.
            limit (Union[Unset, int]):  Default: 100.
            previous_last_row_id (Union[None, Unset, str]):
            log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
            experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
            metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
            filters (Union[Unset, list[Union['LogRecordsBooleanFilter', 'LogRecordsCollectionFilter',
                'LogRecordsDateFilter', 'LogRecordsIDFilter', 'LogRecordsNumberFilter', 'LogRecordsTextFilter']]]):
            filter_tree (Union['AndNodeLogRecordsFilter', 'FilterLeafLogRecordsFilter', 'NotNodeLogRecordsFilter',
                'OrNodeLogRecordsFilter', None, Unset]):
            sort (Union['LogRecordsSortClause', None, Unset]): Sort for the query.  Defaults to native sort (created_at, id
                descending).
            truncate_fields (Union[Unset, bool]):  Default: False.
            include_counts (Union[Unset, bool]): If True, include computed child counts (e.g., num_traces for sessions,
                num_spans for traces). Default: False.
    """

    query: str
    response: str
    chain_poll_template: "ChainPollTemplate"
    scorer_configuration: "GeneratedScorerConfiguration"
    user_prompt: str
    starting_token: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    previous_last_row_id: Union[None, Unset, str] = UNSET
    log_stream_id: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    metrics_testing_id: Union[None, Unset, str] = UNSET
    filters: Union[
        Unset,
        list[
            Union[
                "LogRecordsBooleanFilter",
                "LogRecordsCollectionFilter",
                "LogRecordsDateFilter",
                "LogRecordsIDFilter",
                "LogRecordsNumberFilter",
                "LogRecordsTextFilter",
            ]
        ],
    ] = UNSET
    filter_tree: Union[
        "AndNodeLogRecordsFilter",
        "FilterLeafLogRecordsFilter",
        "NotNodeLogRecordsFilter",
        "OrNodeLogRecordsFilter",
        None,
        Unset,
    ] = UNSET
    sort: Union["LogRecordsSortClause", None, Unset] = UNSET
    truncate_fields: Union[Unset, bool] = False
    include_counts: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
        from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter

        query = self.query

        response = self.response

        chain_poll_template = self.chain_poll_template.to_dict()

        scorer_configuration = self.scorer_configuration.to_dict()

        user_prompt = self.user_prompt

        starting_token = self.starting_token

        limit = self.limit

        previous_last_row_id: Union[None, Unset, str]
        previous_last_row_id = UNSET if isinstance(self.previous_last_row_id, Unset) else self.previous_last_row_id

        log_stream_id: Union[None, Unset, str]
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: Union[None, Unset, str]
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: Union[None, Unset, str]
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item: dict[str, Any]
                if isinstance(
                    filters_item_data,
                    (
                        LogRecordsIDFilter,
                        LogRecordsDateFilter,
                        LogRecordsNumberFilter,
                        LogRecordsBooleanFilter,
                        LogRecordsCollectionFilter,
                    ),
                ):
                    filters_item = filters_item_data.to_dict()
                else:
                    filters_item = filters_item_data.to_dict()

                filters.append(filters_item)

        filter_tree: Union[None, Unset, dict[str, Any]]
        if isinstance(self.filter_tree, Unset):
            filter_tree = UNSET
        elif isinstance(
            self.filter_tree,
            (FilterLeafLogRecordsFilter, AndNodeLogRecordsFilter, OrNodeLogRecordsFilter, NotNodeLogRecordsFilter),
        ):
            filter_tree = self.filter_tree.to_dict()
        else:
            filter_tree = self.filter_tree

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, LogRecordsSortClause):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        truncate_fields = self.truncate_fields

        include_counts = self.include_counts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
                "response": response,
                "chain_poll_template": chain_poll_template,
                "scorer_configuration": scorer_configuration,
                "user_prompt": user_prompt,
            }
        )
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if previous_last_row_id is not UNSET:
            field_dict["previous_last_row_id"] = previous_last_row_id
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if filters is not UNSET:
            field_dict["filters"] = filters
        if filter_tree is not UNSET:
            field_dict["filter_tree"] = filter_tree
        if sort is not UNSET:
            field_dict["sort"] = sort
        if truncate_fields is not UNSET:
            field_dict["truncate_fields"] = truncate_fields
        if include_counts is not UNSET:
            field_dict["include_counts"] = include_counts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter import AndNodeLogRecordsFilter
        from ..models.chain_poll_template import ChainPollTemplate
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.generated_scorer_configuration import GeneratedScorerConfiguration
        from ..models.log_records_boolean_filter import LogRecordsBooleanFilter
        from ..models.log_records_collection_filter import LogRecordsCollectionFilter
        from ..models.log_records_date_filter import LogRecordsDateFilter
        from ..models.log_records_id_filter import LogRecordsIDFilter
        from ..models.log_records_number_filter import LogRecordsNumberFilter
        from ..models.log_records_sort_clause import LogRecordsSortClause
        from ..models.log_records_text_filter import LogRecordsTextFilter
        from ..models.not_node_log_records_filter import NotNodeLogRecordsFilter
        from ..models.or_node_log_records_filter import OrNodeLogRecordsFilter

        d = dict(src_dict)
        query = d.pop("query")

        response = d.pop("response")

        chain_poll_template = ChainPollTemplate.from_dict(d.pop("chain_poll_template"))

        scorer_configuration = GeneratedScorerConfiguration.from_dict(d.pop("scorer_configuration"))

        user_prompt = d.pop("user_prompt")

        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        def _parse_previous_last_row_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        previous_last_row_id = _parse_previous_last_row_id(d.pop("previous_last_row_id", UNSET))

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:

            def _parse_filters_item(
                data: object,
            ) -> Union[
                "LogRecordsBooleanFilter",
                "LogRecordsCollectionFilter",
                "LogRecordsDateFilter",
                "LogRecordsIDFilter",
                "LogRecordsNumberFilter",
                "LogRecordsTextFilter",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsIDFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsDateFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsNumberFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsBooleanFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    return LogRecordsCollectionFilter.from_dict(data)

                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                return LogRecordsTextFilter.from_dict(data)

            filters_item = _parse_filters_item(filters_item_data)

            filters.append(filters_item)

        def _parse_filter_tree(
            data: object,
        ) -> Union[
            "AndNodeLogRecordsFilter",
            "FilterLeafLogRecordsFilter",
            "NotNodeLogRecordsFilter",
            "OrNodeLogRecordsFilter",
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
                return FilterLeafLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return AndNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return OrNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return NotNodeLogRecordsFilter.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "AndNodeLogRecordsFilter",
                    "FilterLeafLogRecordsFilter",
                    "NotNodeLogRecordsFilter",
                    "OrNodeLogRecordsFilter",
                    None,
                    Unset,
                ],
                data,
            )

        filter_tree = _parse_filter_tree(d.pop("filter_tree", UNSET))

        def _parse_sort(data: object) -> Union["LogRecordsSortClause", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return LogRecordsSortClause.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["LogRecordsSortClause", None, Unset], data)

        sort = _parse_sort(d.pop("sort", UNSET))

        truncate_fields = d.pop("truncate_fields", UNSET)

        include_counts = d.pop("include_counts", UNSET)

        validate_llm_scorer_log_record_request = cls(
            query=query,
            response=response,
            chain_poll_template=chain_poll_template,
            scorer_configuration=scorer_configuration,
            user_prompt=user_prompt,
            starting_token=starting_token,
            limit=limit,
            previous_last_row_id=previous_last_row_id,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            filters=filters,
            filter_tree=filter_tree,
            sort=sort,
            truncate_fields=truncate_fields,
            include_counts=include_counts,
        )

        validate_llm_scorer_log_record_request.additional_properties = d
        return validate_llm_scorer_log_record_request

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
