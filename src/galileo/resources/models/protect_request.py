from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payload import Payload
    from ..models.protect_request_headers_type_0 import ProtectRequestHeadersType0
    from ..models.protect_request_metadata_type_0 import ProtectRequestMetadataType0
    from ..models.ruleset import Ruleset


T = TypeVar("T", bound="ProtectRequest")


@_attrs_define
class ProtectRequest:
    """Protect request schema with custom OpenAPI title.

    Attributes
    ----------
        payload (Payload):
        prioritized_rulesets (Union[Unset, list['Ruleset']]): Rulesets to be applied to the payload.
        project_name (Union[None, Unset, str]): Project name.
        project_id (Union[None, Unset, str]): Project ID.
        stage_name (Union[None, Unset, str]): Stage name.
        stage_id (Union[None, Unset, str]): Stage ID.
        stage_version (Union[None, Unset, int]): Stage version to use for the request, if it's a central stage with a
            previously registered version.
        timeout (Union[Unset, float]): Optional timeout for the guardrail execution in seconds. This is not the timeout
            for the request. If not set, a default timeout of 5 minutes will be used. Default: 300.0.
        metadata (Union['ProtectRequestMetadataType0', None, Unset]): Optional additional metadata. This will be echoed
            back in the response.
        headers (Union['ProtectRequestHeadersType0', None, Unset]): Optional additional HTTP headers that should be
            included in the response.
    """

    payload: "Payload"
    prioritized_rulesets: Union[Unset, list["Ruleset"]] = UNSET
    project_name: Union[None, Unset, str] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    stage_name: Union[None, Unset, str] = UNSET
    stage_id: Union[None, Unset, str] = UNSET
    stage_version: Union[None, Unset, int] = UNSET
    timeout: Union[Unset, float] = 300.0
    metadata: Union["ProtectRequestMetadataType0", None, Unset] = UNSET
    headers: Union["ProtectRequestHeadersType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.protect_request_headers_type_0 import ProtectRequestHeadersType0
        from ..models.protect_request_metadata_type_0 import ProtectRequestMetadataType0

        payload = self.payload.to_dict()

        prioritized_rulesets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.prioritized_rulesets, Unset):
            prioritized_rulesets = []
            for prioritized_rulesets_item_data in self.prioritized_rulesets:
                prioritized_rulesets_item = prioritized_rulesets_item_data.to_dict()
                prioritized_rulesets.append(prioritized_rulesets_item)

        project_name: Union[None, Unset, str]
        project_name = UNSET if isinstance(self.project_name, Unset) else self.project_name

        project_id: Union[None, Unset, str]
        project_id = UNSET if isinstance(self.project_id, Unset) else self.project_id

        stage_name: Union[None, Unset, str]
        stage_name = UNSET if isinstance(self.stage_name, Unset) else self.stage_name

        stage_id: Union[None, Unset, str]
        stage_id = UNSET if isinstance(self.stage_id, Unset) else self.stage_id

        stage_version: Union[None, Unset, int]
        stage_version = UNSET if isinstance(self.stage_version, Unset) else self.stage_version

        timeout = self.timeout

        metadata: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ProtectRequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        headers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, ProtectRequestHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"payload": payload})
        if prioritized_rulesets is not UNSET:
            field_dict["prioritized_rulesets"] = prioritized_rulesets
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if stage_name is not UNSET:
            field_dict["stage_name"] = stage_name
        if stage_id is not UNSET:
            field_dict["stage_id"] = stage_id
        if stage_version is not UNSET:
            field_dict["stage_version"] = stage_version
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if headers is not UNSET:
            field_dict["headers"] = headers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payload import Payload
        from ..models.protect_request_headers_type_0 import ProtectRequestHeadersType0
        from ..models.protect_request_metadata_type_0 import ProtectRequestMetadataType0
        from ..models.ruleset import Ruleset

        d = dict(src_dict)
        payload = Payload.from_dict(d.pop("payload"))

        prioritized_rulesets = []
        _prioritized_rulesets = d.pop("prioritized_rulesets", UNSET)
        for prioritized_rulesets_item_data in _prioritized_rulesets or []:
            prioritized_rulesets_item = Ruleset.from_dict(prioritized_rulesets_item_data)

            prioritized_rulesets.append(prioritized_rulesets_item)

        def _parse_project_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_stage_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stage_name = _parse_stage_name(d.pop("stage_name", UNSET))

        def _parse_stage_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stage_id = _parse_stage_id(d.pop("stage_id", UNSET))

        def _parse_stage_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        stage_version = _parse_stage_version(d.pop("stage_version", UNSET))

        timeout = d.pop("timeout", UNSET)

        def _parse_metadata(data: object) -> Union["ProtectRequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProtectRequestMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ProtectRequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_headers(data: object) -> Union["ProtectRequestHeadersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ProtectRequestHeadersType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["ProtectRequestHeadersType0", None, Unset], data)

        headers = _parse_headers(d.pop("headers", UNSET))

        protect_request = cls(
            payload=payload,
            prioritized_rulesets=prioritized_rulesets,
            project_name=project_name,
            project_id=project_id,
            stage_name=stage_name,
            stage_id=stage_id,
            stage_version=stage_version,
            timeout=timeout,
            metadata=metadata,
            headers=headers,
        )

        protect_request.additional_properties = d
        return protect_request

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
