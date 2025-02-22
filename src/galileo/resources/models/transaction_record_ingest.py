import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.node_type import NodeType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transaction_record_ingest_output_logprobs_type_0 import TransactionRecordIngestOutputLogprobsType0
    from ..models.transaction_record_ingest_user_metadata_type_0 import TransactionRecordIngestUserMetadataType0


T = TypeVar("T", bound="TransactionRecordIngest")


@_attrs_define
class TransactionRecordIngest:
    """
    Attributes:
        created_at (datetime.datetime):
        input_text (str):
        node_id (str):
        node_type (NodeType):
        chain_id (Union[None, UUID, Unset]):
        chain_root_id (Union[None, Unset, str]):
        finish_reason (Union[None, Unset, str]):
        has_children (Union[None, Unset, bool]):
        latency_ms (Union[None, Unset, int]):
        model (Union[None, Unset, str]):
        node_name (Union[None, Unset, str]):
        num_input_tokens (Union[None, Unset, int]):
        num_output_tokens (Union[None, Unset, int]):
        num_total_tokens (Union[None, Unset, int]):
        output_logprobs (Union['TransactionRecordIngestOutputLogprobsType0', None, Unset]):
        output_text (Union[None, Unset, str]):
        status_code (Union[None, Unset, int]):
        tags (Union[None, Unset, list[str]]):
        temperature (Union[None, Unset, float]):
        time_to_first_token_ms (Union[None, Unset, float]):
        tools (Union[None, Unset, str]):
        user_metadata (Union['TransactionRecordIngestUserMetadataType0', None, Unset]):
        version (Union[None, Unset, str]):
    """

    created_at: datetime.datetime
    input_text: str
    node_id: str
    node_type: NodeType
    chain_id: Union[None, UUID, Unset] = UNSET
    chain_root_id: Union[None, Unset, str] = UNSET
    finish_reason: Union[None, Unset, str] = UNSET
    has_children: Union[None, Unset, bool] = UNSET
    latency_ms: Union[None, Unset, int] = UNSET
    model: Union[None, Unset, str] = UNSET
    node_name: Union[None, Unset, str] = UNSET
    num_input_tokens: Union[None, Unset, int] = UNSET
    num_output_tokens: Union[None, Unset, int] = UNSET
    num_total_tokens: Union[None, Unset, int] = UNSET
    output_logprobs: Union["TransactionRecordIngestOutputLogprobsType0", None, Unset] = UNSET
    output_text: Union[None, Unset, str] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    tags: Union[None, Unset, list[str]] = UNSET
    temperature: Union[None, Unset, float] = UNSET
    time_to_first_token_ms: Union[None, Unset, float] = UNSET
    tools: Union[None, Unset, str] = UNSET
    user_metadata: Union["TransactionRecordIngestUserMetadataType0", None, Unset] = UNSET
    version: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.transaction_record_ingest_output_logprobs_type_0 import TransactionRecordIngestOutputLogprobsType0
        from ..models.transaction_record_ingest_user_metadata_type_0 import TransactionRecordIngestUserMetadataType0

        created_at = self.created_at.isoformat()

        input_text = self.input_text

        node_id = self.node_id

        node_type = self.node_type.value

        chain_id: Union[None, Unset, str]
        if isinstance(self.chain_id, Unset):
            chain_id = UNSET
        elif isinstance(self.chain_id, UUID):
            chain_id = str(self.chain_id)
        else:
            chain_id = self.chain_id

        chain_root_id: Union[None, Unset, str]
        if isinstance(self.chain_root_id, Unset):
            chain_root_id = UNSET
        else:
            chain_root_id = self.chain_root_id

        finish_reason: Union[None, Unset, str]
        if isinstance(self.finish_reason, Unset):
            finish_reason = UNSET
        else:
            finish_reason = self.finish_reason

        has_children: Union[None, Unset, bool]
        if isinstance(self.has_children, Unset):
            has_children = UNSET
        else:
            has_children = self.has_children

        latency_ms: Union[None, Unset, int]
        if isinstance(self.latency_ms, Unset):
            latency_ms = UNSET
        else:
            latency_ms = self.latency_ms

        model: Union[None, Unset, str]
        if isinstance(self.model, Unset):
            model = UNSET
        else:
            model = self.model

        node_name: Union[None, Unset, str]
        if isinstance(self.node_name, Unset):
            node_name = UNSET
        else:
            node_name = self.node_name

        num_input_tokens: Union[None, Unset, int]
        if isinstance(self.num_input_tokens, Unset):
            num_input_tokens = UNSET
        else:
            num_input_tokens = self.num_input_tokens

        num_output_tokens: Union[None, Unset, int]
        if isinstance(self.num_output_tokens, Unset):
            num_output_tokens = UNSET
        else:
            num_output_tokens = self.num_output_tokens

        num_total_tokens: Union[None, Unset, int]
        if isinstance(self.num_total_tokens, Unset):
            num_total_tokens = UNSET
        else:
            num_total_tokens = self.num_total_tokens

        output_logprobs: Union[None, Unset, dict[str, Any]]
        if isinstance(self.output_logprobs, Unset):
            output_logprobs = UNSET
        elif isinstance(self.output_logprobs, TransactionRecordIngestOutputLogprobsType0):
            output_logprobs = self.output_logprobs.to_dict()
        else:
            output_logprobs = self.output_logprobs

        output_text: Union[None, Unset, str]
        if isinstance(self.output_text, Unset):
            output_text = UNSET
        else:
            output_text = self.output_text

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        tags: Union[None, Unset, list[str]]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        temperature: Union[None, Unset, float]
        if isinstance(self.temperature, Unset):
            temperature = UNSET
        else:
            temperature = self.temperature

        time_to_first_token_ms: Union[None, Unset, float]
        if isinstance(self.time_to_first_token_ms, Unset):
            time_to_first_token_ms = UNSET
        else:
            time_to_first_token_ms = self.time_to_first_token_ms

        tools: Union[None, Unset, str]
        if isinstance(self.tools, Unset):
            tools = UNSET
        else:
            tools = self.tools

        user_metadata: Union[None, Unset, dict[str, Any]]
        if isinstance(self.user_metadata, Unset):
            user_metadata = UNSET
        elif isinstance(self.user_metadata, TransactionRecordIngestUserMetadataType0):
            user_metadata = self.user_metadata.to_dict()
        else:
            user_metadata = self.user_metadata

        version: Union[None, Unset, str]
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"created_at": created_at, "input_text": input_text, "node_id": node_id, "node_type": node_type}
        )
        if chain_id is not UNSET:
            field_dict["chain_id"] = chain_id
        if chain_root_id is not UNSET:
            field_dict["chain_root_id"] = chain_root_id
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason
        if has_children is not UNSET:
            field_dict["has_children"] = has_children
        if latency_ms is not UNSET:
            field_dict["latency_ms"] = latency_ms
        if model is not UNSET:
            field_dict["model"] = model
        if node_name is not UNSET:
            field_dict["node_name"] = node_name
        if num_input_tokens is not UNSET:
            field_dict["num_input_tokens"] = num_input_tokens
        if num_output_tokens is not UNSET:
            field_dict["num_output_tokens"] = num_output_tokens
        if num_total_tokens is not UNSET:
            field_dict["num_total_tokens"] = num_total_tokens
        if output_logprobs is not UNSET:
            field_dict["output_logprobs"] = output_logprobs
        if output_text is not UNSET:
            field_dict["output_text"] = output_text
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if temperature is not UNSET:
            field_dict["temperature"] = temperature
        if time_to_first_token_ms is not UNSET:
            field_dict["time_to_first_token_ms"] = time_to_first_token_ms
        if tools is not UNSET:
            field_dict["tools"] = tools
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.transaction_record_ingest_output_logprobs_type_0 import TransactionRecordIngestOutputLogprobsType0
        from ..models.transaction_record_ingest_user_metadata_type_0 import TransactionRecordIngestUserMetadataType0

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        input_text = d.pop("input_text")

        node_id = d.pop("node_id")

        node_type = NodeType(d.pop("node_type"))

        def _parse_chain_id(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                chain_id_type_0 = UUID(data)

                return chain_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        chain_id = _parse_chain_id(d.pop("chain_id", UNSET))

        def _parse_chain_root_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        chain_root_id = _parse_chain_root_id(d.pop("chain_root_id", UNSET))

        def _parse_finish_reason(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        finish_reason = _parse_finish_reason(d.pop("finish_reason", UNSET))

        def _parse_has_children(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        has_children = _parse_has_children(d.pop("has_children", UNSET))

        def _parse_latency_ms(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        latency_ms = _parse_latency_ms(d.pop("latency_ms", UNSET))

        def _parse_model(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model = _parse_model(d.pop("model", UNSET))

        def _parse_node_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        node_name = _parse_node_name(d.pop("node_name", UNSET))

        def _parse_num_input_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_input_tokens = _parse_num_input_tokens(d.pop("num_input_tokens", UNSET))

        def _parse_num_output_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_output_tokens = _parse_num_output_tokens(d.pop("num_output_tokens", UNSET))

        def _parse_num_total_tokens(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_total_tokens = _parse_num_total_tokens(d.pop("num_total_tokens", UNSET))

        def _parse_output_logprobs(data: object) -> Union["TransactionRecordIngestOutputLogprobsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_logprobs_type_0 = TransactionRecordIngestOutputLogprobsType0.from_dict(data)

                return output_logprobs_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TransactionRecordIngestOutputLogprobsType0", None, Unset], data)

        output_logprobs = _parse_output_logprobs(d.pop("output_logprobs", UNSET))

        def _parse_output_text(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        output_text = _parse_output_text(d.pop("output_text", UNSET))

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_tags(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_temperature(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        temperature = _parse_temperature(d.pop("temperature", UNSET))

        def _parse_time_to_first_token_ms(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        time_to_first_token_ms = _parse_time_to_first_token_ms(d.pop("time_to_first_token_ms", UNSET))

        def _parse_tools(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        tools = _parse_tools(d.pop("tools", UNSET))

        def _parse_user_metadata(data: object) -> Union["TransactionRecordIngestUserMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_metadata_type_0 = TransactionRecordIngestUserMetadataType0.from_dict(data)

                return user_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["TransactionRecordIngestUserMetadataType0", None, Unset], data)

        user_metadata = _parse_user_metadata(d.pop("user_metadata", UNSET))

        def _parse_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        version = _parse_version(d.pop("version", UNSET))

        transaction_record_ingest = cls(
            created_at=created_at,
            input_text=input_text,
            node_id=node_id,
            node_type=node_type,
            chain_id=chain_id,
            chain_root_id=chain_root_id,
            finish_reason=finish_reason,
            has_children=has_children,
            latency_ms=latency_ms,
            model=model,
            node_name=node_name,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            num_total_tokens=num_total_tokens,
            output_logprobs=output_logprobs,
            output_text=output_text,
            status_code=status_code,
            tags=tags,
            temperature=temperature,
            time_to_first_token_ms=time_to_first_token_ms,
            tools=tools,
            user_metadata=user_metadata,
            version=version,
        )

        transaction_record_ingest.additional_properties = d
        return transaction_record_ingest

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
