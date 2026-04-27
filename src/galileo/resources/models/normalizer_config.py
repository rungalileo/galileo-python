from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.normalizer_config_collapse_previous_messages_across import NormalizerConfigCollapsePreviousMessagesAcross
from ..models.normalizer_config_collapse_previous_messages_level import NormalizerConfigCollapsePreviousMessagesLevel
from ..models.normalizer_config_collapse_tools_across import NormalizerConfigCollapseToolsAcross
from ..models.normalizer_config_collapse_tools_level import NormalizerConfigCollapseToolsLevel
from ..models.root_type import RootType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.normalizer_config_span_key_renames import NormalizerConfigSpanKeyRenames


T = TypeVar("T", bound="NormalizerConfig")


@_attrs_define
class NormalizerConfig:
    """Configuration for the normalization process.

    Attributes:
        accumulation_level (RootType): The root-level type of a logged step hierarchy.

            Maps fine-grained StepType values to the three top-level categories
            used throughout the platform: session, trace, and span.
        collapse_tools_level (NormalizerConfigCollapseToolsLevel):
        collapse_previous_messages_level (NormalizerConfigCollapsePreviousMessagesLevel):
        include_session_input_output (bool | Unset):  Default: False.
        include_trace_inputs_and_outputs (bool | Unset):  Default: False.
        include_dataset_output (bool | Unset):  Default: False.
        include_spans (bool | Unset):  Default: True.
        trace_included_fields (list[str] | None | Unset):
        span_key_renames (NormalizerConfigSpanKeyRenames | Unset):
        span_key_order (list[str] | Unset):
        span_key_only_include (list[str] | Unset):
        condense_chat_messages (bool | Unset):  Default: True.
        collapse_tools (bool | Unset):  Default: True.
        collapse_tools_across (None | NormalizerConfigCollapseToolsAcross | Unset):
        collapse_previous_messages (bool | Unset):  Default: True.
        collapse_previous_messages_across (None | NormalizerConfigCollapsePreviousMessagesAcross | Unset):
        include_num_documents_for_retriever_span (bool | Unset):  Default: True.
    """

    accumulation_level: RootType
    collapse_tools_level: NormalizerConfigCollapseToolsLevel
    collapse_previous_messages_level: NormalizerConfigCollapsePreviousMessagesLevel
    include_session_input_output: bool | Unset = False
    include_trace_inputs_and_outputs: bool | Unset = False
    include_dataset_output: bool | Unset = False
    include_spans: bool | Unset = True
    trace_included_fields: list[str] | None | Unset = UNSET
    span_key_renames: NormalizerConfigSpanKeyRenames | Unset = UNSET
    span_key_order: list[str] | Unset = UNSET
    span_key_only_include: list[str] | Unset = UNSET
    condense_chat_messages: bool | Unset = True
    collapse_tools: bool | Unset = True
    collapse_tools_across: None | NormalizerConfigCollapseToolsAcross | Unset = UNSET
    collapse_previous_messages: bool | Unset = True
    collapse_previous_messages_across: None | NormalizerConfigCollapsePreviousMessagesAcross | Unset = UNSET
    include_num_documents_for_retriever_span: bool | Unset = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        accumulation_level = self.accumulation_level.value

        collapse_tools_level = self.collapse_tools_level.value

        collapse_previous_messages_level = self.collapse_previous_messages_level.value

        include_session_input_output = self.include_session_input_output

        include_trace_inputs_and_outputs = self.include_trace_inputs_and_outputs

        include_dataset_output = self.include_dataset_output

        include_spans = self.include_spans

        trace_included_fields: list[str] | None | Unset
        if isinstance(self.trace_included_fields, Unset):
            trace_included_fields = UNSET
        elif isinstance(self.trace_included_fields, list):
            trace_included_fields = self.trace_included_fields

        else:
            trace_included_fields = self.trace_included_fields

        span_key_renames: dict[str, Any] | Unset = UNSET
        if not isinstance(self.span_key_renames, Unset):
            span_key_renames = self.span_key_renames.to_dict()

        span_key_order: list[str] | Unset = UNSET
        if not isinstance(self.span_key_order, Unset):
            span_key_order = self.span_key_order

        span_key_only_include: list[str] | Unset = UNSET
        if not isinstance(self.span_key_only_include, Unset):
            span_key_only_include = self.span_key_only_include

        condense_chat_messages = self.condense_chat_messages

        collapse_tools = self.collapse_tools

        collapse_tools_across: None | str | Unset
        if isinstance(self.collapse_tools_across, Unset):
            collapse_tools_across = UNSET
        elif isinstance(self.collapse_tools_across, NormalizerConfigCollapseToolsAcross):
            collapse_tools_across = self.collapse_tools_across.value
        else:
            collapse_tools_across = self.collapse_tools_across

        collapse_previous_messages = self.collapse_previous_messages

        collapse_previous_messages_across: None | str | Unset
        if isinstance(self.collapse_previous_messages_across, Unset):
            collapse_previous_messages_across = UNSET
        elif isinstance(self.collapse_previous_messages_across, NormalizerConfigCollapsePreviousMessagesAcross):
            collapse_previous_messages_across = self.collapse_previous_messages_across.value
        else:
            collapse_previous_messages_across = self.collapse_previous_messages_across

        include_num_documents_for_retriever_span = self.include_num_documents_for_retriever_span

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accumulation_level": accumulation_level,
                "collapse_tools_level": collapse_tools_level,
                "collapse_previous_messages_level": collapse_previous_messages_level,
            }
        )
        if include_session_input_output is not UNSET:
            field_dict["include_session_input_output"] = include_session_input_output
        if include_trace_inputs_and_outputs is not UNSET:
            field_dict["include_trace_inputs_and_outputs"] = include_trace_inputs_and_outputs
        if include_dataset_output is not UNSET:
            field_dict["include_dataset_output"] = include_dataset_output
        if include_spans is not UNSET:
            field_dict["include_spans"] = include_spans
        if trace_included_fields is not UNSET:
            field_dict["trace_included_fields"] = trace_included_fields
        if span_key_renames is not UNSET:
            field_dict["span_key_renames"] = span_key_renames
        if span_key_order is not UNSET:
            field_dict["span_key_order"] = span_key_order
        if span_key_only_include is not UNSET:
            field_dict["span_key_only_include"] = span_key_only_include
        if condense_chat_messages is not UNSET:
            field_dict["condense_chat_messages"] = condense_chat_messages
        if collapse_tools is not UNSET:
            field_dict["collapse_tools"] = collapse_tools
        if collapse_tools_across is not UNSET:
            field_dict["collapse_tools_across"] = collapse_tools_across
        if collapse_previous_messages is not UNSET:
            field_dict["collapse_previous_messages"] = collapse_previous_messages
        if collapse_previous_messages_across is not UNSET:
            field_dict["collapse_previous_messages_across"] = collapse_previous_messages_across
        if include_num_documents_for_retriever_span is not UNSET:
            field_dict["include_num_documents_for_retriever_span"] = include_num_documents_for_retriever_span

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.normalizer_config_span_key_renames import NormalizerConfigSpanKeyRenames

        d = dict(src_dict)
        accumulation_level = RootType(d.pop("accumulation_level"))

        collapse_tools_level = NormalizerConfigCollapseToolsLevel(d.pop("collapse_tools_level"))

        collapse_previous_messages_level = NormalizerConfigCollapsePreviousMessagesLevel(
            d.pop("collapse_previous_messages_level")
        )

        include_session_input_output = d.pop("include_session_input_output", UNSET)

        include_trace_inputs_and_outputs = d.pop("include_trace_inputs_and_outputs", UNSET)

        include_dataset_output = d.pop("include_dataset_output", UNSET)

        include_spans = d.pop("include_spans", UNSET)

        def _parse_trace_included_fields(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                trace_included_fields_type_0 = cast(list[str], data)

                return trace_included_fields_type_0
            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        trace_included_fields = _parse_trace_included_fields(d.pop("trace_included_fields", UNSET))

        _span_key_renames = d.pop("span_key_renames", UNSET)
        span_key_renames: NormalizerConfigSpanKeyRenames | Unset
        if isinstance(_span_key_renames, Unset):
            span_key_renames = UNSET
        else:
            span_key_renames = NormalizerConfigSpanKeyRenames.from_dict(_span_key_renames)

        span_key_order = cast(list[str], d.pop("span_key_order", UNSET))

        span_key_only_include = cast(list[str], d.pop("span_key_only_include", UNSET))

        condense_chat_messages = d.pop("condense_chat_messages", UNSET)

        collapse_tools = d.pop("collapse_tools", UNSET)

        def _parse_collapse_tools_across(data: object) -> None | NormalizerConfigCollapseToolsAcross | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                collapse_tools_across_type_1 = NormalizerConfigCollapseToolsAcross(data)

                return collapse_tools_across_type_1
            except:  # noqa: E722
                pass
            return cast(None | NormalizerConfigCollapseToolsAcross | Unset, data)

        collapse_tools_across = _parse_collapse_tools_across(d.pop("collapse_tools_across", UNSET))

        collapse_previous_messages = d.pop("collapse_previous_messages", UNSET)

        def _parse_collapse_previous_messages_across(
            data: object,
        ) -> None | NormalizerConfigCollapsePreviousMessagesAcross | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                collapse_previous_messages_across_type_1 = NormalizerConfigCollapsePreviousMessagesAcross(data)

                return collapse_previous_messages_across_type_1
            except:  # noqa: E722
                pass
            return cast(None | NormalizerConfigCollapsePreviousMessagesAcross | Unset, data)

        collapse_previous_messages_across = _parse_collapse_previous_messages_across(
            d.pop("collapse_previous_messages_across", UNSET)
        )

        include_num_documents_for_retriever_span = d.pop("include_num_documents_for_retriever_span", UNSET)

        normalizer_config = cls(
            accumulation_level=accumulation_level,
            collapse_tools_level=collapse_tools_level,
            collapse_previous_messages_level=collapse_previous_messages_level,
            include_session_input_output=include_session_input_output,
            include_trace_inputs_and_outputs=include_trace_inputs_and_outputs,
            include_dataset_output=include_dataset_output,
            include_spans=include_spans,
            trace_included_fields=trace_included_fields,
            span_key_renames=span_key_renames,
            span_key_order=span_key_order,
            span_key_only_include=span_key_only_include,
            condense_chat_messages=condense_chat_messages,
            collapse_tools=collapse_tools,
            collapse_tools_across=collapse_tools_across,
            collapse_previous_messages=collapse_previous_messages,
            collapse_previous_messages_across=collapse_previous_messages_across,
            include_num_documents_for_retriever_span=include_num_documents_for_retriever_span,
        )

        normalizer_config.additional_properties = d
        return normalizer_config

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
