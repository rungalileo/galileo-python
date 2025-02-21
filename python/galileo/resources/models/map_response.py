from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.bar_chart import BarChart


T = TypeVar("T", bound="MAPResponse")


@_attrs_define
class MAPResponse:
    """The main metric for Object Detection.

    mAP, or mean Average Precision, is an Object Detection metric that provides you with a general sense of the
    performance of your model.

    mAP is not simply the average precision for each class, it is much more technical
    https://towardsdatascience.com/breaking-down-mean-average-precision-map-ae462f623a52

    We also provide each error and its "score", which represents how much the model
    would have improved by fixing each value

        Attributes:
            ap_per_class (BarChart): A class to represent a basic bar chart.

                labels: List[str] the x axis labels
                values: List[int | float] the counts for each bar
            error_scores (BarChart): A class to represent a basic bar chart.

                labels: List[str] the x axis labels
                values: List[int | float] the counts for each bar
            map_ (float):
            map_threshold (float):
    """

    ap_per_class: "BarChart"
    error_scores: "BarChart"
    map_: float
    map_threshold: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ap_per_class = self.ap_per_class.to_dict()

        error_scores = self.error_scores.to_dict()

        map_ = self.map_

        map_threshold = self.map_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"ap_per_class": ap_per_class, "error_scores": error_scores, "map": map_, "map_threshold": map_threshold}
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.bar_chart import BarChart

        d = src_dict.copy()
        ap_per_class = BarChart.from_dict(d.pop("ap_per_class"))

        error_scores = BarChart.from_dict(d.pop("error_scores"))

        map_ = d.pop("map")

        map_threshold = d.pop("map_threshold")

        map_response = cls(ap_per_class=ap_per_class, error_scores=error_scores, map_=map_, map_threshold=map_threshold)

        map_response.additional_properties = d
        return map_response

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
