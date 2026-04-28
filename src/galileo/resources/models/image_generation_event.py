from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.event_status import EventStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.image_generation_event_images_type_0_item import ImageGenerationEventImagesType0Item
    from ..models.image_generation_event_metadata_type_0 import ImageGenerationEventMetadataType0


T = TypeVar("T", bound="ImageGenerationEvent")


@_attrs_define
class ImageGenerationEvent:
    """An image generation event from the model.

    Attributes
    ----------
        type_ (Literal['image_generation'] | Unset):  Default: 'image_generation'.
        id (None | str | Unset): Unique identifier for the event
        status (EventStatus | None | Unset): Status of the event
        metadata (ImageGenerationEventMetadataType0 | None | Unset): Provider-specific metadata and additional fields
        error_message (None | str | Unset): Error message if the event failed
        prompt (None | str | Unset): The prompt used for image generation
        images (list[ImageGenerationEventImagesType0Item] | None | Unset): Generated images with URLs or base64 data
        model (None | str | Unset): Image generation model used
    """

    type_: Literal["image_generation"] | Unset = "image_generation"
    id: None | str | Unset = UNSET
    status: EventStatus | None | Unset = UNSET
    metadata: ImageGenerationEventMetadataType0 | None | Unset = UNSET
    error_message: None | str | Unset = UNSET
    prompt: None | str | Unset = UNSET
    images: list[ImageGenerationEventImagesType0Item] | None | Unset = UNSET
    model: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.image_generation_event_metadata_type_0 import ImageGenerationEventMetadataType0

        type_ = self.type_

        id: None | str | Unset
        id = UNSET if isinstance(self.id, Unset) else self.id

        status: None | str | Unset
        if isinstance(self.status, Unset):
            status = UNSET
        elif isinstance(self.status, EventStatus):
            status = self.status.value
        else:
            status = self.status

        metadata: dict[str, Any] | None | Unset
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, ImageGenerationEventMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        error_message: None | str | Unset
        error_message = UNSET if isinstance(self.error_message, Unset) else self.error_message

        prompt: None | str | Unset
        prompt = UNSET if isinstance(self.prompt, Unset) else self.prompt

        images: list[dict[str, Any]] | None | Unset
        if isinstance(self.images, Unset):
            images = UNSET
        elif isinstance(self.images, list):
            images = []
            for images_type_0_item_data in self.images:
                images_type_0_item = images_type_0_item_data.to_dict()
                images.append(images_type_0_item)

        else:
            images = self.images

        model: None | str | Unset
        model = UNSET if isinstance(self.model, Unset) else self.model

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if prompt is not UNSET:
            field_dict["prompt"] = prompt
        if images is not UNSET:
            field_dict["images"] = images
        if model is not UNSET:
            field_dict["model"] = model

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.image_generation_event_images_type_0_item import ImageGenerationEventImagesType0Item
        from ..models.image_generation_event_metadata_type_0 import ImageGenerationEventMetadataType0

        d = dict(src_dict)
        type_ = cast(Literal["image_generation"] | Unset, d.pop("type", UNSET))
        if type_ != "image_generation" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'image_generation', got '{type_}'")

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_status(data: object) -> EventStatus | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return EventStatus(data)

            except:  # noqa: E722
                pass
            return cast(EventStatus | None | Unset, data)

        status = _parse_status(d.pop("status", UNSET))

        def _parse_metadata(data: object) -> ImageGenerationEventMetadataType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return ImageGenerationEventMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(ImageGenerationEventMetadataType0 | None | Unset, data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_error_message(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        error_message = _parse_error_message(d.pop("error_message", UNSET))

        def _parse_prompt(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        prompt = _parse_prompt(d.pop("prompt", UNSET))

        def _parse_images(data: object) -> list[ImageGenerationEventImagesType0Item] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                images_type_0 = []
                _images_type_0 = data
                for images_type_0_item_data in _images_type_0:
                    images_type_0_item = ImageGenerationEventImagesType0Item.from_dict(images_type_0_item_data)

                    images_type_0.append(images_type_0_item)

                return images_type_0
            except:  # noqa: E722
                pass
            return cast(list[ImageGenerationEventImagesType0Item] | None | Unset, data)

        images = _parse_images(d.pop("images", UNSET))

        def _parse_model(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model = _parse_model(d.pop("model", UNSET))

        image_generation_event = cls(
            type_=type_,
            id=id,
            status=status,
            metadata=metadata,
            error_message=error_message,
            prompt=prompt,
            images=images,
            model=model,
        )

        image_generation_event.additional_properties = d
        return image_generation_event

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
