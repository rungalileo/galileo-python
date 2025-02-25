from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

T = TypeVar("T", bound="SimilarToResponse")


@_attrs_define
class SimilarToResponse:
    """
    Attributes:
        from_split (Split):
        project_id (str):
        run_id (str):
        similar_ids (list[int]):
        split (Split):
        from_inference_name (Union[None, Unset, str]):
        inference_name (Union[None, Unset, str]):
        task (Union[None, Unset, str]):
    """

    from_split: Split
    project_id: str
    run_id: str
    similar_ids: list[int]
    split: Split
    from_inference_name: Union[None, Unset, str] = UNSET
    inference_name: Union[None, Unset, str] = UNSET
    task: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_split = self.from_split.value

        project_id = self.project_id

        run_id = self.run_id

        similar_ids = self.similar_ids

        split = self.split.value

        from_inference_name: Union[None, Unset, str]
        if isinstance(self.from_inference_name, Unset):
            from_inference_name = UNSET
        else:
            from_inference_name = self.from_inference_name

        inference_name: Union[None, Unset, str]
        if isinstance(self.inference_name, Unset):
            inference_name = UNSET
        else:
            inference_name = self.inference_name

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from_split": from_split,
                "project_id": project_id,
                "run_id": run_id,
                "similar_ids": similar_ids,
                "split": split,
            }
        )
        if from_inference_name is not UNSET:
            field_dict["from_inference_name"] = from_inference_name
        if inference_name is not UNSET:
            field_dict["inference_name"] = inference_name
        if task is not UNSET:
            field_dict["task"] = task

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        from_split = Split(d.pop("from_split"))

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        similar_ids = cast(list[int], d.pop("similar_ids"))

        split = Split(d.pop("split"))

        def _parse_from_inference_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        from_inference_name = _parse_from_inference_name(d.pop("from_inference_name", UNSET))

        def _parse_inference_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inference_name = _parse_inference_name(d.pop("inference_name", UNSET))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        similar_to_response = cls(
            from_split=from_split,
            project_id=project_id,
            run_id=run_id,
            similar_ids=similar_ids,
            split=split,
            from_inference_name=from_inference_name,
            inference_name=inference_name,
            task=task,
        )

        similar_to_response.additional_properties = d
        return similar_to_response

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
