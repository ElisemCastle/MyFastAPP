import copy
from src.main import app
import os
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
import src.routers.cats as cats

load_dotenv()
TEST_API_KEY = os.getenv("TEST_API_KEY")

@pytest.fixture
def client(monkeypatch):
    # Fake database.
    store = {
        "101": {"breed": "orange_tabby", "name": "Mochi", "favorite_toy": "feather", "age": 3, "picture": "https://cataas.com/cat/orange,tabby,cute"},
        "102": {"breed": "siamese", "name": "Luna", "favorite_toy": "mouse", "age": 5, "picture": "https://cataas.com/cat/siamese"},
    }

    def fake_read_data():
        return copy.deepcopy(store)

    def fake_save_data(new_data):
        # persist to in-memory store
        store.clear()
        store.update(copy.deepcopy(new_data))

    monkeypatch.setattr(cats, "API_KEY", TEST_API_KEY)
    monkeypatch.setattr(cats, "read_data", fake_read_data)
    monkeypatch.setattr(cats, "save_data", fake_save_data)

    c = TestClient(app)
    c._store = store  # optional: useful for debugging in tests
    return c


@pytest.fixture
def auth_headers():
    return {"X-API-Key": TEST_API_KEY}