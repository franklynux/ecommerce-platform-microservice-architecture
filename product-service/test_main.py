from fastapi.testclient import TestClient
import pytest
from main import app, products_db

client = TestClient(app)

@pytest.fixture
def clear_db():
    products_db.clear()
    yield
    products_db.clear()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Product Service API"}

def test_create_product(clear_db):
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "inventory": 100
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["inventory"] == product_data["inventory"]
    assert "id" in data

def test_read_products(clear_db):
    # Create a product first
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "inventory": 100
    }
    client.post("/products/", json=product_data)
    
    # Get all products
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == product_data["name"]

def test_read_product(clear_db):
    # Create a product first
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "inventory": 100
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    # Get the product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == product_data["name"]

def test_read_product_not_found():
    response = client.get("/products/nonexistent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_update_product(clear_db):
    # Create a product first
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "inventory": 100
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    # Update the product
    updated_data = {
        "name": "Updated Product",
        "description": "This is an updated product",
        "price": 29.99,
        "inventory": 50
    }
    response = client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == updated_data["name"]
    assert data["price"] == updated_data["price"]

def test_update_product_not_found():
    updated_data = {
        "name": "Updated Product",
        "description": "This is an updated product",
        "price": 29.99,
        "inventory": 50
    }
    response = client.put("/products/nonexistent-id", json=updated_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_delete_product(clear_db):
    # Create a product first
    product_data = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "inventory": 100
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    # Delete the product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}
    
    # Verify it's deleted
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_delete_product_not_found():
    response = client.delete("/products/nonexistent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}