from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
    Attributes
    ----------
        name (str):
        alias (str):
        integration (Union[Unset, LLMIntegration]):
        user_role (Union[None, Unset, str]):
        assistant_role (Union[None, Unset, str]):
        system_supported (Union[Unset, bool]):  Default: False.
        alternative_names (Union[Unset, list[str]]): Alternative names for the model, used for matching with various
            current, versioned or legacy names.
        input_token_limit (Union[None, Unset, int]):
        output_token_limit (Union[None, Unset, int]):
        token_limit (Union[None, Unset, int]):
        output_price (Union[Unset, float]):  Default: 0.0.
        input_price (Union[Unset, float]):  Default: 0.0.
        cost_by (Union[Unset, ModelCostBy]):
        is_chat (Union[Unset, bool]):  Default: False.
        provides_log_probs (Union[Unset, bool]):  Default: False.
        formatting_tokens (Union[Unset, int]):  Default: 0.
        response_prefix_tokens (Union[Unset, int]):  Default: 0.
        api_version (Union[None, Unset, str]):
        params_map (Union[Unset, RunParamsMap]): Maps the internal settings parameters (left) to the serialized
            parameters (right) we want to send in the API
            requests.
        output_map (Union['OutputMap', None, Unset]):
        input_map (Union['InputMap', None, Unset]):
    """

    name: str
    alias: str
    integration: Union[Unset, LLMIntegration] = UNSET
    user_role: Union[None, Unset, str] = UNSET
    assistant_role: Union[None, Unset, str] = UNSET
    system_supported: Union[Unset, bool] = False
    alternative_names: Union[Unset, list[str]] = UNSET
    input_token_limit: Union[None, Unset, int] = UNSET
    output_token_limit: Union[None, Unset, int] = UNSET
    token_limit: Union[None, Unset, int] = UNSET
    output_price: Union[Unset, float] = 0.0
    input_price: Union[Unset, float] = 0.0
    cost_by: Union[Unset, ModelCostBy] = UNSET
    is_chat: Union[Unset, bool] = False
    provides_log_probs: Union[Unset, bool] = False
    formatting_tokens: Union[Unset, int] = 0
    response_prefix_tokens: Union[Unset, int] = 0
    api_version: Union[None, Unset, str] = UNSET
    params_map: Union[Unset, "RunParamsMap"] = UNSET
    output_map: Union["OutputMap", None, Unset] = UNSET
    input_map: Union["InputMap", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.input_map import InputMap
        from ..models.output_map import OutputMap

        name = self.name

        alias = self.alias

        integration: Union[Unset, str] = UNSET
        if not isinstance(self.integration, Unset):
            integration = self.integration.value

        user_role: Union[None, Unset, str]
        user_role = UNSET if isinstance(self.user_role, Unset) else self.user_role

        assistant_role: Union[None, Unset, str]
        assistant_role = UNSET if isinstance(self.assistant_role, Unset) else self.assistant_role

        system_supported = self.system_supported

        alternative_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.alternative_names, Unset):
            alternative_names = self.alternative_names

        input_token_limit: Union[None, Unset, int]
        input_token_limit = UNSET if isinstance(self.input_token_limit, Unset) else self.input_token_limit

        output_token_limit: Union[None, Unset, int]
        output_token_limit = UNSET if isinstance(self.output_token_limit, Unset) else self.output_token_limit

        token_limit: Union[None, Unset, int]
        token_limit = UNSET if isinstance(self.token_limit, Unset) else self.token_limit

        output_price = self.output_price

        input_price = self.input_price

        cost_by: Union[Unset, str] = UNSET
        if not isinstance(self.cost_by, Unset):
            cost_by = self.cost_by.value

        is_chat = self.is_chat

        provides_log_probs = self.provides_log_probs

        formatting_tokens = self.formatting_tokens

        response_prefix_tokens = self.response_prefix_tokens

        api_version: Union[None, Unset, str]
        api_version = UNSET if isinstance(self.api_version, Unset) else self.api_version

        params_map: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.params_map, Unset):
            params_map = self.params_map.to_dict()

        output_map: Union[None, Unset, dict[str, Any]]
        if isinstance(self.output_map, Unset):
            output_map = UNSET
        elif isinstance(self.output_map, OutputMap):
            output_map = self.output_map.to_dict()
        else:
            output_map = self.output_map

        input_map: Union[None, Unset, dict[str, Any]]
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
        integration: Union[Unset, LLMIntegration]
        integration = UNSET if isinstance(_integration, Unset) else LLMIntegration(_integration)

        def _parse_user_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_role = _parse_user_role(d.pop("user_role", UNSET))

        def _parse_assistant_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        assistant_role = _parse_assistant_role(d.pop("assistant_role", UNSET))

        system_supported = d.pop("system_supported", UNSET)

        alternative_names = cast(list[str], d.pop("alternative_names", UNSET))

        def _parse_input_token_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        input_token_limit = _parse_input_token_limit(d.pop("input_token_limit", UNSET))

        def _parse_output_token_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        output_token_limit = _parse_output_token_limit(d.pop("output_token_limit", UNSET))

        def _parse_token_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        token_limit = _parse_token_limit(d.pop("token_limit", UNSET))

        output_price = d.pop("output_price", UNSET)

        input_price = d.pop("input_price", UNSET)

        _cost_by = d.pop("cost_by", UNSET)
        cost_by: Union[Unset, ModelCostBy]
        cost_by = UNSET if isinstance(_cost_by, Unset) else ModelCostBy(_cost_by)

        is_chat = d.pop("is_chat", UNSET)

        provides_log_probs = d.pop("provides_log_probs", UNSET)

        formatting_tokens = d.pop("formatting_tokens", UNSET)

        response_prefix_tokens = d.pop("response_prefix_tokens", UNSET)

        def _parse_api_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_version = _parse_api_version(d.pop("api_version", UNSET))

        _params_map = d.pop("params_map", UNSET)
        params_map: Union[Unset, RunParamsMap]
        params_map = UNSET if isinstance(_params_map, Unset) else RunParamsMap.from_dict(_params_map)

        def _parse_output_map(data: object) -> Union["OutputMap", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return OutputMap.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["OutputMap", None, Unset], data)

        output_map = _parse_output_map(d.pop("output_map", UNSET))

        def _parse_input_map(data: object) -> Union["InputMap", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return InputMap.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["InputMap", None, Unset], data)

        input_map = _parse_input_map(d.pop("input_map", UNSET))

        model = cls(
            name=name,
            alias=alias,
            integration=integration,
            user_role=user_role,
            assistant_role=assistant_role,
            system_supported=system_supported,
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
