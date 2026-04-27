from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.fine_tuned_scorer_weights_upload_response_object_paths import (
        FineTunedScorerWeightsUploadResponseObjectPaths,
    )
    from ..models.fine_tuned_scorer_weights_upload_response_upload_urls import (
        FineTunedScorerWeightsUploadResponseUploadUrls,
    )


T = TypeVar("T", bound="FineTunedScorerWeightsUploadResponse")


@_attrs_define
class FineTunedScorerWeightsUploadResponse:
    """
    Attributes:
        bucket (str):
        lora_weights_path (str):
        upload_urls (FineTunedScorerWeightsUploadResponseUploadUrls):
        object_paths (FineTunedScorerWeightsUploadResponseObjectPaths):
        presigned_url_expiry_seconds (int):
    """

    bucket: str
    lora_weights_path: str
    upload_urls: FineTunedScorerWeightsUploadResponseUploadUrls
    object_paths: FineTunedScorerWeightsUploadResponseObjectPaths
    presigned_url_expiry_seconds: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bucket = self.bucket

        lora_weights_path = self.lora_weights_path

        upload_urls = self.upload_urls.to_dict()

        object_paths = self.object_paths.to_dict()

        presigned_url_expiry_seconds = self.presigned_url_expiry_seconds

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bucket": bucket,
                "lora_weights_path": lora_weights_path,
                "upload_urls": upload_urls,
                "object_paths": object_paths,
                "presigned_url_expiry_seconds": presigned_url_expiry_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fine_tuned_scorer_weights_upload_response_object_paths import (
            FineTunedScorerWeightsUploadResponseObjectPaths,
        )
        from ..models.fine_tuned_scorer_weights_upload_response_upload_urls import (
            FineTunedScorerWeightsUploadResponseUploadUrls,
        )

        d = dict(src_dict)
        bucket = d.pop("bucket")

        lora_weights_path = d.pop("lora_weights_path")

        upload_urls = FineTunedScorerWeightsUploadResponseUploadUrls.from_dict(d.pop("upload_urls"))

        object_paths = FineTunedScorerWeightsUploadResponseObjectPaths.from_dict(d.pop("object_paths"))

        presigned_url_expiry_seconds = d.pop("presigned_url_expiry_seconds")

        fine_tuned_scorer_weights_upload_response = cls(
            bucket=bucket,
            lora_weights_path=lora_weights_path,
            upload_urls=upload_urls,
            object_paths=object_paths,
            presigned_url_expiry_seconds=presigned_url_expiry_seconds,
        )

        fine_tuned_scorer_weights_upload_response.additional_properties = d
        return fine_tuned_scorer_weights_upload_response

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
