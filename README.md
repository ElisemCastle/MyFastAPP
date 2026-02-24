# 🐾 FastAPI Cat API

A small FastAPI project that serves cat data with pagination/filtering, includes a simple UI login page, and protects destructive actions with an API key (for testing).

---

## ✅ Getting Started

### 1) Install dependencies

Start virtual environment and install `requirements.txt`:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows PowerShell

pip install -r requirements.txt
```

---

### 2) Run the API (Uvicorn)

From the **root of the repository** (the directory that contains the `myfastapp/` folder), run:

```bash
uvicorn myfastapp.main:app --reload
```
Server will be available at:

- API root: `http://localhost:8000`
---

## 📖 API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🔎 Endpoints Overview

### GET `/cats`

Returns a paginated list of cats.

**Query parameters:**

| Parameter      | Type | Description |
|--------------|------|------------|
| `page_num`    | int  | Page number (default: 1) |
| `page_size`   | int  | Items per page (default: 10) |
| `breed`       | str  | Filter by breed |
| `favorite_toy`| str  | Filter by favorite toy |

**Example request**

```bash
curl "http://localhost:8000/cats?page_num=1&page_size=5&breed=Siamese"
```

**Example response**

```json
{
  "data": [...],
  "total": 25,
  "count": 5
}
```

---

## 🔐 Authentication / Authorization

### UI Login (username + password)

This project includes a simple UI that prompts for a **username and password**.

> Note: UI login is separate from the API-key requirement below. The API key specifically protects the delete endpoint.

---

### API Key Required for `/delete`

The `/delete` endpoint requires an API key header.

**Header name**

```
x-api-key
```

**Testing keys configured in the application**

```python
API_KEYS = {"secret_key_1", "my-secret-key"}
```

**Example request**

```bash
curl -X DELETE "http://localhost:8000/delete" \
  -H "x-api-key: my-secret-key"
```

If the header is missing or incorrect, the request will return an authorization error.

---

## 🧱 Pydantic Models

This application uses **Pydantic** (via FastAPI) to define and validate API data.

Pydantic models are used to:

- Validate incoming request data
- Ensure query parameters have the correct types
- Structure and serialize API responses
- Automatically generate the OpenAPI schema used by `/docs`

Because of this, the API will automatically return a validation error (HTTP 422) if a request contains invalid or incorrectly-typed data (for example, sending a string where an integer is expected).

Example:

If an endpoint expects:

```python
page_num: int
```

and a request sends:

```
/cats?page_num=abc
```

FastAPI (using Pydantic) will reject the request and return a structured validation error response.

---

## 🐳 Docker

### Deploy via Docker

```bash
docker build -t fastapi-cat-api .
```

### Run the container

```bash
docker run -p 8000:8000 fastapi-cat-api
```

Then open:

```
http://localhost:8000/docs
```
