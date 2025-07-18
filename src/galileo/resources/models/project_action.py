from typing import Literal, cast

ProjectAction = Literal[
    "configure_crown_logic",
    "configure_human_feedback",
    "create_run",
    "create_stage",
    "delete",
    "delete_data",
    "delete_run",
    "dismiss_alert",
    "edit_alert",
    "edit_edit",
    "edit_run_tags",
    "edit_slice",
    "edit_stage",
    "export_data",
    "log_data",
    "move_run",
    "record_human_feedback",
    "rename",
    "rename_run",
    "set_metric",
    "share",
    "toggle_metric",
    "update",
]

PROJECT_ACTION_VALUES: set[ProjectAction] = {
    "configure_crown_logic",
    "configure_human_feedback",
    "create_run",
    "create_stage",
    "delete",
    "delete_data",
    "delete_run",
    "dismiss_alert",
    "edit_alert",
    "edit_edit",
    "edit_run_tags",
    "edit_slice",
    "edit_stage",
    "export_data",
    "log_data",
    "move_run",
    "record_human_feedback",
    "rename",
    "rename_run",
    "set_metric",
    "share",
    "toggle_metric",
    "update",
}


def check_project_action(value: str) -> ProjectAction:
    if value in PROJECT_ACTION_VALUES:
        return cast(ProjectAction, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PROJECT_ACTION_VALUES!r}")
