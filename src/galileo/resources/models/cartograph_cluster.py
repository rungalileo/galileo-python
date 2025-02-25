from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CartographCluster")


@_attrs_define
class CartographCluster:
    """Information about a Cartograph embedding cluster.

    Attributes:
        cluster_description (str):
        cluster_id (int):
        cluster_size (int):
        average_confidence (Union[None, Unset, float]):
        average_dep (Union[None, Unset, float]):
        average_f1 (Union[None, Unset, float]):
        cluster_summary (Union[None, Unset, str]):
        cluster_topic (Union[None, Unset, str]):
    """

    cluster_description: str
    cluster_id: int
    cluster_size: int
    average_confidence: Union[None, Unset, float] = UNSET
    average_dep: Union[None, Unset, float] = UNSET
    average_f1: Union[None, Unset, float] = UNSET
    cluster_summary: Union[None, Unset, str] = UNSET
    cluster_topic: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cluster_description = self.cluster_description

        cluster_id = self.cluster_id

        cluster_size = self.cluster_size

        average_confidence: Union[None, Unset, float]
        if isinstance(self.average_confidence, Unset):
            average_confidence = UNSET
        else:
            average_confidence = self.average_confidence

        average_dep: Union[None, Unset, float]
        if isinstance(self.average_dep, Unset):
            average_dep = UNSET
        else:
            average_dep = self.average_dep

        average_f1: Union[None, Unset, float]
        if isinstance(self.average_f1, Unset):
            average_f1 = UNSET
        else:
            average_f1 = self.average_f1

        cluster_summary: Union[None, Unset, str]
        if isinstance(self.cluster_summary, Unset):
            cluster_summary = UNSET
        else:
            cluster_summary = self.cluster_summary

        cluster_topic: Union[None, Unset, str]
        if isinstance(self.cluster_topic, Unset):
            cluster_topic = UNSET
        else:
            cluster_topic = self.cluster_topic

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"cluster_description": cluster_description, "cluster_id": cluster_id, "cluster_size": cluster_size}
        )
        if average_confidence is not UNSET:
            field_dict["average_confidence"] = average_confidence
        if average_dep is not UNSET:
            field_dict["average_dep"] = average_dep
        if average_f1 is not UNSET:
            field_dict["average_f1"] = average_f1
        if cluster_summary is not UNSET:
            field_dict["cluster_summary"] = cluster_summary
        if cluster_topic is not UNSET:
            field_dict["cluster_topic"] = cluster_topic

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        cluster_description = d.pop("cluster_description")

        cluster_id = d.pop("cluster_id")

        cluster_size = d.pop("cluster_size")

        def _parse_average_confidence(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_confidence = _parse_average_confidence(d.pop("average_confidence", UNSET))

        def _parse_average_dep(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_dep = _parse_average_dep(d.pop("average_dep", UNSET))

        def _parse_average_f1(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        average_f1 = _parse_average_f1(d.pop("average_f1", UNSET))

        def _parse_cluster_summary(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster_summary = _parse_cluster_summary(d.pop("cluster_summary", UNSET))

        def _parse_cluster_topic(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cluster_topic = _parse_cluster_topic(d.pop("cluster_topic", UNSET))

        cartograph_cluster = cls(
            cluster_description=cluster_description,
            cluster_id=cluster_id,
            cluster_size=cluster_size,
            average_confidence=average_confidence,
            average_dep=average_dep,
            average_f1=average_f1,
            cluster_summary=cluster_summary,
            cluster_topic=cluster_topic,
        )

        cartograph_cluster.additional_properties = d
        return cartograph_cluster

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
