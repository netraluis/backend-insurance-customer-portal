# Backend Insurance Customer Portal

## Requirements
- Python 3.8+
- pip

## Installation and Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

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

## Swagger (API Documentation)

You can view the interactive Swagger UI at:
- [http://localhost:8000/docs](http://localhost:8000/docs)

The OpenAPI JSON schema is available at:
- [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Example Endpoints

All endpoints return mock/example data for easy testing with the frontend or tools like Postman/curl.

### Health Check
- `GET /v1/health` — Check if the server is running

### Auth
- `POST /v1/auth/magic-link` — Send magic link to user email
- `POST /v1/auth/set-password` — Set password using magic link token
- `POST /v1/auth/login` — User login
- `POST /v1/auth/reset-password` — User reset password (send reset email)
- `POST /v1/auth/register` — User registration
- `GET /v1/auth/me` — Get authenticated user info

### Policies
- `GET /v1/policies` — List all user policies (with filters and pagination)
- `GET /v1/policies/{id}` — Get policy details

### Claims
- `GET /v1/claims` — List user claims (with filters and pagination)
- `GET /v1/claims/{id}` — Get claim details
- `POST /v1/policies/{id}/claims` — Create a new claim for a policy

### Documents
- `GET /v1/documents` — List user documents (with filters and pagination)
- `GET /v1/documents/{id}` — Get/download a document
- `POST /v1/documents` — Upload a document

## Example curl/Postman Queries

### Health Check
```bash
curl http://localhost:8000/v1/health
```

### Auth
```bash
curl -X POST http://localhost:8000/v1/auth/magic-link -H 'Content-Type: application/json' -d '{"email": "user@example.com"}'

curl -X POST http://localhost:8000/v1/auth/set-password -H 'Content-Type: application/json' -d '{"token": "sometoken", "password": "newpassword"}'

curl -X POST http://localhost:8000/v1/auth/login -H 'Content-Type: application/json' -d '{"email": "user@example.com", "password": "password"}'

curl -X POST http://localhost:8000/v1/auth/reset-password -H 'Content-Type: application/json' -d '{"email": "user@example.com"}'

curl -X POST http://localhost:8000/v1/auth/register -H 'Content-Type: application/json' -d '{"first_name": "John", "last_name": "Doe", "birth_date": "1990-01-01", "document_id": "NRT123456", "email": "user@example.com", "address": "123 Main St", "user_id": "USR001", "username": "johndoe", "phone": "+123456789", "password": "password"}'

curl http://localhost:8000/v1/auth/me
```

### Policies
```bash
curl http://localhost:8000/v1/policies
curl http://localhost:8000/v1/policies/HOM123
```

### Claims
```bash
curl http://localhost:8000/v1/claims
curl http://localhost:8000/v1/claims/CLM001
curl -X POST http://localhost:8000/v1/policies/HOM123/claims -H 'Content-Type: application/json' -d '{"description": "Water damage in kitchen"}'
```

### Documents
```bash
curl http://localhost:8000/v1/documents
curl http://localhost:8000/v1/documents/DOC001
# For upload, use Postman or a tool that supports multipart/form-data
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

--- 