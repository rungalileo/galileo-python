from enum import Enum


class ProjectAction(str, Enum):
    CONFIGURE_CROWN_LOGIC = "configure_crown_logic"
    CONFIGURE_HUMAN_FEEDBACK = "configure_human_feedback"
    CREATE_RUN = "create_run"
    CREATE_STAGE = "create_stage"
    DELETE = "delete"
    DELETE_DATA = "delete_data"
    DELETE_RUN = "delete_run"
    DISMISS_ALERT = "dismiss_alert"
    EDIT_ALERT = "edit_alert"
    EDIT_EDIT = "edit_edit"
    EDIT_RUN_TAGS = "edit_run_tags"
    EDIT_SLICE = "edit_slice"
    EDIT_STAGE = "edit_stage"
    EXPORT_DATA = "export_data"
    LOG_DATA = "log_data"
    MOVE_RUN = "move_run"
    RECORD_HUMAN_FEEDBACK = "record_human_feedback"
    RENAME = "rename"
    RENAME_RUN = "rename_run"
    SET_METRIC = "set_metric"
    SHARE = "share"
    TOGGLE_METRIC = "toggle_metric"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
