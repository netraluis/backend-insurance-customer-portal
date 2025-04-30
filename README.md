# Backend Insurance Customer Portal

## Requirements
- Python 3.8+
- pip
- python-dotenv (for loading environment variables from .env)

## Installation and Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Environment Variables

You must set the following environment variables for Supabase integration in a `.env` file in the project root. The variables will be loaded automatically using `python-dotenv`:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon or service role key

Example `.env` file:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-role-key
```

> **Best Practice:**
> - Never commit your `.env` file to version control (e.g., Git). It should always be listed in your `.gitignore`.
> - Do not share your `.env` file or sensitive keys publicly.
> - Use different keys for development and production environments.

## Start the Server

```bash
uvicorn app.main:app --reload
```

## Update TypeScript Types (for frontend)

Make sure the backend is running, then run:

```bash
npx openapi-typescript http://localhost:8000/v1/openapi.json --output src/types/openapi-types.ts
```

## API Versioning

All endpoints are now prefixed with `/v1` (e.g., `/v1/health`, `/v1/auth/login`).

## Authentication and Protected Endpoints (Supabase)

- **Authentication and session management are handled entirely by Supabase.**
- The frontend (e.g., React, Next.js) uses the Supabase JS client for login, registration, magic link, etc.
- After login, the frontend receives a JWT (session token) from Supabase.
- The frontend must send this token in the `Authorization` header for all protected backend requests:

```
Authorization: Bearer <your_supabase_jwt>
```

- The backend uses the official Supabase Python client (`supabase-py`) to validate the token and obtain the user for each protected endpoint.
- **No JWT Secret is needed in the backend.**
- All protected endpoints use the dependency:

```python
def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    res = supabase.auth.get_user(token)
    if not res.get("user"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return res["user"]
```

And in the endpoints:

```python
@router.get("/me")
def me(user=Depends(get_current_user)):
    return {"id": user["id"], "email": user["email"]}
```

- If the token is invalid or missing, the backend will automatically return a 401 error.

## Protected Endpoints

All the following endpoints **require a valid Supabase Bearer token** in the `Authorization` header:
- `GET /v1/auth/me`
- All `/v1/policies/*` endpoints
- All `/v1/claims/*` endpoints
- All `/v1/documents/*` endpoints

## Swagger (API Documentation)

You can view the interactive Swagger UI at:
- [http://localhost:8000/docs](http://localhost:8000/docs)

The OpenAPI JSON schema is available at:
- [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Example Endpoints

All endpoints return mock/example data for easy testing with the frontend or tools like Postman/curl.

### Health Check
- `GET /v1/health` — Check if the server is running

### Auth (Supabase)
- `POST /v1/auth/magic-link` — Send magic link to user email
- `POST /v1/auth/set-password` — Set password using magic link token
- `POST /v1/auth/login` — User login
- `POST /v1/auth/reset-password` — User reset password (send reset email)
- `POST /v1/auth/register` — User registration (mock)
- `GET /v1/auth/me` — Get authenticated user info (**requires Bearer token**)

### Policies (**requires Bearer token**)
- `GET /v1/policies` — List all user policies (with filters and pagination)
- `GET /v1/policies/{id}` — Get policy details

### Claims (**requires Bearer token**)
- `GET /v1/claims` — List user claims (with filters and pagination, e.g. `/claims?policy_id=HOM123`)
- `GET /v1/claims/{id}` — Get claim details
- `POST /v1/claims` — Create a new claim (send `policy_id` in the body)

Example body for creating a claim:
```json
{
  "description": "Water damage in kitchen",
  "open_date": "2024-06-01",
  "policy_id": "HOM123"
}
```

### Documents (**requires Bearer token**)
- `GET /v1/documents` — List user documents (with filters and pagination)
- `GET /v1/documents/{id}` — Get/download a document
- `POST /v1/documents` — Upload a document

## Example curl/Postman Queries

### Health Check
```bash
curl http://localhost:8000/v1/health
```

### Auth (Supabase)
```bash
curl -X POST http://localhost:8000/v1/auth/magic-link -H 'Content-Type: application/json' -d '{"email": "user@example.com"}'

curl -X POST http://localhost:8000/v1/auth/set-password -H 'Content-Type: application/json' -d '{"token": "sometoken", "password": "newpassword"}'

curl -X POST http://localhost:8000/v1/auth/login -H 'Content-Type: application/json' -d '{"email": "user@example.com", "password": "password"}'

curl -X POST http://localhost:8000/v1/auth/reset-password -H 'Content-Type: application/json' -d '{"email": "user@example.com"}'

curl -X POST http://localhost:8000/v1/auth/register -H 'Content-Type: application/json' -d '{"first_name": "John", "last_name": "Doe", "birth_date": "1990-01-01", "document_id": "NRT123456", "email": "user@example.com", "address": "123 Main St", "user_id": "USR001", "username": "johndoe", "phone": "+123456789", "password": "password"}'

# Requires Bearer token:
curl -H 'Authorization: Bearer <your_supabase_jwt>' http://localhost:8000/v1/auth/me
```

### Policies (protected)
```bash
curl -H 'Authorization: Bearer <your_supabase_jwt>' http://localhost:8000/v1/policies
curl -H 'Authorization: Bearer <your_supabase_jwt>' http://localhost:8000/v1/policies/HOM123
```

### Claims (protected)
```bash
curl -H 'Authorization: Bearer <your_supabase_jwt>' http://localhost:8000/v1/claims
curl -H 'Authorization: Bearer <your_supabase_jwt>' http://localhost:8000/v1/claims/CLM001
curl -X POST -H 'Authorization: Bearer <your_supabase_jwt>' -H 'Content-Type: application/json' http://localhost:8000/v1/policies/HOM123/claims -d '{"description": "Water damage in kitchen"}'
```

### Documents (protected)
```bash
curl -H 'Authorization: Bearer <your_supabase_jwt>' http://localhost:8000/v1/documents
curl -H 'Authorization: Bearer <your_supabase_jwt>' http://localhost:8000/v1/documents/DOC001
# For upload, use Postman or a tool that supports multipart/form-data and include the Bearer token
```

---

All endpoints return mock/example data to facilitate frontend development.

## Package Justification

- **fastapi**: Chosen for its modern, high-performance, and easy-to-use API design, automatic OpenAPI/Swagger generation, and async support. Alternatives: Flask (less async, less automatic docs), Django REST Framework (heavier, more opinionated), Tornado (lower-level, less batteries-included).
- **uvicorn[standard]**: ASGI server recommended for FastAPI, supports async and hot-reload. Alternatives: Hypercorn (similar, but Uvicorn is more widely used with FastAPI), Daphne (older, less popular for FastAPI).
- **pydantic**: Used for data validation and serialization, tightly integrated with FastAPI. Alternatives: Marshmallow (not as tightly integrated with FastAPI), dataclasses (less validation features).
- **python-jose[cryptography]**: For JWT token creation/validation, secure and widely used. Alternatives: PyJWT (less features, less secure by default), authlib (more complex, broader scope).
- **passlib[bcrypt]**: For secure password hashing. Alternatives: bcrypt (lower-level, less features), argon2-cffi (more secure but less common in Python web stacks).
- **sqlalchemy**: For ORM/database access, if you want to persist data. Alternatives: Tortoise ORM (async, less mature), peewee (simpler, less features), Django ORM (tied to Django framework).
- **email-validator**: Required by Pydantic for validating email fields. Alternatives: validate_email (less integrated), custom regex (less robust).
- **python-multipart**: Required by FastAPI for handling form data and file uploads. Alternatives: starlette's built-in multipart (lower-level, less user-friendly).
- **supabase**: Official Python client for Supabase, used for authentication and user management.

## How to Receive Filters and Parameters in Endpoints

In FastAPI, you can easily receive filters (query parameters), path parameters, and body parameters in your endpoints:

### Query Parameters (Filters)

Use the `Query` helper to define filters in your endpoint function:

```python
from fastapi import Query
from typing import Optional

@router.get("/claims")
def list_claims(
    status: Optional[str] = Query(None, description="Filter by claim status"),
    type: Optional[str] = Query(None, description="Filter by claim type"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Page size for pagination"),
    user=Depends(get_current_user)
):
    # Use 'status', 'type', 'page', 'page_size' as filters in your logic
    ...
```

If the frontend calls `/claims?status=Open&type=Auto`, those values are automatically available in the `status` and `type` arguments.

### Path Parameters

Define them in the route and as function arguments:

```python
@router.get("/claims/{id}")
def get_claim(id: str, user=Depends(get_current_user)):
    # 'id' will contain the value from the URL path
    ...
```

### Body Parameters

Use a Pydantic model as a function argument for POST/PUT requests:

```python
from app.models.claim import ClaimCreateRequest

@router.post("/claims")
def create_claim(data: ClaimCreateRequest, user=Depends(get_current_user)):
    # 'data' will be an instance of ClaimCreateRequest with the parsed JSON body
    ...
```

### Example: Combining Query, Path, and Body Parameters

You can combine all types of parameters in a single endpoint:

```python
from fastapi import Query, Path, Body, Depends
from typing import Optional
from app.models.claim import ClaimCreateRequest

@router.post("/claims/{claim_id}")
def update_claim(
    claim_id: str = Path(..., description="Claim ID from the URL"),
    status: Optional[str] = Query(None, description="Optional status filter"),
    data: ClaimCreateRequest = Body(...),
    user=Depends(get_current_user)
):
    # 'claim_id' from the path, 'status' from query, 'data' from body
    ...
```

--- 