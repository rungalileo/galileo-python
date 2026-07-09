from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.input_type_enum import InputTypeEnum
from ..models.model_type import ModelType
from ..models.multimodal_capability import MultimodalCapability
from ..models.output_type_enum import OutputTypeEnum
from ..models.roll_up_method_display_options import RollUpMethodDisplayOptions
from ..models.scorer_types import ScorerTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_color_picker_boolean import MetricColorPickerBoolean
    from ..models.metric_color_picker_categorical import MetricColorPickerCategorical
    from ..models.metric_color_picker_multi_label import MetricColorPickerMultiLabel
    from ..models.metric_color_picker_numeric import MetricColorPickerNumeric
    from ..models.scorer_defaults import ScorerDefaults


T = TypeVar("T", bound="CreateScorerRequest")


@_attrs_define
class CreateScorerRequest:
    """
    Attributes:
        name (str):
        scorer_type (ScorerTypes):
        description (str | Unset):  Default: ''.
        tags (list[str] | Unset):
        defaults (None | ScorerDefaults | Unset):
        deprecated (bool | None | Unset):
        model_type (ModelType | None | Unset):
        ground_truth (bool | None | Unset):
        default_version_id (None | str | Unset):
        user_prompt (None | str | Unset):
        scoreable_node_types (list[str] | None | Unset):
        output_type (None | OutputTypeEnum | Unset):
        input_type (InputTypeEnum | None | Unset):
        multimodal_capabilities (list[MultimodalCapability] | None | Unset):
        required_scorers (list[str] | None | Unset):
        roll_up_method (None | RollUpMethodDisplayOptions | Unset):
        metric_color_picker_config (MetricColorPickerBoolean | MetricColorPickerCategorical |
            MetricColorPickerMultiLabel | MetricColorPickerNumeric | None | Unset):
    """

    name: str
    scorer_type: ScorerTypes
    description: str | Unset = ""
    tags: list[str] | Unset = UNSET
    defaults: None | ScorerDefaults | Unset = UNSET
    deprecated: bool | None | Unset = UNSET
    model_type: ModelType | None | Unset = UNSET
    ground_truth: bool | None | Unset = UNSET
    default_version_id: None | str | Unset = UNSET
    user_prompt: None | str | Unset = UNSET
    scoreable_node_types: list[str] | None | Unset = UNSET
    output_type: None | OutputTypeEnum | Unset = UNSET
    input_type: InputTypeEnum | None | Unset = UNSET
    multimodal_capabilities: list[MultimodalCapability] | None | Unset = UNSET
    required_scorers: list[str] | None | Unset = UNSET
    roll_up_method: None | RollUpMethodDisplayOptions | Unset = UNSET
    metric_color_picker_config: (
        MetricColorPickerBoolean
        | MetricColorPickerCategorical
        | MetricColorPickerMultiLabel
        | MetricColorPickerNumeric
        | None
        | Unset
    ) = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.metric_color_picker_boolean import MetricColorPickerBoolean
        from ..models.metric_color_picker_categorical import MetricColorPickerCategorical
        from ..models.metric_color_picker_multi_label import MetricColorPickerMultiLabel
        from ..models.metric_color_picker_numeric import MetricColorPickerNumeric
        from ..models.scorer_defaults import ScorerDefaults

        name = self.name

        scorer_type = self.scorer_type.value

        description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        defaults: dict[str, Any] | None | Unset
        if isinstance(self.defaults, Unset):
            defaults = UNSET
        elif isinstance(self.defaults, ScorerDefaults):
            defaults = self.defaults.to_dict()
        else:
            defaults = self.defaults

        deprecated: bool | None | Unset
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        model_type: None | str | Unset
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        ground_truth: bool | None | Unset
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        default_version_id: None | str | Unset
        if isinstance(self.default_version_id, Unset):
            default_version_id = UNSET
        else:
            default_version_id = self.default_version_id

        user_prompt: None | str | Unset
        if isinstance(self.user_prompt, Unset):
            user_prompt = UNSET
        else:
            user_prompt = self.user_prompt

        scoreable_node_types: list[str] | None | Unset
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        output_type: None | str | Unset
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, OutputTypeEnum):
            output_type = self.output_type.value
        else:
            output_type = self.output_type

        input_type: None | str | Unset
        if isinstance(self.input_type, Unset):
            input_type = UNSET
        elif isinstance(self.input_type, InputTypeEnum):
            input_type = self.input_type.value
        else:
            input_type = self.input_type

        multimodal_capabilities: list[str] | None | Unset
        if isinstance(self.multimodal_capabilities, Unset):
            multimodal_capabilities = UNSET
        elif isinstance(self.multimodal_capabilities, list):
            multimodal_capabilities = []
            for multimodal_capabilities_type_0_item_data in self.multimodal_capabilities:
                multimodal_capabilities_type_0_item = multimodal_capabilities_type_0_item_data.value
                multimodal_capabilities.append(multimodal_capabilities_type_0_item)

        else:
            multimodal_capabilities = self.multimodal_capabilities

        required_scorers: list[str] | None | Unset
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        roll_up_method: None | str | Unset
        if isinstance(self.roll_up_method, Unset):
            roll_up_method = UNSET
        elif isinstance(self.roll_up_method, RollUpMethodDisplayOptions):
            roll_up_method = self.roll_up_method.value
        else:
            roll_up_method = self.roll_up_method

        metric_color_picker_config: dict[str, Any] | None | Unset
        if isinstance(self.metric_color_picker_config, Unset):
            metric_color_picker_config = UNSET
        elif isinstance(self.metric_color_picker_config, MetricColorPickerNumeric):
            metric_color_picker_config = self.metric_color_picker_config.to_dict()
        elif isinstance(self.metric_color_picker_config, MetricColorPickerBoolean):
            metric_color_picker_config = self.metric_color_picker_config.to_dict()
        elif isinstance(self.metric_color_picker_config, MetricColorPickerCategorical):
            metric_color_picker_config = self.metric_color_picker_config.to_dict()
        elif isinstance(self.metric_color_picker_config, MetricColorPickerMultiLabel):
            metric_color_picker_config = self.metric_color_picker_config.to_dict()
        else:
            metric_color_picker_config = self.metric_color_picker_config

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"name": name, "scorer_type": scorer_type})
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if default_version_id is not UNSET:
            field_dict["default_version_id"] = default_version_id
        if user_prompt is not UNSET:
            field_dict["user_prompt"] = user_prompt
        if scoreable_node_types is not UNSET:
            field_dict["scoreable_node_types"] = scoreable_node_types
        if output_type is not UNSET:
            field_dict["output_type"] = output_type
        if input_type is not UNSET:
            field_dict["input_type"] = input_type
        if multimodal_capabilities is not UNSET:
            field_dict["multimodal_capabilities"] = multimodal_capabilities
        if required_scorers is not UNSET:
            field_dict["required_scorers"] = required_scorers
        if roll_up_method is not UNSET:
            field_dict["roll_up_method"] = roll_up_method
        if metric_color_picker_config is not UNSET:
            field_dict["metric_color_picker_config"] = metric_color_picker_config

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_color_picker_boolean import MetricColorPickerBoolean
        from ..models.metric_color_picker_categorical import MetricColorPickerCategorical
        from ..models.metric_color_picker_multi_label import MetricColorPickerMultiLabel
        from ..models.metric_color_picker_numeric import MetricColorPickerNumeric
        from ..models.scorer_defaults import ScorerDefaults

        d = dict(src_dict)
        name = d.pop("name")

        scorer_type = ScorerTypes(d.pop("scorer_type"))

        description = d.pop("description", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_defaults(data: object) -> None | ScorerDefaults | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                defaults_type_0 = ScorerDefaults.from_dict(data)

                return defaults_type_0
            except:  # noqa: E722
                pass
            return cast(None | ScorerDefaults | Unset, data)

        defaults = _parse_defaults(d.pop("defaults", UNSET))

        def _parse_deprecated(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        def _parse_model_type(data: object) -> ModelType | None | Unset:
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
            return cast(ModelType | None | Unset, data)

        model_type = _parse_model_type(d.pop("model_type", UNSET))

        def _parse_ground_truth(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_default_version_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        default_version_id = _parse_default_version_id(d.pop("default_version_id", UNSET))

        def _parse_user_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

        def _parse_scoreable_node_types(data: object) -> list[str] | None | Unset:
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
            return cast(list[str] | None | Unset, data)

        scoreable_node_types = _parse_scoreable_node_types(d.pop("scoreable_node_types", UNSET))

        def _parse_output_type(data: object) -> None | OutputTypeEnum | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                output_type_type_0 = OutputTypeEnum(data)

                return output_type_type_0
            except:  # noqa: E722
                pass
            return cast(None | OutputTypeEnum | Unset, data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        def _parse_input_type(data: object) -> InputTypeEnum | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                input_type_type_0 = InputTypeEnum(data)

                return input_type_type_0
            except:  # noqa: E722
                pass
            return cast(InputTypeEnum | None | Unset, data)

        input_type = _parse_input_type(d.pop("input_type", UNSET))

        def _parse_multimodal_capabilities(data: object) -> list[MultimodalCapability] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                multimodal_capabilities_type_0 = []
                _multimodal_capabilities_type_0 = data
                for multimodal_capabilities_type_0_item_data in _multimodal_capabilities_type_0:
                    multimodal_capabilities_type_0_item = MultimodalCapability(multimodal_capabilities_type_0_item_data)

                    multimodal_capabilities_type_0.append(multimodal_capabilities_type_0_item)

                return multimodal_capabilities_type_0
            except:  # noqa: E722
                pass
            return cast(list[MultimodalCapability] | None | Unset, data)

        multimodal_capabilities = _parse_multimodal_capabilities(d.pop("multimodal_capabilities", UNSET))

        def _parse_required_scorers(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                required_scorers_type_0 = cast(list[str], data)

                return required_scorers_type_0
            except:  # noqa: E722
                pass
            return cast(list[str] | None | Unset, data)

        required_scorers = _parse_required_scorers(d.pop("required_scorers", UNSET))

        def _parse_roll_up_method(data: object) -> None | RollUpMethodDisplayOptions | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                roll_up_method_type_0 = RollUpMethodDisplayOptions(data)

                return roll_up_method_type_0
            except:  # noqa: E722
                pass
            return cast(None | RollUpMethodDisplayOptions | Unset, data)

        roll_up_method = _parse_roll_up_method(d.pop("roll_up_method", UNSET))

        def _parse_metric_color_picker_config(
            data: object,
        ) -> (
            MetricColorPickerBoolean
            | MetricColorPickerCategorical
            | MetricColorPickerMultiLabel
            | MetricColorPickerNumeric
            | None
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_color_picker_config_type_0_type_0 = MetricColorPickerNumeric.from_dict(data)

                return metric_color_picker_config_type_0_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_color_picker_config_type_0_type_1 = MetricColorPickerBoolean.from_dict(data)

                return metric_color_picker_config_type_0_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_color_picker_config_type_0_type_2 = MetricColorPickerCategorical.from_dict(data)

                return metric_color_picker_config_type_0_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metric_color_picker_config_type_0_type_3 = MetricColorPickerMultiLabel.from_dict(data)

                return metric_color_picker_config_type_0_type_3
            except:  # noqa: E722
                pass
            return cast(
                MetricColorPickerBoolean
                | MetricColorPickerCategorical
                | MetricColorPickerMultiLabel
                | MetricColorPickerNumeric
                | None
                | Unset,
                data,
            )

        metric_color_picker_config = _parse_metric_color_picker_config(d.pop("metric_color_picker_config", UNSET))

        create_scorer_request = cls(
            name=name,
            scorer_type=scorer_type,
            description=description,
            tags=tags,
            defaults=defaults,
            deprecated=deprecated,
            model_type=model_type,
            ground_truth=ground_truth,
            default_version_id=default_version_id,
            user_prompt=user_prompt,
            scoreable_node_types=scoreable_node_types,
            output_type=output_type,
            input_type=input_type,
            multimodal_capabilities=multimodal_capabilities,
            required_scorers=required_scorers,
            roll_up_method=roll_up_method,
            metric_color_picker_config=metric_color_picker_config,
        )

        create_scorer_request.additional_properties = d
        return create_scorer_request

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
