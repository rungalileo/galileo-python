from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.model_type import ModelType
from ..models.scorer_input_type import ScorerInputType
from ..models.scorer_types import ScorerTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_scorer_version_db import BaseScorerVersionDB
    from ..models.metadata_filter import MetadataFilter
    from ..models.node_name_filter import NodeNameFilter


T = TypeVar("T", bound="ScorerConfig")


@_attrs_define
class ScorerConfig:
    """Used for configuring a scorer for a scorer job.

    Attributes:
        id (str):
        scorer_type (ScorerTypes):
        filters (Union[None, Unset, list[Union['MetadataFilter', 'NodeNameFilter']]]): List of filters to apply to the
            scorer.
        input_type (Union[None, ScorerInputType, Unset]): Type of input that this scorer accepts. Defaults to
            ScorerInputType.basic. Default: ScorerInputType.BASIC.
        model_name (Union[None, Unset, str]):
        model_type (Union[ModelType, None, Unset]): Type of model to use for this scorer. slm maps to luna, and llm maps
            to plus
        name (Union[None, Unset, str]):
        num_judges (Union[None, Unset, int]):
        scoreable_node_types (Union[None, Unset, list[str]]): List of node types that can be scored by this scorer.
            Defaults to llm/chat.
        scorer_version (Union['BaseScorerVersionDB', None, Unset]): ScorerVersion to use for this scorer. If not
            provided, the latest version will be used.
    """

    id: str
    scorer_type: ScorerTypes
    filters: Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]] = UNSET
    input_type: Union[None, ScorerInputType, Unset] = ScorerInputType.BASIC
    model_name: Union[None, Unset, str] = UNSET
    model_type: Union[ModelType, None, Unset] = UNSET
    name: Union[None, Unset, str] = UNSET
    num_judges: Union[None, Unset, int] = UNSET
    scoreable_node_types: Union[None, Unset, list[str]] = UNSET
    scorer_version: Union["BaseScorerVersionDB", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_scorer_version_db import BaseScorerVersionDB
        from ..models.node_name_filter import NodeNameFilter

        id = self.id

        scorer_type = self.scorer_type.value

        filters: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.filters, Unset):
            filters = UNSET
        elif isinstance(self.filters, list):
            filters = []
            for filters_type_0_item_data in self.filters:
                filters_type_0_item: dict[str, Any]
                if isinstance(filters_type_0_item_data, NodeNameFilter):
                    filters_type_0_item = filters_type_0_item_data.to_dict()
                else:
                    filters_type_0_item = filters_type_0_item_data.to_dict()

                filters.append(filters_type_0_item)

        else:
            filters = self.filters

        input_type: Union[None, Unset, str]
        if isinstance(self.input_type, Unset):
            input_type = UNSET
        elif isinstance(self.input_type, ScorerInputType):
            input_type = self.input_type.value
        else:
            input_type = self.input_type

        model_name: Union[None, Unset, str]
        if isinstance(self.model_name, Unset):
            model_name = UNSET
        else:
            model_name = self.model_name

        model_type: Union[None, Unset, str]
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        name: Union[None, Unset, str]
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        num_judges: Union[None, Unset, int]
        if isinstance(self.num_judges, Unset):
            num_judges = UNSET
        else:
            num_judges = self.num_judges

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        scorer_version: Union[None, Unset, dict[str, Any]]
        if isinstance(self.scorer_version, Unset):
            scorer_version = UNSET
        elif isinstance(self.scorer_version, BaseScorerVersionDB):
            scorer_version = self.scorer_version.to_dict()
        else:
            scorer_version = self.scorer_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "scorer_type": scorer_type})
        if filters is not UNSET:
            field_dict["filters"] = filters
        if input_type is not UNSET:
            field_dict["input_type"] = input_type
        if model_name is not UNSET:
            field_dict["model_name"] = model_name
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if name is not UNSET:
            field_dict["name"] = name
        if num_judges is not UNSET:
            field_dict["num_judges"] = num_judges
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if scorer_version is not UNSET:
            field_dict["scorer_version"] = scorer_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_scorer_version_db import BaseScorerVersionDB
        from ..models.metadata_filter import MetadataFilter
        from ..models.node_name_filter import NodeNameFilter

        d = dict(src_dict)
        id = d.pop("id")

        scorer_type = ScorerTypes(d.pop("scorer_type"))

        def _parse_filters(data: object) -> Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                filters_type_0 = []
                _filters_type_0 = data
                for filters_type_0_item_data in _filters_type_0:

                    def _parse_filters_type_0_item(data: object) -> Union["MetadataFilter", "NodeNameFilter"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            filters_type_0_item_type_0 = NodeNameFilter.from_dict(data)

                            return filters_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        filters_type_0_item_type_1 = MetadataFilter.from_dict(data)

                        return filters_type_0_item_type_1

                    filters_type_0_item = _parse_filters_type_0_item(filters_type_0_item_data)

                    filters_type_0.append(filters_type_0_item)

                return filters_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[Union["MetadataFilter", "NodeNameFilter"]]], data)

        filters = _parse_filters(d.pop("filters", UNSET))

        def _parse_input_type(data: object) -> Union[None, ScorerInputType, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                input_type_type_0 = ScorerInputType(data)

                return input_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, ScorerInputType, Unset], data)

        input_type = _parse_input_type(d.pop("input_type", UNSET))

        def _parse_model_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        model_name = _parse_model_name(d.pop("model_name", UNSET))

        def _parse_model_type(data: object) -> Union[ModelType, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                model_type_type_0 = ModelType(data)

                return model_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[ModelType, None, Unset], data)

        model_type = _parse_model_type(d.pop("model_type", UNSET))

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_num_judges(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        num_judges = _parse_num_judges(d.pop("num_judges", UNSET))

        def _parse_scoreable_node_types(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                scoreable_node_types_type_0 = cast(list[str], data)

                return scoreable_node_types_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        def _parse_scorer_version(data: object) -> Union["BaseScorerVersionDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                scorer_version_type_0 = BaseScorerVersionDB.from_dict(data)

                return scorer_version_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseScorerVersionDB", None, Unset], data)

        scorer_version = _parse_scorer_version(d.pop("scorer_version", UNSET))

        scorer_config = cls(
            id=id,
            scorer_type=scorer_type,
            filters=filters,
            input_type=input_type,
            model_name=model_name,
            model_type=model_type,
            name=name,
            num_judges=num_judges,
            scoreable_node_types=scoreable_node_types,
            scorer_version=scorer_version,
        )

        scorer_config.additional_properties = d
        return scorer_config

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
