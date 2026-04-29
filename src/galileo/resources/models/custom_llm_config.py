from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.custom_llm_config_init_kwargs_type_0 import CustomLLMConfigInitKwargsType0


T = TypeVar("T", bound="CustomLLMConfig")


@_attrs_define
class CustomLLMConfig:
    """Configuration for a custom LiteLLM handler class.

    Allows users to specify a custom implementation of litellm.CustomLLM
    that handles acompletion() calls with custom request/response transformation.

    Attributes
    ----------
            file_name (str): Python file name containing the CustomLLM class (e.g., 'my_handler.py')
            class_name (str): Class name within the module (must be a litellm.CustomLLM subclass)
            init_kwargs (Union['CustomLLMConfigInitKwargsType0', None, Unset]): Optional keyword arguments to pass to the
                CustomLLM constructor
    """

    file_name: str
    class_name: str
    init_kwargs: Union["CustomLLMConfigInitKwargsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.custom_llm_config_init_kwargs_type_0 import CustomLLMConfigInitKwargsType0

        file_name = self.file_name

        class_name = self.class_name

        init_kwargs: Union[None, Unset, dict[str, Any]]
        if isinstance(self.init_kwargs, Unset):
            init_kwargs = UNSET
        elif isinstance(self.init_kwargs, CustomLLMConfigInitKwargsType0):
            init_kwargs = self.init_kwargs.to_dict()
        else:
            init_kwargs = self.init_kwargs

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"file_name": file_name, "class_name": class_name})
        if init_kwargs is not UNSET:
            field_dict["init_kwargs"] = init_kwargs

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.custom_llm_config_init_kwargs_type_0 import CustomLLMConfigInitKwargsType0

        d = dict(src_dict)
        file_name = d.pop("file_name")

        class_name = d.pop("class_name")

        def _parse_init_kwargs(data: object) -> Union["CustomLLMConfigInitKwargsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return CustomLLMConfigInitKwargsType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["CustomLLMConfigInitKwargsType0", None, Unset], data)

        init_kwargs = _parse_init_kwargs(d.pop("init_kwargs", UNSET))

        custom_llm_config = cls(file_name=file_name, class_name=class_name, init_kwargs=init_kwargs)

        custom_llm_config.additional_properties = d
        return custom_llm_config

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
