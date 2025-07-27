from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uuid
import httpx
import os
from prometheus_fastapi_instrumentator import Instrumentator

root_path = os.getenv("ROOT_PATH", "")
app = FastAPI(title="Cart Service API", root_path=root_path)

# Initialize Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Cart item model
class CartItem(BaseModel):
    product_id: str
    quantity: int

# Cart model
class Cart(BaseModel):
    id: str
    user_id: str
    items: List[CartItem]

# In-memory database
carts_db = {}                # non-persistent data is stored here

# Product service URL (will be updated in Kubernetes deployment)
PRODUCT_SERVICE_URL = "http://product-service:8000"

@app.get("/")
def read_root():
    return {"message": "Cart Service API"}

# Cart creation model
class CartCreate(BaseModel):
    user_id: str

@app.post("/carts/", response_model=Cart)
def create_cart(cart_data: CartCreate):
    cart_id = str(uuid.uuid4())
    new_cart = {"id": cart_id, "user_id": cart_data.user_id, "items": []}
    carts_db[cart_id] = new_cart
    return new_cart

@app.get("/carts/{cart_id}", response_model=Cart)
def read_cart(cart_id: str):
    if cart_id not in carts_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    return carts_db[cart_id]

@app.post("/carts/{cart_id}/items")
async def add_item_to_cart(cart_id: str, item: CartItem):
    if cart_id not in carts_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Verify product exists (in a real system)
    # This would make an HTTP request to the product service
    # try:
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{item.product_id}")
    #         if response.status_code != 200:
    #             raise HTTPException(status_code=404, detail="Product not found")
    # except httpx.RequestError:
    #     raise HTTPException(status_code=503, detail="Product service unavailable")
    
    # Add item to cart
    cart = carts_db[cart_id]
    
    # Check if product already in cart
    for existing_item in cart["items"]:
        if existing_item["product_id"] == item.product_id:
            existing_item["quantity"] += item.quantity
            return {"message": "Item quantity updated in cart"}
    
    # Add new item
    cart["items"].append(item.model_dump())
    return {"message": "Item added to cart"}

@app.delete("/carts/{cart_id}/items/{product_id}")
def remove_item_from_cart(cart_id: str, product_id: str):
    if cart_id not in carts_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = carts_db[cart_id]
    cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]
    
    return {"message": "Item removed from cart"}

@app.delete("/carts/{cart_id}")
def clear_cart(cart_id: str):
    if cart_id not in carts_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    carts_db[cart_id]["items"] = []
    return {"message": "Cart cleared"}