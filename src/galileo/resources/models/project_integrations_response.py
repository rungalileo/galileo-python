from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_integrations_response_integrations import ProjectIntegrationsResponseIntegrations


T = TypeVar("T", bound="ProjectIntegrationsResponse")


@_attrs_define
class ProjectIntegrationsResponse:
    """
    Attributes:
        integrations (ProjectIntegrationsResponseIntegrations):
    """

    integrations: "ProjectIntegrationsResponseIntegrations"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integrations = self.integrations.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"integrations": integrations})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.project_integrations_response_integrations import ProjectIntegrationsResponseIntegrations

        d = src_dict.copy()
        integrations = ProjectIntegrationsResponseIntegrations.from_dict(d.pop("integrations"))

        project_integrations_response = cls(integrations=integrations)

        project_integrations_response.additional_properties = d
        return project_integrations_response

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
