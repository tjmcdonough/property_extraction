import re
from typing import List, Tuple
from lease_entry.abstract.lease_extractor import LeaseExtractor
from lease_entry.abstract.lease_repository import LeaseRepository
from lease_entry.types.lease_detail import LeaseDetail
from utils.types import PaginatedResponse

class LeaseDetailExtractor(LeaseExtractor):
    def __init__(self, repository: LeaseRepository):
        self.repository = repository
    
    def extract_lease_detail(self, entry_number: str) -> LeaseDetail:
        original_entry = self.repository.get(entry_number)
        lines = original_entry.entryText
        
        note, lines = self.extract_note(lines)
        lessee_title, lines = self.extract_lessee_title(lines)
        date_of_lease, lines = self.extract_date_of_lease(lines)
        registration_date, lines = self.extract_registration_date(lines)
        term, lines = self.extract_term(lines) if len(lines) >= 2 else (None, lines)
        plan_ref, lines = self.extract_plan_ref(lines)
        property_description, lines = self.extract_property_description(lines)

        return LeaseDetail(
            registration_date_and_plan_ref=f"{registration_date} {plan_ref}",
            property_description=property_description,
            date_of_lease_and_term=f"{date_of_lease} {term}",
            lessee_title=lessee_title,
            note_1=note
        )

    def extract_property_description(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        """
        Extract property description from remaining lines.
        Returns a tuple of (property_description, remaining_lines).
        """
        property_description = ' '.join(line.strip() for line in lines if line.strip())
        return property_description if property_description else None, []
    
    def extract_lessee_title(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        """
        Extract the lessee title from the lines and return both the title and remaining lines.
        Returns a tuple of (lessee_title, remaining_lines).
        """
        pattern = r'([A-Z]GL\d{6})\s*$'
        match = re.search(pattern, lines[0])
        
        if match:
            lessee_title = match.group(1)
            lines[0] = lines[0][:match.start()].strip()
        else:
            lessee_title = None
            
        return lessee_title, lines
    
    def extract_date_of_lease(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        """Extract the last date found in the first line and return updated lines."""
        pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})'
        matches = list(re.finditer(pattern, lines[0]))
        if matches:
            date_of_lease = matches[-1].group(1)
            lines[0] = lines[0][:matches[-1].start()].strip()
        else:
            date_of_lease = None
            
        return date_of_lease, lines
    
    def extract_registration_date(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        """Extract registration date from first line and return updated lines."""
        pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})'
        matches = list(re.finditer(pattern, lines[0]))
        if matches:
            registration_date = matches[-1].group(1)
            lines[0] = re.sub(pattern, '', lines[0]).strip()
        else:
            registration_date = None
            
        return registration_date, lines

    def extract_term(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        """
        Extract the term from the remaining lines and return both term and modified lines.
        """
        term_pattern = r'(\d+)\s+years\s+from'
        term_match = re.search(term_pattern, lines[1])
        
        if term_match and len(lines) > 1:
            date_pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})'
            date_match = re.search(date_pattern, lines[2])
            if date_match:
                term_years = term_match.group(1)
                start_date = date_match.group(1)
                lines[1] = lines[1][:term_match.start()].strip()
                lines[2] = lines[2][:date_match.start()].strip()
                return f"{term_years} years from {start_date}", lines
        
        return None, lines

    def extract_plan_ref(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        """
        Extract plan references from available lines.
        Returns a tuple of (plan_ref, remaining_lines).
        """
        if len(lines) <= 1:
            return None, lines
        
        plan_ref_parts = []
        
        patterns_by_line = [
            (1, [
                r'Edged and',
                r'tinted blue',
                r'(\d+)\s+in\s+blue\s+on'
            ]),
            (2, [
                r'numbered\s+(\d+)(?:\s+in)?',
                r'\(part of\)'
            ]),
            (3, [
                r'blue \(part of\)',
                r'plan 1',
                r'blue on'
            ]),
            (4, [
                r'supplementary'
            ]),
            (5, [
                r'plan 1'
            ])
        ]
        
        for line_idx, patterns in patterns_by_line:
            if len(lines) > line_idx:
                for pattern in patterns:
                    match = re.search(pattern, lines[line_idx], re.IGNORECASE)
                    if match:
                        plan_ref_parts.append(match.group(0))
                        lines[line_idx] = re.sub(pattern, '', lines[line_idx], flags=re.IGNORECASE).strip()
        
        plan_ref = ' '.join(plan_ref_parts) if plan_ref_parts else None
        return plan_ref, lines

    def extract_note(self, lines: List[str]) -> Tuple[str | None, List[str]]:
        """
        Extract note if the line starts with 'NOTE:' and return both the note and remaining lines.
        Returns a tuple of (note, remaining_lines).
        """
        pattern = r'^NOTE:\s*(.+)'
        possible_note_line = lines[-1]
        match = re.match(pattern, possible_note_line)
        
        if match:
            return possible_note_line, lines[:-1] 
        else:
            return None, lines 
        
    def get_paginated_entries(self, page: int = 1, page_size: int = 100) -> PaginatedResponse[LeaseDetail]:
      
        lease_schedules = self.repository.list()
        
        total_items = sum(
            len(lease_schedule.leaseschedule.scheduleEntry)
            for lease_schedule in lease_schedules
        )
        
        total_pages = (total_items + page_size - 1) // page_size
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_items)
        
        lease_details = []
        current_idx = 0
        
        for lease_schedule in lease_schedules:
            for entry in lease_schedule.leaseschedule.scheduleEntry:
                if current_idx >= end_idx:
                    break
                    
                if current_idx >= start_idx:
                    lease_detail = self.extract_lease_detail(entry.entryNumber)
                    lease_details.append(lease_detail)
                current_idx += 1
                
        return PaginatedResponse[LeaseDetail](
            page=page,
            total_pages=total_pages,
            total_items=total_items,
            data=lease_details
        ) 