from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_row import DatasetRow


T = TypeVar("T", bound="DatasetContent")


@_attrs_define
class DatasetContent:
    """
    Attributes
    ----------
        starting_token (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 100.
        paginated (Union[Unset, bool]):  Default: False.
        next_starting_token (Union[None, Unset, int]):
        column_names (Union[Unset, list[str]]):
        warning_message (Union[None, Unset, str]):
        rows (Union[Unset, list['DatasetRow']]):
    """

    starting_token: Union[Unset, int] = 0
    limit: Union[Unset, int] = 100
    paginated: Union[Unset, bool] = False
    next_starting_token: Union[None, Unset, int] = UNSET
    column_names: Union[Unset, list[str]] = UNSET
    warning_message: Union[None, Unset, str] = UNSET
    rows: Union[Unset, list["DatasetRow"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        starting_token = self.starting_token

        limit = self.limit

        paginated = self.paginated

        next_starting_token: Union[None, Unset, int]
        next_starting_token = UNSET if isinstance(self.next_starting_token, Unset) else self.next_starting_token

        column_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.column_names, Unset):
            column_names = self.column_names

        warning_message: Union[None, Unset, str]
        warning_message = UNSET if isinstance(self.warning_message, Unset) else self.warning_message

        rows: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data.to_dict()
                rows.append(rows_item)

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
        if column_names is not UNSET:
            field_dict["column_names"] = column_names
        if warning_message is not UNSET:
            field_dict["warning_message"] = warning_message
        if rows is not UNSET:
            field_dict["rows"] = rows

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_row import DatasetRow

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

        column_names = cast(list[str], d.pop("column_names", UNSET))

        def _parse_warning_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        warning_message = _parse_warning_message(d.pop("warning_message", UNSET))

        rows = []
        _rows = d.pop("rows", UNSET)
        for rows_item_data in _rows or []:
            rows_item = DatasetRow.from_dict(rows_item_data)

            rows.append(rows_item)

        dataset_content = cls(
            starting_token=starting_token,
            limit=limit,
            paginated=paginated,
            next_starting_token=next_starting_token,
            column_names=column_names,
            warning_message=warning_message,
            rows=rows,
        )

        dataset_content.additional_properties = d
        return dataset_content

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
