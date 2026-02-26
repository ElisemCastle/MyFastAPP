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

From the **root of the repository** run:

```bash
uvicorn src.main:app --reload
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
| `age`         | int  | Filter by age |
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

Save in a .env file locally.

```bash
API_KEY = "my-secret-key"
```
```bash
source .env
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

## 🧪 Deploy Locally with Kubernetes (Minikube)

This project can be deployed locally to Kubernetes using **Minikube + Helm + NGINX Ingress**.

These steps simulate a real production-style deployment where the app is accessed via a hostname instead of a port.

---

### 1) Install Minikube

Install using Homebrew (macOS):

```bash
brew install minikube
```

Start the cluster:

```bash
minikube start
```

---

### 2) Enable the NGINX Ingress Controller

```bash
minikube addons enable ingress
```

Wait ~30–60 seconds for the controller to fully start.

You can verify:

```bash
kubectl get pods -n ingress-nginx
```

All pods should show `Running`.

---

### 3) Deploy the Helm Chart

From the directory **above** the chart:

```bash
helm install fastapi-cat ./fastapi-cat
```

Verify the pods:

```bash
kubectl get pods
```

Wait until the `fastapi-cat` pod is `Running`.

---

### 4) Expose Ingress via LoadBalancer

By default the ingress controller uses a NodePort.  
We patch it to behave like a cloud LoadBalancer:

```bash
kubectl -n ingress-nginx patch svc ingress-nginx-controller -p '{"spec":{"type":"LoadBalancer"}}'
```

---

### 5) Run the Minikube Tunnel

Keep this running in a separate terminal:

```bash
minikube tunnel
```

> This command requires admin privileges because it creates network routes on your machine.

---

### 6) Update `/etc/hosts`

Edit the hosts file:

```bash
sudo vim /etc/hosts
```

Add the following line:

```
127.0.0.1 fastapi-cat.local
```

Save and exit.

---

### 7) Flush macOS DNS Cache

```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

---

### 8) Access the Application

Open in your browser:

```
http://fastapi-cat.local/login
```

or

```
http://fastapi-cat.local/docs
```

You are now accessing the FastAPI app through:
Kubernetes → Service → Ingress → Hostname routing.

---

### Helpful Commands

Check ingress:

```bash
kubectl get ingress
```

Check services:

```bash
kubectl get svc -n ingress-nginx
```

Delete the deployment:

```bash
helm uninstall fastapi-cat
```