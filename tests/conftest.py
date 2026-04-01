import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.database import db_dependency


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    def override():
        yield mock_db

    app.dependency_overrides[db_dependency] = override
    yield TestClient(app)
    app.dependency_overrides.clear()
