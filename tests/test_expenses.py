import uuid
from decimal import Decimal
from types import SimpleNamespace
from datetime import datetime, timezone

EXPENSE_ID = uuid.uuid4()
USER_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)

FAKE_EXPENSE_ORM = SimpleNamespace(
    id=EXPENSE_ID,
    user_id=USER_ID,
    title="Dinner",
    description=None,
    total_amount=Decimal("50.00"),
    currency="COP",
    category="food",
    merchant=None,
    type="personal",
    payment_method=None,
    expense_date=NOW,
    ai_notes=None,
    created_at=NOW,
    updated_at=NOW,
)


def test_create_expense(client, mock_db):
    def set_attrs(obj):
        obj.id = EXPENSE_ID
        obj.expense_date = NOW
        obj.created_at = NOW
        obj.updated_at = NOW

    mock_db.refresh.side_effect = set_attrs

    response = client.post("/expenses/", json={
        "user_id": str(USER_ID),
        "title": "Dinner",
        "total_amount": "50.00",
    })

    assert response.status_code == 201
    assert response.json()["title"] == "Dinner"


def test_list_expenses(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_EXPENSE_ORM]

    response = client.get("/expenses/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_expenses_by_user(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_EXPENSE_ORM]

    response = client.get(f"/expenses/user/{USER_ID}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_expense(client, mock_db):
    mock_db.get.return_value = FAKE_EXPENSE_ORM

    response = client.get(f"/expenses/{EXPENSE_ID}")

    assert response.status_code == 200
    assert response.json()["title"] == "Dinner"


def test_get_expense_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.get(f"/expenses/{uuid.uuid4()}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_expense(client, mock_db):
    mock_db.get.return_value = FAKE_EXPENSE_ORM
    mock_db.refresh.side_effect = lambda obj: None

    response = client.patch(f"/expenses/{EXPENSE_ID}", json={"title": "Updated Dinner"})

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Dinner"


def test_update_expense_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.patch(f"/expenses/{uuid.uuid4()}", json={"title": "X"})

    assert response.status_code == 404


def test_delete_expense(client, mock_db):
    mock_db.get.return_value = FAKE_EXPENSE_ORM

    response = client.delete(f"/expenses/{EXPENSE_ID}")

    assert response.status_code == 204
    mock_db.delete.assert_called_once()


def test_delete_expense_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.delete(f"/expenses/{uuid.uuid4()}")

    assert response.status_code == 404
