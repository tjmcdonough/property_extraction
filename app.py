from fastapi import FastAPI, Response
from scalar_fastapi import get_scalar_api_reference
from api.lease_entry_route import router as LeaseEntryRouter

app = FastAPI(title="Land Registry API", docs_url=None)

app.include_router(LeaseEntryRouter, tags=["Lease Entry"], prefix="/lease-entry")

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return Response(status_code=307, headers={"Location": "/docs"})

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Land Registry API",
    )