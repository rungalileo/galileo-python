from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_runs_filter_operator import ProjectRunsFilterOperator
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRunsFilter")


@_attrs_define
class ProjectRunsFilter:
    """
    Attributes:
        operator (ProjectRunsFilterOperator):
        value (Union[int, list[int]]):
        name (Union[Literal['runs'], Unset]):  Default: 'runs'.
    """

    operator: ProjectRunsFilterOperator
    value: Union[int, list[int]]
    name: Union[Literal["runs"], Unset] = "runs"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        operator = self.operator.value

        value: Union[int, list[int]]
        if isinstance(self.value, list):
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
        operator = ProjectRunsFilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[int, list[int]]:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(list[int], data)

                return value_type_1
            except:  # noqa: E722
                pass
            return cast(Union[int, list[int]], data)

        value = _parse_value(d.pop("value"))

        name = cast(Union[Literal["runs"], Unset], d.pop("name", UNSET))
        if name != "runs" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'runs', got '{name}'")

        project_runs_filter = cls(operator=operator, value=value, name=name)

        project_runs_filter.additional_properties = d
        return project_runs_filter

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
