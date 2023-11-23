from dataclasses import dataclass
from enum import Enum
from typing import Optional

class PageScanResultStatus(Enum):
    OK = "OK"
    ERR = "ERR"
    SETUP = "SETUP"

@dataclass
class Profile:
    # Profile(id="", fullname="", location="")
    id: str
    fullname: Optional[str] = None
    location: Optional[str] = None #should this be it's own datatype?
    is_alum: Optional[bool] = None
    connections: Optional[str] = None # Not sure if int is appr. I see some listings like ">900"

@dataclass
class PageScanResult:
    """Return type for an individual page scan"""
    status: PageScanResultStatus
    found_ids: list[str] #python 3.9 or later
    profile: Optional[Profile] = None