"""
=============================================================================
ENTERPRISE DATA PLATFORM - FEATURE DEFINITIONS
=============================================================================
Feast feature definitions for ML feature store.
=============================================================================
"""

from datetime import timedelta
from feast import Entity, Feature, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String

# =============================================================================
# ENTITIES
# =============================================================================

customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    description="Customer entity for feature store"
)

product = Entity(
    name="product",
    join_keys=["product_id"],
    description="Product entity for feature store"
)


# =============================================================================
# SOURCES
# =============================================================================

customer_source = FileSource(
    name="customer_features_source",
    path="/data/features/customer_features.parquet",
    timestamp_field="event_timestamp",
)

product_source = FileSource(
    name="product_features_source",
    path="/data/features/product_features.parquet",
    timestamp_field="event_timestamp",
)


# =============================================================================
# FEATURE VIEWS
# =============================================================================

customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="total_revenue", dtype=Float32),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="days_since_last_order", dtype=Int64),
        Field(name="customer_tier", dtype=String),
        Field(name="customer_status", dtype=String),
        Field(name="lifetime_value", dtype=Float32),
    ],
    source=customer_source,
    online=True,
    tags={"team": "data-engineering", "domain": "customer"},
)

product_features = FeatureView(
    name="product_features",
    entities=[product],
    ttl=timedelta(days=1),
    schema=[
        Field(name="total_quantity_sold", dtype=Int64),
        Field(name="total_revenue", dtype=Float32),
        Field(name="times_ordered", dtype=Int64),
        Field(name="unique_buyers", dtype=Int64),
        Field(name="avg_selling_price", dtype=Float32),
        Field(name="product_tier", dtype=String),
    ],
    source=product_source,
    online=True,
    tags={"team": "data-engineering", "domain": "product"},
)
