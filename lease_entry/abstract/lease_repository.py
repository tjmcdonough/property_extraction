from abc import ABC, abstractmethod
from typing import List, Protocol
from land_registry.types.lease_schedule import EntryText

class LeaseRepository(ABC):
    @abstractmethod
    def list(self) -> List[EntryText]:
        pass
    
    @abstractmethod
    def get(self, entry_number: str) -> EntryText:
        pass