from enum import Enum


class EditAction(str, Enum):
    ADD_SPAN = "add_span"
    CREATE_NEW_LABEL = "create_new_label"
    DELETE = "delete"
    RELABEL = "relabel"
    RELABEL_AS_PRED = "relabel_as_pred"
    SELECT_FOR_LABEL = "select_for_label"
    SHIFT_SPAN = "shift_span"
    UPDATE_TEXT = "update_text"

    def __str__(self) -> str:
        return str(self.value)
