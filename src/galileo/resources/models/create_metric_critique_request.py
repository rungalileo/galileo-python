from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateMetricCritiqueRequest")


@_attrs_define
class CreateMetricCritiqueRequest:
    """
    Attributes:
        critique (str):
        intended_value (bool): Set to opposite of actual value for new critiques, and set as same as existing critique
            intended value for updates.
        row_id (Union[UUID, int]):
        run_id (Union[None, str]):
        id (Union[None, Unset, str]): The id of the metric critique if it's being updated. None if it's a new critique.
    """

    critique: str
    intended_value: bool
    row_id: Union[UUID, int]
    run_id: Union[None, str]
    id: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        critique = self.critique

        intended_value = self.intended_value

        row_id: Union[int, str]
        if isinstance(self.row_id, UUID):
            row_id = str(self.row_id)
        else:
            row_id = self.row_id

        run_id: Union[None, str]
        run_id = self.run_id

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"critique": critique, "intended_value": intended_value, "row_id": row_id, "run_id": run_id})
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        critique = d.pop("critique")

        intended_value = d.pop("intended_value")

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

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        create_metric_critique_request = cls(
            critique=critique, intended_value=intended_value, row_id=row_id, run_id=run_id, id=id
        )

        create_metric_critique_request.additional_properties = d
        return create_metric_critique_request

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
