from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.bar_chart import BarChart


T = TypeVar("T", bound="SegmentationMetricsResponse")


@_attrs_define
class SegmentationMetricsResponse:
    """The main metric for Semantic Segmentation.

    IoU, or Intersection over Union, is an Semantic Segmentation metric that provides you with a general sense of the
    performance of your model.

    IoU is defined as the intersection of the predicted and ground truth masks Mean IoU is the average IoU across all
    classes Boundary IoU is the IoU for the boundary of the mask, which protects against   bias towards larger masks
    https://learnopencv.com/intersection-over-union-iou-in-object-detection-and-segmentation/

        Attributes:
            boundary_iou (float):
            boundary_iou_per_class (BarChart): A class to represent a basic bar chart.

                labels: List[str] the x axis labels
                values: List[int | float] the counts for each bar
            dice_coefficient (float):
            dice_per_class (BarChart): A class to represent a basic bar chart.

                labels: List[str] the x axis labels
                values: List[int | float] the counts for each bar
            mean_iou (float):
            mean_iou_per_class (BarChart): A class to represent a basic bar chart.

                labels: List[str] the x axis labels
                values: List[int | float] the counts for each bar
    """

    boundary_iou: float
    boundary_iou_per_class: "BarChart"
    dice_coefficient: float
    dice_per_class: "BarChart"
    mean_iou: float
    mean_iou_per_class: "BarChart"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        boundary_iou = self.boundary_iou

        boundary_iou_per_class = self.boundary_iou_per_class.to_dict()

        dice_coefficient = self.dice_coefficient

        dice_per_class = self.dice_per_class.to_dict()

        mean_iou = self.mean_iou

        mean_iou_per_class = self.mean_iou_per_class.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "boundary_iou": boundary_iou,
                "boundary_iou_per_class": boundary_iou_per_class,
                "dice_coefficient": dice_coefficient,
                "dice_per_class": dice_per_class,
                "mean_iou": mean_iou,
                "mean_iou_per_class": mean_iou_per_class,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.bar_chart import BarChart

        d = src_dict.copy()
        boundary_iou = d.pop("boundary_iou")

        boundary_iou_per_class = BarChart.from_dict(d.pop("boundary_iou_per_class"))

        dice_coefficient = d.pop("dice_coefficient")

        dice_per_class = BarChart.from_dict(d.pop("dice_per_class"))

        mean_iou = d.pop("mean_iou")

        mean_iou_per_class = BarChart.from_dict(d.pop("mean_iou_per_class"))

        segmentation_metrics_response = cls(
            boundary_iou=boundary_iou,
            boundary_iou_per_class=boundary_iou_per_class,
            dice_coefficient=dice_coefficient,
            dice_per_class=dice_per_class,
            mean_iou=mean_iou,
            mean_iou_per_class=mean_iou_per_class,
        )

        segmentation_metrics_response.additional_properties = d
        return segmentation_metrics_response

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
