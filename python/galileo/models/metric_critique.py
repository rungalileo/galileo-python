from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.metric_critique_content import MetricCritiqueContent
    from ..models.metric_inputs import MetricInputs


T = TypeVar("T", bound="MetricCritique")


@_attrs_define
class MetricCritique:
    """
    Attributes:
        critique_info (MetricCritiqueContent):
        id (str):
        is_computed (bool):
        metric (str):
        metric_inputs (MetricInputs): Metric inputs for a prompt template.
            Include an optional inputs_config to help formatting with a prompt template.
        project_id (str):
        revised_explanation (Union[None, str]):
        row_id (Union[UUID, int]):
        run_id (Union[None, str]):
    """

    critique_info: "MetricCritiqueContent"
    id: str
    is_computed: bool
    metric: str
    metric_inputs: "MetricInputs"
    project_id: str
    revised_explanation: Union[None, str]
    row_id: Union[UUID, int]
    run_id: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        critique_info = self.critique_info.to_dict()

        id = self.id

        is_computed = self.is_computed

        metric = self.metric

        metric_inputs = self.metric_inputs.to_dict()

        project_id = self.project_id

        revised_explanation: Union[None, str]
        revised_explanation = self.revised_explanation

        row_id: Union[int, str]
        if isinstance(self.row_id, UUID):
            row_id = str(self.row_id)
        else:
            row_id = self.row_id

        run_id: Union[None, str]
        run_id = self.run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "critique_info": critique_info,
                "id": id,
                "is_computed": is_computed,
                "metric": metric,
                "metric_inputs": metric_inputs,
                "project_id": project_id,
                "revised_explanation": revised_explanation,
                "row_id": row_id,
                "run_id": run_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.metric_critique_content import MetricCritiqueContent
        from ..models.metric_inputs import MetricInputs

        d = src_dict.copy()
        critique_info = MetricCritiqueContent.from_dict(d.pop("critique_info"))

        id = d.pop("id")

        is_computed = d.pop("is_computed")

        metric = d.pop("metric")

        metric_inputs = MetricInputs.from_dict(d.pop("metric_inputs"))

        project_id = d.pop("project_id")

        def _parse_revised_explanation(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        revised_explanation = _parse_revised_explanation(d.pop("revised_explanation"))

        def _parse_row_id(data: object) -> Union[UUID, int]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                row_id_type_0 = UUID(data)

                return row_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[UUID, int], data)

        row_id = _parse_row_id(d.pop("row_id"))

        def _parse_run_id(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        run_id = _parse_run_id(d.pop("run_id"))

        metric_critique = cls(
            critique_info=critique_info,
            id=id,
            is_computed=is_computed,
            metric=metric,
            metric_inputs=metric_inputs,
            project_id=project_id,
            revised_explanation=revised_explanation,
            row_id=row_id,
            run_id=run_id,
        )

        metric_critique.additional_properties = d
        return metric_critique

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
