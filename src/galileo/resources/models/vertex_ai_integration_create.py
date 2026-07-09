from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig
    from ..models.vertex_aigcs_config import VertexAIGCSConfig


T = TypeVar("T", bound="VertexAIIntegrationCreate")


@_attrs_define
class VertexAIIntegrationCreate:
    """
    Attributes:
        token (str):
        multi_modal_config (MultiModalModelIntegrationConfig | None | Unset): Configuration for multi-modal (file
            upload) capabilities.
        gcs_config (None | Unset | VertexAIGCSConfig):
    """

    token: str
    multi_modal_config: MultiModalModelIntegrationConfig | None | Unset = UNSET
    gcs_config: None | Unset | VertexAIGCSConfig = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig
        from ..models.vertex_aigcs_config import VertexAIGCSConfig

        token = self.token

        multi_modal_config: dict[str, Any] | None | Unset
        if isinstance(self.multi_modal_config, Unset):
            multi_modal_config = UNSET
        elif isinstance(self.multi_modal_config, MultiModalModelIntegrationConfig):
            multi_modal_config = self.multi_modal_config.to_dict()
        else:
            multi_modal_config = self.multi_modal_config

        gcs_config: dict[str, Any] | None | Unset
        if isinstance(self.gcs_config, Unset):
            gcs_config = UNSET
        elif isinstance(self.gcs_config, VertexAIGCSConfig):
            gcs_config = self.gcs_config.to_dict()
        else:
            gcs_config = self.gcs_config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"token": token})
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if gcs_config is not UNSET:
            field_dict["gcs_config"] = gcs_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig
        from ..models.vertex_aigcs_config import VertexAIGCSConfig

        d = dict(src_dict)
        token = d.pop("token")

        def _parse_multi_modal_config(data: object) -> MultiModalModelIntegrationConfig | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                multi_modal_config_type_0 = MultiModalModelIntegrationConfig.from_dict(data)

                return multi_modal_config_type_0
            except:  # noqa: E722
                pass
            return cast(MultiModalModelIntegrationConfig | None | Unset, data)

        multi_modal_config = _parse_multi_modal_config(d.pop("multi_modal_config", UNSET))

        def _parse_gcs_config(data: object) -> None | Unset | VertexAIGCSConfig:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gcs_config_type_0 = VertexAIGCSConfig.from_dict(data)

                return gcs_config_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | VertexAIGCSConfig, data)

        gcs_config = _parse_gcs_config(d.pop("gcs_config", UNSET))

        vertex_ai_integration_create = cls(token=token, multi_modal_config=multi_modal_config, gcs_config=gcs_config)

        vertex_ai_integration_create.additional_properties = d
        return vertex_ai_integration_create

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
