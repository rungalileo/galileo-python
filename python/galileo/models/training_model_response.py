from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.model_kind import ModelKind
from ..models.model_upload_status import ModelUploadStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.training_model_response_parameters import TrainingModelResponseParameters


T = TypeVar("T", bound="TrainingModelResponse")


@_attrs_define
class TrainingModelResponse:
    """
    Attributes:
        id (str):
        kind (ModelKind):
        parameters (TrainingModelResponseParameters):
        project_id (str):
        project_name (str):
        run_id (str):
        run_name (str):
        filename (Union[None, Unset, str]):
        storage_url (Union[None, Unset, str]):
        upload_status (Union[Unset, ModelUploadStatus]):
    """

    id: str
    kind: ModelKind
    parameters: "TrainingModelResponseParameters"
    project_id: str
    project_name: str
    run_id: str
    run_name: str
    filename: Union[None, Unset, str] = UNSET
    storage_url: Union[None, Unset, str] = UNSET
    upload_status: Union[Unset, ModelUploadStatus] = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        kind = self.kind.value

        parameters = self.parameters.to_dict()

        project_id = self.project_id

        project_name = self.project_name

        run_id = self.run_id

        run_name = self.run_name

        filename: Union[None, Unset, str]
        if isinstance(self.filename, Unset):
            filename = UNSET
        else:
            filename = self.filename

        storage_url: Union[None, Unset, str]
        if isinstance(self.storage_url, Unset):
            storage_url = UNSET
        else:
            storage_url = self.storage_url

        upload_status: Union[Unset, str] = UNSET
        if not isinstance(self.upload_status, Unset):
            upload_status = self.upload_status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "kind": kind,
                "parameters": parameters,
                "project_id": project_id,
                "project_name": project_name,
                "run_id": run_id,
                "run_name": run_name,
            }
        )
        if filename is not UNSET:
            field_dict["filename"] = filename
        if storage_url is not UNSET:
            field_dict["storage_url"] = storage_url
        if upload_status is not UNSET:
            field_dict["upload_status"] = upload_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.training_model_response_parameters import TrainingModelResponseParameters

        d = src_dict.copy()
        id = d.pop("id")

        kind = ModelKind(d.pop("kind"))

        parameters = TrainingModelResponseParameters.from_dict(d.pop("parameters"))

        project_id = d.pop("project_id")

        project_name = d.pop("project_name")

        run_id = d.pop("run_id")

        run_name = d.pop("run_name")

        def _parse_filename(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        filename = _parse_filename(d.pop("filename", UNSET))

        def _parse_storage_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        storage_url = _parse_storage_url(d.pop("storage_url", UNSET))

        _upload_status = d.pop("upload_status", UNSET)
        upload_status: Union[Unset, ModelUploadStatus]
        if isinstance(_upload_status, Unset):
            upload_status = UNSET
        else:
            upload_status = ModelUploadStatus(_upload_status)

        training_model_response = cls(
            id=id,
            kind=kind,
            parameters=parameters,
            project_id=project_id,
            project_name=project_name,
            run_id=run_id,
            run_name=run_name,
            filename=filename,
            storage_url=storage_url,
            upload_status=upload_status,
        )

        return training_model_response
