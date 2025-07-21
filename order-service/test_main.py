from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock
from main import app, orders_db, OrderStatus

client = TestClient(app)

@pytest.fixture
def clear_db():
    orders_db.clear()
    yield
    orders_db.clear()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Order Service API"}

def test_create_order(clear_db):
    order_data = {"user_id": "test-user-1", "cart_id": "test-cart-1"}
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["user_id"] == order_data["user_id"]
    assert "id" in data
    assert "items" in data
    assert "total_amount" in data
    assert data["status"] == OrderStatus.PENDING
    assert "created_at" in data

def test_read_orders(clear_db):
    # Create an order first
    order_data = {"user_id": "test-user-1", "cart_id": "test-cart-1"}
    client.post("/orders/", json=order_data)
    
    # Get all orders
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == order_data["user_id"]

def test_read_orders_by_user(clear_db):
    # Create orders for different users
    order_data1 = {"user_id": "test-user-1", "cart_id": "test-cart-1"}
    order_data2 = {"user_id": "test-user-2", "cart_id": "test-cart-2"}
    client.post("/orders/", json=order_data1)
    client.post("/orders/", json=order_data2)
    
    # Get orders for specific user
    response = client.get("/orders/?user_id=test-user-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == "test-user-1"

def test_read_order(clear_db):
    # Create an order first
    order_data = {"user_id": "test-user-1", "cart_id": "test-cart-1"}
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Get the order
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["user_id"] == order_data["user_id"]

def test_read_order_not_found():
    response = client.get("/orders/nonexistent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}

def test_update_order_status(clear_db):
    # Create an order first
    order_data = {"user_id": "test-user-1", "cart_id": "test-cart-1"}
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Update order status
    response = client.put(f"/orders/{order_id}/status", params={"status": "shipped"})
    assert response.status_code == 200
    
    # The API returns the enum object in the message
    assert response.json() == {"message": f"Order status updated to {OrderStatus.SHIPPED}"}
    
    # Verify status was updated
    get_response = client.get(f"/orders/{order_id}")
    order = get_response.json()
    assert order["status"] == "shipped"

def test_update_order_status_not_found():
    response = client.put("/orders/nonexistent-id/status", params={"status": "shipped"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}