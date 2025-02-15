import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.categorical_prompt_filter_param import CategoricalPromptFilterParam
    from ..models.evaluate_alert_db_extra_type_0 import EvaluateAlertDBExtraType0
    from ..models.range_prompt_filter_param import RangePromptFilterParam
    from ..models.value_prompt_filter_param import ValuePromptFilterParam


T = TypeVar("T", bound="EvaluateAlertDB")


@_attrs_define
class EvaluateAlertDB:
    """
    Attributes:
        alert_name (str):
        created_at (datetime.datetime):
        description (str):
        field_name (str):
        filter_ (Union['CategoricalPromptFilterParam', 'RangePromptFilterParam', 'ValuePromptFilterParam']):
        id (str):
        project_id (str):
        run_id (str):
        updated_at (datetime.datetime):
        extra (Union['EvaluateAlertDBExtraType0', None, Unset]):
    """

    alert_name: str
    created_at: datetime.datetime
    description: str
    field_name: str
    filter_: Union["CategoricalPromptFilterParam", "RangePromptFilterParam", "ValuePromptFilterParam"]
    id: str
    project_id: str
    run_id: str
    updated_at: datetime.datetime
    extra: Union["EvaluateAlertDBExtraType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluate_alert_db_extra_type_0 import EvaluateAlertDBExtraType0
        from ..models.range_prompt_filter_param import RangePromptFilterParam
        from ..models.value_prompt_filter_param import ValuePromptFilterParam

        alert_name = self.alert_name

        created_at = self.created_at.isoformat()

        description = self.description

        field_name = self.field_name

        filter_: dict[str, Any]
        if isinstance(self.filter_, RangePromptFilterParam):
            filter_ = self.filter_.to_dict()
        elif isinstance(self.filter_, ValuePromptFilterParam):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_.to_dict()

        id = self.id

        project_id = self.project_id

        run_id = self.run_id

        updated_at = self.updated_at.isoformat()

        extra: Union[None, Unset, dict[str, Any]]
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, EvaluateAlertDBExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "alert_name": alert_name,
                "created_at": created_at,
                "description": description,
                "field_name": field_name,
                "filter": filter_,
                "id": id,
                "project_id": project_id,
                "run_id": run_id,
                "updated_at": updated_at,
            }
        )
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.categorical_prompt_filter_param import CategoricalPromptFilterParam
        from ..models.evaluate_alert_db_extra_type_0 import EvaluateAlertDBExtraType0
        from ..models.range_prompt_filter_param import RangePromptFilterParam
        from ..models.value_prompt_filter_param import ValuePromptFilterParam

        d = src_dict.copy()
        alert_name = d.pop("alert_name")

        created_at = isoparse(d.pop("created_at"))

        description = d.pop("description")

        field_name = d.pop("field_name")

        def _parse_filter_(
            data: object,
        ) -> Union["CategoricalPromptFilterParam", "RangePromptFilterParam", "ValuePromptFilterParam"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = RangePromptFilterParam.from_dict(data)

                return filter_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_1 = ValuePromptFilterParam.from_dict(data)

                return filter_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            filter_type_2 = CategoricalPromptFilterParam.from_dict(data)

            return filter_type_2

        filter_ = _parse_filter_(d.pop("filter"))

        id = d.pop("id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        updated_at = isoparse(d.pop("updated_at"))

        def _parse_extra(data: object) -> Union["EvaluateAlertDBExtraType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = EvaluateAlertDBExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EvaluateAlertDBExtraType0", None, Unset], data)

        extra = _parse_extra(d.pop("extra", UNSET))

        evaluate_alert_db = cls(
            alert_name=alert_name,
            created_at=created_at,
            description=description,
            field_name=field_name,
            filter_=filter_,
            id=id,
            project_id=project_id,
            run_id=run_id,
            updated_at=updated_at,
            extra=extra,
        )

        evaluate_alert_db.additional_properties = d
        return evaluate_alert_db

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
