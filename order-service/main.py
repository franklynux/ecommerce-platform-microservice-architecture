from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid
import httpx
from datetime import datetime
import os

root_path = os.getenv("ROOT_PATH", "")
app = FastAPI(title="Order Service API", root_path=root_path)

# Order status enum
class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Order item model
class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

# Order model
class Order(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus
    created_at: str

# Order creation model
class OrderCreate(BaseModel):
    user_id: str
    cart_id: str

# In-memory database
orders_db = {}

# Service URLs (will be updated in Kubernetes deployment)
CART_SERVICE_URL = "http://cart-service:8000"
PRODUCT_SERVICE_URL = "http://product-service:8000"

@app.get("/")
def read_root():
    return {"message": "Order Service API"}

@app.post("/orders/", response_model=Order)
async def create_order(order_create: OrderCreate):
    # In a real system, we would:
    # 1. Get the cart from the cart service
    # 2. Get product details from the product service
    # 3. Calculate the total amount
    # 4. Create the order
    # 5. Clear the cart
    
    # Simulate getting cart items
    cart_items = [
        {"product_id": "sample-product-1", "quantity": 2},
        {"product_id": "sample-product-2", "quantity": 1}
    ]
    
    # Simulate getting product prices
    product_prices = {
        "sample-product-1": 29.99,
        "sample-product-2": 49.99
    }
    
    # Create order items
    order_items = []
    total_amount = 0
    
    for item in cart_items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        price = product_prices.get(product_id, 0)
        
        order_items.append({
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        })
        
        total_amount += price * quantity
    
    # Create order
    order_id = str(uuid.uuid4())
    new_order = {
        "id": order_id,
        "user_id": order_create.user_id,
        "items": order_items,
        "total_amount": total_amount,
        "status": OrderStatus.PENDING,
        "created_at": datetime.now().isoformat()
    }
    
    orders_db[order_id] = new_order
    
    # In a real system, we would clear the cart here
    
    return new_order

@app.get("/orders/", response_model=List[Order])
def read_orders(user_id: Optional[str] = None):
    if user_id:
        return [order for order in orders_db.values() if order["user_id"] == user_id]
    return list(orders_db.values())

@app.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: str, status: OrderStatus):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    orders_db[order_id]["status"] = status
    return {"message": f"Order status updated to {status}"}