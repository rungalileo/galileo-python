from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HasEmbeddingsResponse")


@_attrs_define
class HasEmbeddingsResponse:
    """
    Attributes:
        has_data_embs (Union[Unset, bool]):  Default: False.
        has_model_embs (Union[Unset, bool]):  Default: False.
    """

    has_data_embs: Union[Unset, bool] = False
    has_model_embs: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_data_embs = self.has_data_embs

        has_model_embs = self.has_model_embs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if has_data_embs is not UNSET:
            field_dict["has_data_embs"] = has_data_embs
        if has_model_embs is not UNSET:
            field_dict["has_model_embs"] = has_model_embs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        has_data_embs = d.pop("has_data_embs", UNSET)

        has_model_embs = d.pop("has_model_embs", UNSET)

        has_embeddings_response = cls(has_data_embs=has_data_embs, has_model_embs=has_model_embs)

        has_embeddings_response.additional_properties = d
        return has_embeddings_response

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
