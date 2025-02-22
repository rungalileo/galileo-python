from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..models.model_kind import ModelKind

if TYPE_CHECKING:
    from ..models.upload_model_parameters import UploadModelParameters


T = TypeVar("T", bound="UploadModel")


@_attrs_define
class UploadModel:
    """
    Attributes:
        kind (ModelKind):
        parameters (UploadModelParameters):
    """

    kind: ModelKind
    parameters: "UploadModelParameters"

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update({"kind": kind, "parameters": parameters})

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.upload_model_parameters import UploadModelParameters

        d = src_dict.copy()
        kind = ModelKind(d.pop("kind"))

        parameters = UploadModelParameters.from_dict(d.pop("parameters"))

        upload_model = cls(kind=kind, parameters=parameters)

        return upload_model
