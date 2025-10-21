"""
Tests for UUID utility functions.
"""

import hashlib
from uuid import UUID, uuid4

import pytest

from galileo.utils.uuid_utils import convert_uuid_if_uuid7, is_uuid7, uuid7_to_uuid4


@pytest.fixture
def uuid7() -> UUID:
    return UUID("0199ecc5-3f94-747c-b0d9-ddc8ba29d0d5")


def test_is_uuid7_with_uuid7_object(uuid7: UUID) -> None:
    """Test is_uuid7 with a UUID7 object."""
    # Create a mock UUID7 by setting version to 7
    assert is_uuid7(uuid7) is True


def test_is_uuid7_with_uuid7_string(uuid7: UUID) -> None:
    """Test is_uuid7 with a UUID7 string."""
    # Create a mock UUID7 string
    assert is_uuid7(str(uuid7)) is True


def test_is_uuid7_with_uuid4() -> None:
    """Test is_uuid7 with a UUID4."""
    assert is_uuid7(uuid4()) is False


def test_is_uuid7_with_invalid_uuid() -> None:
    """Test is_uuid7 with invalid UUID."""
    assert is_uuid7("invalid-uuid") is False


def test_uuid7_to_uuid4_conversion(uuid7: UUID) -> None:
    """Test UUID7 to UUID4 conversion."""
    result = uuid7_to_uuid4(uuid7)
    assert isinstance(result, UUID)
    assert result.version == 4

    # Test deterministic conversion - same input should produce same output
    result2 = uuid7_to_uuid4(uuid7)
    assert result == result2


def test_uuid7_to_uuid4_with_non_uuid7_raises_error() -> None:
    """Test that uuid7_to_uuid4 raises error for non-UUID7."""
    uuid4_obj = uuid4()

    with pytest.raises(ValueError, match="Input UUID is version 4, not version 7"):
        uuid7_to_uuid4(uuid4_obj)


def test_uuid7_to_uuid4_with_invalid_uuid_raises_error() -> None:
    """Test that uuid7_to_uuid4 raises error for invalid UUID."""
    with pytest.raises(ValueError):
        uuid7_to_uuid4("invalid-uuid")


def test_convert_uuid_if_uuid7_with_uuid7(uuid7: UUID) -> None:
    """Test convert_uuid_if_uuid7 with UUID7."""
    result = convert_uuid_if_uuid7(uuid7)

    assert isinstance(result, UUID)
    assert result.version == 4
    assert result != uuid7


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


def test_convert_uuid_if_uuid7_with_string() -> None:
    """Test convert_uuid_if_uuid7 with UUID string."""
    uuid4_str = str(uuid4())

    result = convert_uuid_if_uuid7(uuid4_str)

    assert isinstance(result, UUID)
    assert result.version == 4
    assert str(result) == uuid4_str


def test_deterministic_conversion() -> None:
    """Test that UUID7 conversion is deterministic."""
    # Create a mock UUID7
    uuid7_bytes = bytearray(uuid4().bytes)
    uuid7_bytes[6] = (uuid7_bytes[6] & 0x0F) | 0x70  # Set version to 7
    uuid7_obj = UUID(bytes=bytes(uuid7_bytes))

    # Convert multiple times
    result1 = uuid7_to_uuid4(uuid7_obj)
    result2 = uuid7_to_uuid4(uuid7_obj)
    result3 = uuid7_to_uuid4(str(uuid7_obj))

    # All results should be identical
    assert result1 == result2 == result3

    # Verify the conversion matches expected hash
    expected_hash = hashlib.sha256(str(uuid7_obj).encode()).digest()
    expected_uuid = UUID(bytes=expected_hash[:16], version=4)
    assert result1 == expected_uuid
