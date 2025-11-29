import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.core_scorer_name import CoreScorerName
from ..models.luna_input_type_enum import LunaInputTypeEnum
from ..models.luna_output_type_enum import LunaOutputTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fine_tuned_scorer_response_class_name_to_vocab_ix_type_0 import (
        FineTunedScorerResponseClassNameToVocabIxType0,
    )
    from ..models.fine_tuned_scorer_response_class_name_to_vocab_ix_type_1 import (
        FineTunedScorerResponseClassNameToVocabIxType1,
    )


T = TypeVar("T", bound="FineTunedScorerResponse")


@_attrs_define
class FineTunedScorerResponse:
    """
    Attributes
    ----------
        id (str):
        name (str):
        lora_task_id (int):
        prompt (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        created_by (str):
        luna_input_type (Union[LunaInputTypeEnum, None, Unset]):
        luna_output_type (Union[LunaOutputTypeEnum, None, Unset]):
        class_name_to_vocab_ix (Union['FineTunedScorerResponseClassNameToVocabIxType0',
            'FineTunedScorerResponseClassNameToVocabIxType1', None, Unset]):
        executor (Union[CoreScorerName, None, Unset]): Executor pipeline. Defaults to finetuned scorer pipeline but can
            run custom galileo score pipelines.
    """

    id: str
    name: str
    lora_task_id: int
    prompt: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str
    luna_input_type: Union[LunaInputTypeEnum, None, Unset] = UNSET
    luna_output_type: Union[LunaOutputTypeEnum, None, Unset] = UNSET
    class_name_to_vocab_ix: Union[
        "FineTunedScorerResponseClassNameToVocabIxType0", "FineTunedScorerResponseClassNameToVocabIxType1", None, Unset
    ] = UNSET
    executor: Union[CoreScorerName, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.fine_tuned_scorer_response_class_name_to_vocab_ix_type_0 import (
            FineTunedScorerResponseClassNameToVocabIxType0,
        )
        from ..models.fine_tuned_scorer_response_class_name_to_vocab_ix_type_1 import (
            FineTunedScorerResponseClassNameToVocabIxType1,
        )

        id = self.id

        name = self.name

        lora_task_id = self.lora_task_id

        prompt = self.prompt

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by = self.created_by

        luna_input_type: Union[None, Unset, str]
        if isinstance(self.luna_input_type, Unset):
            luna_input_type = UNSET
        elif isinstance(self.luna_input_type, LunaInputTypeEnum):
            luna_input_type = self.luna_input_type.value
        else:
            luna_input_type = self.luna_input_type

        luna_output_type: Union[None, Unset, str]
        if isinstance(self.luna_output_type, Unset):
            luna_output_type = UNSET
        elif isinstance(self.luna_output_type, LunaOutputTypeEnum):
            luna_output_type = self.luna_output_type.value
        else:
            luna_output_type = self.luna_output_type

        class_name_to_vocab_ix: Union[None, Unset, dict[str, Any]]
        if isinstance(self.class_name_to_vocab_ix, Unset):
            class_name_to_vocab_ix = UNSET
        elif isinstance(
            self.class_name_to_vocab_ix,
            (FineTunedScorerResponseClassNameToVocabIxType0, FineTunedScorerResponseClassNameToVocabIxType1),
        ):
            class_name_to_vocab_ix = self.class_name_to_vocab_ix.to_dict()
        else:
            class_name_to_vocab_ix = self.class_name_to_vocab_ix

        executor: Union[None, Unset, str]
        if isinstance(self.executor, Unset):
            executor = UNSET
        elif isinstance(self.executor, CoreScorerName):
            executor = self.executor.value
        else:
            executor = self.executor

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "lora_task_id": lora_task_id,
                "prompt": prompt,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by": created_by,
            }
        )
        if luna_input_type is not UNSET:
            field_dict["luna_input_type"] = luna_input_type
        if luna_output_type is not UNSET:
            field_dict["luna_output_type"] = luna_output_type
        if class_name_to_vocab_ix is not UNSET:
            field_dict["class_name_to_vocab_ix"] = class_name_to_vocab_ix
        if executor is not UNSET:
            field_dict["executor"] = executor

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fine_tuned_scorer_response_class_name_to_vocab_ix_type_0 import (
            FineTunedScorerResponseClassNameToVocabIxType0,
        )
        from ..models.fine_tuned_scorer_response_class_name_to_vocab_ix_type_1 import (
            FineTunedScorerResponseClassNameToVocabIxType1,
        )

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        lora_task_id = d.pop("lora_task_id")

        prompt = d.pop("prompt")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        created_by = d.pop("created_by")

        def _parse_luna_input_type(data: object) -> Union[LunaInputTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LunaInputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[LunaInputTypeEnum, None, Unset], data)

        luna_input_type = _parse_luna_input_type(d.pop("luna_input_type", UNSET))

        def _parse_luna_output_type(data: object) -> Union[LunaOutputTypeEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return LunaOutputTypeEnum(data)

            except:  # noqa: E722
                pass
            return cast(Union[LunaOutputTypeEnum, None, Unset], data)

        luna_output_type = _parse_luna_output_type(d.pop("luna_output_type", UNSET))

        def _parse_class_name_to_vocab_ix(
            data: object,
        ) -> Union[
            "FineTunedScorerResponseClassNameToVocabIxType0",
            "FineTunedScorerResponseClassNameToVocabIxType1",
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
                return FineTunedScorerResponseClassNameToVocabIxType0.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return FineTunedScorerResponseClassNameToVocabIxType1.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "FineTunedScorerResponseClassNameToVocabIxType0",
                    "FineTunedScorerResponseClassNameToVocabIxType1",
                    None,
                    Unset,
                ],
                data,
            )

        class_name_to_vocab_ix = _parse_class_name_to_vocab_ix(d.pop("class_name_to_vocab_ix", UNSET))

        def _parse_executor(data: object) -> Union[CoreScorerName, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return CoreScorerName(data)

            except:  # noqa: E722
                pass
            return cast(Union[CoreScorerName, None, Unset], data)

        executor = _parse_executor(d.pop("executor", UNSET))

        fine_tuned_scorer_response = cls(
            id=id,
            name=name,
            lora_task_id=lora_task_id,
            prompt=prompt,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            luna_input_type=luna_input_type,
            luna_output_type=luna_output_type,
            class_name_to_vocab_ix=class_name_to_vocab_ix,
            executor=executor,
        )

        fine_tuned_scorer_response.additional_properties = d
        return fine_tuned_scorer_response

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
