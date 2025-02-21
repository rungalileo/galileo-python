from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.split import Split

if TYPE_CHECKING:
    from ..models.run_results import RunResults


T = TypeVar("T", bound="SplitRunResults")


@_attrs_define
class SplitRunResults:
    """
    Attributes:
        split_name (Split):
        split_run_results (RunResults):
    """

    split_name: Split
    split_run_results: "RunResults"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        split_name = self.split_name.value

        split_run_results = self.split_run_results.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"split_name": split_name, "split_run_results": split_run_results})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.run_results import RunResults

        d = src_dict.copy()
        split_name = Split(d.pop("split_name"))

        split_run_results = RunResults.from_dict(d.pop("split_run_results"))

        split_run_results = cls(split_name=split_name, split_run_results=split_run_results)

        split_run_results.additional_properties = d
        return split_run_results

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
