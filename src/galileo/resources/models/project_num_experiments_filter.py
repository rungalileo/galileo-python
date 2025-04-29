from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_num_experiments_filter_operator import ProjectNumExperimentsFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectNumExperimentsFilter")


@_attrs_define
class ProjectNumExperimentsFilter:
    """
    Attributes:
        operator (ProjectNumExperimentsFilterOperator):
        value (Union[float, int, list[float], list[int]]):
        name (Union[Literal['num_experiments'], Unset]):  Default: 'num_experiments'.
    """

    operator: ProjectNumExperimentsFilterOperator
    value: Union[float, int, list[float], list[int]]
    name: Union[Literal["num_experiments"], Unset] = "num_experiments"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: Union[float, int, list[float], list[int]]
        if isinstance(self.value, list):
            value = self.value

        elif isinstance(self.value, list):
            value = self.value

        else:
            value = self.value

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"operator": operator, "value": value})
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        operator = ProjectNumExperimentsFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[float, int, list[float], list[int]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_2 = cast(list[int], data)

                return value_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = cast(list[float], data)

                return value_type_3
            except:  # noqa: E722
                pass
            return cast(Union[float, int, list[float], list[int]], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["num_experiments"], Unset], d.pop("name", UNSET))
        if name != "num_experiments" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'num_experiments', got '{name}'")

        project_num_experiments_filter = cls(operator=operator, value=value, name=name)

        project_num_experiments_filter.additional_properties = d
        return project_num_experiments_filter

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
