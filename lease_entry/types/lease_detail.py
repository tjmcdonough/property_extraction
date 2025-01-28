from pydantic import BaseModel, Field

class LeaseDetail(BaseModel):
    registration_date_and_plan_ref: str | None = Field(None, description="The date of registration of the lease")
    property_description: str | None = Field(None, description="The description of the property")
    date_of_lease_and_term: str | None = Field(None, description="The date of the lease and the term")
    lessee_title: str | None = Field(None, description="The title of the lessee")
    note_1: str | None = Field(None, description="The first note of the lease")
