from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast
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
    Attributes
    ----------
        value (bool | datetime.datetime | Document | FeedbackAggregate | FeedbackRatingDB | float | HallucinationSegment
            | int | list[bool | datetime.datetime | Document | FeedbackAggregate | FeedbackRatingDB | float |
            HallucinationSegment | int | None | Segment | str | UUID] | list[list[bool | datetime.datetime | Document |
            FeedbackAggregate | FeedbackRatingDB | float | HallucinationSegment | int | None | Segment | str | UUID]] |
            list[list[list[bool | datetime.datetime | Document | FeedbackAggregate | FeedbackRatingDB | float |
            HallucinationSegment | int | None | Segment | str | UUID]]] | None | Segment | str | UUID):
        status_type (Literal['success'] | Unset):  Default: 'success'.
        scorer_type (None | ScorerType | Unset):
        metric_key_alias (None | str | Unset):
        explanation (None | str | Unset):
        cost (float | None | Unset):
        model_alias (None | str | Unset):
        num_judges (int | None | Unset):
        input_tokens (int | None | Unset):
        output_tokens (int | None | Unset):
        total_tokens (int | None | Unset):
        critique (MetricCritiqueColumnar | None | Unset):
        display_value (None | str | Unset):
        rationale (None | str | Unset):
    """

    value: (
        bool
        | datetime.datetime
        | Document
        | FeedbackAggregate
        | FeedbackRatingDB
        | float
        | HallucinationSegment
        | int
        | list[
            bool
            | datetime.datetime
            | Document
            | FeedbackAggregate
            | FeedbackRatingDB
            | float
            | HallucinationSegment
            | int
            | None
            | Segment
            | str
            | UUID
        ]
        | list[
            list[
                bool
                | datetime.datetime
                | Document
                | FeedbackAggregate
                | FeedbackRatingDB
                | float
                | HallucinationSegment
                | int
                | None
                | Segment
                | str
                | UUID
            ]
        ]
        | list[
            list[
                list[
                    bool
                    | datetime.datetime
                    | Document
                    | FeedbackAggregate
                    | FeedbackRatingDB
                    | float
                    | HallucinationSegment
                    | int
                    | None
                    | Segment
                    | str
                    | UUID
                ]
            ]
        ]
        | None
        | Segment
        | str
        | UUID
    )
    status_type: Literal["success"] | Unset = "success"
    scorer_type: None | ScorerType | Unset = UNSET
    metric_key_alias: None | str | Unset = UNSET
    explanation: None | str | Unset = UNSET
    cost: float | None | Unset = UNSET
    model_alias: None | str | Unset = UNSET
    num_judges: int | None | Unset = UNSET
    input_tokens: int | None | Unset = UNSET
    output_tokens: int | None | Unset = UNSET
    total_tokens: int | None | Unset = UNSET
    critique: MetricCritiqueColumnar | None | Unset = UNSET
    display_value: None | str | Unset = UNSET
    rationale: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.metric_critique_columnar import MetricCritiqueColumnar
        from ..models.segment import Segment

        value: (
            bool
            | dict[str, Any]
            | float
            | int
            | list[bool | dict[str, Any] | float | int | None | str]
            | list[list[bool | dict[str, Any] | float | int | None | str]]
            | list[list[list[bool | dict[str, Any] | float | int | None | str]]]
            | None
            | str
        )
        if isinstance(self.value, UUID):
            value = str(self.value)
        elif isinstance(self.value, datetime.datetime):
            value = self.value.isoformat()
        elif isinstance(self.value, Segment | HallucinationSegment | Document | FeedbackRatingDB | FeedbackAggregate):
            value = self.value.to_dict()
        elif isinstance(self.value, list):
            value = []
            for value_type_11_item_data in self.value:
                value_type_11_item: bool | dict[str, Any] | float | int | None | str
                if isinstance(value_type_11_item_data, UUID):
                    value_type_11_item = str(value_type_11_item_data)
                elif isinstance(value_type_11_item_data, datetime.datetime):
                    value_type_11_item = value_type_11_item_data.isoformat()
                elif isinstance(
                    value_type_11_item_data,
                    Segment | HallucinationSegment | Document | FeedbackRatingDB | FeedbackAggregate,
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
                    value_type_12_item_item: bool | dict[str, Any] | float | int | None | str
                    if isinstance(value_type_12_item_item_data, UUID):
                        value_type_12_item_item = str(value_type_12_item_item_data)
                    elif isinstance(value_type_12_item_item_data, datetime.datetime):
                        value_type_12_item_item = value_type_12_item_item_data.isoformat()
                    elif isinstance(
                        value_type_12_item_item_data,
                        Segment | HallucinationSegment | Document | FeedbackRatingDB | FeedbackAggregate,
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
                        value_type_13_item_item_item: bool | dict[str, Any] | float | int | None | str
                        if isinstance(value_type_13_item_item_item_data, UUID):
                            value_type_13_item_item_item = str(value_type_13_item_item_item_data)
                        elif isinstance(value_type_13_item_item_item_data, datetime.datetime):
                            value_type_13_item_item_item = value_type_13_item_item_item_data.isoformat()
                        elif isinstance(
                            value_type_13_item_item_item_data,
                            Segment | HallucinationSegment | Document | FeedbackRatingDB | FeedbackAggregate,
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

        scorer_type: None | str | Unset
        if isinstance(self.scorer_type, Unset):
            scorer_type = UNSET
        elif isinstance(self.scorer_type, ScorerType):
            scorer_type = self.scorer_type.value
        else:
            scorer_type = self.scorer_type

        metric_key_alias: None | str | Unset
        metric_key_alias = UNSET if isinstance(self.metric_key_alias, Unset) else self.metric_key_alias

        explanation: None | str | Unset
        explanation = UNSET if isinstance(self.explanation, Unset) else self.explanation

        cost: float | None | Unset
        cost = UNSET if isinstance(self.cost, Unset) else self.cost

        model_alias: None | str | Unset
        model_alias = UNSET if isinstance(self.model_alias, Unset) else self.model_alias

        num_judges: int | None | Unset
        num_judges = UNSET if isinstance(self.num_judges, Unset) else self.num_judges

        input_tokens: int | None | Unset
        input_tokens = UNSET if isinstance(self.input_tokens, Unset) else self.input_tokens

        output_tokens: int | None | Unset
        output_tokens = UNSET if isinstance(self.output_tokens, Unset) else self.output_tokens

        total_tokens: int | None | Unset
        total_tokens = UNSET if isinstance(self.total_tokens, Unset) else self.total_tokens

        critique: dict[str, Any] | None | Unset
        if isinstance(self.critique, Unset):
            critique = UNSET
        elif isinstance(self.critique, MetricCritiqueColumnar):
            critique = self.critique.to_dict()
        else:
            critique = self.critique

        display_value: None | str | Unset
        display_value = UNSET if isinstance(self.display_value, Unset) else self.display_value

        rationale: None | str | Unset
        rationale = UNSET if isinstance(self.rationale, Unset) else self.rationale

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"value": value})
        if status_type is not UNSET:
            field_dict["status_type"] = status_type
        if scorer_type is not UNSET:
            field_dict["scorer_type"] = scorer_type
        if metric_key_alias is not UNSET:
            field_dict["metric_key_alias"] = metric_key_alias
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
        if display_value is not UNSET:
            field_dict["display_value"] = display_value
        if rationale is not UNSET:
            field_dict["rationale"] = rationale

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document import Document
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.feedback_rating_db import FeedbackRatingDB
        from ..models.hallucination_segment import HallucinationSegment
        from ..models.metric_critique_columnar import MetricCritiqueColumnar
        from ..models.segment import Segment

        d = dict(src_dict)

        def _parse_value(
            data: object,
        ) -> (
            bool
            | datetime.datetime
            | Document
            | FeedbackAggregate
            | FeedbackRatingDB
            | float
            | HallucinationSegment
            | int
            | list[
                bool
                | datetime.datetime
                | Document
                | FeedbackAggregate
                | FeedbackRatingDB
                | float
                | HallucinationSegment
                | int
                | None
                | Segment
                | str
                | UUID
            ]
            | list[
                list[
                    bool
                    | datetime.datetime
                    | Document
                    | FeedbackAggregate
                    | FeedbackRatingDB
                    | float
                    | HallucinationSegment
                    | int
                    | None
                    | Segment
                    | str
                    | UUID
                ]
            ]
            | list[
                list[
                    list[
                        bool
                        | datetime.datetime
                        | Document
                        | FeedbackAggregate
                        | FeedbackRatingDB
                        | float
                        | HallucinationSegment
                        | int
                        | None
                        | Segment
                        | str
                        | UUID
                    ]
                ]
            ]
            | None
            | Segment
            | str
            | UUID
        ):
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
                    ) -> (
                        bool
                        | datetime.datetime
                        | Document
                        | FeedbackAggregate
                        | FeedbackRatingDB
                        | float
                        | HallucinationSegment
                        | int
                        | None
                        | Segment
                        | str
                        | UUID
                    ):
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
                            bool
                            | datetime.datetime
                            | Document
                            | FeedbackAggregate
                            | FeedbackRatingDB
                            | float
                            | HallucinationSegment
                            | int
                            | None
                            | Segment
                            | str
                            | UUID,
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
                        ) -> (
                            bool
                            | datetime.datetime
                            | Document
                            | FeedbackAggregate
                            | FeedbackRatingDB
                            | float
                            | HallucinationSegment
                            | int
                            | None
                            | Segment
                            | str
                            | UUID
                        ):
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
                                bool
                                | datetime.datetime
                                | Document
                                | FeedbackAggregate
                                | FeedbackRatingDB
                                | float
                                | HallucinationSegment
                                | int
                                | None
                                | Segment
                                | str
                                | UUID,
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
                            ) -> (
                                bool
                                | datetime.datetime
                                | Document
                                | FeedbackAggregate
                                | FeedbackRatingDB
                                | float
                                | HallucinationSegment
                                | int
                                | None
                                | Segment
                                | str
                                | UUID
                            ):
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
                                    bool
                                    | datetime.datetime
                                    | Document
                                    | FeedbackAggregate
                                    | FeedbackRatingDB
                                    | float
                                    | HallucinationSegment
                                    | int
                                    | None
                                    | Segment
                                    | str
                                    | UUID,
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
                bool
                | datetime.datetime
                | Document
                | FeedbackAggregate
                | FeedbackRatingDB
                | float
                | HallucinationSegment
                | int
                | list[
                    bool
                    | datetime.datetime
                    | Document
                    | FeedbackAggregate
                    | FeedbackRatingDB
                    | float
                    | HallucinationSegment
                    | int
                    | None
                    | Segment
                    | str
                    | UUID
                ]
                | list[
                    list[
                        bool
                        | datetime.datetime
                        | Document
                        | FeedbackAggregate
                        | FeedbackRatingDB
                        | float
                        | HallucinationSegment
                        | int
                        | None
                        | Segment
                        | str
                        | UUID
                    ]
                ]
                | list[
                    list[
                        list[
                            bool
                            | datetime.datetime
                            | Document
                            | FeedbackAggregate
                            | FeedbackRatingDB
                            | float
                            | HallucinationSegment
                            | int
                            | None
                            | Segment
                            | str
                            | UUID
                        ]
                    ]
                ]
                | None
                | Segment
                | str
                | UUID,
                data,
            )

        value = _parse_value(d.pop("value"))

        status_type = cast(Literal["success"] | Unset, d.pop("status_type", UNSET))
        if status_type != "success" and not isinstance(status_type, Unset):
            raise ValueError(f"status_type must match const 'success', got '{status_type}'")

        def _parse_scorer_type(data: object) -> None | ScorerType | Unset:
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
            return cast(None | ScorerType | Unset, data)

        scorer_type = _parse_scorer_type(d.pop("scorer_type", UNSET))

        def _parse_metric_key_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        metric_key_alias = _parse_metric_key_alias(d.pop("metric_key_alias", UNSET))

        def _parse_explanation(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        explanation = _parse_explanation(d.pop("explanation", UNSET))

        def _parse_cost(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        cost = _parse_cost(d.pop("cost", UNSET))

        def _parse_model_alias(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_alias = _parse_model_alias(d.pop("model_alias", UNSET))

        def _parse_num_judges(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        def _parse_input_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        input_tokens = _parse_input_tokens(d.pop("input_tokens", UNSET))

        def _parse_output_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        output_tokens = _parse_output_tokens(d.pop("output_tokens", UNSET))

        def _parse_total_tokens(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_tokens = _parse_total_tokens(d.pop("total_tokens", UNSET))

        def _parse_critique(data: object) -> MetricCritiqueColumnar | None | Unset:
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
            return cast(MetricCritiqueColumnar | None | Unset, data)

        critique = _parse_critique(d.pop("critique", UNSET))

        def _parse_display_value(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        display_value = _parse_display_value(d.pop("display_value", UNSET))

        def _parse_rationale(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        rationale = _parse_rationale(d.pop("rationale", UNSET))

        metric_success = cls(
            value=value,
            status_type=status_type,
            scorer_type=scorer_type,
            metric_key_alias=metric_key_alias,
            explanation=explanation,
            cost=cost,
            model_alias=model_alias,
            num_judges=num_judges,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            critique=critique,
            display_value=display_value,
            rationale=rationale,
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
