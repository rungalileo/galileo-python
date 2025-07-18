from typing import Literal, cast

GroupMemberAction = Literal["delete", "update_role"]

GROUP_MEMBER_ACTION_VALUES: set[GroupMemberAction] = {"delete", "update_role"}


def check_group_member_action(value: str) -> GroupMemberAction:
    if value in GROUP_MEMBER_ACTION_VALUES:
        return cast(GroupMemberAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GROUP_MEMBER_ACTION_VALUES!r}")
