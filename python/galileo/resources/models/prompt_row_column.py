import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.job_status import JobStatus
from ..models.scorer_type import ScorerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alert import Alert
    from ..models.document import Document
    from ..models.feedback_aggregate import FeedbackAggregate
    from ..models.feedback_rating_db import FeedbackRatingDB
    from ..models.hallucination_segment import HallucinationSegment
    from ..models.job_info import JobInfo
    from ..models.metric_computing import MetricComputing
    from ..models.metric_error import MetricError
    from ..models.metric_failed import MetricFailed
    from ..models.metric_not_applicable import MetricNotApplicable
    from ..models.metric_not_computed import MetricNotComputed
    from ..models.metric_pending import MetricPending
    from ..models.metric_success import MetricSuccess
    from ..models.metric_threshold import MetricThreshold
    from ..models.segment import Segment


T = TypeVar("T", bound="PromptRowColumn")


@_attrs_define
class PromptRowColumn:
    """
    Attributes:
        name (str): Name of the column.
        alert (Union['Alert', None, Unset]): Alert for a given column with title and message
        can_critique_column (Union[Unset, bool]):  Default: False.
        data_type (Union[Unset, Any]): Data type of the column. This is used to determine how to format the data on the
            UI. Default: 'unknown'.
        description (Union[None, Unset, str]): Description of the column.
        display_values (Union[None, Unset, list[Union[None, str]]]): Display values of the column. This is used to
            display the values in the UI if we want them to be different from the actual values.
        filterable (Union[Unset, bool]): Whether the column is filterable by value. Doesn't include categorical filters
            Default: True.
        group_description (Union[None, Unset, str]): Description of the group (super column).
        group_label (Union[None, Unset, str]): Display label of the group (super column) in the UI.
        group_name (Union[None, Unset, str]): Name of the group (super column).
        job_error_message (Union[None, Unset, str]): Error message to show the users on hover in case the job fails or
            errors out.
        job_info (Union[None, Unset, list[Union['JobInfo', None]]]): Job info used for computing the column. Only
            present for metrics columns that have a separate scorer job.
        job_progress_message (Union[None, Unset, str]): Progress message to show the users on hover in case the job is
            in progress.
        job_status (Union[JobStatus, None, Unset]): Job status used for computing the column. Only set for metrics
            columns that have a separate scorer job.
        job_type (Union[None, ScorerType, Unset]): If a column is associated with a basic or a plus scorer. Defaults to
            None for columns not associated with either.
        label (Union[None, Unset, str]): Display label of the column in the UI.
        metric_critique_computing (Union[Unset, bool]):  Default: False.
        metric_infos (Union[Unset, list[Union['MetricComputing', 'MetricError', 'MetricFailed', 'MetricNotApplicable',
            'MetricNotComputed', 'MetricPending', 'MetricSuccess']]]): Metric values with metadata.
        metric_threshold (Union['MetricThreshold', None, Unset]): Thresholds for the column, if this is a metrics
            column.
        scorer_name (Union[None, Unset, str]): Scorer Name executed by the job.
        sortable (Union[Unset, bool]): Whether the column is sortable. Default: True.
        source (Union[None, Unset, str]): Source DF of the column.
        values (Union[Unset, list[Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB', 'HallucinationSegment',
            'Segment', None, UUID, bool, datetime.datetime, float, int, list[Union['Document', 'FeedbackAggregate',
            'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None, UUID, bool, datetime.datetime, float, int, str]],
            list[list[Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None,
            UUID, bool, datetime.datetime, float, int, str]]], list[list[list[Union['Document', 'FeedbackAggregate',
            'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None, UUID, bool, datetime.datetime, float, int, str]]]],
            str]]]): Values of the column.
    """

    name: str
    alert: Union["Alert", None, Unset] = UNSET
    can_critique_column: Union[Unset, bool] = False
    data_type: Union[Unset, Any] = "unknown"
    description: Union[None, Unset, str] = UNSET
    display_values: Union[None, Unset, list[Union[None, str]]] = UNSET
    filterable: Union[Unset, bool] = True
    group_description: Union[None, Unset, str] = UNSET
    group_label: Union[None, Unset, str] = UNSET
    group_name: Union[None, Unset, str] = UNSET
    job_error_message: Union[None, Unset, str] = UNSET
    job_info: Union[None, Unset, list[Union["JobInfo", None]]] = UNSET
    job_progress_message: Union[None, Unset, str] = UNSET
    job_status: Union[JobStatus, None, Unset] = UNSET
    job_type: Union[None, ScorerType, Unset] = UNSET
    label: Union[None, Unset, str] = UNSET
    metric_critique_computing: Union[Unset, bool] = False
    metric_infos: Union[
        Unset,
        list[
            Union[
                "MetricComputing",
                "MetricError",
                "MetricFailed",
                "MetricNotApplicable",
                "MetricNotComputed",
                "MetricPending",
                "MetricSuccess",
            ]
        ],
    ] = UNSET
    metric_threshold: Union["MetricThreshold", None, Unset] = UNSET
    scorer_name: Union[None, Unset, str] = UNSET
    sortable: Union[Unset, bool] = True
    source: Union[None, Unset, str] = UNSET
    values: Union[
        Unset,
        list[
            Union[
                "Document",
                "FeedbackAggregate",
                "FeedbackRatingDB",
                "HallucinationSegment",
                "Segment",
                None,
                UUID,
                bool,
                datetime.datetime,
                float,
                int,
                list[
                    Union[
                        "Document",
                        "FeedbackAggregate",
                        "FeedbackRatingDB",
                        "HallucinationSegment",
                        "Segment",
                        None,
                        UUID,
                        bool,
                        datetime.datetime,
                        float,
                        int,
                        str,
                    ]
                ],
                list[
                    list[
                        Union[
                            "Document",
                            "FeedbackAggregate",
                            "FeedbackRatingDB",
                            "HallucinationSegment",
                            "Segment",
                            None,
                            UUID,
                            bool,
                            datetime.datetime,
                            float,
                            int,
                            str,
                        ]
                    ]
                ],
                list[
                    list[
                        list[
                            Union[
                                "Document",
                                "FeedbackAggregate",
                                "FeedbackRatingDB",
                                "HallucinationSegment",
                                "Segment",
                                None,
                                UUID,
                                bool,
                                datetime.datetime,
                                float,
                                int,
                                str,
                            ]
                        ]
                    ]
                ],
                str,
            ]
        ],
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.alert import Alert
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.job_info import JobInfo
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_success import MetricSuccess
        from ..models.metric_threshold import MetricThreshold
        from ..models.segment import Segment

        name = self.name

        alert: Union[None, Unset, dict[str, Any]]
        if isinstance(self.alert, Unset):
            alert = UNSET
        elif isinstance(self.alert, Alert):
            alert = self.alert.to_dict()
        else:
            alert = self.alert

        can_critique_column = self.can_critique_column

        data_type = self.data_type

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        display_values: Union[None, Unset, list[Union[None, str]]]
        if isinstance(self.display_values, Unset):
            display_values = UNSET
        elif isinstance(self.display_values, list):
            display_values = []
            for display_values_type_0_item_data in self.display_values:
                display_values_type_0_item: Union[None, str]
                display_values_type_0_item = display_values_type_0_item_data
                display_values.append(display_values_type_0_item)

        else:
            display_values = self.display_values

        filterable = self.filterable

        group_description: Union[None, Unset, str]
        if isinstance(self.group_description, Unset):
            group_description = UNSET
        else:
            group_description = self.group_description

        group_label: Union[None, Unset, str]
        if isinstance(self.group_label, Unset):
            group_label = UNSET
        else:
            group_label = self.group_label

        group_name: Union[None, Unset, str]
        if isinstance(self.group_name, Unset):
            group_name = UNSET
        else:
            group_name = self.group_name

        job_error_message: Union[None, Unset, str]
        if isinstance(self.job_error_message, Unset):
            job_error_message = UNSET
        else:
            job_error_message = self.job_error_message

        job_info: Union[None, Unset, list[Union[None, dict[str, Any]]]]
        if isinstance(self.job_info, Unset):
            job_info = UNSET
        elif isinstance(self.job_info, list):
            job_info = []
            for job_info_type_0_item_data in self.job_info:
                job_info_type_0_item: Union[None, dict[str, Any]]
                if isinstance(job_info_type_0_item_data, JobInfo):
                    job_info_type_0_item = job_info_type_0_item_data.to_dict()
                else:
                    job_info_type_0_item = job_info_type_0_item_data
                job_info.append(job_info_type_0_item)

        else:
            job_info = self.job_info

        job_progress_message: Union[None, Unset, str]
        if isinstance(self.job_progress_message, Unset):
            job_progress_message = UNSET
        else:
            job_progress_message = self.job_progress_message

        job_status: Union[None, Unset, str]
        if isinstance(self.job_status, Unset):
            job_status = UNSET
        elif isinstance(self.job_status, JobStatus):
            job_status = self.job_status.value
        else:
            job_status = self.job_status

        job_type: Union[None, Unset, str]
        if isinstance(self.job_type, Unset):
            job_type = UNSET
        elif isinstance(self.job_type, ScorerType):
            job_type = self.job_type.value
        else:
            job_type = self.job_type

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        metric_critique_computing = self.metric_critique_computing

        metric_infos: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.metric_infos, Unset):
            metric_infos = []
            for metric_infos_item_data in self.metric_infos:
                metric_infos_item: dict[str, Any]
                if isinstance(metric_infos_item_data, MetricNotComputed):
                    metric_infos_item = metric_infos_item_data.to_dict()
                elif isinstance(metric_infos_item_data, MetricPending):
                    metric_infos_item = metric_infos_item_data.to_dict()
                elif isinstance(metric_infos_item_data, MetricComputing):
                    metric_infos_item = metric_infos_item_data.to_dict()
                elif isinstance(metric_infos_item_data, MetricNotApplicable):
                    metric_infos_item = metric_infos_item_data.to_dict()
                elif isinstance(metric_infos_item_data, MetricSuccess):
                    metric_infos_item = metric_infos_item_data.to_dict()
                elif isinstance(metric_infos_item_data, MetricError):
                    metric_infos_item = metric_infos_item_data.to_dict()
                else:
                    metric_infos_item = metric_infos_item_data.to_dict()

                metric_infos.append(metric_infos_item)

        metric_threshold: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metric_threshold, Unset):
            metric_threshold = UNSET
        elif isinstance(self.metric_threshold, MetricThreshold):
            metric_threshold = self.metric_threshold.to_dict()
        else:
            metric_threshold = self.metric_threshold

        scorer_name: Union[None, Unset, str]
        if isinstance(self.scorer_name, Unset):
            scorer_name = UNSET
        else:
            scorer_name = self.scorer_name

        sortable = self.sortable

        source: Union[None, Unset, str]
        if isinstance(self.source, Unset):
            source = UNSET
        else:
            source = self.source

        values: Union[
            Unset,
            list[
                Union[
                    None,
                    bool,
                    dict[str, Any],
                    float,
                    int,
                    list[Union[None, bool, dict[str, Any], float, int, str]],
                    list[list[Union[None, bool, dict[str, Any], float, int, str]]],
                    list[list[list[Union[None, bool, dict[str, Any], float, int, str]]]],
                    str,
                ]
            ],
        ] = UNSET
        if not isinstance(self.values, Unset):
            values = []
            for values_item_data in self.values:
                values_item: Union[
                    None,
                    bool,
                    dict[str, Any],
                    float,
                    int,
                    list[Union[None, bool, dict[str, Any], float, int, str]],
                    list[list[Union[None, bool, dict[str, Any], float, int, str]]],
                    list[list[list[Union[None, bool, dict[str, Any], float, int, str]]]],
                    str,
                ]
                if isinstance(values_item_data, UUID):
                    values_item = str(values_item_data)
                elif isinstance(values_item_data, datetime.datetime):
                    values_item = values_item_data.isoformat()
                elif isinstance(values_item_data, Segment):
                    values_item = values_item_data.to_dict()
                elif isinstance(values_item_data, HallucinationSegment):
                    values_item = values_item_data.to_dict()
                elif isinstance(values_item_data, Document):
                    values_item = values_item_data.to_dict()
                elif isinstance(values_item_data, FeedbackRatingDB):
                    values_item = values_item_data.to_dict()
                elif isinstance(values_item_data, FeedbackAggregate):
                    values_item = values_item_data.to_dict()
                elif isinstance(values_item_data, list):
                    values_item = []
                    for values_item_type_11_item_data in values_item_data:
                        values_item_type_11_item: Union[None, bool, dict[str, Any], float, int, str]
                        if isinstance(values_item_type_11_item_data, UUID):
                            values_item_type_11_item = str(values_item_type_11_item_data)
                        elif isinstance(values_item_type_11_item_data, datetime.datetime):
                            values_item_type_11_item = values_item_type_11_item_data.isoformat()
                        elif isinstance(values_item_type_11_item_data, Segment):
                            values_item_type_11_item = values_item_type_11_item_data.to_dict()
                        elif isinstance(values_item_type_11_item_data, HallucinationSegment):
                            values_item_type_11_item = values_item_type_11_item_data.to_dict()
                        elif isinstance(values_item_type_11_item_data, Document):
                            values_item_type_11_item = values_item_type_11_item_data.to_dict()
                        elif isinstance(values_item_type_11_item_data, FeedbackRatingDB):
                            values_item_type_11_item = values_item_type_11_item_data.to_dict()
                        elif isinstance(values_item_type_11_item_data, FeedbackAggregate):
                            values_item_type_11_item = values_item_type_11_item_data.to_dict()
                        else:
                            values_item_type_11_item = values_item_type_11_item_data
                        values_item.append(values_item_type_11_item)

                elif isinstance(values_item_data, list):
                    values_item = []
                    for values_item_type_12_item_data in values_item_data:
                        values_item_type_12_item = []
                        for values_item_type_12_item_item_data in values_item_type_12_item_data:
                            values_item_type_12_item_item: Union[None, bool, dict[str, Any], float, int, str]
                            if isinstance(values_item_type_12_item_item_data, UUID):
                                values_item_type_12_item_item = str(values_item_type_12_item_item_data)
                            elif isinstance(values_item_type_12_item_item_data, datetime.datetime):
                                values_item_type_12_item_item = values_item_type_12_item_item_data.isoformat()
                            elif isinstance(values_item_type_12_item_item_data, Segment):
                                values_item_type_12_item_item = values_item_type_12_item_item_data.to_dict()
                            elif isinstance(values_item_type_12_item_item_data, HallucinationSegment):
                                values_item_type_12_item_item = values_item_type_12_item_item_data.to_dict()
                            elif isinstance(values_item_type_12_item_item_data, Document):
                                values_item_type_12_item_item = values_item_type_12_item_item_data.to_dict()
                            elif isinstance(values_item_type_12_item_item_data, FeedbackRatingDB):
                                values_item_type_12_item_item = values_item_type_12_item_item_data.to_dict()
                            elif isinstance(values_item_type_12_item_item_data, FeedbackAggregate):
                                values_item_type_12_item_item = values_item_type_12_item_item_data.to_dict()
                            else:
                                values_item_type_12_item_item = values_item_type_12_item_item_data
                            values_item_type_12_item.append(values_item_type_12_item_item)

                        values_item.append(values_item_type_12_item)

                elif isinstance(values_item_data, list):
                    values_item = []
                    for values_item_type_13_item_data in values_item_data:
                        values_item_type_13_item = []
                        for values_item_type_13_item_item_data in values_item_type_13_item_data:
                            values_item_type_13_item_item = []
                            for values_item_type_13_item_item_item_data in values_item_type_13_item_item_data:
                                values_item_type_13_item_item_item: Union[None, bool, dict[str, Any], float, int, str]
                                if isinstance(values_item_type_13_item_item_item_data, UUID):
                                    values_item_type_13_item_item_item = str(values_item_type_13_item_item_item_data)
                                elif isinstance(values_item_type_13_item_item_item_data, datetime.datetime):
                                    values_item_type_13_item_item_item = (
                                        values_item_type_13_item_item_item_data.isoformat()
                                    )
                                elif isinstance(values_item_type_13_item_item_item_data, Segment):
                                    values_item_type_13_item_item_item = (
                                        values_item_type_13_item_item_item_data.to_dict()
                                    )
                                elif isinstance(values_item_type_13_item_item_item_data, HallucinationSegment):
                                    values_item_type_13_item_item_item = (
                                        values_item_type_13_item_item_item_data.to_dict()
                                    )
                                elif isinstance(values_item_type_13_item_item_item_data, Document):
                                    values_item_type_13_item_item_item = (
                                        values_item_type_13_item_item_item_data.to_dict()
                                    )
                                elif isinstance(values_item_type_13_item_item_item_data, FeedbackRatingDB):
                                    values_item_type_13_item_item_item = (
                                        values_item_type_13_item_item_item_data.to_dict()
                                    )
                                elif isinstance(values_item_type_13_item_item_item_data, FeedbackAggregate):
                                    values_item_type_13_item_item_item = (
                                        values_item_type_13_item_item_item_data.to_dict()
                                    )
                                else:
                                    values_item_type_13_item_item_item = values_item_type_13_item_item_item_data
                                values_item_type_13_item_item.append(values_item_type_13_item_item_item)

                            values_item_type_13_item.append(values_item_type_13_item_item)

                        values_item.append(values_item_type_13_item)

                else:
                    values_item = values_item_data
                values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name})
        if alert is not UNSET:
            field_dict["alert"] = alert
        if can_critique_column is not UNSET:
            field_dict["can_critique_column"] = can_critique_column
        if data_type is not UNSET:
            field_dict["data_type"] = data_type
        if description is not UNSET:
            field_dict["description"] = description
        if display_values is not UNSET:
            field_dict["display_values"] = display_values
        if filterable is not UNSET:
            field_dict["filterable"] = filterable
        if group_description is not UNSET:
            field_dict["group_description"] = group_description
        if group_label is not UNSET:
            field_dict["group_label"] = group_label
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if job_error_message is not UNSET:
            field_dict["job_error_message"] = job_error_message
        if job_info is not UNSET:
            field_dict["job_info"] = job_info
        if job_progress_message is not UNSET:
            field_dict["job_progress_message"] = job_progress_message
        if job_status is not UNSET:
            field_dict["job_status"] = job_status
        if job_type is not UNSET:
            field_dict["job_type"] = job_type
        if label is not UNSET:
            field_dict["label"] = label
        if metric_critique_computing is not UNSET:
            field_dict["metric_critique_computing"] = metric_critique_computing
        if metric_infos is not UNSET:
            field_dict["metric_infos"] = metric_infos
        if metric_threshold is not UNSET:
            field_dict["metric_threshold"] = metric_threshold
        if scorer_name is not UNSET:
            field_dict["scorer_name"] = scorer_name
        if sortable is not UNSET:
            field_dict["sortable"] = sortable
        if source is not UNSET:
            field_dict["source"] = source
        if values is not UNSET:
            field_dict["values"] = values

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.alert import Alert
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.job_info import JobInfo
        from ..models.metric_computing import MetricComputing
        from ..models.metric_error import MetricError
        from ..models.metric_failed import MetricFailed
        from ..models.metric_not_applicable import MetricNotApplicable
        from ..models.metric_not_computed import MetricNotComputed
        from ..models.metric_pending import MetricPending
        from ..models.metric_success import MetricSuccess
        from ..models.metric_threshold import MetricThreshold
        from ..models.segment import Segment

        d = src_dict.copy()
        name = d.pop("name")

        def _parse_alert(data: object) -> Union["Alert", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                alert_type_0 = Alert.from_dict(data)

                return alert_type_0
            except:  # noqa: E722
                pass
            return cast(Union["Alert", None, Unset], data)

        alert = _parse_alert(d.pop("alert", UNSET))

        can_critique_column = d.pop("can_critique_column", UNSET)

        data_type = d.pop("data_type", UNSET)

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_display_values(data: object) -> Union[None, Unset, list[Union[None, str]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                display_values_type_0 = []
                _display_values_type_0 = data
                for display_values_type_0_item_data in _display_values_type_0:

                    def _parse_display_values_type_0_item(data: object) -> Union[None, str]:
                        if data is None:
                            return data
                        return cast(Union[None, str], data)

                    display_values_type_0_item = _parse_display_values_type_0_item(display_values_type_0_item_data)

                    display_values_type_0.append(display_values_type_0_item)

                return display_values_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Union[None, str]]], data)

        display_values = _parse_display_values(d.pop("display_values", UNSET))

        filterable = d.pop("filterable", UNSET)

        def _parse_group_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_description = _parse_group_description(d.pop("group_description", UNSET))

        def _parse_group_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_label = _parse_group_label(d.pop("group_label", UNSET))

        def _parse_group_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group_name = _parse_group_name(d.pop("group_name", UNSET))

        def _parse_job_error_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        job_error_message = _parse_job_error_message(d.pop("job_error_message", UNSET))

        def _parse_job_info(data: object) -> Union[None, Unset, list[Union["JobInfo", None]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                job_info_type_0 = []
                _job_info_type_0 = data
                for job_info_type_0_item_data in _job_info_type_0:

                    def _parse_job_info_type_0_item(data: object) -> Union["JobInfo", None]:
                        if data is None:
                            return data
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            job_info_type_0_item_type_0 = JobInfo.from_dict(data)

                            return job_info_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        return cast(Union["JobInfo", None], data)

                    job_info_type_0_item = _parse_job_info_type_0_item(job_info_type_0_item_data)

                    job_info_type_0.append(job_info_type_0_item)

                return job_info_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Union["JobInfo", None]]], data)

        job_info = _parse_job_info(d.pop("job_info", UNSET))

        def _parse_job_progress_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        job_progress_message = _parse_job_progress_message(d.pop("job_progress_message", UNSET))

        def _parse_job_status(data: object) -> Union[JobStatus, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_status_type_0 = JobStatus(data)

                return job_status_type_0
            except:  # noqa: E722
                pass
            return cast(Union[JobStatus, None, Unset], data)

        job_status = _parse_job_status(d.pop("job_status", UNSET))

        def _parse_job_type(data: object) -> Union[None, ScorerType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                job_type_type_0 = ScorerType(data)

                return job_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ScorerType, Unset], data)

        job_type = _parse_job_type(d.pop("job_type", UNSET))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        metric_critique_computing = d.pop("metric_critique_computing", UNSET)

        metric_infos = []
        _metric_infos = d.pop("metric_infos", UNSET)
        for metric_infos_item_data in _metric_infos or []:

            def _parse_metric_infos_item(
                data: object,
            ) -> Union[
                "MetricComputing",
                "MetricError",
                "MetricFailed",
                "MetricNotApplicable",
                "MetricNotComputed",
                "MetricPending",
                "MetricSuccess",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    metric_infos_item_type_0 = MetricNotComputed.from_dict(data)

                    return metric_infos_item_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    metric_infos_item_type_1 = MetricPending.from_dict(data)

                    return metric_infos_item_type_1
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    metric_infos_item_type_2 = MetricComputing.from_dict(data)

                    return metric_infos_item_type_2
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    metric_infos_item_type_3 = MetricNotApplicable.from_dict(data)

                    return metric_infos_item_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    metric_infos_item_type_4 = MetricSuccess.from_dict(data)

                    return metric_infos_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    metric_infos_item_type_5 = MetricError.from_dict(data)

                    return metric_infos_item_type_5
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                metric_infos_item_type_6 = MetricFailed.from_dict(data)

                return metric_infos_item_type_6

            metric_infos_item = _parse_metric_infos_item(metric_infos_item_data)

            metric_infos.append(metric_infos_item)

        def _parse_metric_threshold(data: object) -> Union["MetricThreshold", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_threshold_type_0 = MetricThreshold.from_dict(data)

                return metric_threshold_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MetricThreshold", None, Unset], data)

        metric_threshold = _parse_metric_threshold(d.pop("metric_threshold", UNSET))

        def _parse_scorer_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        scorer_name = _parse_scorer_name(d.pop("scorer_name", UNSET))

        sortable = d.pop("sortable", UNSET)

        def _parse_source(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        source = _parse_source(d.pop("source", UNSET))

        values = []
        _values = d.pop("values", UNSET)
        for values_item_data in _values or []:

            def _parse_values_item(
                data: object,
            ) -> Union[
                "Document",
                "FeedbackAggregate",
                "FeedbackRatingDB",
                "HallucinationSegment",
                "Segment",
                None,
                UUID,
                bool,
                datetime.datetime,
                float,
                int,
                list[
                    Union[
                        "Document",
                        "FeedbackAggregate",
                        "FeedbackRatingDB",
                        "HallucinationSegment",
                        "Segment",
                        None,
                        UUID,
                        bool,
                        datetime.datetime,
                        float,
                        int,
                        str,
                    ]
                ],
                list[
                    list[
                        Union[
                            "Document",
                            "FeedbackAggregate",
                            "FeedbackRatingDB",
                            "HallucinationSegment",
                            "Segment",
                            None,
                            UUID,
                            bool,
                            datetime.datetime,
                            float,
                            int,
                            str,
                        ]
                    ]
                ],
                list[
                    list[
                        list[
                            Union[
                                "Document",
                                "FeedbackAggregate",
                                "FeedbackRatingDB",
                                "HallucinationSegment",
                                "Segment",
                                None,
                                UUID,
                                bool,
                                datetime.datetime,
                                float,
                                int,
                                str,
                            ]
                        ]
                    ]
                ],
                str,
            ]:
                if data is None:
                    return data
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    values_item_type_4 = UUID(data)

                    return values_item_type_4
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    values_item_type_5 = isoparse(data)

                    return values_item_type_5
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    values_item_type_6 = Segment.from_dict(data)

                    return values_item_type_6
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    values_item_type_7 = HallucinationSegment.from_dict(data)

                    return values_item_type_7
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    values_item_type_8 = Document.from_dict(data)

                    return values_item_type_8
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    values_item_type_9 = FeedbackRatingDB.from_dict(data)

                    return values_item_type_9
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    values_item_type_10 = FeedbackAggregate.from_dict(data)

                    return values_item_type_10
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    values_item_type_11 = []
                    _values_item_type_11 = data
                    for values_item_type_11_item_data in _values_item_type_11:

                        def _parse_values_item_type_11_item(
                            data: object,
                        ) -> Union[
                            "Document",
                            "FeedbackAggregate",
                            "FeedbackRatingDB",
                            "HallucinationSegment",
                            "Segment",
                            None,
                            UUID,
                            bool,
                            datetime.datetime,
                            float,
                            int,
                            str,
                        ]:
                            if data is None:
                                return data
                            try:
                                if not isinstance(data, str):
                                    raise TypeError()
                                values_item_type_11_item_type_4 = UUID(data)

                                return values_item_type_11_item_type_4
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, str):
                                    raise TypeError()
                                values_item_type_11_item_type_5 = isoparse(data)

                                return values_item_type_11_item_type_5
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                values_item_type_11_item_type_6 = Segment.from_dict(data)

                                return values_item_type_11_item_type_6
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                values_item_type_11_item_type_7 = HallucinationSegment.from_dict(data)

                                return values_item_type_11_item_type_7
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                values_item_type_11_item_type_8 = Document.from_dict(data)

                                return values_item_type_11_item_type_8
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                values_item_type_11_item_type_9 = FeedbackRatingDB.from_dict(data)

                                return values_item_type_11_item_type_9
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                values_item_type_11_item_type_10 = FeedbackAggregate.from_dict(data)

                                return values_item_type_11_item_type_10
                            except:  # noqa: E722
                                pass
                            return cast(
                                Union[
                                    "Document",
                                    "FeedbackAggregate",
                                    "FeedbackRatingDB",
                                    "HallucinationSegment",
                                    "Segment",
                                    None,
                                    UUID,
                                    bool,
                                    datetime.datetime,
                                    float,
                                    int,
                                    str,
                                ],
                                data,
                            )

                        values_item_type_11_item = _parse_values_item_type_11_item(values_item_type_11_item_data)

                        values_item_type_11.append(values_item_type_11_item)

                    return values_item_type_11
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    values_item_type_12 = []
                    _values_item_type_12 = data
                    for values_item_type_12_item_data in _values_item_type_12:
                        values_item_type_12_item = []
                        _values_item_type_12_item = values_item_type_12_item_data
                        for values_item_type_12_item_item_data in _values_item_type_12_item:

                            def _parse_values_item_type_12_item_item(
                                data: object,
                            ) -> Union[
                                "Document",
                                "FeedbackAggregate",
                                "FeedbackRatingDB",
                                "HallucinationSegment",
                                "Segment",
                                None,
                                UUID,
                                bool,
                                datetime.datetime,
                                float,
                                int,
                                str,
                            ]:
                                if data is None:
                                    return data
                                try:
                                    if not isinstance(data, str):
                                        raise TypeError()
                                    values_item_type_12_item_item_type_4 = UUID(data)

                                    return values_item_type_12_item_item_type_4
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, str):
                                        raise TypeError()
                                    values_item_type_12_item_item_type_5 = isoparse(data)

                                    return values_item_type_12_item_item_type_5
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    values_item_type_12_item_item_type_6 = Segment.from_dict(data)

                                    return values_item_type_12_item_item_type_6
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    values_item_type_12_item_item_type_7 = HallucinationSegment.from_dict(data)

                                    return values_item_type_12_item_item_type_7
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    values_item_type_12_item_item_type_8 = Document.from_dict(data)

                                    return values_item_type_12_item_item_type_8
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    values_item_type_12_item_item_type_9 = FeedbackRatingDB.from_dict(data)

                                    return values_item_type_12_item_item_type_9
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    values_item_type_12_item_item_type_10 = FeedbackAggregate.from_dict(data)

                                    return values_item_type_12_item_item_type_10
                                except:  # noqa: E722
                                    pass
                                return cast(
                                    Union[
                                        "Document",
                                        "FeedbackAggregate",
                                        "FeedbackRatingDB",
                                        "HallucinationSegment",
                                        "Segment",
                                        None,
                                        UUID,
                                        bool,
                                        datetime.datetime,
                                        float,
                                        int,
                                        str,
                                    ],
                                    data,
                                )

                            values_item_type_12_item_item = _parse_values_item_type_12_item_item(
                                values_item_type_12_item_item_data
                            )

                            values_item_type_12_item.append(values_item_type_12_item_item)

                        values_item_type_12.append(values_item_type_12_item)

                    return values_item_type_12
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    values_item_type_13 = []
                    _values_item_type_13 = data
                    for values_item_type_13_item_data in _values_item_type_13:
                        values_item_type_13_item = []
                        _values_item_type_13_item = values_item_type_13_item_data
                        for values_item_type_13_item_item_data in _values_item_type_13_item:
                            values_item_type_13_item_item = []
                            _values_item_type_13_item_item = values_item_type_13_item_item_data
                            for values_item_type_13_item_item_item_data in _values_item_type_13_item_item:

                                def _parse_values_item_type_13_item_item_item(
                                    data: object,
                                ) -> Union[
                                    "Document",
                                    "FeedbackAggregate",
                                    "FeedbackRatingDB",
                                    "HallucinationSegment",
                                    "Segment",
                                    None,
                                    UUID,
                                    bool,
                                    datetime.datetime,
                                    float,
                                    int,
                                    str,
                                ]:
                                    if data is None:
                                        return data
                                    try:
                                        if not isinstance(data, str):
                                            raise TypeError()
                                        values_item_type_13_item_item_item_type_4 = UUID(data)

                                        return values_item_type_13_item_item_item_type_4
                                    except:  # noqa: E722
                                        pass
                                    try:
                                        if not isinstance(data, str):
                                            raise TypeError()
                                        values_item_type_13_item_item_item_type_5 = isoparse(data)

                                        return values_item_type_13_item_item_item_type_5
                                    except:  # noqa: E722
                                        pass
                                    try:
                                        if not isinstance(data, dict):
                                            raise TypeError()
                                        values_item_type_13_item_item_item_type_6 = Segment.from_dict(data)

                                        return values_item_type_13_item_item_item_type_6
                                    except:  # noqa: E722
                                        pass
                                    try:
                                        if not isinstance(data, dict):
                                            raise TypeError()
                                        values_item_type_13_item_item_item_type_7 = HallucinationSegment.from_dict(data)

                                        return values_item_type_13_item_item_item_type_7
                                    except:  # noqa: E722
                                        pass
                                    try:
                                        if not isinstance(data, dict):
                                            raise TypeError()
                                        values_item_type_13_item_item_item_type_8 = Document.from_dict(data)

                                        return values_item_type_13_item_item_item_type_8
                                    except:  # noqa: E722
                                        pass
                                    try:
                                        if not isinstance(data, dict):
                                            raise TypeError()
                                        values_item_type_13_item_item_item_type_9 = FeedbackRatingDB.from_dict(data)

                                        return values_item_type_13_item_item_item_type_9
                                    except:  # noqa: E722
                                        pass
                                    try:
                                        if not isinstance(data, dict):
                                            raise TypeError()
                                        values_item_type_13_item_item_item_type_10 = FeedbackAggregate.from_dict(data)

                                        return values_item_type_13_item_item_item_type_10
                                    except:  # noqa: E722
                                        pass
                                    return cast(
                                        Union[
                                            "Document",
                                            "FeedbackAggregate",
                                            "FeedbackRatingDB",
                                            "HallucinationSegment",
                                            "Segment",
                                            None,
                                            UUID,
                                            bool,
                                            datetime.datetime,
                                            float,
                                            int,
                                            str,
                                        ],
                                        data,
                                    )

                                values_item_type_13_item_item_item = _parse_values_item_type_13_item_item_item(
                                    values_item_type_13_item_item_item_data
                                )

                                values_item_type_13_item_item.append(values_item_type_13_item_item_item)

                            values_item_type_13_item.append(values_item_type_13_item_item)

                        values_item_type_13.append(values_item_type_13_item)

                    return values_item_type_13
                except:  # noqa: E722
                    pass
                return cast(
                    Union[
                        "Document",
                        "FeedbackAggregate",
                        "FeedbackRatingDB",
                        "HallucinationSegment",
                        "Segment",
                        None,
                        UUID,
                        bool,
                        datetime.datetime,
                        float,
                        int,
                        list[
                            Union[
                                "Document",
                                "FeedbackAggregate",
                                "FeedbackRatingDB",
                                "HallucinationSegment",
                                "Segment",
                                None,
                                UUID,
                                bool,
                                datetime.datetime,
                                float,
                                int,
                                str,
                            ]
                        ],
                        list[
                            list[
                                Union[
                                    "Document",
                                    "FeedbackAggregate",
                                    "FeedbackRatingDB",
                                    "HallucinationSegment",
                                    "Segment",
                                    None,
                                    UUID,
                                    bool,
                                    datetime.datetime,
                                    float,
                                    int,
                                    str,
                                ]
                            ]
                        ],
                        list[
                            list[
                                list[
                                    Union[
                                        "Document",
                                        "FeedbackAggregate",
                                        "FeedbackRatingDB",
                                        "HallucinationSegment",
                                        "Segment",
                                        None,
                                        UUID,
                                        bool,
                                        datetime.datetime,
                                        float,
                                        int,
                                        str,
                                    ]
                                ]
                            ]
                        ],
                        str,
                    ],
                    data,
                )

            values_item = _parse_values_item(values_item_data)

            values.append(values_item)

        prompt_row_column = cls(
            name=name,
            alert=alert,
            can_critique_column=can_critique_column,
            data_type=data_type,
            description=description,
            display_values=display_values,
            filterable=filterable,
            group_description=group_description,
            group_label=group_label,
            group_name=group_name,
            job_error_message=job_error_message,
            job_info=job_info,
            job_progress_message=job_progress_message,
            job_status=job_status,
            job_type=job_type,
            label=label,
            metric_critique_computing=metric_critique_computing,
            metric_infos=metric_infos,
            metric_threshold=metric_threshold,
            scorer_name=scorer_name,
            sortable=sortable,
            source=source,
            values=values,
        )

        prompt_row_column.additional_properties = d
        return prompt_row_column

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
