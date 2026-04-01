import uuid
from types import SimpleNamespace
from datetime import datetime, timezone

MSG_ID = uuid.uuid4()
CHAT_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)

FAKE_MSG_ORM = SimpleNamespace(
    id=MSG_ID,
    chat_id=CHAT_ID,
    role="user",
    content="Hello!",
    created_at=NOW,
)


def test_create_message(client, mock_db):
    def set_attrs(obj):
        obj.id = MSG_ID
        obj.created_at = NOW

    mock_db.refresh.side_effect = set_attrs

    response = client.post("/messages/", json={
        "chat_id": str(CHAT_ID),
        "role": "user",
        "content": "Hello!",
    })

    assert response.status_code == 201
    assert response.json()["role"] == "user"


def test_list_messages_by_chat(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_MSG_ORM]

    response = client.get(f"/messages/chat/{CHAT_ID}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_message(client, mock_db):
    mock_db.get.return_value = FAKE_MSG_ORM

    response = client.get(f"/messages/{MSG_ID}")

    assert response.status_code == 200
    assert response.json()["role"] == "user"


def test_get_message_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.get(f"/messages/{uuid.uuid4()}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_message(client, mock_db):
    mock_db.get.return_value = FAKE_MSG_ORM

    response = client.delete(f"/messages/{MSG_ID}")

    assert response.status_code == 204
    mock_db.delete.assert_called_once()


def test_delete_message_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.delete(f"/messages/{uuid.uuid4()}")

    assert response.status_code == 404
