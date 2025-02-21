from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.feedback_aggregate import FeedbackAggregate
    from ..models.run_metric_create_request_extra_type_1 import RunMetricCreateRequestExtraType1


T = TypeVar("T", bound="RunMetricCreateRequest")


@_attrs_define
class RunMetricCreateRequest:
    """
    Attributes:
        key (str):
        epoch (Union[Unset, int]):  Default: 0.
        extra (Union['RunMetricCreateRequestExtraType1', None, Unset, list[Any]]):
        object_value (Union['FeedbackAggregate', None, Unset]):
        value (Union[None, Unset, float]):
    """

    key: str
    epoch: Union[Unset, int] = 0
    extra: Union["RunMetricCreateRequestExtraType1", None, Unset, list[Any]] = UNSET
    object_value: Union["FeedbackAggregate", None, Unset] = UNSET
    value: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.run_metric_create_request_extra_type_1 import RunMetricCreateRequestExtraType1

        key = self.key

        epoch = self.epoch

        extra: Union[None, Unset, dict[str, Any], list[Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, list):
            extra = self.extra

        elif isinstance(self.extra, RunMetricCreateRequestExtraType1):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        object_value: Union[None, Unset, dict[str, Any]]
        if isinstance(self.object_value, Unset):
            object_value = UNSET
        elif isinstance(self.object_value, FeedbackAggregate):
            object_value = self.object_value.to_dict()
        else:
            object_value = self.object_value

        value: Union[None, Unset, float]
        if isinstance(self.value, Unset):
            value = UNSET
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"key": key})
        if epoch is not UNSET:
            field_dict["epoch"] = epoch
        if extra is not UNSET:
            field_dict["extra"] = extra
        if object_value is not UNSET:
            field_dict["object_value"] = object_value
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.feedback_aggregate import FeedbackAggregate
        from ..models.run_metric_create_request_extra_type_1 import RunMetricCreateRequestExtraType1

        d = src_dict.copy()
        key = d.pop("key")

        epoch = d.pop("epoch", UNSET)

        def _parse_extra(data: object) -> Union["RunMetricCreateRequestExtraType1", None, Unset, list[Any]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                extra_type_0 = cast(list[Any], data)

                return extra_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_1 = RunMetricCreateRequestExtraType1.from_dict(data)

                return extra_type_1
            except:  # noqa: E722
                pass
            return cast(Union["RunMetricCreateRequestExtraType1", None, Unset, list[Any]], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        def _parse_object_value(data: object) -> Union["FeedbackAggregate", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                object_value_type_0 = FeedbackAggregate.from_dict(data)

                return object_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FeedbackAggregate", None, Unset], data)

        object_value = _parse_object_value(d.pop("object_value", UNSET))

        def _parse_value(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        value = _parse_value(d.pop("value", UNSET))

        run_metric_create_request = cls(key=key, epoch=epoch, extra=extra, object_value=object_value, value=value)

        run_metric_create_request.additional_properties = d
        return run_metric_create_request

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
