"""
UUID utility functions for handling UUID version detection and conversion.

This module provides utilities for detecting UUID7s and converting them to UUID4s
to ensure compatibility with systems that expect UUID4 format.
"""

import hashlib
import logging
from typing import Optional, Union
from uuid import UUID

_logger = logging.getLogger(__name__)


def is_uuid7(uuid_obj: Union[UUID, str]) -> bool:
    """
    Check if a UUID is version 7.

    Parameters
    ----------
    uuid_obj : Union[UUID, str]
        The UUID to check, either as a UUID object or string.

    Returns
    -------
    bool
        True if the UUID is version 7, False otherwise.
    """
    try:
        if isinstance(uuid_obj, str):
            uuid_obj = UUID(uuid_obj)
        return uuid_obj.version == 7
    except (ValueError, AttributeError):
        return False


def uuid7_to_uuid4(uuid_obj: Union[UUID, str]) -> UUID:
    """
    Convert a UUID7 to a UUID4 by hashing its string representation.

    This function takes a UUID7 and generates a deterministic UUID4 by hashing
    the string representation of the UUID7 using SHA-256 and using the first
    16 bytes to create a new UUID4.

    Parameters
    ----------
    uuid_obj : Union[UUID, str]
        The UUID7 to convert, either as a UUID object or string.

    Returns
    -------
    UUID
        A UUID4 generated from the hash of the input UUID7.

    Raises
    ------
    ValueError
        If the input is not a valid UUID or not a UUID7.
    """
    try:
        if isinstance(uuid_obj, str):
            uuid_str = uuid_obj
            uuid_obj = UUID(uuid_obj)
        else:
            uuid_str = str(uuid_obj)

        if uuid_obj.version != 7:
            raise ValueError(f"Input UUID is version {uuid_obj.version}, not version 7")

        # Hash the UUID string using SHA-256
        hash_digest = hashlib.sha256(uuid_str.encode()).digest()

        # Use the first 16 bytes of the hash to create a version 4 UUID
        new_uuid = UUID(bytes=hash_digest[:16], version=4)

        _logger.debug(f"Converted UUID7 {uuid_str} to UUID4 {new_uuid}")
        return new_uuid

    except ValueError as e:
        _logger.error(f"Failed to convert UUID7 to UUID4: {e}")
        raise


def convert_uuid_if_uuid7(uuid_obj: Optional[Union[UUID, str]]) -> Optional[UUID]:
    """
    Convert a UUID to UUID4 if it's a UUID7, otherwise return the original UUID.

    This is a convenience function that checks if a UUID is version 7 and converts
    it to UUID4 if so, otherwise returns the original UUID as a UUID object.

    Parameters
    ----------
    uuid_obj : Optional[Union[UUID, str]]
        The UUID to potentially convert, either as a UUID object, string, or None.

    Returns
    -------
    Optional[UUID]
        The converted UUID4 if input was UUID7, the original UUID object if not UUID7,
        or None if input was None.
    """
    if uuid_obj is None:
        return None

    try:
        if isinstance(uuid_obj, str):
            uuid_obj = UUID(uuid_obj)

        if is_uuid7(uuid_obj):
            return uuid7_to_uuid4(uuid_obj)
        return uuid_obj

    except ValueError as e:
        _logger.warning(f"Invalid UUID format: {uuid_obj}, returning None. Error: {e}")
        return None
