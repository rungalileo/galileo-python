from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.column_mapping_config import ColumnMappingConfig


T = TypeVar("T", bound="ColumnMapping")


@_attrs_define
class ColumnMapping:
    """
    Attributes:
        input_ (Union['ColumnMappingConfig', None, list[str]]):
        metadata (Union['ColumnMappingConfig', None, list[str]]):
        output (Union['ColumnMappingConfig', None, list[str]]):
    """

    input_: Union["ColumnMappingConfig", None, list[str]]
    metadata: Union["ColumnMappingConfig", None, list[str]]
    output: Union["ColumnMappingConfig", None, list[str]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.column_mapping_config import ColumnMappingConfig

        input_: Union[None, dict[str, Any], list[str]]
        if isinstance(self.input_, ColumnMappingConfig):
            input_ = self.input_.to_dict()
        elif isinstance(self.input_, list):
            input_ = self.input_

        else:
            input_ = self.input_

        metadata: Union[None, dict[str, Any], list[str]]
        if isinstance(self.metadata, ColumnMappingConfig):
            metadata = self.metadata.to_dict()
        elif isinstance(self.metadata, list):
            metadata = self.metadata

        else:
            metadata = self.metadata

        output: Union[None, dict[str, Any], list[str]]
        if isinstance(self.output, ColumnMappingConfig):
            output = self.output.to_dict()
        elif isinstance(self.output, list):
            output = self.output

        else:
            output = self.output

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"input": input_, "metadata": metadata, "output": output})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.column_mapping_config import ColumnMappingConfig

        d = dict(src_dict)

        def _parse_input_(data: object) -> Union["ColumnMappingConfig", None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_type_0 = ColumnMappingConfig.from_dict(data)

                return input_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                input_type_1 = cast(list[str], data)

                return input_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ColumnMappingConfig", None, list[str]], data)

        input_ = _parse_input_(d.pop("input"))

        def _parse_metadata(data: object) -> Union["ColumnMappingConfig", None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ColumnMappingConfig.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                metadata_type_1 = cast(list[str], data)

                return metadata_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ColumnMappingConfig", None, list[str]], data)

        metadata = _parse_metadata(d.pop("metadata"))

        def _parse_output(data: object) -> Union["ColumnMappingConfig", None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                output_type_0 = ColumnMappingConfig.from_dict(data)

                return output_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_type_1 = cast(list[str], data)

                return output_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ColumnMappingConfig", None, list[str]], data)

        output = _parse_output(d.pop("output"))

        column_mapping = cls(input_=input_, metadata=metadata, output=output)

        column_mapping.additional_properties = d
        return column_mapping

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
