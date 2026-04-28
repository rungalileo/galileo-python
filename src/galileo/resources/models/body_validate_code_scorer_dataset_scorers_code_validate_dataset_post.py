from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="BodyValidateCodeScorerDatasetScorersCodeValidateDatasetPost")


@_attrs_define
class BodyValidateCodeScorerDatasetScorersCodeValidateDatasetPost:
    """
    Attributes
    ----------
        file (File):
        dataset_id (UUID):
        dataset_version_index (int | None | Unset):
        limit (int | Unset):  Default: 100.
        starting_token (int | None | Unset):
        required_scorers (list[str] | None | str | Unset):
        scoreable_node_types (list[str] | None | str | Unset):
        score_type (None | str | Unset):
    """

    file: File
    dataset_id: UUID
    dataset_version_index: int | None | Unset = UNSET
    limit: int | Unset = 100
    starting_token: int | None | Unset = UNSET
    required_scorers: list[str] | None | str | Unset = UNSET
    scoreable_node_types: list[str] | None | str | Unset = UNSET
    score_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        dataset_id = str(self.dataset_id)

        dataset_version_index: int | None | Unset
        dataset_version_index = UNSET if isinstance(self.dataset_version_index, Unset) else self.dataset_version_index

        limit = self.limit

        starting_token: int | None | Unset
        starting_token = UNSET if isinstance(self.starting_token, Unset) else self.starting_token

        required_scorers: list[str] | None | str | Unset
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        scoreable_node_types: list[str] | None | str | Unset
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        score_type: None | str | Unset
        score_type = UNSET if isinstance(self.score_type, Unset) else self.score_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"file": file, "dataset_id": dataset_id})
        if dataset_version_index is not UNSET:
            field_dict["dataset_version_index"] = dataset_version_index
        if limit is not UNSET:
            field_dict["limit"] = limit
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if score_type is not UNSET:
            field_dict["score_type"] = score_type

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        files.append(("dataset_id", (None, str(self.dataset_id), "text/plain")))

        if not isinstance(self.dataset_version_index, Unset):
            if isinstance(self.dataset_version_index, int):
                files.append(("dataset_version_index", (None, str(self.dataset_version_index).encode(), "text/plain")))
            else:
                files.append(("dataset_version_index", (None, str(self.dataset_version_index).encode(), "text/plain")))

        if not isinstance(self.limit, Unset):
            files.append(("limit", (None, str(self.limit).encode(), "text/plain")))

        if not isinstance(self.starting_token, Unset):
            if isinstance(self.starting_token, int):
                files.append(("starting_token", (None, str(self.starting_token).encode(), "text/plain")))
            else:
                files.append(("starting_token", (None, str(self.starting_token).encode(), "text/plain")))

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

        if not isinstance(self.score_type, Unset):
            if isinstance(self.score_type, str):
                files.append(("score_type", (None, str(self.score_type).encode(), "text/plain")))
            else:
                files.append(("score_type", (None, str(self.score_type).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file = File(payload=BytesIO(d.pop("file")))

        dataset_id = UUID(d.pop("dataset_id"))

        def _parse_dataset_version_index(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        dataset_version_index = _parse_dataset_version_index(d.pop("dataset_version_index", UNSET))

        limit = d.pop("limit", UNSET)

        def _parse_starting_token(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        starting_token = _parse_starting_token(d.pop("starting_token", UNSET))

        def _parse_required_scorers(data: object) -> list[str] | None | str | Unset:
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
            return cast(list[str] | None | str | Unset, data)

        required_scorers = _parse_required_scorers(d.pop("required_scorers", UNSET))

        def _parse_scoreable_node_types(data: object) -> list[str] | None | str | Unset:
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
            return cast(list[str] | None | str | Unset, data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        def _parse_score_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        score_type = _parse_score_type(d.pop("score_type", UNSET))

        body_validate_code_scorer_dataset_scorers_code_validate_dataset_post = cls(
            file=file,
            dataset_id=dataset_id,
            dataset_version_index=dataset_version_index,
            limit=limit,
            starting_token=starting_token,
            required_scorers=required_scorers,
            scoreable_node_types=scoreable_node_types,
            score_type=score_type,
        )

        body_validate_code_scorer_dataset_scorers_code_validate_dataset_post.additional_properties = d
        return body_validate_code_scorer_dataset_scorers_code_validate_dataset_post

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
