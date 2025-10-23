"""
Tests for UUID utility functions.
"""

from uuid import UUID, uuid4

import pytest

from galileo.utils.uuid_utils import convert_uuid_if_uuid7, uuid7_to_uuid4


@pytest.fixture
def uuid7() -> UUID:
    return UUID("0199ecc5-3f94-747c-b0d9-ddc8ba29d0d5")


def test_convert_uuid_if_uuid7_with_uuid4() -> None:
    """Test convert_uuid_if_uuid7 with UUID4."""
    uuid4_obj = uuid4()

    result = convert_uuid_if_uuid7(uuid4_obj)

    assert result == uuid4_obj
    assert result is not None
    assert result.version == 4


def test_convert_uuid_if_uuid7_with_none() -> None:
    """Test convert_uuid_if_uuid7 with None."""
    result = convert_uuid_if_uuid7(None)
    assert result is None


def test_convert_uuid_if_uuid7_with_invalid_uuid() -> None:
    """Test convert_uuid_if_uuid7 with invalid UUID."""
    result = convert_uuid_if_uuid7("invalid-uuid")
    assert result is None


def test_deterministic_conversion(uuid7: UUID) -> None:
    """Test that UUID7 conversion is deterministic."""
    # Convert multiple times
    result1 = uuid7_to_uuid4(uuid7)
    result2 = uuid7_to_uuid4(uuid7)
    result3 = uuid7_to_uuid4(str(uuid7))

    # All results should be identical
    assert result1 == result2 == result3
    assert result1.version == 4
