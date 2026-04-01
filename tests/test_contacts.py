import uuid
from types import SimpleNamespace
from datetime import datetime, timezone

CONTACT_ID = uuid.uuid4()
USER_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)

FAKE_CONTACT_ORM = SimpleNamespace(
    id=CONTACT_ID,
    user_id=USER_ID,
    name="Alice",
    email="alice@example.com",
    phone="123456789",
    created_at=NOW,
    updated_at=NOW,
)


def test_create_contact(client, mock_db):
    def set_attrs(obj):
        obj.id = CONTACT_ID
        obj.created_at = NOW
        obj.updated_at = NOW

    mock_db.refresh.side_effect = set_attrs

    response = client.post("/contacts/", json={
        "user_id": str(USER_ID),
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "123456789",
    })

    assert response.status_code == 201
    assert response.json()["name"] == "Alice"


def test_list_contacts(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_CONTACT_ORM]

    response = client.get("/contacts/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_contacts_by_user(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_CONTACT_ORM]

    response = client.get(f"/contacts/user/{USER_ID}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_contact(client, mock_db):
    mock_db.get.return_value = FAKE_CONTACT_ORM

    response = client.get(f"/contacts/{CONTACT_ID}")

    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_contact_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.get(f"/contacts/{uuid.uuid4()}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_contact(client, mock_db):
    mock_db.get.return_value = FAKE_CONTACT_ORM
    mock_db.refresh.side_effect = lambda obj: None

    response = client.patch(f"/contacts/{CONTACT_ID}", json={"name": "Alice Updated"})

    assert response.status_code == 200
    assert response.json()["name"] == "Alice Updated"


def test_update_contact_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.patch(f"/contacts/{uuid.uuid4()}", json={"name": "X"})

    assert response.status_code == 404


def test_delete_contact(client, mock_db):
    mock_db.get.return_value = FAKE_CONTACT_ORM

    response = client.delete(f"/contacts/{CONTACT_ID}")

    assert response.status_code == 204
    mock_db.delete.assert_called_once()


def test_delete_contact_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.delete(f"/contacts/{uuid.uuid4()}")

    assert response.status_code == 404
