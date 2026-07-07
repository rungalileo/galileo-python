import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.input_type_enum import InputTypeEnum
from ..models.model_type import ModelType
from ..models.multimodal_capability import MultimodalCapability
from ..models.output_type_enum import OutputTypeEnum
from ..models.roll_up_method_display_options import RollUpMethodDisplayOptions
from ..models.scorer_types import ScorerTypes
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_metric_roll_up_config_db import BaseMetricRollUpConfigDB
    from ..models.base_scorer_version_db import BaseScorerVersionDB
    from ..models.metric_color_picker_boolean import MetricColorPickerBoolean
    from ..models.metric_color_picker_categorical import MetricColorPickerCategorical
    from ..models.metric_color_picker_multi_label import MetricColorPickerMultiLabel
    from ..models.metric_color_picker_numeric import MetricColorPickerNumeric
    from ..models.permission import Permission
    from ..models.scorer_defaults import ScorerDefaults
    from ..models.scorer_scope_project_ref import ScorerScopeProjectRef


T = TypeVar("T", bound="ScorerResponse")


@_attrs_define
class ScorerResponse:
    """
    Attributes:
        id (str):
        name (str):
        scorer_type (ScorerTypes):
        tags (list[str]):
        permissions (Union[Unset, list['Permission']]):
        defaults (Union['ScorerDefaults', None, Unset]):
        latest_version (Union['BaseScorerVersionDB', None, Unset]):
        model_type (Union[ModelType, None, Unset]):
        ground_truth (Union[None, Unset, bool]):
        default_version_id (Union[None, Unset, str]):
        default_version (Union['BaseScorerVersionDB', None, Unset]):
        user_prompt (Union[None, Unset, str]):
        scoreable_node_types (Union[None, Unset, list[str]]):
        output_type (Union[None, OutputTypeEnum, Unset]):
        input_type (Union[InputTypeEnum, None, Unset]):
        multimodal_capabilities (Union[None, Unset, list[MultimodalCapability]]):
        required_scorers (Union[None, Unset, list[str]]):
        required_metric_ids (Union[None, Unset, list[str]]):
        deprecated (Union[None, Unset, bool]):
        roll_up_method (Union[None, RollUpMethodDisplayOptions, Unset]):
        roll_up_config (Union['BaseMetricRollUpConfigDB', None, Unset]):
        label (Union[None, Unset, str]):  Default: ''.
        included_fields (Union[Unset, list[str]]): Fields that can be used in the scorer to configure it. i.e. model,
            num_judges, etc. This enables the ui to know which fields a user can configure when they're setting a scorer
        description (Union[None, Unset, str]):
        created_by (Union[None, Unset, str]):
        created_at (Union[None, Unset, datetime.datetime]):
        updated_at (Union[None, Unset, datetime.datetime]):
        metric_color_picker_config (Union['MetricColorPickerBoolean', 'MetricColorPickerCategorical',
            'MetricColorPickerMultiLabel', 'MetricColorPickerNumeric', None, Unset]):
        color_threshold_config (Union['MetricColorPickerNumeric', None, Unset]):
        metric_name (Union[None, Unset, str]):
        is_global (Union[Unset, bool]):  Default: False.
        scope_projects (Union[Unset, list['ScorerScopeProjectRef']]):
    """

    id: str
    name: str
    scorer_type: ScorerTypes
    tags: list[str]
    permissions: Union[Unset, list["Permission"]] = UNSET
    defaults: Union["ScorerDefaults", None, Unset] = UNSET
    latest_version: Union["BaseScorerVersionDB", None, Unset] = UNSET
    model_type: Union[ModelType, None, Unset] = UNSET
    ground_truth: Union[None, Unset, bool] = UNSET
    default_version_id: Union[None, Unset, str] = UNSET
    default_version: Union["BaseScorerVersionDB", None, Unset] = UNSET
    user_prompt: Union[None, Unset, str] = UNSET
    scoreable_node_types: Union[None, Unset, list[str]] = UNSET
    output_type: Union[None, OutputTypeEnum, Unset] = UNSET
    input_type: Union[InputTypeEnum, None, Unset] = UNSET
    multimodal_capabilities: Union[None, Unset, list[MultimodalCapability]] = UNSET
    required_scorers: Union[None, Unset, list[str]] = UNSET
    required_metric_ids: Union[None, Unset, list[str]] = UNSET
    deprecated: Union[None, Unset, bool] = UNSET
    roll_up_method: Union[None, RollUpMethodDisplayOptions, Unset] = UNSET
    roll_up_config: Union["BaseMetricRollUpConfigDB", None, Unset] = UNSET
    label: Union[None, Unset, str] = ""
    included_fields: Union[Unset, list[str]] = UNSET
    description: Union[None, Unset, str] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    metric_color_picker_config: Union[
        "MetricColorPickerBoolean",
        "MetricColorPickerCategorical",
        "MetricColorPickerMultiLabel",
        "MetricColorPickerNumeric",
        None,
        Unset,
    ] = UNSET
    color_threshold_config: Union["MetricColorPickerNumeric", None, Unset] = UNSET
    metric_name: Union[None, Unset, str] = UNSET
    is_global: Union[Unset, bool] = False
    scope_projects: Union[Unset, list["ScorerScopeProjectRef"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_metric_roll_up_config_db import BaseMetricRollUpConfigDB
        from ..models.base_scorer_version_db import BaseScorerVersionDB
        from ..models.metric_color_picker_boolean import MetricColorPickerBoolean
        from ..models.metric_color_picker_categorical import MetricColorPickerCategorical
        from ..models.metric_color_picker_multi_label import MetricColorPickerMultiLabel
        from ..models.metric_color_picker_numeric import MetricColorPickerNumeric
        from ..models.scorer_defaults import ScorerDefaults

        id = self.id

        name = self.name

        scorer_type = self.scorer_type.value

        tags = self.tags

        permissions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = []
            for permissions_item_data in self.permissions:
                permissions_item = permissions_item_data.to_dict()
                permissions.append(permissions_item)

        defaults: Union[None, Unset, dict[str, Any]]
        if isinstance(self.defaults, Unset):
            defaults = UNSET
        elif isinstance(self.defaults, ScorerDefaults):
            defaults = self.defaults.to_dict()
        else:
            defaults = self.defaults

        latest_version: Union[None, Unset, dict[str, Any]]
        if isinstance(self.latest_version, Unset):
            latest_version = UNSET
        elif isinstance(self.latest_version, BaseScorerVersionDB):
            latest_version = self.latest_version.to_dict()
        else:
            latest_version = self.latest_version

        model_type: Union[None, Unset, str]
        if isinstance(self.model_type, Unset):
            model_type = UNSET
        elif isinstance(self.model_type, ModelType):
            model_type = self.model_type.value
        else:
            model_type = self.model_type

        ground_truth: Union[None, Unset, bool]
        if isinstance(self.ground_truth, Unset):
            ground_truth = UNSET
        else:
            ground_truth = self.ground_truth

        default_version_id: Union[None, Unset, str]
        if isinstance(self.default_version_id, Unset):
            default_version_id = UNSET
        else:
            default_version_id = self.default_version_id

        default_version: Union[None, Unset, dict[str, Any]]
        if isinstance(self.default_version, Unset):
            default_version = UNSET
        elif isinstance(self.default_version, BaseScorerVersionDB):
            default_version = self.default_version.to_dict()
        else:
            default_version = self.default_version

        user_prompt: Union[None, Unset, str]
        if isinstance(self.user_prompt, Unset):
            user_prompt = UNSET
        else:
            user_prompt = self.user_prompt

        scoreable_node_types: Union[None, Unset, list[str]]
        if isinstance(self.scoreable_node_types, Unset):
            scoreable_node_types = UNSET
        elif isinstance(self.scoreable_node_types, list):
            scoreable_node_types = self.scoreable_node_types

        else:
            scoreable_node_types = self.scoreable_node_types

        output_type: Union[None, Unset, str]
        if isinstance(self.output_type, Unset):
            output_type = UNSET
        elif isinstance(self.output_type, OutputTypeEnum):
            output_type = self.output_type.value
        else:
            output_type = self.output_type

        input_type: Union[None, Unset, str]
        if isinstance(self.input_type, Unset):
            input_type = UNSET
        elif isinstance(self.input_type, InputTypeEnum):
            input_type = self.input_type.value
        else:
            input_type = self.input_type

        multimodal_capabilities: Union[None, Unset, list[str]]
        if isinstance(self.multimodal_capabilities, Unset):
            multimodal_capabilities = UNSET
        elif isinstance(self.multimodal_capabilities, list):
            multimodal_capabilities = []
            for multimodal_capabilities_type_0_item_data in self.multimodal_capabilities:
                multimodal_capabilities_type_0_item = multimodal_capabilities_type_0_item_data.value
                multimodal_capabilities.append(multimodal_capabilities_type_0_item)

        else:
            multimodal_capabilities = self.multimodal_capabilities

        required_scorers: Union[None, Unset, list[str]]
        if isinstance(self.required_scorers, Unset):
            required_scorers = UNSET
        elif isinstance(self.required_scorers, list):
            required_scorers = self.required_scorers

        else:
            required_scorers = self.required_scorers

        required_metric_ids: Union[None, Unset, list[str]]
        if isinstance(self.required_metric_ids, Unset):
            required_metric_ids = UNSET
        elif isinstance(self.required_metric_ids, list):
            required_metric_ids = self.required_metric_ids

        else:
            required_metric_ids = self.required_metric_ids

        deprecated: Union[None, Unset, bool]
        if isinstance(self.deprecated, Unset):
            deprecated = UNSET
        else:
            deprecated = self.deprecated

        roll_up_method: Union[None, Unset, str]
        if isinstance(self.roll_up_method, Unset):
            roll_up_method = UNSET
        elif isinstance(self.roll_up_method, RollUpMethodDisplayOptions):
            roll_up_method = self.roll_up_method.value
        else:
            roll_up_method = self.roll_up_method

        roll_up_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.roll_up_config, Unset):
            roll_up_config = UNSET
        elif isinstance(self.roll_up_config, BaseMetricRollUpConfigDB):
            roll_up_config = self.roll_up_config.to_dict()
        else:
            roll_up_config = self.roll_up_config

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        included_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.included_fields, Unset):
            included_fields = self.included_fields

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        metric_color_picker_config: Union[None, Unset, dict[str, Any]]
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

        color_threshold_config: Union[None, Unset, dict[str, Any]]
        if isinstance(self.color_threshold_config, Unset):
            color_threshold_config = UNSET
        elif isinstance(self.color_threshold_config, MetricColorPickerNumeric):
            color_threshold_config = self.color_threshold_config.to_dict()
        else:
            color_threshold_config = self.color_threshold_config

        metric_name: Union[None, Unset, str]
        if isinstance(self.metric_name, Unset):
            metric_name = UNSET
        else:
            metric_name = self.metric_name

        is_global = self.is_global

        scope_projects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.scope_projects, Unset):
            scope_projects = []
            for scope_projects_item_data in self.scope_projects:
                scope_projects_item = scope_projects_item_data.to_dict()
                scope_projects.append(scope_projects_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "name": name, "scorer_type": scorer_type, "tags": tags})
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if defaults is not UNSET:
            field_dict["defaults"] = defaults
        if latest_version is not UNSET:
            field_dict["latest_version"] = latest_version
        if model_type is not UNSET:
            field_dict["model_type"] = model_type
        if ground_truth is not UNSET:
            field_dict["ground_truth"] = ground_truth
        if default_version_id is not UNSET:
            field_dict["default_version_id"] = default_version_id
        if default_version is not UNSET:
            field_dict["default_version"] = default_version
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
        if required_metric_ids is not UNSET:
            field_dict["required_metric_ids"] = required_metric_ids
        if deprecated is not UNSET:
            field_dict["deprecated"] = deprecated
        if roll_up_method is not UNSET:
            field_dict["roll_up_method"] = roll_up_method
        if roll_up_config is not UNSET:
            field_dict["roll_up_config"] = roll_up_config
        if label is not UNSET:
            field_dict["label"] = label
        if included_fields is not UNSET:
            field_dict["included_fields"] = included_fields
        if description is not UNSET:
            field_dict["description"] = description
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if metric_color_picker_config is not UNSET:
            field_dict["metric_color_picker_config"] = metric_color_picker_config
        if color_threshold_config is not UNSET:
            field_dict["color_threshold_config"] = color_threshold_config
        if metric_name is not UNSET:
            field_dict["metric_name"] = metric_name
        if is_global is not UNSET:
            field_dict["is_global"] = is_global
        if scope_projects is not UNSET:
            field_dict["scope_projects"] = scope_projects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_metric_roll_up_config_db import BaseMetricRollUpConfigDB
        from ..models.base_scorer_version_db import BaseScorerVersionDB
        from ..models.metric_color_picker_boolean import MetricColorPickerBoolean
        from ..models.metric_color_picker_categorical import MetricColorPickerCategorical
        from ..models.metric_color_picker_multi_label import MetricColorPickerMultiLabel
        from ..models.metric_color_picker_numeric import MetricColorPickerNumeric
        from ..models.permission import Permission
        from ..models.scorer_defaults import ScorerDefaults
        from ..models.scorer_scope_project_ref import ScorerScopeProjectRef

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        scorer_type = ScorerTypes(d.pop("scorer_type"))

        tags = cast(list[str], d.pop("tags"))

        permissions = []
        _permissions = d.pop("permissions", UNSET)
        for permissions_item_data in _permissions or []:
            permissions_item = Permission.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        def _parse_defaults(data: object) -> Union["ScorerDefaults", None, Unset]:
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
            return cast(Union["ScorerDefaults", None, Unset], data)

        defaults = _parse_defaults(d.pop("defaults", UNSET))

        def _parse_latest_version(data: object) -> Union["BaseScorerVersionDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_version_type_0 = BaseScorerVersionDB.from_dict(data)

                return latest_version_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseScorerVersionDB", None, Unset], data)

        latest_version = _parse_latest_version(d.pop("latest_version", UNSET))

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

        def _parse_ground_truth(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        ground_truth = _parse_ground_truth(d.pop("ground_truth", UNSET))

        def _parse_default_version_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        default_version_id = _parse_default_version_id(d.pop("default_version_id", UNSET))

        def _parse_default_version(data: object) -> Union["BaseScorerVersionDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                default_version_type_0 = BaseScorerVersionDB.from_dict(data)

                return default_version_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseScorerVersionDB", None, Unset], data)

        default_version = _parse_default_version(d.pop("default_version", UNSET))

        def _parse_user_prompt(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_prompt = _parse_user_prompt(d.pop("user_prompt", UNSET))

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

        def _parse_output_type(data: object) -> Union[None, OutputTypeEnum, Unset]:
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
            return cast(Union[None, OutputTypeEnum, Unset], data)

        output_type = _parse_output_type(d.pop("output_type", UNSET))

        def _parse_input_type(data: object) -> Union[InputTypeEnum, None, Unset]:
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
            return cast(Union[InputTypeEnum, None, Unset], data)

        input_type = _parse_input_type(d.pop("input_type", UNSET))

        def _parse_multimodal_capabilities(data: object) -> Union[None, Unset, list[MultimodalCapability]]:
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
            return cast(Union[None, Unset, list[MultimodalCapability]], data)

        multimodal_capabilities = _parse_multimodal_capabilities(d.pop("multimodal_capabilities", UNSET))

        def _parse_required_scorers(data: object) -> Union[None, Unset, list[str]]:
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
            return cast(Union[None, Unset, list[str]], data)

        required_scorers = _parse_required_scorers(d.pop("required_scorers", UNSET))

        def _parse_required_metric_ids(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                required_metric_ids_type_0 = cast(list[str], data)

                return required_metric_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        required_metric_ids = _parse_required_metric_ids(d.pop("required_metric_ids", UNSET))

        def _parse_deprecated(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        deprecated = _parse_deprecated(d.pop("deprecated", UNSET))

        def _parse_roll_up_method(data: object) -> Union[None, RollUpMethodDisplayOptions, Unset]:
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
            return cast(Union[None, RollUpMethodDisplayOptions, Unset], data)

        roll_up_method = _parse_roll_up_method(d.pop("roll_up_method", UNSET))

        def _parse_roll_up_config(data: object) -> Union["BaseMetricRollUpConfigDB", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                roll_up_config_type_0 = BaseMetricRollUpConfigDB.from_dict(data)

                return roll_up_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["BaseMetricRollUpConfigDB", None, Unset], data)

        roll_up_config = _parse_roll_up_config(d.pop("roll_up_config", UNSET))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        included_fields = cast(list[str], d.pop("included_fields", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        def _parse_metric_color_picker_config(
            data: object,
        ) -> Union[
            "MetricColorPickerBoolean",
            "MetricColorPickerCategorical",
            "MetricColorPickerMultiLabel",
            "MetricColorPickerNumeric",
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
                Union[
                    "MetricColorPickerBoolean",
                    "MetricColorPickerCategorical",
                    "MetricColorPickerMultiLabel",
                    "MetricColorPickerNumeric",
                    None,
                    Unset,
                ],
                data,
            )

        metric_color_picker_config = _parse_metric_color_picker_config(d.pop("metric_color_picker_config", UNSET))

        def _parse_color_threshold_config(data: object) -> Union["MetricColorPickerNumeric", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                color_threshold_config_type_0 = MetricColorPickerNumeric.from_dict(data)

                return color_threshold_config_type_0
            except:  # noqa: E722
                pass
            return cast(Union["MetricColorPickerNumeric", None, Unset], data)

        color_threshold_config = _parse_color_threshold_config(d.pop("color_threshold_config", UNSET))

        def _parse_metric_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metric_name = _parse_metric_name(d.pop("metric_name", UNSET))

        is_global = d.pop("is_global", UNSET)

        scope_projects = []
        _scope_projects = d.pop("scope_projects", UNSET)
        for scope_projects_item_data in _scope_projects or []:
            scope_projects_item = ScorerScopeProjectRef.from_dict(scope_projects_item_data)

            scope_projects.append(scope_projects_item)

        scorer_response = cls(
            id=id,
            name=name,
            scorer_type=scorer_type,
            tags=tags,
            permissions=permissions,
            defaults=defaults,
            latest_version=latest_version,
            model_type=model_type,
            ground_truth=ground_truth,
            default_version_id=default_version_id,
            default_version=default_version,
            user_prompt=user_prompt,
            scoreable_node_types=scoreable_node_types,
            output_type=output_type,
            input_type=input_type,
            multimodal_capabilities=multimodal_capabilities,
            required_scorers=required_scorers,
            required_metric_ids=required_metric_ids,
            deprecated=deprecated,
            roll_up_method=roll_up_method,
            roll_up_config=roll_up_config,
            label=label,
            included_fields=included_fields,
            description=description,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
            metric_color_picker_config=metric_color_picker_config,
            color_threshold_config=color_threshold_config,
            metric_name=metric_name,
            is_global=is_global,
            scope_projects=scope_projects,
        )

        scorer_response.additional_properties = d
        return scorer_response

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
