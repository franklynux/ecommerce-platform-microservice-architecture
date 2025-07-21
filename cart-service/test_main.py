from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock
from main import app, carts_db

client = TestClient(app)

@pytest.fixture
def clear_db():
    carts_db.clear()
    yield
    carts_db.clear()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Cart Service API"}

def test_create_cart(clear_db):
    cart_data = {"user_id": "test-user-1"}
    response = client.post("/carts/", json=cart_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["user_id"] == cart_data["user_id"]
    assert data["items"] == []
    assert "id" in data

def test_read_cart(clear_db):
    # Create a cart first
    cart_data = {"user_id": "test-user-1"}
    create_response = client.post("/carts/", json=cart_data)
    cart_id = create_response.json()["id"]
    
    # Get the cart
    response = client.get(f"/carts/{cart_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cart_id
    assert data["user_id"] == cart_data["user_id"]
    assert data["items"] == []

def test_read_cart_not_found():
    response = client.get("/carts/nonexistent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart not found"}

def test_add_item_to_cart(clear_db):
    # Create a cart first
    cart_data = {"user_id": "test-user-1"}
    create_response = client.post("/carts/", json=cart_data)
    cart_id = create_response.json()["id"]
    
    # Add item to cart
    item_data = {"product_id": "test-product-1", "quantity": 2}
    response = client.post(f"/carts/{cart_id}/items", json=item_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Item added to cart"}
    
    # Verify item was added
    get_response = client.get(f"/carts/{cart_id}")
    cart = get_response.json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["product_id"] == item_data["product_id"]
    assert cart["items"][0]["quantity"] == item_data["quantity"]

def test_add_item_to_cart_update_quantity(clear_db):
    # Create a cart first
    cart_data = {"user_id": "test-user-1"}
    create_response = client.post("/carts/", json=cart_data)
    cart_id = create_response.json()["id"]
    
    # Add item to cart
    item_data = {"product_id": "test-product-1", "quantity": 2}
    client.post(f"/carts/{cart_id}/items", json=item_data)
    
    # Add same item again
    item_data = {"product_id": "test-product-1", "quantity": 3}
    response = client.post(f"/carts/{cart_id}/items", json=item_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Item quantity updated in cart"}
    
    # Verify quantity was updated
    get_response = client.get(f"/carts/{cart_id}")
    cart = get_response.json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["product_id"] == item_data["product_id"]
    assert cart["items"][0]["quantity"] == 5  # 2 + 3

def test_add_item_to_nonexistent_cart():
    item_data = {"product_id": "test-product-1", "quantity": 2}
    response = client.post("/carts/nonexistent-id/items", json=item_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart not found"}

def test_remove_item_from_cart(clear_db):
    # Create a cart first
    cart_data = {"user_id": "test-user-1"}
    create_response = client.post("/carts/", json=cart_data)
    cart_id = create_response.json()["id"]
    
    # Add items to cart
    item1_data = {"product_id": "test-product-1", "quantity": 2}
    item2_data = {"product_id": "test-product-2", "quantity": 1}
    client.post(f"/carts/{cart_id}/items", json=item1_data)
    client.post(f"/carts/{cart_id}/items", json=item2_data)
    
    # Remove an item
    response = client.delete(f"/carts/{cart_id}/items/test-product-1")
    assert response.status_code == 200
    assert response.json() == {"message": "Item removed from cart"}
    
    # Verify item was removed
    get_response = client.get(f"/carts/{cart_id}")
    cart = get_response.json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["product_id"] == "test-product-2"

def test_remove_item_from_nonexistent_cart():
    response = client.delete("/carts/nonexistent-id/items/test-product-1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart not found"}

def test_clear_cart(clear_db):
    # Create a cart first
    cart_data = {"user_id": "test-user-1"}
    create_response = client.post("/carts/", json=cart_data)
    cart_id = create_response.json()["id"]
    
    # Add item to cart
    item_data = {"product_id": "test-product-1", "quantity": 2}
    client.post(f"/carts/{cart_id}/items", json=item_data)
    
    # Clear the cart
    response = client.delete(f"/carts/{cart_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Cart cleared"}
    
    # Verify cart is empty
    get_response = client.get(f"/carts/{cart_id}")
    cart = get_response.json()
    assert cart["items"] == []

def test_clear_nonexistent_cart():
    response = client.delete("/carts/nonexistent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cart not found"}