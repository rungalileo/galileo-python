from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CBORunCluster")


@_attrs_define
class CBORunCluster:
    """
    Attributes:
        id (int):
        labels (list[str]):
        num_samples (int):
        score (float):
    """

    id: int
    labels: list[str]
    num_samples: int
    score: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        labels = self.labels

        num_samples = self.num_samples

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "labels": labels, "num_samples": num_samples, "score": score})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        labels = cast(list[str], d.pop("labels"))

        num_samples = d.pop("num_samples")

        score = d.pop("score")

        cbo_run_cluster = cls(id=id, labels=labels, num_samples=num_samples, score=score)

        cbo_run_cluster.additional_properties = d
        return cbo_run_cluster

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
