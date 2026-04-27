from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.content_modality import ContentModality
from ..models.llm_integration import LLMIntegration
from ..models.model_cost_by import ModelCostBy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.input_map import InputMap
    from ..models.output_map import OutputMap
    from ..models.run_params_map import RunParamsMap


T = TypeVar("T", bound="Model")


@_attrs_define
class Model:
    """
    Attributes:
        name (str):
        alias (str):
        integration (LLMIntegration | Unset):
        user_role (None | str | Unset):
        assistant_role (None | str | Unset):
        system_supported (bool | Unset):  Default: False.
        input_modalities (list[ContentModality] | Unset): Input modalities that the model can accept.
        alternative_names (list[str] | Unset): Alternative names for the model, used for matching with various current,
            versioned or legacy names.
        input_token_limit (int | None | Unset):
        output_token_limit (int | None | Unset):
        token_limit (int | None | Unset):
        output_price (float | Unset):  Default: 0.0.
        input_price (float | Unset):  Default: 0.0.
        cost_by (ModelCostBy | Unset):
        is_chat (bool | Unset):  Default: False.
        provides_log_probs (bool | Unset):  Default: False.
        formatting_tokens (int | Unset):  Default: 0.
        response_prefix_tokens (int | Unset):  Default: 0.
        api_version (None | str | Unset):
        legacy_mistral_prompt_format (bool | Unset):  Default: False.
        requires_max_tokens (bool | Unset):  Default: False.
        max_top_p (float | None | Unset):
        params_map (RunParamsMap | Unset): Maps the internal settings parameters (left) to the serialized parameters
            (right) we want to send in the API
            requests.
        output_map (None | OutputMap | Unset):
        input_map (InputMap | None | Unset):
    """

    name: str
    alias: str
    integration: LLMIntegration | Unset = UNSET
    user_role: None | str | Unset = UNSET
    assistant_role: None | str | Unset = UNSET
    system_supported: bool | Unset = False
    input_modalities: list[ContentModality] | Unset = UNSET
    alternative_names: list[str] | Unset = UNSET
    input_token_limit: int | None | Unset = UNSET
    output_token_limit: int | None | Unset = UNSET
    token_limit: int | None | Unset = UNSET
    output_price: float | Unset = 0.0
    input_price: float | Unset = 0.0
    cost_by: ModelCostBy | Unset = UNSET
    is_chat: bool | Unset = False
    provides_log_probs: bool | Unset = False
    formatting_tokens: int | Unset = 0
    response_prefix_tokens: int | Unset = 0
    api_version: None | str | Unset = UNSET
    legacy_mistral_prompt_format: bool | Unset = False
    requires_max_tokens: bool | Unset = False
    max_top_p: float | None | Unset = UNSET
    params_map: RunParamsMap | Unset = UNSET
    output_map: None | OutputMap | Unset = UNSET
    input_map: InputMap | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.input_map import InputMap
        from ..models.output_map import OutputMap

        name = self.name

        alias = self.alias

        integration: str | Unset = UNSET
        if not isinstance(self.integration, Unset):
            integration = self.integration.value

        user_role: None | str | Unset
        if isinstance(self.user_role, Unset):
            user_role = UNSET
        else:
            user_role = self.user_role

        assistant_role: None | str | Unset
        if isinstance(self.assistant_role, Unset):
            assistant_role = UNSET
        else:
            assistant_role = self.assistant_role

        system_supported = self.system_supported

        input_modalities: list[str] | Unset = UNSET
        if not isinstance(self.input_modalities, Unset):
            input_modalities = []
            for input_modalities_item_data in self.input_modalities:
                input_modalities_item = input_modalities_item_data.value
                input_modalities.append(input_modalities_item)

        alternative_names: list[str] | Unset = UNSET
        if not isinstance(self.alternative_names, Unset):
            alternative_names = self.alternative_names

        input_token_limit: int | None | Unset
        if isinstance(self.input_token_limit, Unset):
            input_token_limit = UNSET
        else:
            input_token_limit = self.input_token_limit

        output_token_limit: int | None | Unset
        if isinstance(self.output_token_limit, Unset):
            output_token_limit = UNSET
        else:
            output_token_limit = self.output_token_limit

        token_limit: int | None | Unset
        if isinstance(self.token_limit, Unset):
            token_limit = UNSET
        else:
            token_limit = self.token_limit

        output_price = self.output_price

        input_price = self.input_price

        cost_by: str | Unset = UNSET
        if not isinstance(self.cost_by, Unset):
            cost_by = self.cost_by.value

        is_chat = self.is_chat

        provides_log_probs = self.provides_log_probs

        formatting_tokens = self.formatting_tokens

        response_prefix_tokens = self.response_prefix_tokens

        api_version: None | str | Unset
        if isinstance(self.api_version, Unset):
            api_version = UNSET
        else:
            api_version = self.api_version

        legacy_mistral_prompt_format = self.legacy_mistral_prompt_format

        requires_max_tokens = self.requires_max_tokens

        max_top_p: float | None | Unset
        if isinstance(self.max_top_p, Unset):
            max_top_p = UNSET
        else:
            max_top_p = self.max_top_p

        params_map: dict[str, Any] | Unset = UNSET
        if not isinstance(self.params_map, Unset):
            params_map = self.params_map.to_dict()

        output_map: dict[str, Any] | None | Unset
        if isinstance(self.output_map, Unset):
            output_map = UNSET
        elif isinstance(self.output_map, OutputMap):
            output_map = self.output_map.to_dict()
        else:
            output_map = self.output_map

        input_map: dict[str, Any] | None | Unset
        if isinstance(self.input_map, Unset):
            input_map = UNSET
        elif isinstance(self.input_map, InputMap):
            input_map = self.input_map.to_dict()
        else:
            input_map = self.input_map

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "alias": alias})
        if integration is not UNSET:
            field_dict["integration"] = integration
        if user_role is not UNSET:
            field_dict["user_role"] = user_role
        if assistant_role is not UNSET:
            field_dict["assistant_role"] = assistant_role
        if system_supported is not UNSET:
            field_dict["system_supported"] = system_supported
        if input_modalities is not UNSET:
            field_dict["input_modalities"] = input_modalities
        if alternative_names is not UNSET:
            field_dict["alternative_names"] = alternative_names
        if input_token_limit is not UNSET:
            field_dict["input_token_limit"] = input_token_limit
        if output_token_limit is not UNSET:
            field_dict["output_token_limit"] = output_token_limit
        if token_limit is not UNSET:
            field_dict["token_limit"] = token_limit
        if output_price is not UNSET:
            field_dict["output_price"] = output_price
        if input_price is not UNSET:
            field_dict["input_price"] = input_price
        if cost_by is not UNSET:
            field_dict["cost_by"] = cost_by
        if is_chat is not UNSET:
            field_dict["is_chat"] = is_chat
        if provides_log_probs is not UNSET:
            field_dict["provides_log_probs"] = provides_log_probs
        if formatting_tokens is not UNSET:
            field_dict["formatting_tokens"] = formatting_tokens
        if response_prefix_tokens is not UNSET:
            field_dict["response_prefix_tokens"] = response_prefix_tokens
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if legacy_mistral_prompt_format is not UNSET:
            field_dict["legacy_mistral_prompt_format"] = legacy_mistral_prompt_format
        if requires_max_tokens is not UNSET:
            field_dict["requires_max_tokens"] = requires_max_tokens
        if max_top_p is not UNSET:
            field_dict["max_top_p"] = max_top_p
        if params_map is not UNSET:
            field_dict["params_map"] = params_map
        if output_map is not UNSET:
            field_dict["output_map"] = output_map
        if input_map is not UNSET:
            field_dict["input_map"] = input_map

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.input_map import InputMap
        from ..models.output_map import OutputMap
        from ..models.run_params_map import RunParamsMap

        d = dict(src_dict)
        name = d.pop("name")

        alias = d.pop("alias")

        _integration = d.pop("integration", UNSET)
        integration: LLMIntegration | Unset
        if isinstance(_integration, Unset):
            integration = UNSET
        else:
            integration = LLMIntegration(_integration)

        def _parse_user_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_role = _parse_user_role(d.pop("user_role", UNSET))

        def _parse_assistant_role(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        assistant_role = _parse_assistant_role(d.pop("assistant_role", UNSET))

        system_supported = d.pop("system_supported", UNSET)

        _input_modalities = d.pop("input_modalities", UNSET)
        input_modalities: list[ContentModality] | Unset = UNSET
        if _input_modalities is not UNSET:
            input_modalities = []
            for input_modalities_item_data in _input_modalities:
                input_modalities_item = ContentModality(input_modalities_item_data)

                input_modalities.append(input_modalities_item)

        alternative_names = cast(list[str], d.pop("alternative_names", UNSET))

        def _parse_input_token_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        input_token_limit = _parse_input_token_limit(d.pop("input_token_limit", UNSET))

        def _parse_output_token_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        output_token_limit = _parse_output_token_limit(d.pop("output_token_limit", UNSET))

        def _parse_token_limit(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        token_limit = _parse_token_limit(d.pop("token_limit", UNSET))

        output_price = d.pop("output_price", UNSET)

        input_price = d.pop("input_price", UNSET)

        _cost_by = d.pop("cost_by", UNSET)
        cost_by: ModelCostBy | Unset
        if isinstance(_cost_by, Unset):
            cost_by = UNSET
        else:
            cost_by = ModelCostBy(_cost_by)

        is_chat = d.pop("is_chat", UNSET)

        provides_log_probs = d.pop("provides_log_probs", UNSET)

        formatting_tokens = d.pop("formatting_tokens", UNSET)

        response_prefix_tokens = d.pop("response_prefix_tokens", UNSET)

        def _parse_api_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        api_version = _parse_api_version(d.pop("api_version", UNSET))

        legacy_mistral_prompt_format = d.pop("legacy_mistral_prompt_format", UNSET)

        requires_max_tokens = d.pop("requires_max_tokens", UNSET)

        def _parse_max_top_p(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_top_p = _parse_max_top_p(d.pop("max_top_p", UNSET))

        _params_map = d.pop("params_map", UNSET)
        params_map: RunParamsMap | Unset
        if isinstance(_params_map, Unset):
            params_map = UNSET
        else:
            params_map = RunParamsMap.from_dict(_params_map)

        def _parse_output_map(data: object) -> None | OutputMap | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_map_type_0 = OutputMap.from_dict(data)

                return output_map_type_0
            except:  # noqa: E722
                pass
            return cast(None | OutputMap | Unset, data)

        output_map = _parse_output_map(d.pop("output_map", UNSET))

        def _parse_input_map(data: object) -> InputMap | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_map_type_0 = InputMap.from_dict(data)

                return input_map_type_0
            except:  # noqa: E722
                pass
            return cast(InputMap | None | Unset, data)

        input_map = _parse_input_map(d.pop("input_map", UNSET))

        model = cls(
            name=name,
            alias=alias,
            integration=integration,
            user_role=user_role,
            assistant_role=assistant_role,
            system_supported=system_supported,
            input_modalities=input_modalities,
            alternative_names=alternative_names,
            input_token_limit=input_token_limit,
            output_token_limit=output_token_limit,
            token_limit=token_limit,
            output_price=output_price,
            input_price=input_price,
            cost_by=cost_by,
            is_chat=is_chat,
            provides_log_probs=provides_log_probs,
            formatting_tokens=formatting_tokens,
            response_prefix_tokens=response_prefix_tokens,
            api_version=api_version,
            legacy_mistral_prompt_format=legacy_mistral_prompt_format,
            requires_max_tokens=requires_max_tokens,
            max_top_p=max_top_p,
            params_map=params_map,
            output_map=output_map,
            input_map=input_map,
        )

        model.additional_properties = d
        return model

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
