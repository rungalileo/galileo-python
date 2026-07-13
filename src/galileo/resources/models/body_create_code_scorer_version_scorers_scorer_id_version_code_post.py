from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import File

T = TypeVar("T", bound="BodyCreateCodeScorerVersionScorersScorerIdVersionCodePost")


@_attrs_define
class BodyCreateCodeScorerVersionScorersScorerIdVersionCodePost:
    """
    Attributes
    ----------
        file (File):
        validation_result (str): Pre-validated result as JSON string from the validate endpoint.
    """

    file: File
    validation_result: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        validation_result = self.validation_result

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"file": file, "validation_result": validation_result})

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        files.append(("validation_result", (None, str(self.validation_result).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file = File(payload=BytesIO(d.pop("file")))

        validation_result = d.pop("validation_result")

        body_create_code_scorer_version_scorers_scorer_id_version_code_post = cls(
            file=file, validation_result=validation_result
        )

        body_create_code_scorer_version_scorers_scorer_id_version_code_post.additional_properties = d
        return body_create_code_scorer_version_scorers_scorer_id_version_code_post

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
