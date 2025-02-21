import json

from galileo.utils.serialization import EventSerializer


def test_event_serializer_default() -> None:
    # test empty dict
    assert json.dumps({}, cls=EventSerializer) == "{}"

    # test unknown type
    class Unknown: ...
    assert json.dumps(Unknown(), cls=EventSerializer) == "{}"

    # test None against NoneType
    assert json.dumps(None, cls=EventSerializer) == '"\\"<not serializable object of type: NoneType>\\""'

    # test list
    assert json.dumps([], cls=EventSerializer) == '[]'
