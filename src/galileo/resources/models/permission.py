from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_key_action import ApiKeyAction, check_api_key_action
from ..models.dataset_action import DatasetAction, check_dataset_action
from ..models.fine_tuned_scorer_action import FineTunedScorerAction, check_fine_tuned_scorer_action
from ..models.generated_scorer_action import GeneratedScorerAction, check_generated_scorer_action
from ..models.group_action import GroupAction, check_group_action
from ..models.group_member_action import GroupMemberAction, check_group_member_action
from ..models.integration_action import IntegrationAction, check_integration_action
from ..models.organization_action import OrganizationAction, check_organization_action
from ..models.project_action import ProjectAction, check_project_action
from ..models.registered_scorer_action import RegisteredScorerAction, check_registered_scorer_action
from ..models.user_action import UserAction, check_user_action
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
        if isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        elif isinstance(self.action, str):
            action = self.action
        else:
            action = self.action

        allowed = self.allowed

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

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
                action_type_0 = check_user_action(data)

                return action_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_1 = check_group_action(data)

                return action_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_2 = check_group_member_action(data)

                return action_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_3 = check_project_action(data)

                return action_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_4 = check_registered_scorer_action(data)

                return action_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_5 = check_api_key_action(data)

                return action_type_5
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_6 = check_generated_scorer_action(data)

                return action_type_6
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_7 = check_fine_tuned_scorer_action(data)

                return action_type_7
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_8 = check_dataset_action(data)

                return action_type_8
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_type_9 = check_integration_action(data)

                return action_type_9
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            action_type_10 = check_organization_action(data)

            return action_type_10

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
