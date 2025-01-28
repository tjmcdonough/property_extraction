from typing import List, Optional, Union
from pydantic import BaseModel, RootModel

class EntryText(BaseModel):
    entryNumber: Optional[str] = None
    entryDate: str
    entryType: str
    entryText: List[Union[str, None]]

class ScheduleEntry(BaseModel):
    scheduleType: Optional[str] = None
    scheduleEntry: List[EntryText]

class LeaseSchedule(BaseModel):
    leaseschedule: ScheduleEntry

class LeaseScheduleList(RootModel[List[LeaseSchedule]]):
    root: List[LeaseSchedule]