from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

class PageScanResultStatus(Enum):
    OK = "OK"
    ERR = "ERR"
    SETUP = "SETUP"

@dataclass
class Profile:
    id: str
    is_alum: Optional[bool] = None
    fullname: Optional[str] = None
    location: Optional[str] = None #should this be it's own datatype?
    connections: Optional[str] = None # Not sure if int is appr. I see some listings like ">900"

    @classmethod
    def from_record(cls, tup: Optional[tuple] = None) -> Union['Profile', None]:
        if tup is None:
            return None
        expected_vals = 8
        if len(tup) != expected_vals:
            raise ValueError(f"Provided tuple is expected to have {expected_vals} values")
        return Profile(id=tup[3], is_alum=tup[4], fullname=tup[5], connections=tup[6])

    def to_tuple(self):
        return (self.id, self.is_alum, self.fullname, self.location, self.connections)

@dataclass
class PageScanResult:
    """Return type for an individual page scan"""
    status: PageScanResultStatus
    found_ids: list[str] #python 3.9 or later
    profile: Optional[Profile] = None