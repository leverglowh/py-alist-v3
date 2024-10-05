from typing import Dict

class Result:
    def __init__(self, code: int, message: str = '', data: Dict = None):
        """
        Result returned from RestAdapter
        :param code: Standard HTTP Status code
        :param message: Human readable result
        :param data: the response data
        """
        self.code = int(code)
        self.message = str(message)
        self.data = data