from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.cartograph_cluster import CartographCluster


T = TypeVar("T", bound="CartographClusterResponse")


@_attrs_define
class CartographClusterResponse:
    """
    Attributes:
        cartograph_clusters (list['CartographCluster']):
    """

    cartograph_clusters: list["CartographCluster"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cartograph_clusters = []
        for cartograph_clusters_item_data in self.cartograph_clusters:
            cartograph_clusters_item = cartograph_clusters_item_data.to_dict()
            cartograph_clusters.append(cartograph_clusters_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"cartograph_clusters": cartograph_clusters})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.cartograph_cluster import CartographCluster

        d = src_dict.copy()
        cartograph_clusters = []
        _cartograph_clusters = d.pop("cartograph_clusters")
        for cartograph_clusters_item_data in _cartograph_clusters:
            cartograph_clusters_item = CartographCluster.from_dict(cartograph_clusters_item_data)

            cartograph_clusters.append(cartograph_clusters_item)

        cartograph_cluster_response = cls(cartograph_clusters=cartograph_clusters)

        cartograph_cluster_response.additional_properties = d
        return cartograph_cluster_response

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
