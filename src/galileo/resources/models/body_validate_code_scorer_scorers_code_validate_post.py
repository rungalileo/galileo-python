from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="BodyValidateCodeScorerScorersCodeValidatePost")


@_attrs_define
class BodyValidateCodeScorerScorersCodeValidatePost:
    """
    Attributes
    ----------
        file (File):
        test_input (Union[None, Unset, str]):
        test_output (Union[None, Unset, str]):
        required_scorers (Union[None, Unset, list[str], str]):
        scoreable_node_types (Union[None, Unset, list[str], str]):
    """

    file: File
    test_input: Union[None, Unset, str] = UNSET
    test_output: Union[None, Unset, str] = UNSET
    required_scorers: Union[None, Unset, list[str], str] = UNSET
    scoreable_node_types: Union[None, Unset, list[str], str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        test_input: Union[None, Unset, str]
        test_input = UNSET if isinstance(self.test_input, Unset) else self.test_input

        test_output: Union[None, Unset, str]
        test_output = UNSET if isinstance(self.test_output, Unset) else self.test_output

        required_scorers: Union[None, Unset, list[str], str]
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        scoreable_node_types: Union[None, Unset, list[str], str]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"file": file})
        if test_input is not UNSET:
            field_dict["test_input"] = test_input
        if test_output is not UNSET:
            field_dict["test_output"] = test_output
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        if not isinstance(self.test_input, Unset):
            if isinstance(self.test_input, str):
                files.append(("test_input", (None, str(self.test_input).encode(), "text/plain")))
            else:
                files.append(("test_input", (None, str(self.test_input).encode(), "text/plain")))

        if not isinstance(self.test_output, Unset):
            if isinstance(self.test_output, str):
                files.append(("test_output", (None, str(self.test_output).encode(), "text/plain")))
            else:
                files.append(("test_output", (None, str(self.test_output).encode(), "text/plain")))

        if not isinstance(self.required_scorers, Unset):
            if isinstance(self.required_scorers, str):
                files.append(("required_scorers", (None, str(self.required_scorers).encode(), "text/plain")))
            elif isinstance(self.required_scorers, list):
                for required_scorers_type_1_item_element in self.required_scorers:
                    files.append(
                        ("required_scorers", (None, str(required_scorers_type_1_item_element).encode(), "text/plain"))
                    )
            else:
                files.append(("required_scorers", (None, str(self.required_scorers).encode(), "text/plain")))

        if not isinstance(self.scoreable_node_types, Unset):
            if isinstance(self.scoreable_node_types, str):
                files.append(("scoreable_node_types", (None, str(self.scoreable_node_types).encode(), "text/plain")))
            elif isinstance(self.scoreable_node_types, list):
                for scoreable_node_types_type_1_item_element in self.scoreable_node_types:
                    files.append(
                        (
                            "scoreable_node_types",
                            (None, str(scoreable_node_types_type_1_item_element).encode(), "text/plain"),
                        )
                    )
            else:
                files.append(("scoreable_node_types", (None, str(self.scoreable_node_types).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file = File(payload=BytesIO(d.pop("file")))

        def _parse_test_input(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_input = _parse_test_input(d.pop("test_input", UNSET))

        def _parse_test_output(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        test_output = _parse_test_output(d.pop("test_output", UNSET))

        def _parse_required_scorers(data: object) -> Union[None, Unset, list[str], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str], str], data)

        required_scorers = _parse_required_scorers(d.pop("required_scorers", UNSET))

        def _parse_scoreable_node_types(data: object) -> Union[None, Unset, list[str], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                return cast(list[str], data)

            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str], str], data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        body_validate_code_scorer_scorers_code_validate_post = cls(
            file=file,
            test_input=test_input,
            test_output=test_output,
            required_scorers=required_scorers,
            scoreable_node_types=scoreable_node_types,
        )

        body_validate_code_scorer_scorers_code_validate_post.additional_properties = d
        return body_validate_code_scorer_scorers_code_validate_post

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
