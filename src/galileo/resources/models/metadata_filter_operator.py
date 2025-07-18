from typing import Literal, cast

MetadataFilterOperator = Literal["eq", "ne", "not_in", "one_of"]

METADATA_FILTER_OPERATOR_VALUES: set[MetadataFilterOperator] = {"eq", "ne", "not_in", "one_of"}


def check_metadata_filter_operator(value: str) -> MetadataFilterOperator:
    if value in METADATA_FILTER_OPERATOR_VALUES:
        return cast(MetadataFilterOperator, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {METADATA_FILTER_OPERATOR_VALUES!r}")
