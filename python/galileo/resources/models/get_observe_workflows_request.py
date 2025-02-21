from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_metadata_filter import UserMetadataFilter


T = TypeVar("T", bound="GetObserveWorkflowsRequest")


@_attrs_define
class GetObserveWorkflowsRequest:
    """
    Attributes:
        filters (Union[Unset, list['UserMetadataFilter']]):
        limit (Union[Unset, int]):  Default: 100.
        starting_token (Union[Unset, int]):  Default: 0.
    """

    filters: Union[Unset, list["UserMetadataFilter"]] = UNSET
    limit: Union[Unset, int] = 100
    starting_token: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)

        limit = self.limit

        starting_token = self.starting_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if limit is not UNSET:
            field_dict["limit"] = limit
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.user_metadata_filter import UserMetadataFilter

        d = src_dict.copy()
        filters = []
        _filters = d.pop("filters", UNSET)
        for filters_item_data in _filters or []:
            filters_item = UserMetadataFilter.from_dict(filters_item_data)

            filters.append(filters_item)

        limit = d.pop("limit", UNSET)

        starting_token = d.pop("starting_token", UNSET)

        get_observe_workflows_request = cls(filters=filters, limit=limit, starting_token=starting_token)

        get_observe_workflows_request.additional_properties = d
        return get_observe_workflows_request

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
