import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.scorer_type import ScorerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.feedback_aggregate import FeedbackAggregate
    from ..models.feedback_rating_db import FeedbackRatingDB
    from ..models.hallucination_segment import HallucinationSegment
    from ..models.metric_critique_columnar import MetricCritiqueColumnar
    from ..models.metric_roll_up_roll_up_metrics_type_0 import MetricRollUpRollUpMetricsType0
    from ..models.metric_roll_up_roll_up_metrics_type_1 import MetricRollUpRollUpMetricsType1
    from ..models.segment import Segment


T = TypeVar("T", bound="MetricRollUp")


@_attrs_define
class MetricRollUp:
    """
    Attributes
    ----------
        value (Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None, UUID,
            bool, datetime.datetime, float, int, list[Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB',
            'HallucinationSegment', 'Segment', None, UUID, bool, datetime.datetime, float, int, str]],
            list[list[Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None,
            UUID, bool, datetime.datetime, float, int, str]]], list[list[list[Union['Document', 'FeedbackAggregate',
            'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None, UUID, bool, datetime.datetime, float, int, str]]]],
            str]):
        status_type (Union[Literal['roll_up'], Unset]):  Default: 'roll_up'.
        scorer_type (Union[None, ScorerType, Unset]):
        explanation (Union[None, Unset, str]):
        cost (Union[None, Unset, float]):
        model_alias (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        input_tokens (Union[None, Unset, int]):
        output_tokens (Union[None, Unset, int]):
        total_tokens (Union[None, Unset, int]):
        critique (Union['MetricCritiqueColumnar', None, Unset]):
        roll_up_metrics (Union['MetricRollUpRollUpMetricsType0', 'MetricRollUpRollUpMetricsType1', Unset]): Roll up
            metrics e.g. sum, average, min, max for numeric, and category_count for categorical metrics.
    """

    value: Union[
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
    status_type: Union[Literal["roll_up"], Unset] = "roll_up"
    scorer_type: Union[None, ScorerType, Unset] = UNSET
    explanation: Union[None, Unset, str] = UNSET
    cost: Union[None, Unset, float] = UNSET
    model_alias: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    input_tokens: Union[None, Unset, int] = UNSET
    output_tokens: Union[None, Unset, int] = UNSET
    total_tokens: Union[None, Unset, int] = UNSET
    critique: Union["MetricCritiqueColumnar", None, Unset] = UNSET
    roll_up_metrics: Union["MetricRollUpRollUpMetricsType0", "MetricRollUpRollUpMetricsType1", Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.metric_critique_columnar import MetricCritiqueColumnar
        from ..models.metric_roll_up_roll_up_metrics_type_0 import MetricRollUpRollUpMetricsType0
        from ..models.segment import Segment

        value: Union[
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
        if isinstance(self.value, UUID):
            value = str(self.value)
        elif isinstance(self.value, datetime.datetime):
            value = self.value.isoformat()
        elif isinstance(self.value, (Segment, HallucinationSegment, Document, FeedbackRatingDB, FeedbackAggregate)):
            value = self.value.to_dict()
        elif isinstance(self.value, list):
            value = []
            for value_type_11_item_data in self.value:
                value_type_11_item: Union[None, bool, dict[str, Any], float, int, str]
                if isinstance(value_type_11_item_data, UUID):
                    value_type_11_item = str(value_type_11_item_data)
                elif isinstance(value_type_11_item_data, datetime.datetime):
                    value_type_11_item = value_type_11_item_data.isoformat()
                elif isinstance(
                    value_type_11_item_data,
                    (Segment, HallucinationSegment, Document, FeedbackRatingDB, FeedbackAggregate),
                ):
                    value_type_11_item = value_type_11_item_data.to_dict()
                else:
                    value_type_11_item = value_type_11_item_data
                value.append(value_type_11_item)

        elif isinstance(self.value, list):
            value = []
            for value_type_12_item_data in self.value:
                value_type_12_item = []
                for value_type_12_item_item_data in value_type_12_item_data:
                    value_type_12_item_item: Union[None, bool, dict[str, Any], float, int, str]
                    if isinstance(value_type_12_item_item_data, UUID):
                        value_type_12_item_item = str(value_type_12_item_item_data)
                    elif isinstance(value_type_12_item_item_data, datetime.datetime):
                        value_type_12_item_item = value_type_12_item_item_data.isoformat()
                    elif isinstance(
                        value_type_12_item_item_data,
                        (Segment, HallucinationSegment, Document, FeedbackRatingDB, FeedbackAggregate),
                    ):
                        value_type_12_item_item = value_type_12_item_item_data.to_dict()
                    else:
                        value_type_12_item_item = value_type_12_item_item_data
                    value_type_12_item.append(value_type_12_item_item)

                value.append(value_type_12_item)

        elif isinstance(self.value, list):
            value = []
            for value_type_13_item_data in self.value:
                value_type_13_item = []
                for value_type_13_item_item_data in value_type_13_item_data:
                    value_type_13_item_item = []
                    for value_type_13_item_item_item_data in value_type_13_item_item_data:
                        value_type_13_item_item_item: Union[None, bool, dict[str, Any], float, int, str]
                        if isinstance(value_type_13_item_item_item_data, UUID):
                            value_type_13_item_item_item = str(value_type_13_item_item_item_data)
                        elif isinstance(value_type_13_item_item_item_data, datetime.datetime):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.isoformat()
                        elif isinstance(
                            value_type_13_item_item_item_data,
                            (Segment, HallucinationSegment, Document, FeedbackRatingDB, FeedbackAggregate),
                        ):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.to_dict()
                        else:
                            value_type_13_item_item_item = value_type_13_item_item_item_data
                        value_type_13_item_item.append(value_type_13_item_item_item)

                    value_type_13_item.append(value_type_13_item_item)

                value.append(value_type_13_item)

        else:
            value = self.value

        status_type = self.status_type

        scorer_type: Union[None, Unset, str]
        if isinstance(self.scorer_type, Unset):
            scorer_type = UNSET
        elif isinstance(self.scorer_type, ScorerType):
            scorer_type = self.scorer_type.value
        else:
            scorer_type = self.scorer_type

        explanation: Union[None, Unset, str]
        explanation = UNSET if isinstance(self.explanation, Unset) else self.explanation

        cost: Union[None, Unset, float]
        cost = UNSET if isinstance(self.cost, Unset) else self.cost

        model_alias: Union[None, Unset, str]
        model_alias = UNSET if isinstance(self.model_alias, Unset) else self.model_alias

        num_judges: Union[None, Unset, int]
        num_judges = UNSET if isinstance(self.num_judges, Unset) else self.num_judges

        input_tokens: Union[None, Unset, int]
        input_tokens = UNSET if isinstance(self.input_tokens, Unset) else self.input_tokens

        output_tokens: Union[None, Unset, int]
        output_tokens = UNSET if isinstance(self.output_tokens, Unset) else self.output_tokens

        total_tokens: Union[None, Unset, int]
        total_tokens = UNSET if isinstance(self.total_tokens, Unset) else self.total_tokens

        critique: Union[None, Unset, dict[str, Any]]
        if isinstance(self.critique, Unset):
            critique = UNSET
        elif isinstance(self.critique, MetricCritiqueColumnar):
            critique = self.critique.to_dict()
        else:
            critique = self.critique

        roll_up_metrics: Union[Unset, dict[str, Any]]
        if isinstance(self.roll_up_metrics, Unset):
            roll_up_metrics = UNSET
        elif isinstance(self.roll_up_metrics, MetricRollUpRollUpMetricsType0):
            roll_up_metrics = self.roll_up_metrics.to_dict()
        else:
            roll_up_metrics = self.roll_up_metrics.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if status_type is not UNSET:
            field_dict["status_type"] = status_type
        if scorer_type is not UNSET:
            field_dict["scorer_type"] = scorer_type
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if cost is not UNSET:
            field_dict["cost"] = cost
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if total_tokens is not UNSET:
            field_dict["total_tokens"] = total_tokens
        if critique is not UNSET:
            field_dict["critique"] = critique
        if roll_up_metrics is not UNSET:
            field_dict["roll_up_metrics"] = roll_up_metrics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.metric_critique_columnar import MetricCritiqueColumnar
        from ..models.metric_roll_up_roll_up_metrics_type_0 import MetricRollUpRollUpMetricsType0
        from ..models.metric_roll_up_roll_up_metrics_type_1 import MetricRollUpRollUpMetricsType1
        from ..models.segment import Segment

        d = dict(src_dict)

        def _parse_value(
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
                return UUID(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return isoparse(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Segment.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return HallucinationSegment.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return Document.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return FeedbackRatingDB.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return FeedbackAggregate.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_11 = []
                _value_type_11 = data
                for value_type_11_item_data in _value_type_11:

                    def _parse_value_type_11_item(
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
                            return UUID(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, str):
                                raise TypeError()
                            return isoparse(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return Segment.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return HallucinationSegment.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return Document.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return FeedbackRatingDB.from_dict(data)

                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            return FeedbackAggregate.from_dict(data)

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

                    value_type_11_item = _parse_value_type_11_item(value_type_11_item_data)

                    value_type_11.append(value_type_11_item)

                return value_type_11
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_12 = []
                _value_type_12 = data
                for value_type_12_item_data in _value_type_12:
                    value_type_12_item = []
                    _value_type_12_item = value_type_12_item_data
                    for value_type_12_item_item_data in _value_type_12_item:

                        def _parse_value_type_12_item_item(
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
                                return UUID(data)

                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, str):
                                    raise TypeError()
                                return isoparse(data)

                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                return Segment.from_dict(data)

                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                return HallucinationSegment.from_dict(data)

                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                return Document.from_dict(data)

                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                return FeedbackRatingDB.from_dict(data)

                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                return FeedbackAggregate.from_dict(data)

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

                        value_type_12_item_item = _parse_value_type_12_item_item(value_type_12_item_item_data)

                        value_type_12_item.append(value_type_12_item_item)

                    value_type_12.append(value_type_12_item)

                return value_type_12
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_13 = []
                _value_type_13 = data
                for value_type_13_item_data in _value_type_13:
                    value_type_13_item = []
                    _value_type_13_item = value_type_13_item_data
                    for value_type_13_item_item_data in _value_type_13_item:
                        value_type_13_item_item = []
                        _value_type_13_item_item = value_type_13_item_item_data
                        for value_type_13_item_item_item_data in _value_type_13_item_item:

                            def _parse_value_type_13_item_item_item(
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
                                    return UUID(data)

                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, str):
                                        raise TypeError()
                                    return isoparse(data)

                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    return Segment.from_dict(data)

                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    return HallucinationSegment.from_dict(data)

                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    return Document.from_dict(data)

                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    return FeedbackRatingDB.from_dict(data)

                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    return FeedbackAggregate.from_dict(data)

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

                            value_type_13_item_item_item = _parse_value_type_13_item_item_item(
                                value_type_13_item_item_item_data
                            )

                            value_type_13_item_item.append(value_type_13_item_item_item)

                        value_type_13_item.append(value_type_13_item_item)

                    value_type_13.append(value_type_13_item)

                return value_type_13
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

        value = _parse_value(d.pop("value"))

        status_type = cast(Union[Literal["roll_up"], Unset], d.pop("status_type", UNSET))
        if status_type != "roll_up" and not isinstance(status_type, Unset):
            raise ValueError(f"status_type must match const 'roll_up', got '{status_type}'")

        def _parse_scorer_type(data: object) -> Union[None, ScorerType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ScorerType(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, ScorerType, Unset], data)

        scorer_type = _parse_scorer_type(d.pop("scorer_type", UNSET))

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        def _parse_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        cost = _parse_cost(d.pop("cost", UNSET))

        def _parse_model_alias(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_alias = _parse_model_alias(d.pop("model_alias", UNSET))

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        def _parse_input_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        def _parse_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        def _parse_total_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        total_tokens = _parse_total_tokens(d.pop("total_tokens", UNSET))

        def _parse_critique(data: object) -> Union["MetricCritiqueColumnar", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MetricCritiqueColumnar.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["MetricCritiqueColumnar", None, Unset], data)

        critique = _parse_critique(d.pop("critique", UNSET))

        def _parse_roll_up_metrics(
            data: object,
        ) -> Union["MetricRollUpRollUpMetricsType0", "MetricRollUpRollUpMetricsType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return MetricRollUpRollUpMetricsType0.from_dict(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            return MetricRollUpRollUpMetricsType1.from_dict(data)

        roll_up_metrics = _parse_roll_up_metrics(d.pop("roll_up_metrics", UNSET))

        metric_roll_up = cls(
            value=value,
            status_type=status_type,
            scorer_type=scorer_type,
            explanation=explanation,
            cost=cost,
            model_alias=model_alias,
            num_judges=num_judges,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            critique=critique,
            roll_up_metrics=roll_up_metrics,
        )

        metric_roll_up.additional_properties = d
        return metric_roll_up

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
