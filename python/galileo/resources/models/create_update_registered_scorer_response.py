import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.data_type_options import DataTypeOptions

T = TypeVar("T", bound="CreateUpdateRegisteredScorerResponse")


@_attrs_define
class CreateUpdateRegisteredScorerResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        created_by (str):
        data_type (Union[DataTypeOptions, None]):
        id (str):
        name (str):
        score_type (Union[None, str]):
        scoreable_node_types (Union[None, list[str]]):
        updated_at (datetime.datetime):
    """

    created_at: datetime.datetime
    created_by: str
    data_type: Union[DataTypeOptions, None]
    id: str
    name: str
    score_type: Union[None, str]
    scoreable_node_types: Union[None, list[str]]
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        data_type: Union[None, str]
        if isinstance(self.data_type, DataTypeOptions):
            data_type = self.data_type.value
        else:
            data_type = self.data_type

        id = self.id

        name = self.name

        score_type: Union[None, str]
        score_type = self.score_type

        scoreable_node_types: Union[None, list[str]]
        if isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "data_type": data_type,
                "id": id,
                "name": name,
                "score_type": score_type,
                "scoreable_node_types": scoreable_node_types,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        def _parse_data_type(data: object) -> Union[DataTypeOptions, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                data_type_type_0 = DataTypeOptions(data)

                return data_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[DataTypeOptions, None], data)

        data_type = _parse_data_type(d.pop("data_type"))

        id = d.pop("id")

        name = d.pop("name")

        def _parse_score_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        score_type = _parse_score_type(d.pop("score_type"))

        def _parse_scoreable_node_types(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scoreable_node_types_type_0 = cast(list[str], data)

                return scoreable_node_types_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types"))

        updated_at = isoparse(d.pop("updated_at"))

        create_update_registered_scorer_response = cls(
            created_at=created_at,
            created_by=created_by,
            data_type=data_type,
            id=id,
            name=name,
            score_type=score_type,
            scoreable_node_types=scoreable_node_types,
            updated_at=updated_at,
        )

        create_update_registered_scorer_response.additional_properties = d
        return create_update_registered_scorer_response

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
