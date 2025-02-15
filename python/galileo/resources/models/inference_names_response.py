from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InferenceNamesResponse")


@_attrs_define
class InferenceNamesResponse:
    """
    Attributes:
        inference_names (list[str]):
        project_id (str):
        run_id (str):
    """

    inference_names: list[str]
    project_id: str
    run_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inference_names = self.inference_names

        project_id = self.project_id

        run_id = self.run_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inference_names": inference_names,
                "project_id": project_id,
                "run_id": run_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        inference_names = cast(list[str], d.pop("inference_names"))

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        inference_names_response = cls(
            inference_names=inference_names,
            project_id=project_id,
            run_id=run_id,
        )

        inference_names_response.additional_properties = d
        return inference_names_response

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
