import datetime
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
    from ..models.segment import Segment


T = TypeVar("T", bound="MetricSuccess")


@_attrs_define
class MetricSuccess:
    """
    Attributes:
        value (Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None, UUID,
            bool, datetime.datetime, float, int, list[Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB',
            'HallucinationSegment', 'Segment', None, UUID, bool, datetime.datetime, float, int, str]],
            list[list[Union['Document', 'FeedbackAggregate', 'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None,
            UUID, bool, datetime.datetime, float, int, str]]], list[list[list[Union['Document', 'FeedbackAggregate',
            'FeedbackRatingDB', 'HallucinationSegment', 'Segment', None, UUID, bool, datetime.datetime, float, int, str]]]],
            str]):
        cost (Union[None, Unset, float]):
        critique (Union['MetricCritiqueColumnar', None, Unset]):
        display_value (Union[None, Unset, str]):
        explanation (Union[None, Unset, str]):
        model_alias (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        rationale (Union[None, Unset, str]):
        scorer_type (Union[None, ScorerType, Unset]):
        status_type (Union[Literal['success'], Unset]):  Default: 'success'.
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
    cost: Union[None, Unset, float] = UNSET
    critique: Union["MetricCritiqueColumnar", None, Unset] = UNSET
    display_value: Union[None, Unset, str] = UNSET
    explanation: Union[None, Unset, str] = UNSET
    model_alias: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    rationale: Union[None, Unset, str] = UNSET
    scorer_type: Union[None, ScorerType, Unset] = UNSET
    status_type: Union[Literal["success"], Unset] = "success"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.metric_critique_columnar import MetricCritiqueColumnar
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
        elif isinstance(self.value, Segment):
            value = self.value.to_dict()
        elif isinstance(self.value, HallucinationSegment):
            value = self.value.to_dict()
        elif isinstance(self.value, Document):
            value = self.value.to_dict()
        elif isinstance(self.value, FeedbackRatingDB):
            value = self.value.to_dict()
        elif isinstance(self.value, FeedbackAggregate):
            value = self.value.to_dict()
        elif isinstance(self.value, list):
            value = []
            for value_type_11_item_data in self.value:
                value_type_11_item: Union[None, bool, dict[str, Any], float, int, str]
                if isinstance(value_type_11_item_data, UUID):
                    value_type_11_item = str(value_type_11_item_data)
                elif isinstance(value_type_11_item_data, datetime.datetime):
                    value_type_11_item = value_type_11_item_data.isoformat()
                elif isinstance(value_type_11_item_data, Segment):
                    value_type_11_item = value_type_11_item_data.to_dict()
                elif isinstance(value_type_11_item_data, HallucinationSegment):
                    value_type_11_item = value_type_11_item_data.to_dict()
                elif isinstance(value_type_11_item_data, Document):
                    value_type_11_item = value_type_11_item_data.to_dict()
                elif isinstance(value_type_11_item_data, FeedbackRatingDB):
                    value_type_11_item = value_type_11_item_data.to_dict()
                elif isinstance(value_type_11_item_data, FeedbackAggregate):
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
                    elif isinstance(value_type_12_item_item_data, Segment):
                        value_type_12_item_item = value_type_12_item_item_data.to_dict()
                    elif isinstance(value_type_12_item_item_data, HallucinationSegment):
                        value_type_12_item_item = value_type_12_item_item_data.to_dict()
                    elif isinstance(value_type_12_item_item_data, Document):
                        value_type_12_item_item = value_type_12_item_item_data.to_dict()
                    elif isinstance(value_type_12_item_item_data, FeedbackRatingDB):
                        value_type_12_item_item = value_type_12_item_item_data.to_dict()
                    elif isinstance(value_type_12_item_item_data, FeedbackAggregate):
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
                        elif isinstance(value_type_13_item_item_item_data, Segment):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.to_dict()
                        elif isinstance(value_type_13_item_item_item_data, HallucinationSegment):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.to_dict()
                        elif isinstance(value_type_13_item_item_item_data, Document):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.to_dict()
                        elif isinstance(value_type_13_item_item_item_data, FeedbackRatingDB):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.to_dict()
                        elif isinstance(value_type_13_item_item_item_data, FeedbackAggregate):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.to_dict()
                        else:
                            value_type_13_item_item_item = value_type_13_item_item_item_data
                        value_type_13_item_item.append(value_type_13_item_item_item)

                    value_type_13_item.append(value_type_13_item_item)

                value.append(value_type_13_item)

        else:
            value = self.value

        cost: Union[None, Unset, float]
        if isinstance(self.cost, Unset):
            cost = UNSET
        else:
            cost = self.cost

        critique: Union[None, Unset, dict[str, Any]]
        if isinstance(self.critique, Unset):
            critique = UNSET
        elif isinstance(self.critique, MetricCritiqueColumnar):
            critique = self.critique.to_dict()
        else:
            critique = self.critique

        display_value: Union[None, Unset, str]
        if isinstance(self.display_value, Unset):
            display_value = UNSET
        else:
            display_value = self.display_value

        explanation: Union[None, Unset, str]
        if isinstance(self.explanation, Unset):
            explanation = UNSET
        else:
            explanation = self.explanation

        model_alias: Union[None, Unset, str]
        if isinstance(self.model_alias, Unset):
            model_alias = UNSET
        else:
            model_alias = self.model_alias

        num_judges: Union[None, Unset, int]
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        rationale: Union[None, Unset, str]
        if isinstance(self.rationale, Unset):
            rationale = UNSET
        else:
            rationale = self.rationale

        scorer_type: Union[None, Unset, str]
        if isinstance(self.scorer_type, Unset):
            scorer_type = UNSET
        elif isinstance(self.scorer_type, ScorerType):
            scorer_type = self.scorer_type.value
        else:
            scorer_type = self.scorer_type

        status_type = self.status_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if cost is not UNSET:
            field_dict["cost"] = cost
        if critique is not UNSET:
            field_dict["critique"] = critique
        if display_value is not UNSET:
            field_dict["display_value"] = display_value
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if model_alias is not UNSET:
            field_dict["model_alias"] = model_alias
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if rationale is not UNSET:
            field_dict["rationale"] = rationale
        if scorer_type is not UNSET:
            field_dict["scorer_type"] = scorer_type
        if status_type is not UNSET:
            field_dict["status_type"] = status_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.metric_critique_columnar import MetricCritiqueColumnar
        from ..models.segment import Segment

        d = src_dict.copy()

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
                value_type_4 = UUID(data)

                return value_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                value_type_5 = isoparse(data)

                return value_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_6 = Segment.from_dict(data)

                return value_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_7 = HallucinationSegment.from_dict(data)

                return value_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_8 = Document.from_dict(data)

                return value_type_8
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_9 = FeedbackRatingDB.from_dict(data)

                return value_type_9
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                value_type_10 = FeedbackAggregate.from_dict(data)

                return value_type_10
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
                            value_type_11_item_type_4 = UUID(data)

                            return value_type_11_item_type_4
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, str):
                                raise TypeError()
                            value_type_11_item_type_5 = isoparse(data)

                            return value_type_11_item_type_5
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            value_type_11_item_type_6 = Segment.from_dict(data)

                            return value_type_11_item_type_6
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            value_type_11_item_type_7 = HallucinationSegment.from_dict(data)

                            return value_type_11_item_type_7
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            value_type_11_item_type_8 = Document.from_dict(data)

                            return value_type_11_item_type_8
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            value_type_11_item_type_9 = FeedbackRatingDB.from_dict(data)

                            return value_type_11_item_type_9
                        except:  # noqa: E722
                            pass
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            value_type_11_item_type_10 = FeedbackAggregate.from_dict(data)

                            return value_type_11_item_type_10
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
                                value_type_12_item_item_type_4 = UUID(data)

                                return value_type_12_item_item_type_4
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, str):
                                    raise TypeError()
                                value_type_12_item_item_type_5 = isoparse(data)

                                return value_type_12_item_item_type_5
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                value_type_12_item_item_type_6 = Segment.from_dict(data)

                                return value_type_12_item_item_type_6
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                value_type_12_item_item_type_7 = HallucinationSegment.from_dict(data)

                                return value_type_12_item_item_type_7
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                value_type_12_item_item_type_8 = Document.from_dict(data)

                                return value_type_12_item_item_type_8
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                value_type_12_item_item_type_9 = FeedbackRatingDB.from_dict(data)

                                return value_type_12_item_item_type_9
                            except:  # noqa: E722
                                pass
                            try:
                                if not isinstance(data, dict):
                                    raise TypeError()
                                value_type_12_item_item_type_10 = FeedbackAggregate.from_dict(data)

                                return value_type_12_item_item_type_10
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
                                    value_type_13_item_item_item_type_4 = UUID(data)

                                    return value_type_13_item_item_item_type_4
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, str):
                                        raise TypeError()
                                    value_type_13_item_item_item_type_5 = isoparse(data)

                                    return value_type_13_item_item_item_type_5
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    value_type_13_item_item_item_type_6 = Segment.from_dict(data)

                                    return value_type_13_item_item_item_type_6
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    value_type_13_item_item_item_type_7 = HallucinationSegment.from_dict(data)

                                    return value_type_13_item_item_item_type_7
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    value_type_13_item_item_item_type_8 = Document.from_dict(data)

                                    return value_type_13_item_item_item_type_8
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    value_type_13_item_item_item_type_9 = FeedbackRatingDB.from_dict(data)

                                    return value_type_13_item_item_item_type_9
                                except:  # noqa: E722
                                    pass
                                try:
                                    if not isinstance(data, dict):
                                        raise TypeError()
                                    value_type_13_item_item_item_type_10 = FeedbackAggregate.from_dict(data)

                                    return value_type_13_item_item_item_type_10
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

        def _parse_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        cost = _parse_cost(d.pop("cost", UNSET))

        def _parse_critique(data: object) -> Union["MetricCritiqueColumnar", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                critique_type_0 = MetricCritiqueColumnar.from_dict(data)

                return critique_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MetricCritiqueColumnar", None, Unset], data)

        critique = _parse_critique(d.pop("critique", UNSET))

        def _parse_display_value(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        display_value = _parse_display_value(d.pop("display_value", UNSET))

        def _parse_explanation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

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

        def _parse_rationale(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        rationale = _parse_rationale(d.pop("rationale", UNSET))

        def _parse_scorer_type(data: object) -> Union[None, ScorerType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scorer_type_type_0 = ScorerType(data)

                return scorer_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ScorerType, Unset], data)

        scorer_type = _parse_scorer_type(d.pop("scorer_type", UNSET))

        status_type = cast(Union[Literal["success"], Unset], d.pop("status_type", UNSET))
        if status_type != "success" and not isinstance(status_type, Unset):
            raise ValueError(f"status_type must match const 'success', got '{status_type}'")

        metric_success = cls(
            value=value,
            cost=cost,
            critique=critique,
            display_value=display_value,
            explanation=explanation,
            model_alias=model_alias,
            num_judges=num_judges,
            rationale=rationale,
            scorer_type=scorer_type,
            status_type=status_type,
        )

        metric_success.additional_properties = d
        return metric_success

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
