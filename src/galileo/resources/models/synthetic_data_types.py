from typing import Literal, cast

SyntheticDataTypes = Literal[
    "General Query",
    "Multiple Questions in Query",
    "Off-Topic Query",
    "Prompt Injection",
    "Sexist Content in Query",
    "Toxic Content in Query",
]

SYNTHETIC_DATA_TYPES_VALUES: set[SyntheticDataTypes] = {
    "General Query",
    "Multiple Questions in Query",
    "Off-Topic Query",
    "Prompt Injection",
    "Sexist Content in Query",
    "Toxic Content in Query",
}


def check_synthetic_data_types(value: str) -> SyntheticDataTypes:
    if value in SYNTHETIC_DATA_TYPES_VALUES:
        return cast(SyntheticDataTypes, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SYNTHETIC_DATA_TYPES_VALUES!r}")
