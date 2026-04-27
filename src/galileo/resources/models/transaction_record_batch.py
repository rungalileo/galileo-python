from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.transaction_logging_method import TransactionLoggingMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transaction_record_ingest import TransactionRecordIngest


T = TypeVar("T", bound="TransactionRecordBatch")


@_attrs_define
class TransactionRecordBatch:
    """
    Attributes:
        records (list[TransactionRecordIngest]):
        logging_method (TransactionLoggingMethod | Unset):
        client_version (None | str | Unset):
    """

    records: list[TransactionRecordIngest]
    logging_method: TransactionLoggingMethod | Unset = UNSET
    client_version: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        records = []
        for records_item_data in self.records:
            records_item = records_item_data.to_dict()
            records.append(records_item)

        logging_method: str | Unset = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        client_version: None | str | Unset
        if isinstance(self.client_version, Unset):
            client_version = UNSET
        else:
            client_version = self.client_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"records": records})
        if logging_method is not UNSET:
            field_dict["logging_method"] = logging_method
        if client_version is not UNSET:
            field_dict["client_version"] = client_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction_record_ingest import TransactionRecordIngest

        d = dict(src_dict)
        records = []
        _records = d.pop("records")
        for records_item_data in _records:
            records_item = TransactionRecordIngest.from_dict(records_item_data)

            records.append(records_item)

        _logging_method = d.pop("logging_method", UNSET)
        logging_method: TransactionLoggingMethod | Unset
        if isinstance(_logging_method, Unset):
            logging_method = UNSET
        else:
            logging_method = TransactionLoggingMethod(_logging_method)

        def _parse_client_version(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        client_version = _parse_client_version(d.pop("client_version", UNSET))

        transaction_record_batch = cls(records=records, logging_method=logging_method, client_version=client_version)

        transaction_record_batch.additional_properties = d
        return transaction_record_batch

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
