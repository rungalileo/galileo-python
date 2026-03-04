from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="BodyValidateCodeScorerLogRecordScorersCodeValidateLogRecordPost")


@_attrs_define
class BodyValidateCodeScorerLogRecordScorersCodeValidateLogRecordPost:
    """
    Attributes
    ----------
        file (File):
        log_stream_id (Union[None, Unset, str]):
        experiment_id (Union[None, Unset, str]):
        limit (Union[Unset, int]):  Default: 100.
        starting_token (Union[None, Unset, int]):
        filters (Union[None, Unset, str]): JSON string array of LogRecordsQueryFilter
        sort (Union[None, Unset, str]): JSON string of LogRecordsSortClause
        required_scorers (Union[None, Unset, list[str], str]):
        scoreable_node_types (Union[None, Unset, list[str], str]):
    """

    file: File
    log_stream_id: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    limit: Union[Unset, int] = 100
    starting_token: Union[None, Unset, int] = UNSET
    filters: Union[None, Unset, str] = UNSET
    sort: Union[None, Unset, str] = UNSET
    required_scorers: Union[None, Unset, list[str], str] = UNSET
    scoreable_node_types: Union[None, Unset, list[str], str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file = self.file.to_tuple()

        log_stream_id: Union[None, Unset, str]
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: Union[None, Unset, str]
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        limit = self.limit

        starting_token: Union[None, Unset, int]
        starting_token = UNSET if isinstance(self.starting_token, Unset) else self.starting_token

        filters: Union[None, Unset, str]
        filters = UNSET if isinstance(self.filters, Unset) else self.filters

        sort: Union[None, Unset, str]
        sort = UNSET if isinstance(self.sort, Unset) else self.sort

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
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if limit is not UNSET:
            field_dict["limit"] = limit
        if starting_token is not UNSET:
            field_dict["starting_token"] = starting_token
        if filters is not UNSET:
            field_dict["filters"] = filters
        if sort is not UNSET:
            field_dict["sort"] = sort
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("file", self.file.to_tuple()))

        if not isinstance(self.log_stream_id, Unset):
            if isinstance(self.log_stream_id, str):
                files.append(("log_stream_id", (None, str(self.log_stream_id).encode(), "text/plain")))
            else:
                files.append(("log_stream_id", (None, str(self.log_stream_id).encode(), "text/plain")))

        if not isinstance(self.experiment_id, Unset):
            if isinstance(self.experiment_id, str):
                files.append(("experiment_id", (None, str(self.experiment_id).encode(), "text/plain")))
            else:
                files.append(("experiment_id", (None, str(self.experiment_id).encode(), "text/plain")))

        if not isinstance(self.limit, Unset):
            files.append(("limit", (None, str(self.limit).encode(), "text/plain")))

        if not isinstance(self.starting_token, Unset):
            if isinstance(self.starting_token, int):
                files.append(("starting_token", (None, str(self.starting_token).encode(), "text/plain")))
            else:
                files.append(("starting_token", (None, str(self.starting_token).encode(), "text/plain")))

        if not isinstance(self.filters, Unset):
            if isinstance(self.filters, str):
                files.append(("filters", (None, str(self.filters).encode(), "text/plain")))
            else:
                files.append(("filters", (None, str(self.filters).encode(), "text/plain")))

        if not isinstance(self.sort, Unset):
            if isinstance(self.sort, str):
                files.append(("sort", (None, str(self.sort).encode(), "text/plain")))
            else:
                files.append(("sort", (None, str(self.sort).encode(), "text/plain")))

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

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        limit = d.pop("limit", UNSET)

        def _parse_starting_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        starting_token = _parse_starting_token(d.pop("starting_token", UNSET))

        def _parse_filters(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        filters = _parse_filters(d.pop("filters", UNSET))

        def _parse_sort(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        sort = _parse_sort(d.pop("sort", UNSET))

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

        body_validate_code_scorer_log_record_scorers_code_validate_log_record_post = cls(
            file=file,
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            limit=limit,
            starting_token=starting_token,
            filters=filters,
            sort=sort,
            required_scorers=required_scorers,
            scoreable_node_types=scoreable_node_types,
        )

        body_validate_code_scorer_log_record_scorers_code_validate_log_record_post.additional_properties = d
        return body_validate_code_scorer_log_record_scorers_code_validate_log_record_post

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
