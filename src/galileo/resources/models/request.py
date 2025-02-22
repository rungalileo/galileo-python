from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payload import Payload
    from ..models.request_headers_type_0 import RequestHeadersType0
    from ..models.request_metadata_type_0 import RequestMetadataType0
    from ..models.ruleset import Ruleset


T = TypeVar("T", bound="Request")


@_attrs_define
class Request:
    """
    Attributes:
        payload (Payload):
        headers (Union['RequestHeadersType0', None, Unset]): Optional additional HTTP headers that should be included in
            the response.
        metadata (Union['RequestMetadataType0', None, Unset]): Optional additional metadata. This will be echoed back in
            the response.
        prioritized_rulesets (Union[Unset, list['Ruleset']]): Rulesets to be applied to the payload.
        project_id (Union[None, Unset, str]): Project ID.
        project_name (Union[None, Unset, str]): Project name.
        stage_id (Union[None, Unset, str]): Stage ID.
        stage_name (Union[None, Unset, str]): Stage name.
        stage_version (Union[None, Unset, int]): Stage version to use for the request, if it's a central stage with a
            previously registered version.
        timeout (Union[Unset, float]): Optional timeout for the guardrail execution in seconds. This is not the timeout
            for the request. If not set, a default timeout of 5 minutes will be used. Default: 300.0.
    """

    payload: "Payload"
    headers: Union["RequestHeadersType0", None, Unset] = UNSET
    metadata: Union["RequestMetadataType0", None, Unset] = UNSET
    prioritized_rulesets: Union[Unset, list["Ruleset"]] = UNSET
    project_id: Union[None, Unset, str] = UNSET
    project_name: Union[None, Unset, str] = UNSET
    stage_id: Union[None, Unset, str] = UNSET
    stage_name: Union[None, Unset, str] = UNSET
    stage_version: Union[None, Unset, int] = UNSET
    timeout: Union[Unset, float] = 300.0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.request_headers_type_0 import RequestHeadersType0
        from ..models.request_metadata_type_0 import RequestMetadataType0

        payload = self.payload.to_dict()

        headers: Union[None, Unset, dict[str, Any]]
        if isinstance(self.headers, Unset):
            headers = UNSET
        elif isinstance(self.headers, RequestHeadersType0):
            headers = self.headers.to_dict()
        else:
            headers = self.headers

        metadata: Union[None, Unset, dict[str, Any]]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, RequestMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        prioritized_rulesets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.prioritized_rulesets, Unset):
            prioritized_rulesets = []
            for prioritized_rulesets_item_data in self.prioritized_rulesets:
                prioritized_rulesets_item = prioritized_rulesets_item_data.to_dict()
                prioritized_rulesets.append(prioritized_rulesets_item)

        project_id: Union[None, Unset, str]
        if isinstance(self.project_id, Unset):
            project_id = UNSET
        else:
            project_id = self.project_id

        project_name: Union[None, Unset, str]
        if isinstance(self.project_name, Unset):
            project_name = UNSET
        else:
            project_name = self.project_name

        stage_id: Union[None, Unset, str]
        if isinstance(self.stage_id, Unset):
            stage_id = UNSET
        else:
            stage_id = self.stage_id

        stage_name: Union[None, Unset, str]
        if isinstance(self.stage_name, Unset):
            stage_name = UNSET
        else:
            stage_name = self.stage_name

        stage_version: Union[None, Unset, int]
        if isinstance(self.stage_version, Unset):
            stage_version = UNSET
        else:
            stage_version = self.stage_version

        timeout = self.timeout

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"payload": payload})
        if headers is not UNSET:
            field_dict["headers"] = headers
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if prioritized_rulesets is not UNSET:
            field_dict["prioritized_rulesets"] = prioritized_rulesets
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if stage_id is not UNSET:
            field_dict["stage_id"] = stage_id
        if stage_name is not UNSET:
            field_dict["stage_name"] = stage_name
        if stage_version is not UNSET:
            field_dict["stage_version"] = stage_version
        if timeout is not UNSET:
            field_dict["timeout"] = timeout

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.payload import Payload
        from ..models.request_headers_type_0 import RequestHeadersType0
        from ..models.request_metadata_type_0 import RequestMetadataType0
        from ..models.ruleset import Ruleset

        d = src_dict.copy()
        payload = Payload.from_dict(d.pop("payload"))

        def _parse_headers(data: object) -> Union["RequestHeadersType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                headers_type_0 = RequestHeadersType0.from_dict(data)

                return headers_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RequestHeadersType0", None, Unset], data)

        headers = _parse_headers(d.pop("headers", UNSET))

        def _parse_metadata(data: object) -> Union["RequestMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = RequestMetadataType0.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["RequestMetadataType0", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        prioritized_rulesets = []
        _prioritized_rulesets = d.pop("prioritized_rulesets", UNSET)
        for prioritized_rulesets_item_data in _prioritized_rulesets or []:
            prioritized_rulesets_item = Ruleset.from_dict(prioritized_rulesets_item_data)

            prioritized_rulesets.append(prioritized_rulesets_item)

        def _parse_project_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_id = _parse_project_id(d.pop("project_id", UNSET))

        def _parse_project_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project_name = _parse_project_name(d.pop("project_name", UNSET))

        def _parse_stage_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stage_id = _parse_stage_id(d.pop("stage_id", UNSET))

        def _parse_stage_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        stage_name = _parse_stage_name(d.pop("stage_name", UNSET))

        def _parse_stage_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        stage_version = _parse_stage_version(d.pop("stage_version", UNSET))

        timeout = d.pop("timeout", UNSET)

        request = cls(
            payload=payload,
            headers=headers,
            metadata=metadata,
            prioritized_rulesets=prioritized_rulesets,
            project_id=project_id,
            project_name=project_name,
            stage_id=stage_id,
            stage_name=stage_name,
            stage_version=stage_version,
            timeout=timeout,
        )

        request.additional_properties = d
        return request

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
