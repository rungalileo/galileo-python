from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig
    from ..models.vertex_ai_integration_extra_type_0 import VertexAIIntegrationExtraType0
    from ..models.vertex_aigcs_config_response import VertexAIGCSConfigResponse


T = TypeVar("T", bound="VertexAIIntegration")


@_attrs_define
class VertexAIIntegration:
    """
    Attributes:
        multi_modal_config (MultiModalModelIntegrationConfig | None | Unset): Configuration for multi-modal (file
            upload) capabilities.
        gcs_config (None | Unset | VertexAIGCSConfigResponse):
        id (None | str | Unset):
        name (Literal['vertex_ai'] | Unset):  Default: 'vertex_ai'.
        extra (None | Unset | VertexAIIntegrationExtraType0):
    """

    multi_modal_config: MultiModalModelIntegrationConfig | None | Unset = UNSET
    gcs_config: None | Unset | VertexAIGCSConfigResponse = UNSET
    id: None | str | Unset = UNSET
    name: Literal["vertex_ai"] | Unset = "vertex_ai"
    extra: None | Unset | VertexAIIntegrationExtraType0 = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig
        from ..models.vertex_ai_integration_extra_type_0 import VertexAIIntegrationExtraType0
        from ..models.vertex_aigcs_config_response import VertexAIGCSConfigResponse

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
        elif isinstance(self.gcs_config, VertexAIGCSConfigResponse):
            gcs_config = self.gcs_config.to_dict()
        else:
            gcs_config = self.gcs_config

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        name = self.name

        extra: dict[str, Any] | None | Unset
        if isinstance(self.extra, Unset):
            extra = UNSET
        elif isinstance(self.extra, VertexAIIntegrationExtraType0):
            extra = self.extra.to_dict()
        else:
            extra = self.extra

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if multi_modal_config is not UNSET:
            field_dict["multi_modal_config"] = multi_modal_config
        if gcs_config is not UNSET:
            field_dict["gcs_config"] = gcs_config
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if extra is not UNSET:
            field_dict["extra"] = extra

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.multi_modal_model_integration_config import MultiModalModelIntegrationConfig
        from ..models.vertex_ai_integration_extra_type_0 import VertexAIIntegrationExtraType0
        from ..models.vertex_aigcs_config_response import VertexAIGCSConfigResponse

        d = dict(src_dict)

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

        def _parse_gcs_config(data: object) -> None | Unset | VertexAIGCSConfigResponse:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                gcs_config_type_0 = VertexAIGCSConfigResponse.from_dict(data)

                return gcs_config_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | VertexAIGCSConfigResponse, data)

        gcs_config = _parse_gcs_config(d.pop("gcs_config", UNSET))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        name = cast(Literal["vertex_ai"] | Unset, d.pop("name", UNSET))
        if name != "vertex_ai" and not isinstance(name, Unset):
            raise ValueError(f"name must match const 'vertex_ai', got '{name}'")

        def _parse_extra(data: object) -> None | Unset | VertexAIIntegrationExtraType0:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                extra_type_0 = VertexAIIntegrationExtraType0.from_dict(data)

                return extra_type_0
            except:  # noqa: E722
                pass
            return cast(None | Unset | VertexAIIntegrationExtraType0, data)

        extra = _parse_extra(d.pop("extra", UNSET))

        vertex_ai_integration = cls(
            multi_modal_config=multi_modal_config, gcs_config=gcs_config, id=id, name=name, extra=extra
        )

        vertex_ai_integration.additional_properties = d
        return vertex_ai_integration

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
