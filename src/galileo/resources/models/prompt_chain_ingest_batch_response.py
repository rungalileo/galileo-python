from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PromptChainIngestBatchResponse")


@_attrs_define
class PromptChainIngestBatchResponse:
    """
    Attributes:
        num_rows (int):
        message (str):
        job_id (str):
        link (str):
        num_chains (int):
        total_chains (int):
    """

    num_rows: int
    message: str
    job_id: str
    link: str
    num_chains: int
    total_chains: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        num_rows = self.num_rows

        message = self.message

        job_id = self.job_id

        link = self.link

        num_chains = self.num_chains

        total_chains = self.total_chains

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "num_rows": num_rows,
                "message": message,
                "job_id": job_id,
                "link": link,
                "num_chains": num_chains,
                "total_chains": total_chains,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        num_rows = d.pop("num_rows")

        message = d.pop("message")

        job_id = d.pop("job_id")

        link = d.pop("link")

        num_chains = d.pop("num_chains")

        total_chains = d.pop("total_chains")

        prompt_chain_ingest_batch_response = cls(
            num_rows=num_rows,
            message=message,
            job_id=job_id,
            link=link,
            num_chains=num_chains,
            total_chains=total_chains,
        )

        prompt_chain_ingest_batch_response.additional_properties = d
        return prompt_chain_ingest_batch_response

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
