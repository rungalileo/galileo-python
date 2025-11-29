from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="LabelStudioExportRequest")


@_attrs_define
class LabelStudioExportRequest:
    """Schema for requesting data to be sent to labelstudio.

    Coming soon!

    Attributes
    ----------
            project_name (str):
            project_id (str):
            run_id (str):
            split (Split):
            task (Union[None, Unset, str]):
            filter_params (Union[Unset, FilterParams]):
            compare_to (Union[None, Split, Unset]):
            map_threshold (Union[Unset, float]):  Default: 0.5.
            workspace (Union[None, Unset, str]):
            inference_name (Union[None, Unset, str]):
            labels (Union[None, Unset, list[str]]):
    """

    project_name: str
    project_id: str
    run_id: str
    split: Split
    task: Union[None, Unset, str] = UNSET
    filter_params: Union[Unset, "FilterParams"] = UNSET
    compare_to: Union[None, Split, Unset] = UNSET
    map_threshold: Union[Unset, float] = 0.5
    workspace: Union[None, Unset, str] = UNSET
    inference_name: Union[None, Unset, str] = UNSET
    labels: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_name = self.project_name

        project_id = self.project_id

        run_id = self.run_id

        split = self.split.value

        task: Union[None, Unset, str]
        task = UNSET if isinstance(self.task, Unset) else self.task

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        compare_to: Union[None, Unset, str]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET
        elif isinstance(self.compare_to, Split):
            compare_to = self.compare_to.value
        else:
            compare_to = self.compare_to

        map_threshold = self.map_threshold

        workspace: Union[None, Unset, str]
        workspace = UNSET if isinstance(self.workspace, Unset) else self.workspace

        inference_name: Union[None, Unset, str]
        inference_name = UNSET if isinstance(self.inference_name, Unset) else self.inference_name

        labels: Union[None, Unset, list[str]]
        if isinstance(self.labels, Unset):
            labels = UNSET
        elif isinstance(self.labels, list):
            labels = self.labels

        else:
            labels = self.labels

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"project_name": project_name, "project_id": project_id, "run_id": run_id, "split": split})
        if task is not UNSET:
            field_dict["task"] = task
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if workspace is not UNSET:
            field_dict["workspace"] = workspace
        if inference_name is not UNSET:
            field_dict["inference_name"] = inference_name
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_params import FilterParams

        d = dict(src_dict)
        project_name = d.pop("project_name")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        split = Split(d.pop("split"))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        _filter_params = d.pop("filter_params", UNSET)
        filter_params: Union[Unset, FilterParams]
        filter_params = UNSET if isinstance(_filter_params, Unset) else FilterParams.from_dict(_filter_params)

        def _parse_compare_to(data: object) -> Union[None, Split, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return Split(data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Split, Unset], data)

        compare_to = _parse_compare_to(d.pop("compare_to", UNSET))

        map_threshold = d.pop("map_threshold", UNSET)

        def _parse_workspace(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        workspace = _parse_workspace(d.pop("workspace", UNSET))

        def _parse_inference_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inference_name = _parse_inference_name(d.pop("inference_name", UNSET))

        def _parse_labels(data: object) -> Union[None, Unset, list[str]]:
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
            return cast(Union[None, Unset, list[str]], data)

        labels = _parse_labels(d.pop("labels", UNSET))

        label_studio_export_request = cls(
            project_name=project_name,
            project_id=project_id,
            run_id=run_id,
            split=split,
            task=task,
            filter_params=filter_params,
            compare_to=compare_to,
            map_threshold=map_threshold,
            workspace=workspace,
            inference_name=inference_name,
            labels=labels,
        )

        label_studio_export_request.additional_properties = d
        return label_studio_export_request

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
