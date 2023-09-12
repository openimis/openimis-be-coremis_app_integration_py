from dataclasses import dataclass, field
from coremis_app_integration.dataclasses.user_details import UserDetails


@dataclass
class SuccessResponse:
    status: bool = True
    count: int = 1
    result: UserDetails = field(default_factory=UserDetails)
    message: str = "SUCCESS"
