from dataclasses import dataclass


@dataclass
class FailedResponse:
    status: bool = False
    count: int = 1
    result: str = ""
    message: str = "ERROR"
