from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.and_node_log_records_filter_output import AndNodeLogRecordsFilterOutput
    from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
    from ..models.not_node_log_records_filter_output import NotNodeLogRecordsFilterOutput
    from ..models.or_node_log_records_filter_output import OrNodeLogRecordsFilterOutput
    from ..models.section_response import SectionResponse
    from ..models.trends_dashboard_response_layout_map import TrendsDashboardResponseLayoutMap
    from ..models.widget_response import WidgetResponse


T = TypeVar("T", bound="TrendsDashboardResponse")


@_attrs_define
class TrendsDashboardResponse:
    """
    Attributes:
        id (str):
        log_stream_id (str):
        project_id (str):
        layout_map (TrendsDashboardResponseLayoutMap):
        interval_mins (int):
        start_time (int):
        end_time (int):
        widgets (list[WidgetResponse] | Unset):
        sections (list[SectionResponse] | Unset):
        group_by (None | str | Unset):
        filter_tree (AndNodeLogRecordsFilterOutput | FilterLeafLogRecordsFilter | None | NotNodeLogRecordsFilterOutput |
            OrNodeLogRecordsFilterOutput | Unset):
        relative_time (None | str | Unset):
    """

    id: str
    log_stream_id: str
    project_id: str
    layout_map: TrendsDashboardResponseLayoutMap
    interval_mins: int
    start_time: int
    end_time: int
    widgets: list[WidgetResponse] | Unset = UNSET
    sections: list[SectionResponse] | Unset = UNSET
    group_by: None | str | Unset = UNSET
    filter_tree: (
        AndNodeLogRecordsFilterOutput
        | FilterLeafLogRecordsFilter
        | None
        | NotNodeLogRecordsFilterOutput
        | OrNodeLogRecordsFilterOutput
        | Unset
    ) = UNSET
    relative_time: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.and_node_log_records_filter_output import AndNodeLogRecordsFilterOutput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter_output import NotNodeLogRecordsFilterOutput
        from ..models.or_node_log_records_filter_output import OrNodeLogRecordsFilterOutput

        id = self.id

        log_stream_id = self.log_stream_id

        project_id = self.project_id

        layout_map = self.layout_map.to_dict()

        interval_mins = self.interval_mins

        start_time = self.start_time

        end_time = self.end_time

        widgets: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.widgets, Unset):
            widgets = []
            for widgets_item_data in self.widgets:
                widgets_item = widgets_item_data.to_dict()
                widgets.append(widgets_item)

        sections: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.sections, Unset):
            sections = []
            for sections_item_data in self.sections:
                sections_item = sections_item_data.to_dict()
                sections.append(sections_item)

        group_by: None | str | Unset
        if isinstance(self.group_by, Unset):
            group_by = UNSET
        else:
            group_by = self.group_by

        filter_tree: dict[str, Any] | None | Unset
        if isinstance(self.filter_tree, Unset):
            filter_tree = UNSET
        elif isinstance(self.filter_tree, FilterLeafLogRecordsFilter):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, AndNodeLogRecordsFilterOutput):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, OrNodeLogRecordsFilterOutput):
            filter_tree = self.filter_tree.to_dict()
        elif isinstance(self.filter_tree, NotNodeLogRecordsFilterOutput):
            filter_tree = self.filter_tree.to_dict()
        else:
            filter_tree = self.filter_tree

        relative_time: None | str | Unset
        if isinstance(self.relative_time, Unset):
            relative_time = UNSET
        else:
            relative_time = self.relative_time

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "log_stream_id": log_stream_id,
                "project_id": project_id,
                "layout_map": layout_map,
                "interval_mins": interval_mins,
                "start_time": start_time,
                "end_time": end_time,
            }
        )
        if widgets is not UNSET:
            field_dict["widgets"] = widgets
        if sections is not UNSET:
            field_dict["sections"] = sections
        if group_by is not UNSET:
            field_dict["group_by"] = group_by
        if filter_tree is not UNSET:
            field_dict["filter_tree"] = filter_tree
        if relative_time is not UNSET:
            field_dict["relative_time"] = relative_time

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.and_node_log_records_filter_output import AndNodeLogRecordsFilterOutput
        from ..models.filter_leaf_log_records_filter import FilterLeafLogRecordsFilter
        from ..models.not_node_log_records_filter_output import NotNodeLogRecordsFilterOutput
        from ..models.or_node_log_records_filter_output import OrNodeLogRecordsFilterOutput
        from ..models.section_response import SectionResponse
        from ..models.trends_dashboard_response_layout_map import TrendsDashboardResponseLayoutMap
        from ..models.widget_response import WidgetResponse

        d = dict(src_dict)
        id = d.pop("id")

        log_stream_id = d.pop("log_stream_id")

        project_id = d.pop("project_id")

        layout_map = TrendsDashboardResponseLayoutMap.from_dict(d.pop("layout_map"))

        interval_mins = d.pop("interval_mins")

        start_time = d.pop("start_time")

        end_time = d.pop("end_time")

        _widgets = d.pop("widgets", UNSET)
        widgets: list[WidgetResponse] | Unset = UNSET
        if _widgets is not UNSET:
            widgets = []
            for widgets_item_data in _widgets:
                widgets_item = WidgetResponse.from_dict(widgets_item_data)

                widgets.append(widgets_item)

        _sections = d.pop("sections", UNSET)
        sections: list[SectionResponse] | Unset = UNSET
        if _sections is not UNSET:
            sections = []
            for sections_item_data in _sections:
                sections_item = SectionResponse.from_dict(sections_item_data)

                sections.append(sections_item)

        def _parse_group_by(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group_by = _parse_group_by(d.pop("group_by", UNSET))

        def _parse_filter_tree(
            data: object,
        ) -> (
            AndNodeLogRecordsFilterOutput
            | FilterLeafLogRecordsFilter
            | None
            | NotNodeLogRecordsFilterOutput
            | OrNodeLogRecordsFilterOutput
            | Unset
        ):
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_0 = FilterLeafLogRecordsFilter.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_1 = AndNodeLogRecordsFilterOutput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_2 = OrNodeLogRecordsFilterOutput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_3 = NotNodeLogRecordsFilterOutput.from_dict(
                    data
                )

                return componentsschemas_filter_expression_annotated_union_log_records_id_filter_log_records_date_filter_log_records_number_filter_log_records_boolean_filter_log_records_collection_filter_log_records_text_filter_log_records_fully_annotated_filter_field_info_annotation_none_type_required_true_discriminator_type_output_type_3
            except:  # noqa: E722
                pass
            return cast(
                AndNodeLogRecordsFilterOutput
                | FilterLeafLogRecordsFilter
                | None
                | NotNodeLogRecordsFilterOutput
                | OrNodeLogRecordsFilterOutput
                | Unset,
                data,
            )

        filter_tree = _parse_filter_tree(d.pop("filter_tree", UNSET))

        def _parse_relative_time(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        relative_time = _parse_relative_time(d.pop("relative_time", UNSET))

        trends_dashboard_response = cls(
            id=id,
            log_stream_id=log_stream_id,
            project_id=project_id,
            layout_map=layout_map,
            interval_mins=interval_mins,
            start_time=start_time,
            end_time=end_time,
            widgets=widgets,
            sections=sections,
            group_by=group_by,
            filter_tree=filter_tree,
            relative_time=relative_time,
        )

        trends_dashboard_response.additional_properties = d
        return trends_dashboard_response

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
