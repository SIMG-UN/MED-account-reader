import uuid
from types import SimpleNamespace
from datetime import datetime, timezone

CHAT_ID = uuid.uuid4()
USER_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)

FAKE_CHAT_ORM = SimpleNamespace(
    id=CHAT_ID,
    user_id=USER_ID,
    title="My Chat",
    created_at=NOW,
    updated_at=NOW,
)


def test_create_chat(client, mock_db):
    def set_attrs(obj):
        obj.id = CHAT_ID
        obj.created_at = NOW
        obj.updated_at = NOW

    mock_db.refresh.side_effect = set_attrs

    response = client.post("/chats/", json={"user_id": str(USER_ID), "title": "My Chat"})

    assert response.status_code == 201
    assert response.json()["title"] == "My Chat"


def test_list_chats(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_CHAT_ORM]

    response = client.get("/chats/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_chats_by_user(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_CHAT_ORM]

    response = client.get(f"/chats/user/{USER_ID}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_chat(client, mock_db):
    mock_db.get.return_value = FAKE_CHAT_ORM

    response = client.get(f"/chats/{CHAT_ID}")

    assert response.status_code == 200
    assert response.json()["title"] == "My Chat"


def test_get_chat_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.get(f"/chats/{uuid.uuid4()}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_chat(client, mock_db):
    mock_db.get.return_value = FAKE_CHAT_ORM
    mock_db.refresh.side_effect = lambda obj: None

    response = client.patch(f"/chats/{CHAT_ID}", json={"title": "Updated"})

    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_chat_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.patch(f"/chats/{uuid.uuid4()}", json={"title": "X"})

    assert response.status_code == 404


def test_delete_chat(client, mock_db):
    mock_db.get.return_value = FAKE_CHAT_ORM

    response = client.delete(f"/chats/{CHAT_ID}")

    assert response.status_code == 204
    mock_db.delete.assert_called_once()


def test_delete_chat_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.delete(f"/chats/{uuid.uuid4()}")

    assert response.status_code == 404
