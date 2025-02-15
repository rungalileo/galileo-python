import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.edit_action import EditAction
from ..models.split import Split
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_create_response_edit_spans_type_0 import EditCreateResponseEditSpansType0
    from ..models.filter_params import FilterParams


T = TypeVar("T", bound="EditCreateResponse")


@_attrs_define
class EditCreateResponse:
    """
    Attributes:
        created_at (datetime.datetime):
        edit_action (EditAction): The available actions you can take in an edit.
        exported (bool):
        id (str):
        project_id (str):
        run_id (str):
        split (Split):
        created_by (Union[None, Unset, str]):
        edit_spans (Union['EditCreateResponseEditSpansType0', None, Unset]):
        filter_ (Union['FilterParams', None, Unset]):
        inference_name (Union[None, Unset, str]):
        map_threshold (Union[None, Unset, float]):
        new_label (Union[None, Unset, str]):
        note (Union[None, Unset, str]):
        sample_ids (Union[Unset, list[int]]):
        search_string (Union[None, Unset, str]):
        shift_span_end_num_words (Union[None, Unset, int]):
        shift_span_start_num_words (Union[None, Unset, int]):
        task (Union[None, Unset, str]):
        text_replacement (Union[None, Unset, str]):
        use_regex (Union[None, Unset, bool]):  Default: False.
    """

    created_at: datetime.datetime
    edit_action: EditAction
    exported: bool
    id: str
    project_id: str
    run_id: str
    split: Split
    created_by: Union[None, Unset, str] = UNSET
    edit_spans: Union["EditCreateResponseEditSpansType0", None, Unset] = UNSET
    filter_: Union["FilterParams", None, Unset] = UNSET
    inference_name: Union[None, Unset, str] = UNSET
    map_threshold: Union[None, Unset, float] = UNSET
    new_label: Union[None, Unset, str] = UNSET
    note: Union[None, Unset, str] = UNSET
    sample_ids: Union[Unset, list[int]] = UNSET
    search_string: Union[None, Unset, str] = UNSET
    shift_span_end_num_words: Union[None, Unset, int] = UNSET
    shift_span_start_num_words: Union[None, Unset, int] = UNSET
    task: Union[None, Unset, str] = UNSET
    text_replacement: Union[None, Unset, str] = UNSET
    use_regex: Union[None, Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.edit_create_response_edit_spans_type_0 import EditCreateResponseEditSpansType0
        from ..models.filter_params import FilterParams

        created_at = self.created_at.isoformat()

        edit_action = self.edit_action.value

        exported = self.exported

        id = self.id

        project_id = self.project_id

        run_id = self.run_id

        split = self.split.value

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        edit_spans: Union[None, Unset, dict[str, Any]]
        if isinstance(self.edit_spans, Unset):
            edit_spans = UNSET
        elif isinstance(self.edit_spans, EditCreateResponseEditSpansType0):
            edit_spans = self.edit_spans.to_dict()
        else:
            edit_spans = self.edit_spans

        filter_: Union[None, Unset, dict[str, Any]]
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, FilterParams):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_

        inference_name: Union[None, Unset, str]
        if isinstance(self.inference_name, Unset):
            inference_name = UNSET
        else:
            inference_name = self.inference_name

        map_threshold: Union[None, Unset, float]
        if isinstance(self.map_threshold, Unset):
            map_threshold = UNSET
        else:
            map_threshold = self.map_threshold

        new_label: Union[None, Unset, str]
        if isinstance(self.new_label, Unset):
            new_label = UNSET
        else:
            new_label = self.new_label

        note: Union[None, Unset, str]
        if isinstance(self.note, Unset):
            note = UNSET
        else:
            note = self.note

        sample_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.sample_ids, Unset):
            sample_ids = self.sample_ids

        search_string: Union[None, Unset, str]
        if isinstance(self.search_string, Unset):
            search_string = UNSET
        else:
            search_string = self.search_string

        shift_span_end_num_words: Union[None, Unset, int]
        if isinstance(self.shift_span_end_num_words, Unset):
            shift_span_end_num_words = UNSET
        else:
            shift_span_end_num_words = self.shift_span_end_num_words

        shift_span_start_num_words: Union[None, Unset, int]
        if isinstance(self.shift_span_start_num_words, Unset):
            shift_span_start_num_words = UNSET
        else:
            shift_span_start_num_words = self.shift_span_start_num_words

        task: Union[None, Unset, str]
        if isinstance(self.task, Unset):
            task = UNSET
        else:
            task = self.task

        text_replacement: Union[None, Unset, str]
        if isinstance(self.text_replacement, Unset):
            text_replacement = UNSET
        else:
            text_replacement = self.text_replacement

        use_regex: Union[None, Unset, bool]
        if isinstance(self.use_regex, Unset):
            use_regex = UNSET
        else:
            use_regex = self.use_regex

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "edit_action": edit_action,
                "exported": exported,
                "id": id,
                "project_id": project_id,
                "run_id": run_id,
                "split": split,
            }
        )
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if edit_spans is not UNSET:
            field_dict["edit_spans"] = edit_spans
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if inference_name is not UNSET:
            field_dict["inference_name"] = inference_name
        if map_threshold is not UNSET:
            field_dict["map_threshold"] = map_threshold
        if new_label is not UNSET:
            field_dict["new_label"] = new_label
        if note is not UNSET:
            field_dict["note"] = note
        if sample_ids is not UNSET:
            field_dict["sample_ids"] = sample_ids
        if search_string is not UNSET:
            field_dict["search_string"] = search_string
        if shift_span_end_num_words is not UNSET:
            field_dict["shift_span_end_num_words"] = shift_span_end_num_words
        if shift_span_start_num_words is not UNSET:
            field_dict["shift_span_start_num_words"] = shift_span_start_num_words
        if task is not UNSET:
            field_dict["task"] = task
        if text_replacement is not UNSET:
            field_dict["text_replacement"] = text_replacement
        if use_regex is not UNSET:
            field_dict["use_regex"] = use_regex

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.edit_create_response_edit_spans_type_0 import EditCreateResponseEditSpansType0
        from ..models.filter_params import FilterParams

        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        edit_action = EditAction(d.pop("edit_action"))

        exported = d.pop("exported")

        id = d.pop("id")

        project_id = d.pop("project_id")

        run_id = d.pop("run_id")

        split = Split(d.pop("split"))

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        def _parse_edit_spans(data: object) -> Union["EditCreateResponseEditSpansType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                edit_spans_type_0 = EditCreateResponseEditSpansType0.from_dict(data)

                return edit_spans_type_0
            except:  # noqa: E722
                pass
            return cast(Union["EditCreateResponseEditSpansType0", None, Unset], data)

        edit_spans = _parse_edit_spans(d.pop("edit_spans", UNSET))

        def _parse_filter_(data: object) -> Union["FilterParams", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = FilterParams.from_dict(data)

                return filter_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FilterParams", None, Unset], data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        def _parse_inference_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        inference_name = _parse_inference_name(d.pop("inference_name", UNSET))

        def _parse_map_threshold(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        map_threshold = _parse_map_threshold(d.pop("map_threshold", UNSET))

        def _parse_new_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        new_label = _parse_new_label(d.pop("new_label", UNSET))

        def _parse_note(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        note = _parse_note(d.pop("note", UNSET))

        sample_ids = cast(list[int], d.pop("sample_ids", UNSET))

        def _parse_search_string(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        search_string = _parse_search_string(d.pop("search_string", UNSET))

        def _parse_shift_span_end_num_words(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        shift_span_end_num_words = _parse_shift_span_end_num_words(d.pop("shift_span_end_num_words", UNSET))

        def _parse_shift_span_start_num_words(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        shift_span_start_num_words = _parse_shift_span_start_num_words(d.pop("shift_span_start_num_words", UNSET))

        def _parse_task(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        task = _parse_task(d.pop("task", UNSET))

        def _parse_text_replacement(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        text_replacement = _parse_text_replacement(d.pop("text_replacement", UNSET))

        def _parse_use_regex(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        use_regex = _parse_use_regex(d.pop("use_regex", UNSET))

        edit_create_response = cls(
            created_at=created_at,
            edit_action=edit_action,
            exported=exported,
            id=id,
            project_id=project_id,
            run_id=run_id,
            split=split,
            created_by=created_by,
            edit_spans=edit_spans,
            filter_=filter_,
            inference_name=inference_name,
            map_threshold=map_threshold,
            new_label=new_label,
            note=note,
            sample_ids=sample_ids,
            search_string=search_string,
            shift_span_end_num_words=shift_span_end_num_words,
            shift_span_start_num_words=shift_span_start_num_words,
            task=task,
            text_replacement=text_replacement,
            use_regex=use_regex,
        )

        edit_create_response.additional_properties = d
        return edit_create_response

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
