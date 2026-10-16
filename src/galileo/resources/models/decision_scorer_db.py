import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.decision_level import DecisionLevel


T = TypeVar("T", bound="DecisionScorerDB")


@_attrs_define
class DecisionScorerDB:
    """A row of the decision_scorers table.

    answer_options depends on the output type of the scorer:
    - categorical: a list of labels (list[str]).
    - discrete: a list of DecisionLevel.
    - boolean_probability: None.

    Attributes
    ----------
            id (str):
            organization_id (str):
            question (str):
            created_at (datetime.datetime):
            created_by (Union[None, Unset, str]):
            answer_options (Union[None, Unset, list['DecisionLevel'], list[str]]):
    """

    id: str
    organization_id: str
    question: str
    created_at: datetime.datetime
    created_by: None | Unset | str = UNSET
    answer_options: None | Unset | list["DecisionLevel"] | list[str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        organization_id = self.organization_id

        question = self.question

        created_at = self.created_at.isoformat()

        created_by: None | Unset | str
        created_by = UNSET if isinstance(self.created_by, Unset) else self.created_by

        answer_options: None | Unset | list[dict[str, Any]] | list[str]
        if isinstance(self.answer_options, Unset):
            answer_options = UNSET
        elif isinstance(self.answer_options, list):
            answer_options = self.answer_options

        elif isinstance(self.answer_options, list):
            answer_options = []
            for answer_options_type_1_item_data in self.answer_options:
                answer_options_type_1_item = answer_options_type_1_item_data.to_dict()
                answer_options.append(answer_options_type_1_item)

        else:
            answer_options = self.answer_options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"id": id, "organization_id": organization_id, "question": question, "created_at": created_at}
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if answer_options is not UNSET:
            field_dict["answer_options"] = answer_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.decision_level import DecisionLevel

        d = dict(src_dict)
        id = d.pop("id")

        organization_id = d.pop("organization_id")

        question = d.pop("question")

        created_at = isoparse(d.pop("created_at"))

        def _parse_created_by(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_answer_options(data: object) -> None | Unset | list["DecisionLevel"] | list[str]:
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
            try:
                if not isinstance(data, list):
                    raise TypeError()
                answer_options_type_1 = []
                _answer_options_type_1 = data
                for answer_options_type_1_item_data in _answer_options_type_1:
                    answer_options_type_1_item = DecisionLevel.from_dict(answer_options_type_1_item_data)

                    answer_options_type_1.append(answer_options_type_1_item)

                return answer_options_type_1
            except:  # noqa: E722
                pass
            return cast(None | Unset | list["DecisionLevel"] | list[str], data)

        answer_options = _parse_answer_options(d.pop("answer_options", UNSET))

        decision_scorer_db = cls(
            id=id,
            organization_id=organization_id,
            question=question,
            created_at=created_at,
            created_by=created_by,
            answer_options=answer_options,
        )

        decision_scorer_db.additional_properties = d
        return decision_scorer_db

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
