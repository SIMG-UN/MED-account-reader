import uuid
from decimal import Decimal
from types import SimpleNamespace
from datetime import datetime, timezone

PAYMENT_ID = uuid.uuid4()
SPLIT_ID = uuid.uuid4()
NOW = datetime.now(timezone.utc)

FAKE_PAYMENT_ORM = SimpleNamespace(
    id=PAYMENT_ID,
    expense_split_id=SPLIT_ID,
    amount_paid=Decimal("25.00"),
    method="cash",
    paid_at=NOW,
    note=None,
    created_at=NOW,
    updated_at=NOW,
)


def test_create_payment(client, mock_db):
    def set_attrs(obj):
        obj.id = PAYMENT_ID
        obj.paid_at = NOW
        obj.created_at = NOW
        obj.updated_at = NOW

    mock_db.refresh.side_effect = set_attrs

    response = client.post("/payments/", json={
        "expense_split_id": str(SPLIT_ID),
        "amount_paid": "25.00",
        "method": "cash",
    })

    assert response.status_code == 201
    assert response.json()["method"] == "cash"


def test_list_payments(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_PAYMENT_ORM]

    response = client.get("/payments/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_payments_by_split(client, mock_db):
    mock_db.scalars.return_value.all.return_value = [FAKE_PAYMENT_ORM]

    response = client.get(f"/payments/split/{SPLIT_ID}")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_payment(client, mock_db):
    mock_db.get.return_value = FAKE_PAYMENT_ORM

    response = client.get(f"/payments/{PAYMENT_ID}")

    assert response.status_code == 200
    assert response.json()["method"] == "cash"


def test_get_payment_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.get(f"/payments/{uuid.uuid4()}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_payment(client, mock_db):
    mock_db.get.return_value = FAKE_PAYMENT_ORM
    mock_db.refresh.side_effect = lambda obj: None

    response = client.patch(f"/payments/{PAYMENT_ID}", json={"note": "updated"})

    assert response.status_code == 200
    assert response.json()["note"] == "updated"


def test_update_payment_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.patch(f"/payments/{uuid.uuid4()}", json={"note": "X"})

    assert response.status_code == 404


def test_delete_payment(client, mock_db):
    mock_db.get.return_value = FAKE_PAYMENT_ORM

    response = client.delete(f"/payments/{PAYMENT_ID}")

    assert response.status_code == 204
    mock_db.delete.assert_called_once()


def test_delete_payment_not_found(client, mock_db):
    mock_db.get.return_value = None

    response = client.delete(f"/payments/{uuid.uuid4()}")

    assert response.status_code == 404
