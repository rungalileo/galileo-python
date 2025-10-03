from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_key_action import ApiKeyAction
from ..models.dataset_action import DatasetAction
from ..models.fine_tuned_scorer_action import FineTunedScorerAction
from ..models.generated_scorer_action import GeneratedScorerAction
from ..models.group_action import GroupAction
from ..models.group_member_action import GroupMemberAction
from ..models.integration_action import IntegrationAction
from ..models.organization_action import OrganizationAction
from ..models.project_action import ProjectAction
from ..models.registered_scorer_action import RegisteredScorerAction
from ..models.user_action import UserAction
from ..types import UNSET, Unset

T = TypeVar("T", bound="Permission")


@_attrs_define
class Permission:
    """
    Attributes:
        action (Union[ApiKeyAction, DatasetAction, FineTunedScorerAction, GeneratedScorerAction, GroupAction,
            GroupMemberAction, IntegrationAction, OrganizationAction, ProjectAction, RegisteredScorerAction, UserAction]):
        allowed (bool):
        message (Union[None, Unset, str]):
    """

    action: Union[
        ApiKeyAction,
        DatasetAction,
        FineTunedScorerAction,
        GeneratedScorerAction,
        GroupAction,
        GroupMemberAction,
        IntegrationAction,
        OrganizationAction,
        ProjectAction,
        RegisteredScorerAction,
        UserAction,
    ]
    allowed: bool
    message: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action: str
        if isinstance(
            self.action,
            (
                UserAction,
                GroupAction,
                GroupMemberAction,
                ProjectAction,
                RegisteredScorerAction,
                ApiKeyAction,
                GeneratedScorerAction,
                FineTunedScorerAction,
                DatasetAction,
                IntegrationAction,
            ),
        ):
            action = self.action.value
        else:
            action = self.action.value

        allowed = self.allowed

        message: Union[None, Unset, str]
        message = UNSET if isinstance(self.message, Unset) else self.message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({"action": action, "allowed": allowed})
        if message is not UNSET:
            field_dict["message"] = message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_action(
            data: object,
        ) -> Union[
            ApiKeyAction,
            DatasetAction,
            FineTunedScorerAction,
            GeneratedScorerAction,
            GroupAction,
            GroupMemberAction,
            IntegrationAction,
            OrganizationAction,
            ProjectAction,
            RegisteredScorerAction,
            UserAction,
        ]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return UserAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return GroupAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return GroupMemberAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ProjectAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return RegisteredScorerAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return ApiKeyAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return GeneratedScorerAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return FineTunedScorerAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return DatasetAction(data)

            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                return IntegrationAction(data)

            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            return OrganizationAction(data)

        action = _parse_action(d.pop("action"))

        allowed = d.pop("allowed")

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        permission = cls(action=action, allowed=allowed, message=message)

        permission.additional_properties = d
        return permission

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
