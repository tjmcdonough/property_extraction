# property_extraction

## Setup and Installation

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

- Windows:

```bash
.\.venv\Scripts\activate
```

- Unix/MacOS:

```bash
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install --upgrade -r requirements.txt
```

4. Run the application:

```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```

## API Usage

The API provides two main endpoints for extracting lease information:

### 1. Get All Lease Entries (Paginated)

```bash
curl http://localhost:8080/lease-entry/extract?page=1&page_size=100
```

Response format:
```json
{
  "page": 1,
  "total_pages": 10,
  "total_items": 1000,
  "data": [
    {
      "registration_date_and_plan_ref": "2020-01-01 Plan ref: ABC123",
      "property_description": "Ground floor shop",
      "date_of_lease_and_term": "01.01.2020 25 years",
      "lessee_title": "ACME Corporation",
      "note_1": "Additional notes"
    }
    // ... more entries ...
  ]
}
```

### 2. Get Specific Lease Entry

```bash
curl http://localhost:8080/lease-entry/ABC123/extract
```

Response format:
```json
{
  "registration_date_and_plan_ref": "2020-01-01 Plan ref: ABC123",
  "property_description": "Ground floor shop",
  "date_of_lease_and_term": "01.01.2020 25 years",
  "lessee_title": "ACME Corporation",
  "note_1": "Additional notes"
}
```

Both endpoints will return a 404 error if the entry is not found, or a 500 error if there's a server-side issue.