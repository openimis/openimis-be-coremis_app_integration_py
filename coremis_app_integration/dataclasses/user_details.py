from dataclasses import dataclass


@dataclass
class UserDetails:
    id: int = None
    username: str = None
    fullname: str = None
    phone: str = None
    email: str = None
    firstRunDate: str = None
    institutionName: str = None
    loginCount: int = None
    lastLogin: str = None
    lastActivityDate: str = None
    lastSyncData: str = None
    deviceId: str = None
    requiresPasswordReset: bool = None
    active: bool = None
    dateCreated: str = None
