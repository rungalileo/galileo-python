from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.prompt_sample_i_ds_sample_indices import PromptSampleIDsSampleIndices


T = TypeVar("T", bound="PromptSampleIDs")


@_attrs_define
class PromptSampleIDs:
    """
    Attributes:
        sample_indices (PromptSampleIDsSampleIndices):
        total_samples (int):
    """

    sample_indices: "PromptSampleIDsSampleIndices"
    total_samples: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sample_indices = self.sample_indices.to_dict()

        total_samples = self.total_samples

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"sample_indices": sample_indices, "total_samples": total_samples})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.prompt_sample_i_ds_sample_indices import PromptSampleIDsSampleIndices

        d = src_dict.copy()
        sample_indices = PromptSampleIDsSampleIndices.from_dict(d.pop("sample_indices"))

        total_samples = d.pop("total_samples")

        prompt_sample_i_ds = cls(sample_indices=sample_indices, total_samples=total_samples)

        prompt_sample_i_ds.additional_properties = d
        return prompt_sample_i_ds

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
