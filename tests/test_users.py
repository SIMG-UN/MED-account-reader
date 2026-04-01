import uuid
from types import SimpleNamespace
from datetime import datetime, timezone

USER_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)

FAKE_USER_ORM = SimpleNamespace(
    id=USER_ID,
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    created_at=NOW,
    updated_at=NOW,
)


def test_create_user(client, mock_db):
    def set_attrs(obj):
        obj.id = USER_ID
        obj.created_at = NOW
        obj.updated_at = NOW

    mock_db.refresh.side_effect = set_attrs

    response = client.post("/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
    })

    assert response.status_code == 201
    assert response.json()["email"] == "john@example.com"


def test_list_users(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_USER_ORM]

    response = client.get("/users/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["first_name"] == "John"


def test_get_user(client, mock_db):
    mock_db.get.return_value = FAKE_USER_ORM

    response = client.get(f"/users/{USER_ID}")

    assert response.status_code == 200
    assert response.json()["first_name"] == "John"


def test_get_user_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.get(f"/users/{uuid.uuid4()}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_user(client, mock_db):
    mock_db.get.return_value = FAKE_USER_ORM
    mock_db.refresh.side_effect = lambda obj: None

    response = client.patch(f"/users/{USER_ID}", json={"first_name": "Jane"})

    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"


def test_update_user_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.patch(f"/users/{uuid.uuid4()}", json={"first_name": "Jane"})

    assert response.status_code == 404


def test_delete_user(client, mock_db):
    mock_db.get.return_value = FAKE_USER_ORM

    response = client.delete(f"/users/{USER_ID}")

    assert response.status_code == 204
    mock_db.delete.assert_called_once()


def test_delete_user_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.delete(f"/users/{uuid.uuid4()}")

    assert response.status_code == 404
