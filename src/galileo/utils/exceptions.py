import json


class APIException(Exception):
    """
    APIException is base exception for all API errors. It tries to parse content.detail
    and put it to message.
    """

    def __init__(self, message):
        try:
            self.message = json.loads(message)["detail"]
        except (KeyError, TypeError, ValueError):
            self.message = message
        super().__init__(self.message)
