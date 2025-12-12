"""
=============================================================================
ENTERPRISE DATA PLATFORM - GOLD LAYER PROCESSOR
=============================================================================
Business aggregations and analytics-ready data models for Gold layer.
=============================================================================
"""

import os
import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, lit, current_timestamp, sum as spark_sum, count, avg,
    max as spark_max, min as spark_min, countDistinct,
    to_date, year, month, dayofmonth, hour, weekofyear,
    datediff, current_date, when, coalesce, first
)
from pyspark.sql.window import Window
from delta.tables import DeltaTable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GoldConfig:
    DELTA_BASE_PATH = os.getenv('DELTA_LAKE_PATH', '/data/delta')
    SILVER_PATH = os.path.join(DELTA_BASE_PATH, 'silver')
    GOLD_PATH = os.path.join(DELTA_BASE_PATH, 'gold')


class GoldLayerProcessor:
    """Gold layer processor for business aggregations and analytics-ready models."""
    
    def __init__(self, spark):
        self.spark = spark
        self.config = GoldConfig()
    
    def read_silver(self, table_name):
        return self.spark.read.format("delta").load(f"{self.config.SILVER_PATH}/{table_name}")
    
    def write_gold(self, df, table_name, mode="overwrite"):
        path = f"{self.config.GOLD_PATH}/{table_name}"
        df.write.format("delta").mode(mode).save(path)
        logger.info(f"Written {df.count()} records to {path}")
    
    def upsert_gold(self, df, table_name, merge_keys):
        path = f"{self.config.GOLD_PATH}/{table_name}"
        if DeltaTable.isDeltaTable(self.spark, path):
            delta_table = DeltaTable.forPath(self.spark, path)
            merge_condition = " AND ".join([f"target.{k} = source.{k}" for k in merge_keys])
            delta_table.alias("target").merge(df.alias("source"), merge_condition)\
                .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        else:
            self.write_gold(df, table_name)
    
    # -------------------------------------------------------------------------
    # FACT: DAILY SALES
    # -------------------------------------------------------------------------
    def build_fact_daily_sales(self):
        """Build daily sales fact table with key metrics."""
        logger.info("Building Fact: Daily Sales")
        
        orders = self.read_silver("orders")
        order_items = self.read_silver("order_items")
        
        daily_sales = (
            orders.filter(col("status").isin(["COMPLETED", "DELIVERED"]))
            .groupBy("order_date")
            .agg(
                count("order_id").alias("total_orders"),
                countDistinct("customer_id").alias("unique_customers"),
                spark_sum("total_amount").alias("total_revenue"),
                avg("total_amount").alias("avg_order_value"),
                spark_max("total_amount").alias("max_order_value"),
                spark_min("total_amount").alias("min_order_value"),
                spark_sum("item_count").alias("total_items_sold")
            )
            .withColumn("revenue_per_customer", col("total_revenue") / col("unique_customers"))
            .withColumn("_processed_at", current_timestamp())
            .orderBy("order_date")
        )
        
        self.upsert_gold(daily_sales, "fact_daily_sales", ["order_date"])
        return daily_sales
    
    # -------------------------------------------------------------------------
    # FACT: CUSTOMER ORDERS
    # -------------------------------------------------------------------------
    def build_fact_customer_orders(self):
        """Build customer order summary fact table."""
        logger.info("Building Fact: Customer Orders")
        
        orders = self.read_silver("orders")
        customers = self.read_silver("customers")
        
        customer_orders = (
            orders
            .groupBy("customer_id")
            .agg(
                count("order_id").alias("total_orders"),
                spark_sum("total_amount").alias("total_spent"),
                avg("total_amount").alias("avg_order_value"),
                spark_min("order_date").alias("first_order_date"),
                spark_max("order_date").alias("last_order_date"),
                spark_sum("item_count").alias("total_items_purchased")
            )
            .withColumn("days_since_first_order", datediff(current_date(), col("first_order_date")))
            .withColumn("days_since_last_order", datediff(current_date(), col("last_order_date")))
            .withColumn("order_frequency", col("total_orders") / (col("days_since_first_order") + 1))
        )
        
        # Enrich with customer data
        enriched = (
            customer_orders.join(
                customers.select("customer_id", "email", "first_name", "last_name", "segment"),
                "customer_id", "left"
            )
            .withColumn("customer_tier",
                when(col("total_spent") >= 10000, "platinum")
                .when(col("total_spent") >= 5000, "gold")
                .when(col("total_spent") >= 1000, "silver")
                .otherwise("bronze"))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.upsert_gold(enriched, "fact_customer_orders", ["customer_id"])
        return enriched
    
    # -------------------------------------------------------------------------
    # FACT: PRODUCT PERFORMANCE
    # -------------------------------------------------------------------------
    def build_fact_product_performance(self):
        """Build product performance fact table."""
        logger.info("Building Fact: Product Performance")
        
        order_items = self.read_silver("order_items")
        products = self.read_silver("products")
        
        product_perf = (
            order_items
            .groupBy("product_id")
            .agg(
                count("*").alias("times_ordered"),
                spark_sum("quantity").alias("total_quantity_sold"),
                spark_sum("line_total").alias("total_revenue"),
                avg("unit_price").alias("avg_selling_price"),
                countDistinct("customer_id").alias("unique_buyers")
            )
        )
        
        # Enrich with product data
        enriched = (
            product_perf.join(
                products.select("product_id", "name", "category", "subcategory", "brand", "price"),
                "product_id", "left"
            )
            .withColumn("revenue_per_order", col("total_revenue") / col("times_ordered"))
            .withColumn("avg_quantity_per_order", col("total_quantity_sold") / col("times_ordered"))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.upsert_gold(enriched, "fact_product_performance", ["product_id"])
        return enriched
    
    # -------------------------------------------------------------------------
    # DIM: DATE
    # -------------------------------------------------------------------------
    def build_dim_date(self):
        """Build date dimension table."""
        logger.info("Building Dim: Date")
        
        from pyspark.sql.functions import sequence, explode, to_date
        
        # Generate date range
        date_df = self.spark.sql("""
            SELECT explode(sequence(to_date('2020-01-01'), to_date('2030-12-31'), interval 1 day)) as date
        """)
        
        dim_date = (
            date_df
            .withColumn("date_key", col("date").cast("int"))
            .withColumn("year", year("date"))
            .withColumn("month", month("date"))
            .withColumn("day", dayofmonth("date"))
            .withColumn("week", weekofyear("date"))
            .withColumn("quarter", ((month("date") - 1) / 3 + 1).cast("int"))
            .withColumn("day_of_week", ((dayofmonth("date") % 7) + 1))
            .withColumn("is_weekend", when(col("day_of_week").isin([1, 7]), True).otherwise(False))
            .withColumn("month_name", when(col("month") == 1, "January")
                .when(col("month") == 2, "February")
                .when(col("month") == 3, "March")
                .when(col("month") == 4, "April")
                .when(col("month") == 5, "May")
                .when(col("month") == 6, "June")
                .when(col("month") == 7, "July")
                .when(col("month") == 8, "August")
                .when(col("month") == 9, "September")
                .when(col("month") == 10, "October")
                .when(col("month") == 11, "November")
                .otherwise("December"))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.write_gold(dim_date, "dim_date")
        return dim_date
    
    # -------------------------------------------------------------------------
    # ANALYTICS: SESSION ANALYSIS
    # -------------------------------------------------------------------------
    def build_session_analytics(self):
        """Build session-level analytics for clickstream."""
        logger.info("Building Analytics: Session Analysis")
        
        clickstream = self.read_silver("clickstream")
        
        session_analytics = (
            clickstream
            .groupBy("session_id", "resolved_user_id", "event_date", "device_category", "country")
            .agg(
                count("*").alias("total_events"),
                countDistinct("page_url").alias("unique_pages"),
                countDistinct("action").alias("unique_actions"),
                spark_min("event_ts").alias("session_start"),
                spark_max("event_ts").alias("session_end"),
                spark_sum(when(col("action") == "add_to_cart", 1).otherwise(0)).alias("cart_adds"),
                spark_sum(when(col("action") == "purchase", 1).otherwise(0)).alias("purchases")
            )
            .withColumn("session_duration_sec", 
                (col("session_end").cast("long") - col("session_start").cast("long")))
            .withColumn("is_converted", col("purchases") > 0)
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.write_gold(session_analytics, "analytics_sessions")
        return session_analytics
    
    def process_all(self):
        """Process all Gold layer tables."""
        logger.info("GOLD LAYER PROCESSING - START")
        results = {
            "fact_daily_sales": self.build_fact_daily_sales().count(),
            "fact_customer_orders": self.build_fact_customer_orders().count(),
            "fact_product_performance": self.build_fact_product_performance().count(),
            "dim_date": self.build_dim_date().count(),
            "analytics_sessions": self.build_session_analytics().count()
        }
        logger.info(f"GOLD LAYER PROCESSING - COMPLETE: {results}")
        return results


def main():
    spark = SparkSession.builder.appName("GoldLayerProcessor")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
        .getOrCreate()
    
    processor = GoldLayerProcessor(spark)
    processor.process_all()
    spark.stop()


if __name__ == "__main__":
    main()
