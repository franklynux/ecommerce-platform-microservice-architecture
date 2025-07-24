from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os

root_path = os.getenv("ROOT_PATH", "")

app = FastAPI(title="Product Service API", root_path=root_path)

# Product model
class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    inventory: int

# Product creation model
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    inventory: int

# In-memory database
products_db = {}

@app.get("/")
def read_root():
    return {"message": "Product Service API"}

@app.post("/products/", response_model=Product)
def create_product(product: ProductCreate):
    product_id = str(uuid.uuid4())
    product_dict = product.model_dump()
    new_product = {**product_dict, "id": product_id}
    products_db[product_id] = new_product
    return new_product

@app.get("/products/", response_model=List[Product])
def read_products():
    return list(products_db.values())

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: str):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, product: ProductCreate):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_dict = product.model_dump()
    updated_product = {**product_dict, "id": product_id}
    products_db[product_id] = updated_product
    return updated_product

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    
    del products_db[product_id]
    return {"message": "Product deleted successfully"}