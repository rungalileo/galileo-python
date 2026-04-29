from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.logging_method import LoggingMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.session_create_request_user_metadata_type_0 import SessionCreateRequestUserMetadataType0


T = TypeVar("T", bound="SessionCreateRequest")


@_attrs_define
class SessionCreateRequest:
    """
    Attributes
    ----------
        log_stream_id (Union[None, Unset, str]): Log stream id associated with the traces.
        experiment_id (Union[None, Unset, str]): Experiment id associated with the traces.
        metrics_testing_id (Union[None, Unset, str]): Metrics testing id associated with the traces.
        logging_method (Union[Unset, LoggingMethod]):
        client_version (Union[None, Unset, str]):
        reliable (Union[Unset, bool]): Whether or not to use reliable logging.  If set to False, the method will respond
            immediately before verifying that the traces have been successfully ingested, and no error message will be
            returned if ingestion fails.  If set to True, the method will wait for the traces to be successfully ingested or
            return an error message if there is an ingestion failure. Default: True.
        name (Union[None, Unset, str]): Name of the session.
        previous_session_id (Union[None, Unset, str]): Id of the previous session.
        external_id (Union[None, Unset, str]): External id of the session.
        user_metadata (Union['SessionCreateRequestUserMetadataType0', None, Unset]): User metadata for the session.
    """

    log_stream_id: Union[None, Unset, str] = UNSET
    experiment_id: Union[None, Unset, str] = UNSET
    metrics_testing_id: Union[None, Unset, str] = UNSET
    logging_method: Union[Unset, LoggingMethod] = UNSET
    client_version: Union[None, Unset, str] = UNSET
    reliable: Union[Unset, bool] = True
    name: Union[None, Unset, str] = UNSET
    previous_session_id: Union[None, Unset, str] = UNSET
    external_id: Union[None, Unset, str] = UNSET
    user_metadata: Union["SessionCreateRequestUserMetadataType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.session_create_request_user_metadata_type_0 import SessionCreateRequestUserMetadataType0

        log_stream_id: Union[None, Unset, str]
        log_stream_id = UNSET if isinstance(self.log_stream_id, Unset) else self.log_stream_id

        experiment_id: Union[None, Unset, str]
        experiment_id = UNSET if isinstance(self.experiment_id, Unset) else self.experiment_id

        metrics_testing_id: Union[None, Unset, str]
        metrics_testing_id = UNSET if isinstance(self.metrics_testing_id, Unset) else self.metrics_testing_id

        logging_method: Union[Unset, str] = UNSET
        if not isinstance(self.logging_method, Unset):
            logging_method = self.logging_method.value

        client_version: Union[None, Unset, str]
        client_version = UNSET if isinstance(self.client_version, Unset) else self.client_version

        reliable = self.reliable

        name: Union[None, Unset, str]
        name = UNSET if isinstance(self.name, Unset) else self.name

        previous_session_id: Union[None, Unset, str]
        previous_session_id = UNSET if isinstance(self.previous_session_id, Unset) else self.previous_session_id

        external_id: Union[None, Unset, str]
        external_id = UNSET if isinstance(self.external_id, Unset) else self.external_id

        user_metadata: Union[None, Unset, dict[str, Any]]
        if isinstance(self.user_metadata, Unset):
            user_metadata = UNSET
        elif isinstance(self.user_metadata, SessionCreateRequestUserMetadataType0):
            user_metadata = self.user_metadata.to_dict()
        else:
            user_metadata = self.user_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if log_stream_id is not UNSET:
            field_dict["log_stream_id"] = log_stream_id
        if experiment_id is not UNSET:
            field_dict["experiment_id"] = experiment_id
        if metrics_testing_id is not UNSET:
            field_dict["metrics_testing_id"] = metrics_testing_id
        if logging_method is not UNSET:
            field_dict["logging_method"] = logging_method
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if reliable is not UNSET:
            field_dict["reliable"] = reliable
        if name is not UNSET:
            field_dict["name"] = name
        if previous_session_id is not UNSET:
            field_dict["previous_session_id"] = previous_session_id
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if user_metadata is not UNSET:
            field_dict["user_metadata"] = user_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.session_create_request_user_metadata_type_0 import SessionCreateRequestUserMetadataType0

        d = dict(src_dict)

        def _parse_log_stream_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        log_stream_id = _parse_log_stream_id(d.pop("log_stream_id", UNSET))

        def _parse_experiment_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        experiment_id = _parse_experiment_id(d.pop("experiment_id", UNSET))

        def _parse_metrics_testing_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        metrics_testing_id = _parse_metrics_testing_id(d.pop("metrics_testing_id", UNSET))

        _logging_method = d.pop("logging_method", UNSET)
        logging_method: Union[Unset, LoggingMethod]
        logging_method = UNSET if isinstance(_logging_method, Unset) else LoggingMethod(_logging_method)

        def _parse_client_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        client_version = _parse_client_version(d.pop("client_version", UNSET))

        reliable = d.pop("reliable", UNSET)

        def _parse_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        name = _parse_name(d.pop("name", UNSET))

        def _parse_previous_session_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        previous_session_id = _parse_previous_session_id(d.pop("previous_session_id", UNSET))

        def _parse_external_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        external_id = _parse_external_id(d.pop("external_id", UNSET))

        def _parse_user_metadata(data: object) -> Union["SessionCreateRequestUserMetadataType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                return SessionCreateRequestUserMetadataType0.from_dict(data)

            except:  # noqa: E722
                pass
            return cast(Union["SessionCreateRequestUserMetadataType0", None, Unset], data)

        user_metadata = _parse_user_metadata(d.pop("user_metadata", UNSET))

        session_create_request = cls(
            log_stream_id=log_stream_id,
            experiment_id=experiment_id,
            metrics_testing_id=metrics_testing_id,
            logging_method=logging_method,
            client_version=client_version,
            reliable=reliable,
            name=name,
            previous_session_id=previous_session_id,
            external_id=external_id,
            user_metadata=user_metadata,
        )

        session_create_request.additional_properties = d
        return session_create_request

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
