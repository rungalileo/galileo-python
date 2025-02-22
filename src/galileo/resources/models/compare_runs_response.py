from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split

if TYPE_CHECKING:
    from ..models.project_run_summary import ProjectRunSummary


T = TypeVar("T", bound="CompareRunsResponse")


@_attrs_define
class CompareRunsResponse:
    """
    Attributes:
        project_id (str):
        runs (list['ProjectRunSummary']):
        split (Split):
    """

    project_id: str
    runs: list["ProjectRunSummary"]
    split: Split
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        runs = []
        for runs_item_data in self.runs:
            runs_item = runs_item_data.to_dict()
            runs.append(runs_item)

        split = self.split.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_id": project_id, "runs": runs, "split": split})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.project_run_summary import ProjectRunSummary

        d = src_dict.copy()
        project_id = d.pop("project_id")

        runs = []
        _runs = d.pop("runs")
        for runs_item_data in _runs:
            runs_item = ProjectRunSummary.from_dict(runs_item_data)

            runs.append(runs_item)

        split = Split(d.pop("split"))

        compare_runs_response = cls(project_id=project_id, runs=runs, split=split)

        compare_runs_response.additional_properties = d
        return compare_runs_response

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
