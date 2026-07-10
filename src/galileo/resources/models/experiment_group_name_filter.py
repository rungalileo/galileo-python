from collections.abc import Mapping
from typing import Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.experiment_group_name_filter_operator import ExperimentGroupNameFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExperimentGroupNameFilter")


@_attrs_define
class ExperimentGroupNameFilter:
    """
    Attributes
    ----------
        operator (ExperimentGroupNameFilterOperator):
        value (Union[list[str], str]):
        name (Union[Literal['experiment_group_name'], Unset]):  Default: 'experiment_group_name'.
        case_sensitive (Union[Unset, bool]):  Default: True.
    """

    operator: ExperimentGroupNameFilterOperator
    value: list[str] | str
    name: Literal["experiment_group_name"] | Unset = "experiment_group_name"
    case_sensitive: Unset | bool = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: list[str] | str
        value = self.value if isinstance(self.value, list) else self.value

        name = self.name

        case_sensitive = self.case_sensitive

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name
        if case_sensitive is not UNSET:
            field_dict["case_sensitive"] = case_sensitive

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        operator = ExperimentGroupNameFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> list[str] | str:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(list[str] | str, data)

        value = _parse_value(d.pop("value"))

        name = cast(Literal["experiment_group_name"] | Unset, d.pop("name", UNSET))
        if name != "experiment_group_name" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'experiment_group_name', got '{name}'")

        case_sensitive = d.pop("case_sensitive", UNSET)

        experiment_group_name_filter = cls(operator=operator, value=value, name=name, case_sensitive=case_sensitive)

        experiment_group_name_filter.additional_properties = d
        return experiment_group_name_filter

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
