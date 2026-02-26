from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {'status': 'alive'}

def test_get_cats(client):
    response = client.get("/cats")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert data["total"] == 2
    assert len(data["data"]) == 2

def test_get_cats_filter_by_breed(client):
    response = client.get("/cats?breed=orange_tabby")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["data"][0]["breed"] == "orange_tabby"

def test_post_cat(client):
    new_cat = {
        "breed": "main_coon",
        "name": "Pumpkin",
        "favorite_toy": "string",
        "age": 2,
        "picture": "https://cataas.com/cat/fluffy,tabby,cute",
    }
    response = client.post("/cats", json=new_cat)
    # Add response.text to see why an assertion failed.
    assert response.status_code in (200, 201), response.json()
    body = response.json()
    assert "cat" in body
    assert body["cat"]["name"] == "Pumpkin"

    # Verify it was added.
    response2 = client.get("/cats")
    assert response2.status_code == 200
    assert response2.json()["total"] == 3

def test_delete_cat(client, auth_headers):
    response = client.delete("/cats/101", headers=auth_headers)
    assert response.status_code == 200, response.json()
    body = response.json()
    assert body["message"] == ("Cat successfully removed")
    assert body["cat"]["name"] == "Mochi"

    # Confirm it is deleted.
    response2 = client.delete("/cats/101", headers=auth_headers)
    assert response2.status_code == 404
    assert response2.json()["message"] == ("Cat not found")

def test_missing_api_key_reject(client):
    response = client.delete("/cats/101")
    assert response.status_code in (401, 403), response.json()
