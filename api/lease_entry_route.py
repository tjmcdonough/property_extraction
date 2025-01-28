from fastapi import APIRouter, HTTPException, Depends
from typing import List
from land_registry.services.land_registry_service import LandRegistryService
from lease_entry.repositories.land_registry_lease_repository import LandRegistryLeaseRepository
from lease_entry.services.lease_detail_extractor import LeaseDetailExtractor
from lease_entry.types.lease_detail import LeaseDetail
from utils.types import PaginatedResponse

router = APIRouter()

def get_land_registry_service():
    return LandRegistryService("land_registry/notices_of_lease.json")

def get_repository(service: LandRegistryService = Depends(get_land_registry_service)):
    return LandRegistryLeaseRepository(service)

def get_extractor(repository = Depends(get_repository)):
    return LeaseDetailExtractor(repository)

@router.get("/extract")
async def extract_lease_entries(
    page: int = 1,
    page_size: int = 100,
    service: LeaseDetailExtractor = Depends(get_extractor)
) -> PaginatedResponse[LeaseDetail]:
    """Extract all lease schedule entries with pagination."""
    try:
        response = service.get_paginated_entries(page, page_size)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{entry_number}/extract")
async def extract_lease_entry_from_entry_text(
    entry_number: str,
    extractor: LeaseDetailExtractor = Depends(get_extractor)
) -> LeaseDetail:
    """Get a specific entry by its number."""
    try:
        return extractor.extract_lease_detail(entry_number)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Entry not found")