from typing import Any

class ParameterUnvalid(Exception):
    value: Any
    def __init__(self, value: Any) -> None: ...
