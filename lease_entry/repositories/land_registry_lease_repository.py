from typing import List
from land_registry.types.lease_schedule import EntryText
from land_registry.services.land_registry_service import LandRegistryService
from lease_entry.abstract.lease_repository import LeaseRepository

class LandRegistryLeaseRepository(LeaseRepository):
    def __init__(self, land_registry_service: LandRegistryService):
        self.land_registry_service = land_registry_service
    
    def list(self) -> List[EntryText]:
        return self.land_registry_service.list()
    
    def get(self, entry_number: str) -> EntryText:
        return self.land_registry_service.get(entry_number) 