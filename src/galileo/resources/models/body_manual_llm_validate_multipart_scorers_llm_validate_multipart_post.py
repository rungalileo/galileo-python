from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyManualLlmValidateMultipartScorersLlmValidateMultipartPost")


@_attrs_define
class BodyManualLlmValidateMultipartScorersLlmValidateMultipartPost:
    """
    Attributes:
        body (str): JSON-encoded GeneratedScorerValidationRequest
        query_files (Union[Unset, list[str]]):
        response_files (Union[Unset, list[str]]):
    """

    body: str
    query_files: Union[Unset, list[str]] = UNSET
    response_files: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        query_files: Union[Unset, list[str]] = UNSET
        if not isinstance(self.query_files, Unset):
            query_files = self.query_files

        response_files: Union[Unset, list[str]] = UNSET
        if not isinstance(self.response_files, Unset):
            response_files = self.response_files

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"body": body})
        if query_files is not UNSET:
            field_dict["query_files"] = query_files
        if response_files is not UNSET:
            field_dict["response_files"] = response_files

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("body", (None, str(self.body).encode(), "text/plain")))

        if not isinstance(self.query_files, Unset):
            for query_files_item_element in self.query_files:
                files.append(("query_files", (None, str(query_files_item_element).encode(), "text/plain")))

        if not isinstance(self.response_files, Unset):
            for response_files_item_element in self.response_files:
                files.append(("response_files", (None, str(response_files_item_element).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        body = d.pop("body")

        query_files = cast(list[str], d.pop("query_files", UNSET))

        response_files = cast(list[str], d.pop("response_files", UNSET))

        body_manual_llm_validate_multipart_scorers_llm_validate_multipart_post = cls(
            body=body, query_files=query_files, response_files=response_files
        )

        body_manual_llm_validate_multipart_scorers_llm_validate_multipart_post.additional_properties = d
        return body_manual_llm_validate_multipart_scorers_llm_validate_multipart_post

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
