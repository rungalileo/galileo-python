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
    Attributes:
        alias (str):
        name (str):
        api_version (Union[None, Unset, str]):
        assistant_role (Union[None, Unset, str]):
        cost_by (Union[Unset, ModelCostBy]):
        formatting_tokens (Union[Unset, int]):  Default: 0.
        input_map (Union['InputMap', None, Unset]):
        input_price (Union[Unset, float]):  Default: 0.0.
        input_token_limit (Union[None, Unset, int]):
        integration (Union[Unset, LLMIntegration]):
        is_chat (Union[Unset, bool]):  Default: False.
        output_map (Union['OutputMap', None, Unset]):
        output_price (Union[Unset, float]):  Default: 0.0.
        output_token_limit (Union[None, Unset, int]):
        params_map (Union[Unset, RunParamsMap]): Maps the internal settings parameters (left) to the serialized
            parameters (right) we want to send in the API
            requests.
        provides_log_probs (Union[Unset, bool]):  Default: False.
        response_prefix_tokens (Union[Unset, int]):  Default: 0.
        system_supported (Union[Unset, bool]):  Default: False.
        token_limit (Union[None, Unset, int]):
        user_role (Union[None, Unset, str]):
    """

    alias: str
    name: str
    api_version: Union[None, Unset, str] = UNSET
    assistant_role: Union[None, Unset, str] = UNSET
    cost_by: Union[Unset, ModelCostBy] = UNSET
    formatting_tokens: Union[Unset, int] = 0
    input_map: Union["InputMap", None, Unset] = UNSET
    input_price: Union[Unset, float] = 0.0
    input_token_limit: Union[None, Unset, int] = UNSET
    integration: Union[Unset, LLMIntegration] = UNSET
    is_chat: Union[Unset, bool] = False
    output_map: Union["OutputMap", None, Unset] = UNSET
    output_price: Union[Unset, float] = 0.0
    output_token_limit: Union[None, Unset, int] = UNSET
    params_map: Union[Unset, "RunParamsMap"] = UNSET
    provides_log_probs: Union[Unset, bool] = False
    response_prefix_tokens: Union[Unset, int] = 0
    system_supported: Union[Unset, bool] = False
    token_limit: Union[None, Unset, int] = UNSET
    user_role: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.input_map import InputMap
        from ..models.output_map import OutputMap

        alias = self.alias

        name = self.name

        api_version: Union[None, Unset, str]
        if isinstance(self.api_version, Unset):
            api_version = UNSET
        else:
            api_version = self.api_version

        assistant_role: Union[None, Unset, str]
        if isinstance(self.assistant_role, Unset):
            assistant_role = UNSET
        else:
            assistant_role = self.assistant_role

        cost_by: Union[Unset, str] = UNSET
        if not isinstance(self.cost_by, Unset):
            cost_by = self.cost_by.value

        formatting_tokens = self.formatting_tokens

        input_map: Union[None, Unset, dict[str, Any]]
        if isinstance(self.input_map, Unset):
            input_map = UNSET
        elif isinstance(self.input_map, InputMap):
            input_map = self.input_map.to_dict()
        else:
            input_map = self.input_map

        input_price = self.input_price

        input_token_limit: Union[None, Unset, int]
        if isinstance(self.input_token_limit, Unset):
            input_token_limit = UNSET
        else:
            input_token_limit = self.input_token_limit

        integration: Union[Unset, str] = UNSET
        if not isinstance(self.integration, Unset):
            integration = self.integration.value

        is_chat = self.is_chat

        output_map: Union[None, Unset, dict[str, Any]]
        if isinstance(self.output_map, Unset):
            output_map = UNSET
        elif isinstance(self.output_map, OutputMap):
            output_map = self.output_map.to_dict()
        else:
            output_map = self.output_map

        output_price = self.output_price

        output_token_limit: Union[None, Unset, int]
        if isinstance(self.output_token_limit, Unset):
            output_token_limit = UNSET
        else:
            output_token_limit = self.output_token_limit

        params_map: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.params_map, Unset):
            params_map = self.params_map.to_dict()

        provides_log_probs = self.provides_log_probs

        response_prefix_tokens = self.response_prefix_tokens

        system_supported = self.system_supported

        token_limit: Union[None, Unset, int]
        if isinstance(self.token_limit, Unset):
            token_limit = UNSET
        else:
            token_limit = self.token_limit

        user_role: Union[None, Unset, str]
        if isinstance(self.user_role, Unset):
            user_role = UNSET
        else:
            user_role = self.user_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"alias": alias, "name": name})
        if api_version is not UNSET:
            field_dict["api_version"] = api_version
        if assistant_role is not UNSET:
            field_dict["assistant_role"] = assistant_role
        if cost_by is not UNSET:
            field_dict["cost_by"] = cost_by
        if formatting_tokens is not UNSET:
            field_dict["formatting_tokens"] = formatting_tokens
        if input_map is not UNSET:
            field_dict["input_map"] = input_map
        if input_price is not UNSET:
            field_dict["input_price"] = input_price
        if input_token_limit is not UNSET:
            field_dict["input_token_limit"] = input_token_limit
        if integration is not UNSET:
            field_dict["integration"] = integration
        if is_chat is not UNSET:
            field_dict["is_chat"] = is_chat
        if output_map is not UNSET:
            field_dict["output_map"] = output_map
        if output_price is not UNSET:
            field_dict["output_price"] = output_price
        if output_token_limit is not UNSET:
            field_dict["output_token_limit"] = output_token_limit
        if params_map is not UNSET:
            field_dict["params_map"] = params_map
        if provides_log_probs is not UNSET:
            field_dict["provides_log_probs"] = provides_log_probs
        if response_prefix_tokens is not UNSET:
            field_dict["response_prefix_tokens"] = response_prefix_tokens
        if system_supported is not UNSET:
            field_dict["system_supported"] = system_supported
        if token_limit is not UNSET:
            field_dict["token_limit"] = token_limit
        if user_role is not UNSET:
            field_dict["user_role"] = user_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.input_map import InputMap
        from ..models.output_map import OutputMap
        from ..models.run_params_map import RunParamsMap

        d = src_dict.copy()
        alias = d.pop("alias")

        name = d.pop("name")

        def _parse_api_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        api_version = _parse_api_version(d.pop("api_version", UNSET))

        def _parse_assistant_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        assistant_role = _parse_assistant_role(d.pop("assistant_role", UNSET))

        _cost_by = d.pop("cost_by", UNSET)
        cost_by: Union[Unset, ModelCostBy]
        if isinstance(_cost_by, Unset):
            cost_by = UNSET
        else:
            cost_by = ModelCostBy(_cost_by)

        formatting_tokens = d.pop("formatting_tokens", UNSET)

        def _parse_input_map(data: object) -> Union["InputMap", None, Unset]:
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
            return cast(Union["InputMap", None, Unset], data)

        input_map = _parse_input_map(d.pop("input_map", UNSET))

        input_price = d.pop("input_price", UNSET)

        def _parse_input_token_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        input_token_limit = _parse_input_token_limit(d.pop("input_token_limit", UNSET))

        _integration = d.pop("integration", UNSET)
        integration: Union[Unset, LLMIntegration]
        if isinstance(_integration, Unset):
            integration = UNSET
        else:
            integration = LLMIntegration(_integration)

        is_chat = d.pop("is_chat", UNSET)

        def _parse_output_map(data: object) -> Union["OutputMap", None, Unset]:
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
            return cast(Union["OutputMap", None, Unset], data)

        output_map = _parse_output_map(d.pop("output_map", UNSET))

        output_price = d.pop("output_price", UNSET)

        def _parse_output_token_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        output_token_limit = _parse_output_token_limit(d.pop("output_token_limit", UNSET))

        _params_map = d.pop("params_map", UNSET)
        params_map: Union[Unset, RunParamsMap]
        if isinstance(_params_map, Unset):
            params_map = UNSET
        else:
            params_map = RunParamsMap.from_dict(_params_map)

        provides_log_probs = d.pop("provides_log_probs", UNSET)

        response_prefix_tokens = d.pop("response_prefix_tokens", UNSET)

        system_supported = d.pop("system_supported", UNSET)

        def _parse_token_limit(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        token_limit = _parse_token_limit(d.pop("token_limit", UNSET))

        def _parse_user_role(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_role = _parse_user_role(d.pop("user_role", UNSET))

        model = cls(
            alias=alias,
            name=name,
            api_version=api_version,
            assistant_role=assistant_role,
            cost_by=cost_by,
            formatting_tokens=formatting_tokens,
            input_map=input_map,
            input_price=input_price,
            input_token_limit=input_token_limit,
            integration=integration,
            is_chat=is_chat,
            output_map=output_map,
            output_price=output_price,
            output_token_limit=output_token_limit,
            params_map=params_map,
            provides_log_probs=provides_log_probs,
            response_prefix_tokens=response_prefix_tokens,
            system_supported=system_supported,
            token_limit=token_limit,
            user_role=user_role,
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
