from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_row_column import PromptRowColumn


T = TypeVar("T", bound="GetPromptRowsColumnarResponse")


@_attrs_define
class GetPromptRowsColumnarResponse:
    """
    Attributes:
        columns (Union[Unset, list['PromptRowColumn']]):
        limit (Union[Unset, int]):  Default: 100.
        next_starting_token (Union[None, Unset, int]):
        num_filtered_rows (Union[None, Unset, int]):
        num_rows (Union[None, Unset, int]):
        paginated (Union[Unset, bool]):  Default: False.
        starting_token (Union[Unset, int]):  Default: 0.
    """

    columns: Union[Unset, list["PromptRowColumn"]] = UNSET
    limit: Union[Unset, int] = 100
    next_starting_token: Union[None, Unset, int] = UNSET
    num_filtered_rows: Union[None, Unset, int] = UNSET
    num_rows: Union[None, Unset, int] = UNSET
    paginated: Union[Unset, bool] = False
    starting_token: Union[Unset, int] = 0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        columns: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()
                columns.append(columns_item)

        limit = self.limit

        next_starting_token: Union[None, Unset, int]
        if isinstance(self.next_starting_token, Unset):
            next_starting_token = UNSET
        else:
            next_starting_token = self.next_starting_token

        num_filtered_rows: Union[None, Unset, int]
        if isinstance(self.num_filtered_rows, Unset):
            num_filtered_rows = UNSET
        else:
            num_filtered_rows = self.num_filtered_rows

        num_rows: Union[None, Unset, int]
        if isinstance(self.num_rows, Unset):
            num_rows = UNSET
        else:
            num_rows = self.num_rows

        paginated = self.paginated

        starting_token = self.starting_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if columns is not UNSET:
            field_dict["columns"] = columns
        if limit is not UNSET:
            field_dict["limit"] = limit
        if next_starting_token is not UNSET:
            field_dict["next_starting_token"] = next_starting_token
        if num_filtered_rows is not UNSET:
            field_dict["num_filtered_rows"] = num_filtered_rows
        if num_rows is not UNSET:
            field_dict["num_rows"] = num_rows
        if paginated is not UNSET:
            field_dict["paginated"] = paginated
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.prompt_row_column import PromptRowColumn

        d = src_dict.copy()
        columns = []
        _columns = d.pop("columns", UNSET)
        for columns_item_data in _columns or []:
            columns_item = PromptRowColumn.from_dict(columns_item_data)

            columns.append(columns_item)

        limit = d.pop("limit", UNSET)

        def _parse_next_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_starting_token = _parse_next_starting_token(d.pop("next_starting_token", UNSET))

        def _parse_num_filtered_rows(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_filtered_rows = _parse_num_filtered_rows(d.pop("num_filtered_rows", UNSET))

        def _parse_num_rows(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_rows = _parse_num_rows(d.pop("num_rows", UNSET))

        paginated = d.pop("paginated", UNSET)

        starting_token = d.pop("starting_token", UNSET)

        get_prompt_rows_columnar_response = cls(
            columns=columns,
            limit=limit,
            next_starting_token=next_starting_token,
            num_filtered_rows=num_filtered_rows,
            num_rows=num_rows,
            paginated=paginated,
            starting_token=starting_token,
        )

        get_prompt_rows_columnar_response.additional_properties = d
        return get_prompt_rows_columnar_response

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
