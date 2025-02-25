from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

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
        records (list['TransactionRecordIngest']):
        client_version (Union[None, Unset, str]):
        logging_method (Union[Unset, TransactionLoggingMethod]):
    """

    records: list["TransactionRecordIngest"]
    client_version: Union[None, Unset, str] = UNSET
    logging_method: Union[Unset, TransactionLoggingMethod] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        records = []
        for records_item_data in self.records:
            records_item = records_item_data.to_dict()
            records.append(records_item)

        client_version: Union[None, Unset, str]
        if isinstance(self.client_version, Unset):
            client_version = UNSET
        else:
            client_version = self.client_version

        logging_method: Union[Unset, str] = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"records": records})
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if logging_method is not UNSET:
            field_dict["logging_method"] = logging_method

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.transaction_record_ingest import TransactionRecordIngest

        d = src_dict.copy()
        records = []
        _records = d.pop("records")
        for records_item_data in _records:
            records_item = TransactionRecordIngest.from_dict(records_item_data)

            records.append(records_item)

        def _parse_client_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        client_version = _parse_client_version(d.pop("client_version", UNSET))

        _logging_method = d.pop("logging_method", UNSET)
        logging_method: Union[Unset, TransactionLoggingMethod]
        if isinstance(_logging_method, Unset):
            logging_method = UNSET
        else:
            logging_method = TransactionLoggingMethod(_logging_method)

        transaction_record_batch = cls(records=records, client_version=client_version, logging_method=logging_method)

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
