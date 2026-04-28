from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_severity import ErrorSeverity
from ..models.error_type import ErrorType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.standard_error_context import StandardErrorContext


T = TypeVar("T", bound="StandardError")


@_attrs_define
class StandardError:
    """
    Attributes
    ----------
        error_code (int):
        error_type (ErrorType):
        error_group (str):
        severity (ErrorSeverity): Error severity levels for catalog entries.
        message (str):
        user_action (None | str | Unset):
        documentation_link (None | str | Unset):
        retriable (bool | Unset):  Default: False.
        blocking (bool | Unset):  Default: False.
        http_status_code (int | None | Unset):
        source_service (None | str | Unset):
        context (StandardErrorContext | Unset):
    """

    error_code: int
    error_type: ErrorType
    error_group: str
    severity: ErrorSeverity
    message: str
    user_action: None | str | Unset = UNSET
    documentation_link: None | str | Unset = UNSET
    retriable: bool | Unset = False
    blocking: bool | Unset = False
    http_status_code: int | None | Unset = UNSET
    source_service: None | str | Unset = UNSET
    context: StandardErrorContext | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_code = self.error_code

        error_type = self.error_type.value

        error_group = self.error_group

        severity = self.severity.value

        message = self.message

        user_action: None | str | Unset
        user_action = UNSET if isinstance(self.user_action, Unset) else self.user_action

        documentation_link: None | str | Unset
        documentation_link = UNSET if isinstance(self.documentation_link, Unset) else self.documentation_link

        retriable = self.retriable

        blocking = self.blocking

        http_status_code: int | None | Unset
        http_status_code = UNSET if isinstance(self.http_status_code, Unset) else self.http_status_code

        source_service: None | str | Unset
        source_service = UNSET if isinstance(self.source_service, Unset) else self.source_service

        context: dict[str, Any] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "error_code": error_code,
                "error_type": error_type,
                "error_group": error_group,
                "severity": severity,
                "message": message,
            }
        )
        if user_action is not UNSET:
            field_dict["user_action"] = user_action
        if documentation_link is not UNSET:
            field_dict["documentation_link"] = documentation_link
        if retriable is not UNSET:
            field_dict["retriable"] = retriable
        if blocking is not UNSET:
            field_dict["blocking"] = blocking
        if http_status_code is not UNSET:
            field_dict["http_status_code"] = http_status_code
        if source_service is not UNSET:
            field_dict["source_service"] = source_service
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.standard_error_context import StandardErrorContext

        d = dict(src_dict)
        error_code = d.pop("error_code")

        error_type = ErrorType(d.pop("error_type"))

        error_group = d.pop("error_group")

        severity = ErrorSeverity(d.pop("severity"))

        message = d.pop("message")

        def _parse_user_action(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_action = _parse_user_action(d.pop("user_action", UNSET))

        def _parse_documentation_link(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        documentation_link = _parse_documentation_link(d.pop("documentation_link", UNSET))

        retriable = d.pop("retriable", UNSET)

        blocking = d.pop("blocking", UNSET)

        def _parse_http_status_code(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        http_status_code = _parse_http_status_code(d.pop("http_status_code", UNSET))

        def _parse_source_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        source_service = _parse_source_service(d.pop("source_service", UNSET))

        _context = d.pop("context", UNSET)
        context: StandardErrorContext | Unset
        context = UNSET if isinstance(_context, Unset) else StandardErrorContext.from_dict(_context)

        standard_error = cls(
            error_code=error_code,
            error_type=error_type,
            error_group=error_group,
            severity=severity,
            message=message,
            user_action=user_action,
            documentation_link=documentation_link,
            retriable=retriable,
            blocking=blocking,
            http_status_code=http_status_code,
            source_service=source_service,
            context=context,
        )

        standard_error.additional_properties = d
        return standard_error

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
