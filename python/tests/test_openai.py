from typing import Dict, Any, Optional
from unittest.mock import patch, Mock

import pytest
from pytest_mock import MockerFixture

from galileo.openai import openai # OpenAI integration


class NestedDictToObject:
    """
    Converts a nested dictionary into an object.
    """

    def __init__(self, dictionary: Dict[str, Any]) -> None:
        """
        Initializes an instance of NestedDictToObject.

        Args:
            dictionary: A nested dictionary to convert into an object.
        """
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, NestedDictToObject(value))
            else:
                setattr(self, key, value)


class MockedCompletion:
    """
    Mock OpenAI API completion.
    """

    def __init__(self, message: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the mocked API parameters.

        Args:
            message: Dictionary containing the message to be mocked.
                     Will be converted to an object.
        """
        if message is None:
            message = {"message": {"content": "This is a mocked message."}}

        # Convert to object
        message_obj = NestedDictToObject(message)

        self.choices = [message_obj]

    def __next__(self) -> "MockedCompletion":
        """
        Return the class instance itself.

        Unittest mock expects an iterable object, so we need to implement
        this method. Otherwise, we would get an error like this:
            TypeError: 'MockedCompletion' object is not iterable

        Returns:
            The class instance itself.
        """
        return self


def test_basic_openai_call(mocker: MockerFixture):
    mocker.patch("openai.ChatCompletion.create", side_effect=MockedCompletion())

    chat_completion = openai.chat.completions.create(
        messages=[{"role": "user", "content": "Say this is a test"}], model="gpt-4o",
    )

    print(chat_completion.choices[0].message.content)
