from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_project import DatasetProject


T = TypeVar("T", bound="ListDatasetProjectsResponse")


@_attrs_define
class ListDatasetProjectsResponse:
    """
    Attributes
    ----------
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        paginated (Union[Unset, bool]):  Default: False.
        next_starting_token (Union[None, Unset, int]):
        projects (Union[Unset, list['DatasetProject']]):
    """

    starting_token: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    paginated: Union[Unset, bool] = False
    next_starting_token: Union[None, Unset, int] = UNSET
    projects: Union[Unset, list["DatasetProject"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        starting_token = self.starting_token

        limit = self.limit

        paginated = self.paginated

        next_starting_token: Union[None, Unset, int]
        next_starting_token = UNSET if isinstance(self.next_starting_token, Unset) else self.next_starting_token

        projects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = []
            for projects_item_data in self.projects:
                projects_item = projects_item_data.to_dict()
                projects.append(projects_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if limit is not UNSET:
            field_dict["limit"] = limit
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token
        if projects is not UNSET:
            field_dict["projects"] = projects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_project import DatasetProject

        d = dict(src_dict)
        starting_token = d.pop("starting_token", UNSET)

        limit = d.pop("limit", UNSET)

        paginated = d.pop("paginated", UNSET)

        def _parse_next_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        projects = []
        _projects = d.pop("projects", UNSET)
        for projects_item_data in _projects or []:
            projects_item = DatasetProject.from_dict(projects_item_data)

            projects.append(projects_item)

        list_dataset_projects_response = cls(
            starting_token=starting_token,
            limit=limit,
            paginated=paginated,
            next_starting_token=next_starting_token,
            projects=projects,
        )

        list_dataset_projects_response.additional_properties = d
        return list_dataset_projects_response

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
