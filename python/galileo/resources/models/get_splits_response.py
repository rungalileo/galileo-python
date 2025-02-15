from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split

T = TypeVar("T", bound="GetSplitsResponse")


@_attrs_define
class GetSplitsResponse:
    """
    Attributes:
        inference_comparison_splits (list[Split]):
        project_id (str):
        run_id (str):
        splits (list[Split]):
    """

    inference_comparison_splits: list[Split]
    project_id: str
    run_id: str
    splits: list[Split]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inference_comparison_splits = []
        for inference_comparison_splits_item_data in self.inference_comparison_splits:
            inference_comparison_splits_item = inference_comparison_splits_item_data.value
            inference_comparison_splits.append(inference_comparison_splits_item)

        project_id = self.project_id

        run_id = self.run_id

        splits = []
        for splits_item_data in self.splits:
            splits_item = splits_item_data.value
            splits.append(splits_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inference_comparison_splits": inference_comparison_splits,
                "project_id": project_id,
                "run_id": run_id,
                "splits": splits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        inference_comparison_splits = []
        _inference_comparison_splits = d.pop("inference_comparison_splits")
        for inference_comparison_splits_item_data in _inference_comparison_splits:
            inference_comparison_splits_item = Split(inference_comparison_splits_item_data)

            inference_comparison_splits.append(inference_comparison_splits_item)

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        splits = []
        _splits = d.pop("splits")
        for splits_item_data in _splits:
            splits_item = Split(splits_item_data)

            splits.append(splits_item)

        get_splits_response = cls(
            inference_comparison_splits=inference_comparison_splits,
            project_id=project_id,
            run_id=run_id,
            splits=splits,
        )

        get_splits_response.additional_properties = d
        return get_splits_response

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
