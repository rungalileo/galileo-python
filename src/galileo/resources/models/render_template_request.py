from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dataset_data import DatasetData
    from ..models.string_data import StringData


T = TypeVar("T", bound="RenderTemplateRequest")


@_attrs_define
class RenderTemplateRequest:
    """
    Attributes:
        data (Union['DatasetData', 'StringData']):
        template (str):
    """

    data: Union["DatasetData", "StringData"]
    template: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.dataset_data import DatasetData

        data: dict[str, Any]
        if isinstance(self.data, DatasetData):
            data = self.data.to_dict()
        else:
            data = self.data.to_dict()

        template = self.template

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"data": data, "template": template})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dataset_data import DatasetData
        from ..models.string_data import StringData

        d = dict(src_dict)

        def _parse_data(data: object) -> Union["DatasetData", "StringData"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                data_type_0 = DatasetData.from_dict(data)

                return data_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            data_type_1 = StringData.from_dict(data)

            return data_type_1

        data = _parse_data(d.pop("data"))

        template = d.pop("template")

        render_template_request = cls(data=data, template=template)

        render_template_request.additional_properties = d
        return render_template_request

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
