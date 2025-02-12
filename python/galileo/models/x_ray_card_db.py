from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.alert_importance import AlertImportance
from ..models.x_ray_class import XRayClass
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extra_alert_filters import ExtraAlertFilters
    from ..models.filter_params import FilterParams
    from ..models.x_ray_card_db_message_fields import XRayCardDBMessageFields


T = TypeVar("T", bound="XRayCardDB")


@_attrs_define
class XRayCardDB:
    """
    Attributes:
        alert_id (int):
        dismissed (bool):
        id (str):
        message_fields (XRayCardDBMessageFields):
        xray_class (XRayClass):
        extra_filters (Union['ExtraAlertFilters', None, Unset]):
        importance (Union[AlertImportance, None, Unset]):
        logic (Union['FilterParams', None, Unset]):
        message (Union[Unset, str]):  Default: ''.
        pct_samples (Union[None, Unset, float]):
        score (Union[None, Unset, float]):
        suggestion (Union[None, Unset, str]):
        xray_classname (Union[Unset, str]):  Default: ''.
    """

    alert_id: int
    dismissed: bool
    id: str
    message_fields: "XRayCardDBMessageFields"
    xray_class: XRayClass
    extra_filters: Union["ExtraAlertFilters", None, Unset] = UNSET
    importance: Union[AlertImportance, None, Unset] = UNSET
    logic: Union["FilterParams", None, Unset] = UNSET
    message: Union[Unset, str] = ""
    pct_samples: Union[None, Unset, float] = UNSET
    score: Union[None, Unset, float] = UNSET
    suggestion: Union[None, Unset, str] = UNSET
    xray_classname: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.extra_alert_filters import ExtraAlertFilters
        from ..models.filter_params import FilterParams

        alert_id = self.alert_id

        dismissed = self.dismissed

        id = self.id

        message_fields = self.message_fields.to_dict()

        xray_class = self.xray_class.value

        extra_filters: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra_filters, Unset):
            extra_filters = UNSET
        elif isinstance(self.extra_filters, ExtraAlertFilters):
            extra_filters = self.extra_filters.to_dict()
        else:
            extra_filters = self.extra_filters

        importance: Union[None, Unset, str]
        if isinstance(self.importance, Unset):
            importance = UNSET
        elif isinstance(self.importance, AlertImportance):
            importance = self.importance.value
        else:
            importance = self.importance

        logic: Union[None, Unset, dict[str, Any]]
        if isinstance(self.logic, Unset):
            logic = UNSET
        elif isinstance(self.logic, FilterParams):
            logic = self.logic.to_dict()
        else:
            logic = self.logic

        message = self.message

        pct_samples: Union[None, Unset, float]
        if isinstance(self.pct_samples, Unset):
            pct_samples = UNSET
        else:
            pct_samples = self.pct_samples

        score: Union[None, Unset, float]
        if isinstance(self.score, Unset):
            score = UNSET
        else:
            score = self.score

        suggestion: Union[None, Unset, str]
        if isinstance(self.suggestion, Unset):
            suggestion = UNSET
        else:
            suggestion = self.suggestion

        xray_classname = self.xray_classname

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alert_id": alert_id,
                "dismissed": dismissed,
                "id": id,
                "message_fields": message_fields,
                "xray_class": xray_class,
            }
        )
        if extra_filters is not UNSET:
            field_dict["extra_filters"] = extra_filters
        if importance is not UNSET:
            field_dict["importance"] = importance
        if logic is not UNSET:
            field_dict["logic"] = logic
        if message is not UNSET:
            field_dict["message"] = message
        if pct_samples is not UNSET:
            field_dict["pct_samples"] = pct_samples
        if score is not UNSET:
            field_dict["score"] = score
        if suggestion is not UNSET:
            field_dict["suggestion"] = suggestion
        if xray_classname is not UNSET:
            field_dict["xray_classname"] = xray_classname

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.extra_alert_filters import ExtraAlertFilters
        from ..models.filter_params import FilterParams
        from ..models.x_ray_card_db_message_fields import XRayCardDBMessageFields

        d = src_dict.copy()
        alert_id = d.pop("alert_id")

        dismissed = d.pop("dismissed")

        id = d.pop("id")

        message_fields = XRayCardDBMessageFields.from_dict(d.pop("message_fields"))

        xray_class = XRayClass(d.pop("xray_class"))

        def _parse_extra_filters(data: object) -> Union["ExtraAlertFilters", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_filters_type_0 = ExtraAlertFilters.from_dict(data)

                return extra_filters_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ExtraAlertFilters", None, Unset], data)

        extra_filters = _parse_extra_filters(d.pop("extra_filters", UNSET))

        def _parse_importance(data: object) -> Union[AlertImportance, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                importance_type_0 = AlertImportance(data)

                return importance_type_0
            except:  # noqa: E722
                pass
            return cast(Union[AlertImportance, None, Unset], data)

        importance = _parse_importance(d.pop("importance", UNSET))

        def _parse_logic(data: object) -> Union["FilterParams", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                logic_type_0 = FilterParams.from_dict(data)

                return logic_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FilterParams", None, Unset], data)

        logic = _parse_logic(d.pop("logic", UNSET))

        message = d.pop("message", UNSET)

        def _parse_pct_samples(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        pct_samples = _parse_pct_samples(d.pop("pct_samples", UNSET))

        def _parse_score(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        score = _parse_score(d.pop("score", UNSET))

        def _parse_suggestion(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        suggestion = _parse_suggestion(d.pop("suggestion", UNSET))

        xray_classname = d.pop("xray_classname", UNSET)

        x_ray_card_db = cls(
            alert_id=alert_id,
            dismissed=dismissed,
            id=id,
            message_fields=message_fields,
            xray_class=xray_class,
            extra_filters=extra_filters,
            importance=importance,
            logic=logic,
            message=message,
            pct_samples=pct_samples,
            score=score,
            suggestion=suggestion,
            xray_classname=xray_classname,
        )

        x_ray_card_db.additional_properties = d
        return x_ray_card_db

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
