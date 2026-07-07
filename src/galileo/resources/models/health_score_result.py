from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.health_score_type import HealthScoreType

if TYPE_CHECKING:
    from ..models.health_score_result_secondary import HealthScoreResultSecondary


T = TypeVar("T", bound="HealthScoreResult")


@_attrs_define
class HealthScoreResult:
    """
    Attributes:
        health_score_type (Union[HealthScoreType, None]):
        value (Union[None, float]): Primary health score metric value, or None if no valid rows.
        skipped_rows (int): Rows excluded because MGT or score could not be parsed.
        secondary (HealthScoreResultSecondary): Secondary metrics (MAE, RMSE, R², per-class F1, etc.).
        total_scored_rows (int): Rows with a successful scorer result.
        total_mgt_rows (int): Rows with a non-null MGT value after overlay.
        joined_rows (int): Rows with both a score and a MGT value (used for computation).
    """

    health_score_type: Union[HealthScoreType, None]
    value: Union[None, float]
    skipped_rows: int
    secondary: "HealthScoreResultSecondary"
    total_scored_rows: int
    total_mgt_rows: int
    joined_rows: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        health_score_type: Union[None, str]
        if isinstance(self.health_score_type, HealthScoreType):
            health_score_type = self.health_score_type.value
        else:
            health_score_type = self.health_score_type

        value: Union[None, float]
        value = self.value

        skipped_rows = self.skipped_rows

        secondary = self.secondary.to_dict()

        total_scored_rows = self.total_scored_rows

        total_mgt_rows = self.total_mgt_rows

        joined_rows = self.joined_rows

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "health_score_type": health_score_type,
                "value": value,
                "skipped_rows": skipped_rows,
                "secondary": secondary,
                "total_scored_rows": total_scored_rows,
                "total_mgt_rows": total_mgt_rows,
                "joined_rows": joined_rows,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.health_score_result_secondary import HealthScoreResultSecondary

        d = dict(src_dict)

        def _parse_health_score_type(data: object) -> Union[HealthScoreType, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                health_score_type_type_0 = HealthScoreType(data)

                return health_score_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[HealthScoreType, None], data)

        health_score_type = _parse_health_score_type(d.pop("health_score_type"))

        def _parse_value(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        value = _parse_value(d.pop("value"))

        skipped_rows = d.pop("skipped_rows")

        secondary = HealthScoreResultSecondary.from_dict(d.pop("secondary"))

        total_scored_rows = d.pop("total_scored_rows")

        total_mgt_rows = d.pop("total_mgt_rows")

        joined_rows = d.pop("joined_rows")

        health_score_result = cls(
            health_score_type=health_score_type,
            value=value,
            skipped_rows=skipped_rows,
            secondary=secondary,
            total_scored_rows=total_scored_rows,
            total_mgt_rows=total_mgt_rows,
            joined_rows=joined_rows,
        )

        health_score_result.additional_properties = d
        return health_score_result

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
