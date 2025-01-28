import json
from typing import List
from land_registry.types.lease_schedule import LeaseSchedule, LeaseScheduleList, EntryText

class LandRegistryService:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self) -> dict:
        """Load JSON data from file."""
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _parse_data(self, data: dict) -> List[LeaseSchedule]:
        """Parse JSON data using Pydantic model."""
        return LeaseScheduleList.model_validate(data).root
    
    def list(self) -> List[LeaseSchedule]:
      """Parse JSON data using Pydantic model."""
      data = self._load_data()
      return self._parse_data(data)
    
    def get(self, entry_number: str) -> EntryText:
      """Get a lease schedule by its id."""
      notices = self.list()
      for notice in notices:
            for entry in notice.leaseschedule.scheduleEntry:
                if entry.entryNumber == entry_number:
                    return entry
      return None
    

    def process_lease_schedules(self) -> None:
        """Process all lease schedules and their entries."""
        notices = self.list()

        for lease_schedule in notices:
            self._process_lease_schedule(lease_schedule)

    def _process_lease_schedule(self, lease_schedule: LeaseSchedule) -> None:
        """Process individual lease schedule entries."""
        for entry in lease_schedule.leaseschedule.scheduleEntry:
            self._print_entry_details(entry)

    def _print_entry_details(self, entry: EntryText) -> None:
        """Print details of a single entry."""
        print(f"Entry Number: {entry.entryNumber}")
        print(f"Entry Date: {entry.entryDate}")
        print(f"Entry Type: {entry.entryType}")
        print(f"Entry Text: {entry.entryText}")
        print("---") 