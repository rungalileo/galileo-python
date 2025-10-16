from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.core_scorer_name import CoreScorerName
from ..models.luna_input_type_enum import LunaInputTypeEnum
from ..models.luna_output_type_enum import LunaOutputTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.base_finetuned_scorer_db_class_name_to_vocab_ix_type_0 import (
        BaseFinetunedScorerDBClassNameToVocabIxType0,
    )
    from ..models.base_finetuned_scorer_db_class_name_to_vocab_ix_type_1 import (
        BaseFinetunedScorerDBClassNameToVocabIxType1,
    )


T = TypeVar("T", bound="BaseFinetunedScorerDB")


@_attrs_define
class BaseFinetunedScorerDB:
    """
    Attributes
    ----------
        id (str):
        lora_task_id (int):
        name (str):
        prompt (str):
        class_name_to_vocab_ix (Union['BaseFinetunedScorerDBClassNameToVocabIxType0',
            'BaseFinetunedScorerDBClassNameToVocabIxType1', None, Unset]):
        executor (Union[CoreScorerName, None, Unset]): Executor pipeline. Defaults to finetuned scorer pipeline but can
            run custom galileo score pipelines.
        luna_input_type (Union[LunaInputTypeEnum, None, Unset]):
        luna_output_type (Union[LunaOutputTypeEnum, None, Unset]):
    """

    id: str
    lora_task_id: int
    name: str
    prompt: str
    class_name_to_vocab_ix: Union[
        "BaseFinetunedScorerDBClassNameToVocabIxType0", "BaseFinetunedScorerDBClassNameToVocabIxType1", None, Unset
    ] = UNSET
    executor: Union[CoreScorerName, None, Unset] = UNSET
    luna_input_type: Union[LunaInputTypeEnum, None, Unset] = UNSET
    luna_output_type: Union[LunaOutputTypeEnum, None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.base_finetuned_scorer_db_class_name_to_vocab_ix_type_0 import (
            BaseFinetunedScorerDBClassNameToVocabIxType0,
        )
        from ..models.base_finetuned_scorer_db_class_name_to_vocab_ix_type_1 import (
            BaseFinetunedScorerDBClassNameToVocabIxType1,
        )

        id = self.id

        lora_task_id = self.lora_task_id

        name = self.name

        prompt = self.prompt

        class_name_to_vocab_ix: Union[None, Unset, dict[str, Any]]
        if isinstance(self.class_name_to_vocab_ix, Unset):
            class_name_to_vocab_ix = UNSET
        elif isinstance(
            self.class_name_to_vocab_ix,
            (BaseFinetunedScorerDBClassNameToVocabIxType0, BaseFinetunedScorerDBClassNameToVocabIxType1),
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"id": id, "lora_task_id": lora_task_id, "name": name, "prompt": prompt})
        if class_name_to_vocab_ix is not UNSET:
            field_dict["class_name_to_vocab_ix"] = class_name_to_vocab_ix
        if executor is not UNSET:
            field_dict["executor"] = executor
        if luna_input_type is not UNSET:
            field_dict["luna_input_type"] = luna_input_type
        if luna_output_type is not UNSET:
            field_dict["luna_output_type"] = luna_output_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.base_finetuned_scorer_db_class_name_to_vocab_ix_type_0 import (
            BaseFinetunedScorerDBClassNameToVocabIxType0,
        )
        from ..models.base_finetuned_scorer_db_class_name_to_vocab_ix_type_1 import (
            BaseFinetunedScorerDBClassNameToVocabIxType1,
        )

        d = dict(src_dict)
        id = d.pop("id")

        lora_task_id = d.pop("lora_task_id")

        name = d.pop("name")

        prompt = d.pop("prompt")

        def _parse_class_name_to_vocab_ix(
            data: object,
        ) -> Union[
            "BaseFinetunedScorerDBClassNameToVocabIxType0", "BaseFinetunedScorerDBClassNameToVocabIxType1", None, Unset
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseFinetunedScorerDBClassNameToVocabIxType0.from_dict(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return BaseFinetunedScorerDBClassNameToVocabIxType1.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(
                Union[
                    "BaseFinetunedScorerDBClassNameToVocabIxType0",
                    "BaseFinetunedScorerDBClassNameToVocabIxType1",
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

        base_finetuned_scorer_db = cls(
            id=id,
            lora_task_id=lora_task_id,
            name=name,
            prompt=prompt,
            class_name_to_vocab_ix=class_name_to_vocab_ix,
            executor=executor,
            luna_input_type=luna_input_type,
            luna_output_type=luna_output_type,
        )

        base_finetuned_scorer_db.additional_properties = d
        return base_finetuned_scorer_db

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
