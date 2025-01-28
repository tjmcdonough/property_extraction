from abc import ABC, abstractmethod
from typing import List, Tuple
from lease_entry.types.lease_detail import LeaseDetail

class LeaseExtractor(ABC):
    @abstractmethod
    def extract_lease_detail(self, entry_number: str) -> LeaseDetail:
        pass
    
    @abstractmethod
    def extract_note(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        pass
    
    @abstractmethod
    def extract_lessee_title(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        pass
    
    @abstractmethod
    def extract_date_of_lease(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        pass
    
    @abstractmethod
    def extract_registration_date(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        pass
    
    @abstractmethod
    def extract_term(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        pass
    
    @abstractmethod
    def extract_plan_ref(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        pass
    
    @abstractmethod
    def extract_property_description(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        pass 