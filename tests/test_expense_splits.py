import uuid
from decimal import Decimal
from types import SimpleNamespace
from datetime import datetime, timezone

SPLIT_ID = uuid.uuid4()
EXPENSE_ID = uuid.uuid4()
CONTACT_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)

FAKE_SPLIT_ORM = SimpleNamespace(
    id=SPLIT_ID,
    expense_id=EXPENSE_ID,
    contact_id=CONTACT_ID,
    amount_owed=Decimal("25.00"),
    status="pending",
    due_date=None,
    created_at=NOW,
    updated_at=NOW,
)


def test_create_split(client, mock_db):
    def set_attrs(obj):
        obj.id = SPLIT_ID
        obj.created_at = NOW
        obj.updated_at = NOW

    mock_db.refresh.side_effect = set_attrs

    response = client.post("/expense-splits/", json={
        "expense_id": str(EXPENSE_ID),
        "contact_id": str(CONTACT_ID),
        "amount_owed": "25.00",
    })

    assert response.status_code == 201
    assert response.json()["status"] == "pending"


def test_list_splits(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_SPLIT_ORM]

    response = client.get("/expense-splits/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_splits_by_expense(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_SPLIT_ORM]

    response = client.get(f"/expense-splits/expense/{EXPENSE_ID}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_split(client, mock_db):
    mock_db.get.return_value = FAKE_SPLIT_ORM

    response = client.get(f"/expense-splits/{SPLIT_ID}")

    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_get_split_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.get(f"/expense-splits/{uuid.uuid4()}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_split(client, mock_db):
    mock_db.get.return_value = FAKE_SPLIT_ORM
    mock_db.refresh.side_effect = lambda obj: None

    response = client.patch(f"/expense-splits/{SPLIT_ID}", json={"status": "paid"})

    assert response.status_code == 200
    assert response.json()["status"] == "paid"


def test_update_split_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.patch(f"/expense-splits/{uuid.uuid4()}", json={"status": "paid"})

    assert response.status_code == 404


def test_delete_split(client, mock_db):
    mock_db.get.return_value = FAKE_SPLIT_ORM

    response = client.delete(f"/expense-splits/{SPLIT_ID}")

    assert response.status_code == 204
    mock_db.delete.assert_called_once()


def test_delete_split_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.delete(f"/expense-splits/{uuid.uuid4()}")

    assert response.status_code == 404
