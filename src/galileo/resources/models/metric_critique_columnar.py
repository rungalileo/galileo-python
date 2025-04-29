from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_critique_content import MetricCritiqueContent


T = TypeVar("T", bound="MetricCritiqueColumnar")


@_attrs_define
class MetricCritiqueColumnar:
    """
    Attributes:
        critique_info (MetricCritiqueContent):
        id (str):
        is_computed (bool):
        revised_explanation (Union[None, str]):
    """

    critique_info: "MetricCritiqueContent"
    id: str
    is_computed: bool
    revised_explanation: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        critique_info = self.critique_info.to_dict()

        id = self.id

        is_computed = self.is_computed

        revised_explanation: Union[None, str]
        revised_explanation = self.revised_explanation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "critique_info": critique_info,
                "id": id,
                "is_computed": is_computed,
                "revised_explanation": revised_explanation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_critique_content import MetricCritiqueContent

        d = src_dict.copy()
        critique_info = MetricCritiqueContent.from_dict(d.pop("critique_info"))

        id = d.pop("id")

        is_computed = d.pop("is_computed")

        def _parse_revised_explanation(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        revised_explanation = _parse_revised_explanation(d.pop("revised_explanation"))

        metric_critique_columnar = cls(
            critique_info=critique_info, id=id, is_computed=is_computed, revised_explanation=revised_explanation
        )

        metric_critique_columnar.additional_properties = d
        return metric_critique_columnar

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
