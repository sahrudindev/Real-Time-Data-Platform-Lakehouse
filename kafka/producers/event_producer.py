"""
=============================================================================
ENTERPRISE DATA PLATFORM - KAFKA EVENT PRODUCER WITH FAKER
=============================================================================
Realistic data generation using Faker library for e-commerce events.
=============================================================================
"""

import json
import logging
import os
import random
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from faker import Faker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Faker with Indonesian locale
fake = Faker(['id_ID', 'en_US'])
Faker.seed(42)


# =============================================================================
# EVENT MODELS
# =============================================================================

@dataclass
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str = ""
    event_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_source: str = "ecommerce-platform"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class OrderEvent(BaseEvent):
    order_id: str = ""
    customer_id: str = ""
    items: List[Dict[str, Any]] = field(default_factory=list)
    total_amount: float = 0.0
    currency: str = "IDR"
    status: str = "pending"
    shipping_address: Dict[str, str] = field(default_factory=dict)
    payment_method: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CustomerEvent(BaseEvent):
    customer_id: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: str = ""
    address: Dict[str, str] = field(default_factory=dict)
    segment: str = "standard"
    lifetime_value: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ProductEvent(BaseEvent):
    product_id: str = ""
    name: str = ""
    description: str = ""
    category: str = ""
    subcategory: str = ""
    price: float = 0.0
    currency: str = "IDR"
    sku: str = ""
    brand: str = ""
    is_active: bool = True


@dataclass
class ClickstreamEvent(BaseEvent):
    session_id: str = ""
    user_id: str = ""
    anonymous_id: str = ""
    page_url: str = ""
    page_title: str = ""
    referrer: str = ""
    user_agent: str = ""
    ip_address: str = ""
    device_type: str = ""
    country: str = ""
    city: str = ""
    action: str = ""


# =============================================================================
# FAKER-BASED EVENT GENERATOR
# =============================================================================

class RealisticEventGenerator:
    """Generate realistic e-commerce events using Faker."""
    
    CATEGORIES = [
        ("Elektronik", ["Smartphone", "Laptop", "Tablet", "Headphone", "Kamera"]),
        ("Fashion", ["Baju", "Celana", "Sepatu", "Tas", "Aksesoris"]),
        ("Rumah Tangga", ["Perabotan", "Dekorasi", "Dapur", "Kebersihan"]),
        ("Kesehatan", ["Vitamin", "Suplemen", "Alat Kesehatan", "Skincare"]),
        ("Makanan", ["Snack", "Minuman", "Makanan Instan", "Bahan Masakan"]),
    ]
    
    BRANDS = ["Samsung", "Apple", "Xiaomi", "Nike", "Adidas", "Uniqlo", "IKEA", 
              "Sony", "LG", "Asus", "Lenovo", "H&M", "Zara", "Wardah", "Somethinc"]
    
    PAYMENT_METHODS = ["credit_card", "debit_card", "bank_transfer", "gopay", "ovo", "dana", "shopeepay"]
    
    SEGMENTS = ["standard", "premium", "vip", "enterprise"]
    
    ACTIONS = ["page_view", "product_view", "add_to_cart", "remove_from_cart", "checkout", "purchase"]
    
    DEVICES = ["mobile", "desktop", "tablet"]
    
    def __init__(self):
        self.customer_ids = [f"CUST-{uuid.uuid4().hex[:8].upper()}" for _ in range(100)]
        self.product_ids = [f"PROD-{uuid.uuid4().hex[:8].upper()}" for _ in range(200)]
    
    def generate_product(self) -> ProductEvent:
        """Generate a realistic product."""
        category, subcategories = random.choice(self.CATEGORIES)
        subcategory = random.choice(subcategories)
        brand = random.choice(self.BRANDS)
        
        product_names = {
            "Smartphone": f"{brand} {fake.word().title()} Pro {random.randint(10, 15)}",
            "Laptop": f"{brand} {fake.word().title()}Book {random.choice(['Air', 'Pro', 'Ultra'])}",
            "Baju": f"Kaos {brand} {fake.color_name()} Edition",
            "Sepatu": f"{brand} {fake.word().title()} Runner {random.randint(1, 5)}.0",
        }
        
        name = product_names.get(subcategory, f"{brand} {subcategory} {fake.word().title()}")
        price = random.randint(50000, 15000000)
        
        return ProductEvent(
            event_type="product.created",
            product_id=random.choice(self.product_ids),
            name=name,
            description=fake.paragraph(nb_sentences=3),
            category=category,
            subcategory=subcategory,
            price=price,
            currency="IDR",
            sku=f"SKU-{fake.bothify('???-#####').upper()}",
            brand=brand,
            is_active=True
        )
    
    def generate_customer(self) -> CustomerEvent:
        """Generate a realistic customer."""
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        return CustomerEvent(
            event_type="customer.registered",
            customer_id=random.choice(self.customer_ids),
            email=fake.email(),
            first_name=first_name,
            last_name=last_name,
            phone=fake.phone_number(),
            address={
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.administrative_unit(),
                "zip": fake.postcode(),
                "country": "Indonesia"
            },
            segment=random.choice(self.SEGMENTS),
            lifetime_value=random.uniform(0, 50000000)
        )
    
    def generate_order(self) -> OrderEvent:
        """Generate a realistic order."""
        customer_id = random.choice(self.customer_ids)
        num_items = random.randint(1, 5)
        
        items = []
        total = 0
        for _ in range(num_items):
            product = self.generate_product()
            quantity = random.randint(1, 3)
            line_total = product.price * quantity
            total += line_total
            
            items.append({
                "product_id": product.product_id,
                "name": product.name,
                "quantity": quantity,
                "unit_price": product.price,
                "total_price": line_total
            })
        
        return OrderEvent(
            event_type="order.created",
            order_id=f"ORD-{fake.bothify('????????').upper()}",
            customer_id=customer_id,
            items=items,
            total_amount=total,
            currency="IDR",
            status=random.choice(["pending", "processing", "completed", "delivered"]),
            shipping_address={
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.administrative_unit(),
                "zip": fake.postcode(),
                "country": "Indonesia"
            },
            payment_method=random.choice(self.PAYMENT_METHODS)
        )
    
    def generate_clickstream(self) -> ClickstreamEvent:
        """Generate realistic clickstream event."""
        pages = [
            ("/", "Home - Toko Online"),
            ("/products", "Semua Produk"),
            ("/products/electronics", "Elektronik"),
            ("/products/fashion", "Fashion"),
            ("/cart", "Keranjang Belanja"),
            ("/checkout", "Checkout"),
            ("/account", "Akun Saya"),
        ]
        
        page_url, page_title = random.choice(pages)
        
        return ClickstreamEvent(
            event_type=f"clickstream.{random.choice(self.ACTIONS)}",
            session_id=str(uuid.uuid4()),
            user_id=random.choice(self.customer_ids) if random.random() > 0.3 else "",
            anonymous_id=str(uuid.uuid4()),
            page_url=f"https://toko.example.com{page_url}",
            page_title=page_title,
            referrer=random.choice(["https://google.com", "https://facebook.com", "direct", ""]),
            user_agent=fake.user_agent(),
            ip_address=fake.ipv4(),
            device_type=random.choice(self.DEVICES),
            country="Indonesia",
            city=fake.city(),
            action=random.choice(self.ACTIONS)
        )


# =============================================================================
# DATA STORE (In-Memory for Demo)
# =============================================================================

class DataStore:
    """Simple in-memory data store for demo purposes."""
    
    def __init__(self):
        self.orders: List[Dict] = []
        self.customers: List[Dict] = []
        self.products: List[Dict] = []
        self.clickstream: List[Dict] = []
    
    def add_order(self, order: OrderEvent):
        self.orders.append(order.to_dict())
    
    def add_customer(self, customer: CustomerEvent):
        self.customers.append(customer.to_dict())
    
    def add_product(self, product: ProductEvent):
        self.products.append(product.to_dict())
    
    def add_clickstream(self, event: ClickstreamEvent):
        self.clickstream.append(event.to_dict())
    
    def get_stats(self) -> Dict[str, Any]:
        total_revenue = sum(o.get('total_amount', 0) for o in self.orders)
        return {
            "total_orders": len(self.orders),
            "total_customers": len(self.customers),
            "total_products": len(self.products),
            "total_revenue": total_revenue,
            "total_events": len(self.clickstream),
            "avg_order_value": total_revenue / max(1, len(self.orders))
        }
    
    def to_json(self) -> str:
        return json.dumps({
            "orders": self.orders[-50:],  # Last 50
            "customers": self.customers[-50:],
            "products": self.products[-50:],
            "stats": self.get_stats()
        }, default=str, indent=2)


# =============================================================================
# MAIN
# =============================================================================

# Global data store instance
data_store = DataStore()
generator = RealisticEventGenerator()


def generate_sample_data(num_orders=50, num_customers=30, num_products=100):
    """Generate sample data."""
    logger.info("Generating sample data with Faker...")
    
    # Generate products
    for _ in range(num_products):
        product = generator.generate_product()
        data_store.add_product(product)
    
    # Generate customers
    for _ in range(num_customers):
        customer = generator.generate_customer()
        data_store.add_customer(customer)
    
    # Generate orders
    for _ in range(num_orders):
        order = generator.generate_order()
        data_store.add_order(order)
    
    # Generate clickstream
    for _ in range(200):
        event = generator.generate_clickstream()
        data_store.add_clickstream(event)
    
    stats = data_store.get_stats()
    logger.info(f"Generated data: {stats}")
    
    return stats


if __name__ == "__main__":
    stats = generate_sample_data()
    print(json.dumps(stats, indent=2))
