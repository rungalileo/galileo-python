from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

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
        created_at_ns (Union[Unset, int]): Timestamp of the step's creation, as nanoseconds since epoch.
        duration_ns (Union[Unset, int]): Duration of the step in nanoseconds. Default: 0.
        ground_truth (Union[None, Unset, str]): Ground truth expected output for the step.
        metadata (Union[Unset, RetrieverStepMetadata]): Metadata associated with this step.
        name (Union[Unset, str]): Name of the step. Default: ''.
        output (Union[Unset, list['Document']]): Documents retrieved from the retriever. This can be a list of strings
            or `Document`s.
        status_code (Union[None, Unset, int]): Status code of the step. Used for logging failed/errored steps.
        type_ (Union[Literal['retriever'], Unset]): Type of the step. By default, it is set to retriever. Default:
            'retriever'.
    """

    input_: str
    created_at_ns: Union[Unset, int] = UNSET
    duration_ns: Union[Unset, int] = 0
    ground_truth: Union[None, Unset, str] = UNSET
    metadata: Union[Unset, "RetrieverStepMetadata"] = UNSET
    name: Union[Unset, str] = ""
    output: Union[Unset, list["Document"]] = UNSET
    status_code: Union[None, Unset, int] = UNSET
    type_: Union[Literal["retriever"], Unset] = "retriever"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        input_ = self.input_

        created_at_ns = self.created_at_ns

        duration_ns = self.duration_ns

        ground_truth: Union[None, Unset, str]
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name = self.name

        output: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.output, Unset):
            output = []
            for output_item_data in self.output:
                output_item = output_item_data.to_dict()
                output.append(output_item)

        status_code: Union[None, Unset, int]
        if isinstance(self.status_code, Unset):
            status_code = UNSET
        else:
            status_code = self.status_code

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_})
        if created_at_ns is not UNSET:
            field_dict["created_at_ns"] = created_at_ns
        if duration_ns is not UNSET:
            field_dict["duration_ns"] = duration_ns
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name
        if output is not UNSET:
            field_dict["output"] = output
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.document import Document
        from ..models.retriever_step_metadata import RetrieverStepMetadata

        d = src_dict.copy()
        input_ = d.pop("input")

        created_at_ns = d.pop("created_at_ns", UNSET)

        duration_ns = d.pop("duration_ns", UNSET)

        def _parse_ground_truth(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, RetrieverStepMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = RetrieverStepMetadata.from_dict(_metadata)

        name = d.pop("name", UNSET)

        output = []
        _output = d.pop("output", UNSET)
        for output_item_data in _output or []:
            output_item = Document.from_dict(output_item_data)

            output.append(output_item)

        def _parse_status_code(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        status_code = _parse_status_code(d.pop("status_code", UNSET))

        type_ = cast(Union[Literal["retriever"], Unset], d.pop("type", UNSET))
        if type_ != "retriever" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'retriever', got '{type_}'")

        retriever_step = cls(
            input_=input_,
            created_at_ns=created_at_ns,
            duration_ns=duration_ns,
            ground_truth=ground_truth,
            metadata=metadata,
            name=name,
            output=output,
            status_code=status_code,
            type_=type_,
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
