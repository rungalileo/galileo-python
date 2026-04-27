from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.document import Document
    from ..models.retriever_step_metadata import RetrieverStepMetadata


T = TypeVar("T", bound="RetrieverStep")


@_attrs_define
class RetrieverStep:
    """
    Attributes:
        input_ (str): Input query to the retriever.
        type_ (Literal['retriever'] | Unset): Type of the step. By default, it is set to retriever. Default:
            'retriever'.
        redacted_input (None | str | Unset): Redacted input of the retriever step. This is used to redact sensitive
            information.
        output (list[Document] | Unset): Documents retrieved from the retriever. This can be a list of strings or
            `Document`s.
        redacted_output (list[Document] | None | Unset): Redacted output of the retriever step. This is used to redact
            sensitive information.
        name (str | Unset): Name of the step. Default: ''.
        created_at_ns (int | Unset): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (int | Unset): Duration of the step in nanoseconds. Default: 0.
        metadata (RetrieverStepMetadata | Unset): Metadata associated with this step.
        status_code (int | None | Unset): Status code of the step. Used for logging failed/errored steps.
        ground_truth (None | str | Unset): Ground truth expected output for the step.
    """

    input_: str
    type_: Literal["retriever"] | Unset = "retriever"
    redacted_input: None | str | Unset = UNSET
    output: list[Document] | Unset = UNSET
    redacted_output: list[Document] | None | Unset = UNSET
    name: str | Unset = ""
    created_at_ns: int | Unset = UNSET
    duration_ns: int | Unset = 0
    metadata: RetrieverStepMetadata | Unset = UNSET
    status_code: int | None | Unset = UNSET
    ground_truth: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        type_ = self.type_

        redacted_input: None | str | Unset
        if isinstance(self.redacted_input, Unset):
            redacted_input = UNSET
        else:
            redacted_input = self.redacted_input

        output: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.output, Unset):
            output = []
            for output_item_data in self.output:
                output_item = output_item_data.to_dict()
                output.append(output_item)

        redacted_output: list[dict[str, Any]] | None | Unset
        if isinstance(self.redacted_output, Unset):
            redacted_output = UNSET
        elif isinstance(self.redacted_output, list):
            redacted_output = []
            for redacted_output_type_0_item_data in self.redacted_output:
                redacted_output_type_0_item = redacted_output_type_0_item_data.to_dict()
                redacted_output.append(redacted_output_type_0_item)

        else:
            redacted_output = self.redacted_output

        name = self.name

        created_at_ns = self.created_at_ns

        duration_ns = self.duration_ns

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        status_code: int | None | Unset
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        ground_truth: None | str | Unset
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if redacted_input is not UNSET:
            field_dict["redacted_input"] = redacted_input
        if output is not UNSET:
            field_dict["output"] = output
        if redacted_output is not UNSET:
            field_dict["redacted_output"] = redacted_output
        if name is not UNSET:
            field_dict["name"] = name
        if created_at_ns is not UNSET:
            field_dict["created_at_ns"] = created_at_ns
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.document import Document
        from ..models.retriever_step_metadata import RetrieverStepMetadata

        d = dict(src_dict)
        input_ = d.pop("input")

        type_ = cast(Literal["retriever"] | Unset, d.pop("type", UNSET))
        if type_ != "retriever" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'retriever', got '{type_}'")

        def _parse_redacted_input(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        redacted_input = _parse_redacted_input(d.pop("redacted_input", UNSET))

        _output = d.pop("output", UNSET)
        output: list[Document] | Unset = UNSET
        if _output is not UNSET:
            output = []
            for output_item_data in _output:
                output_item = Document.from_dict(output_item_data)

                output.append(output_item)

        def _parse_redacted_output(data: object) -> list[Document] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                redacted_output_type_0 = []
                _redacted_output_type_0 = data
                for redacted_output_type_0_item_data in _redacted_output_type_0:
                    redacted_output_type_0_item = Document.from_dict(redacted_output_type_0_item_data)

                    redacted_output_type_0.append(redacted_output_type_0_item)

                return redacted_output_type_0
            except:  # noqa: E722
                pass
            return cast(list[Document] | None | Unset, data)

        redacted_output = _parse_redacted_output(d.pop("redacted_output", UNSET))

        name = d.pop("name", UNSET)

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: RetrieverStepMetadata | Unset
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = RetrieverStepMetadata.from_dict(_metadata)

        def _parse_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        def _parse_ground_truth(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        retriever_step = cls(
            input_=input_,
            type_=type_,
            redacted_input=redacted_input,
            output=output,
            redacted_output=redacted_output,
            name=name,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            metadata=metadata,
            status_code=status_code,
            ground_truth=ground_truth,
        )

        retriever_step.additional_properties = d
        return retriever_step

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
