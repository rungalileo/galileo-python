from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.prompt_template_version_created_at_sort import PromptTemplateVersionCreatedAtSort
    from ..models.prompt_template_version_number_sort import PromptTemplateVersionNumberSort
    from ..models.prompt_template_version_updated_at_sort import PromptTemplateVersionUpdatedAtSort


T = TypeVar("T", bound="ListPromptTemplateVersionParams")


@_attrs_define
class ListPromptTemplateVersionParams:
    """
    Attributes:
        sort (Union['PromptTemplateVersionCreatedAtSort', 'PromptTemplateVersionNumberSort',
            'PromptTemplateVersionUpdatedAtSort', None, Unset]):
    """

    sort: Union[
        "PromptTemplateVersionCreatedAtSort",
        "PromptTemplateVersionNumberSort",
        "PromptTemplateVersionUpdatedAtSort",
        None,
        Unset,
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.prompt_template_version_created_at_sort import PromptTemplateVersionCreatedAtSort
        from ..models.prompt_template_version_number_sort import PromptTemplateVersionNumberSort
        from ..models.prompt_template_version_updated_at_sort import PromptTemplateVersionUpdatedAtSort

        sort: Union[None, Unset, dict[str, Any]]
        if isinstance(self.sort, Unset):
            sort = UNSET
        elif isinstance(self.sort, PromptTemplateVersionNumberSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, PromptTemplateVersionCreatedAtSort):
            sort = self.sort.to_dict()
        elif isinstance(self.sort, PromptTemplateVersionUpdatedAtSort):
            sort = self.sort.to_dict()
        else:
            sort = self.sort

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sort is not UNSET:
            field_dict["sort"] = sort

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.prompt_template_version_created_at_sort import PromptTemplateVersionCreatedAtSort
        from ..models.prompt_template_version_number_sort import PromptTemplateVersionNumberSort
        from ..models.prompt_template_version_updated_at_sort import PromptTemplateVersionUpdatedAtSort

        d = dict(src_dict)

        def _parse_sort(
            data: object,
        ) -> Union[
            "PromptTemplateVersionCreatedAtSort",
            "PromptTemplateVersionNumberSort",
            "PromptTemplateVersionUpdatedAtSort",
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_0 = PromptTemplateVersionNumberSort.from_dict(data)

                return sort_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_1 = PromptTemplateVersionCreatedAtSort.from_dict(data)

                return sort_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                sort_type_0_type_2 = PromptTemplateVersionUpdatedAtSort.from_dict(data)

                return sort_type_0_type_2
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "PromptTemplateVersionCreatedAtSort",
                    "PromptTemplateVersionNumberSort",
                    "PromptTemplateVersionUpdatedAtSort",
                    None,
                    Unset,
                ],
                data,
            )

        sort = _parse_sort(d.pop("sort", UNSET))

        list_prompt_template_version_params = cls(sort=sort)

        list_prompt_template_version_params.additional_properties = d
        return list_prompt_template_version_params

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
