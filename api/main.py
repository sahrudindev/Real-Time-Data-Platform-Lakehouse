"""
=============================================================================
ENTERPRISE DATA PLATFORM - REST API WITH FAKER
=============================================================================
"""

import json
import random
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

try:
    from faker import Faker
    fake = Faker(['id_ID', 'en_US'])
except ImportError:
    fake = None

# =============================================================================
# DATA STORE
# =============================================================================
class DataStore:
    def __init__(self):
        self.orders = []
        self.customers = []
        self.products = []
    
    def get_stats(self):
        total_revenue = sum(o.get('total_amount', 0) for o in self.orders)
        return {
            "total_orders": len(self.orders),
            "total_customers": len(self.customers),
            "total_products": len(self.products),
            "total_revenue": total_revenue,
            "total_events": len(self.orders) * 5,
            "avg_order_value": total_revenue / max(1, len(self.orders))
        }

data_store = DataStore()

# =============================================================================
# DATA GENERATOR
# =============================================================================
CATEGORIES = ["Elektronik", "Fashion", "Rumah Tangga", "Kesehatan", "Makanan"]
BRANDS = ["Samsung", "Apple", "Xiaomi", "Nike", "Adidas", "Uniqlo", "Sony"]
PAYMENTS = ["credit_card", "gopay", "ovo", "dana", "bank_transfer", "shopeepay"]
STATUSES = ["pending", "processing", "completed", "delivered"]
SEGMENTS = ["standard", "premium", "vip"]

def generate_product():
    name = f"{random.choice(BRANDS)} {fake.word().title() if fake else 'Product'} {random.randint(1,100)}"
    return {
        "product_id": f"PROD-{uuid.uuid4().hex[:8].upper()}",
        "name": name,
        "category": random.choice(CATEGORIES),
        "price": random.randint(50000, 15000000),
        "brand": random.choice(BRANDS),
    }

def generate_customer():
    return {
        "customer_id": f"CUST-{uuid.uuid4().hex[:8].upper()}",
        "email": fake.email() if fake else f"user{random.randint(1,1000)}@email.com",
        "first_name": fake.first_name() if fake else f"User{random.randint(1,100)}",
        "last_name": fake.last_name() if fake else "Test",
        "phone": fake.phone_number() if fake else "08123456789",
        "city": fake.city() if fake else "Jakarta",
        "segment": random.choice(SEGMENTS),
    }

def generate_order():
    items = []
    total = 0
    for _ in range(random.randint(1, 4)):
        price = random.randint(100000, 5000000)
        qty = random.randint(1, 3)
        items.append({"product_id": f"PROD-{uuid.uuid4().hex[:8].upper()}", "qty": qty, "price": price})
        total += price * qty
    
    return {
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "customer_id": f"CUST-{uuid.uuid4().hex[:8].upper()}",
        "items": items,
        "total_amount": total,
        "status": random.choice(STATUSES),
        "payment_method": random.choice(PAYMENTS),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

def generate_sample_data(num_orders=100, num_customers=50, num_products=150):
    for _ in range(num_products):
        data_store.products.append(generate_product())
    for _ in range(num_customers):
        data_store.customers.append(generate_customer())
    for _ in range(num_orders):
        data_store.orders.append(generate_order())
    return data_store.get_stats()

# =============================================================================
# FASTAPI APP
# =============================================================================
app = FastAPI(title="Enterprise Data Platform API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    generate_sample_data()
    print("Generated sample data with Faker!")

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/v1/stats")
async def get_stats():
    return data_store.get_stats()

@app.get("/api/v1/orders")
async def get_orders(limit: int = Query(default=50, le=100)):
    return {"count": len(data_store.orders), "orders": data_store.orders[-limit:]}

@app.get("/api/v1/customers")
async def get_customers(limit: int = Query(default=50, le=100)):
    return {"count": len(data_store.customers), "customers": data_store.customers[-limit:]}

@app.get("/api/v1/products")
async def get_products(limit: int = Query(default=50, le=100)):
    return {"count": len(data_store.products), "products": data_store.products[-limit:]}

@app.post("/api/v1/generate")
async def generate_more(orders: int = 10):
    for _ in range(orders):
        data_store.orders.append(generate_order())
    return {"message": f"Generated {orders} orders", "stats": data_store.get_stats()}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
