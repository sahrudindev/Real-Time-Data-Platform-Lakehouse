"""
=============================================================================
ENTERPRISE DATA PLATFORM - SILVER LAYER PROCESSOR
=============================================================================
Data cleansing, enrichment, and transformation from Bronze to Silver layer.
=============================================================================
"""

import os
import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, when, lit, current_timestamp, sha2, concat_ws,
    trim, lower, upper, regexp_replace, coalesce,
    to_date, year, month, dayofmonth, row_number,
    size, posexplode, expr
)
from pyspark.sql.window import Window
from pyspark.sql.types import TimestampType
from delta.tables import DeltaTable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SilverConfig:
    DELTA_BASE_PATH = os.getenv('DELTA_LAKE_PATH', '/data/delta')
    BRONZE_PATH = os.path.join(DELTA_BASE_PATH, 'bronze')
    SILVER_PATH = os.path.join(DELTA_BASE_PATH, 'silver')


class DataQualityRules:
    @staticmethod
    def add_surrogate_key(df, key_columns, key_name="sk"):
        concat_expr = concat_ws("_", *[col(c) for c in key_columns])
        return df.withColumn(key_name, sha2(concat_expr, 256))
    
    @staticmethod
    def standardize_email(df, column):
        return df.withColumn(column, lower(trim(col(column))))
    
    @staticmethod
    def clean_phone(df, column):
        return df.withColumn(column, regexp_replace(col(column), r'[^\d+]', ''))


class SilverLayerProcessor:
    def __init__(self, spark):
        self.spark = spark
        self.config = SilverConfig()
        self.quality = DataQualityRules()
    
    def read_bronze(self, table_name):
        return self.spark.read.format("delta").load(f"{self.config.BRONZE_PATH}/{table_name}")
    
    def write_silver(self, df, table_name, partition_columns=None, mode="overwrite"):
        path = f"{self.config.SILVER_PATH}/{table_name}"
        writer = df.write.format("delta").mode(mode)
        if partition_columns:
            writer = writer.partitionBy(*partition_columns)
        writer.save(path)
        logger.info(f"Written to {path}")
    
    def upsert_silver(self, df, table_name, merge_keys, partition_columns=None):
        path = f"{self.config.SILVER_PATH}/{table_name}"
        if DeltaTable.isDeltaTable(self.spark, path):
            delta_table = DeltaTable.forPath(self.spark, path)
            merge_condition = " AND ".join([f"target.{k} = source.{k}" for k in merge_keys])
            delta_table.alias("target").merge(df.alias("source"), merge_condition)\
                .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        else:
            self.write_silver(df, table_name, partition_columns)
    
    def process_orders(self):
        logger.info("Processing Orders: Bronze -> Silver")
        bronze_df = self.read_bronze("orders")
        
        silver_df = (
            bronze_df
            .filter(col("order_id").isNotNull() & col("customer_id").isNotNull())
            .filter(col("total_amount") >= 0)
            .withColumn("status", upper(trim(col("status"))))
            .transform(lambda df: self.quality.add_surrogate_key(df, ["order_id"], "order_sk"))
            .withColumn("order_date", to_date(col("event_ts")))
            .withColumn("order_year", year(col("event_ts")))
            .withColumn("order_month", month(col("event_ts")))
            .withColumn("item_count", size(col("items")))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.upsert_silver(silver_df, "orders", ["order_id"], ["order_date"])
        return silver_df
    
    def process_customers(self):
        logger.info("Processing Customers: Bronze -> Silver")
        bronze_df = self.read_bronze("customers")
        
        window_spec = Window.partitionBy("customer_id").orderBy(col("event_ts").desc())
        
        silver_df = (
            bronze_df
            .filter(col("customer_id").isNotNull() & col("email").isNotNull())
            .transform(lambda df: self.quality.standardize_email(df, "email"))
            .transform(lambda df: self.quality.clean_phone(df, "phone"))
            .withColumn("first_name", trim(col("first_name")))
            .withColumn("last_name", trim(col("last_name")))
            .transform(lambda df: self.quality.add_surrogate_key(df, ["customer_id", "event_timestamp"], "customer_sk"))
            .withColumn("_row_num", row_number().over(window_spec))
            .filter(col("_row_num") == 1).drop("_row_num")
            .withColumn("_valid_from", col("event_ts"))
            .withColumn("_valid_to", lit(None).cast(TimestampType()))
            .withColumn("_is_current", lit(True))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.upsert_silver(silver_df, "customers", ["customer_id"])
        return silver_df
    
    def process_products(self):
        logger.info("Processing Products: Bronze -> Silver")
        bronze_df = self.read_bronze("products")
        
        silver_df = (
            bronze_df
            .filter(col("product_id").isNotNull() & col("name").isNotNull())
            .filter(col("price") >= 0)
            .withColumn("category", upper(trim(col("category"))))
            .withColumn("subcategory", upper(trim(col("subcategory"))))
            .transform(lambda df: self.quality.add_surrogate_key(df, ["product_id"], "product_sk"))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.upsert_silver(silver_df, "products", ["product_id"])
        return silver_df
    
    def process_clickstream(self):
        logger.info("Processing Clickstream: Bronze -> Silver")
        bronze_df = self.read_bronze("clickstream")
        
        silver_df = (
            bronze_df
            .filter(col("session_id").isNotNull())
            .transform(lambda df: self.quality.add_surrogate_key(df, ["event_id"], "clickstream_sk"))
            .withColumn("resolved_user_id", coalesce(col("user_id"), col("anonymous_id")))
            .withColumn("device_category", when(col("device_type").isin(["mobile", "tablet"]), "mobile")
                .when(col("device_type") == "desktop", "desktop").otherwise("other"))
            .withColumn("event_date", to_date(col("event_ts")))
            .withColumn("event_hour", expr("hour(event_ts)"))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.write_silver(silver_df, "clickstream", ["event_date"], mode="append")
        return silver_df
    
    def process_order_items(self):
        logger.info("Processing Order Items: Bronze -> Silver")
        bronze_df = self.read_bronze("orders")
        
        silver_df = (
            bronze_df
            .filter(col("order_id").isNotNull() & (size(col("items")) > 0))
            .select("order_id", "customer_id", "currency", "event_ts", posexplode("items").alias("line_number", "item"))
            .select("order_id", "customer_id", "currency", "event_ts", (col("line_number") + 1).alias("line_number"),
                col("item.product_id").alias("product_id"), col("item.name").alias("product_name"),
                col("item.quantity").alias("quantity"), col("item.unit_price").alias("unit_price"),
                col("item.total_price").alias("line_total"))
            .transform(lambda df: self.quality.add_surrogate_key(df, ["order_id", "line_number"], "order_item_sk"))
            .withColumn("_processed_at", current_timestamp())
        )
        
        self.write_silver(silver_df, "order_items")
        return silver_df
    
    def process_all(self):
        logger.info("SILVER LAYER PROCESSING - START")
        results = {
            "orders": self.process_orders().count(),
            "customers": self.process_customers().count(),
            "products": self.process_products().count(),
            "clickstream": self.process_clickstream().count(),
            "order_items": self.process_order_items().count()
        }
        logger.info(f"SILVER LAYER PROCESSING - COMPLETE: {results}")
        return results


def main():
    spark = SparkSession.builder.appName("SilverLayerProcessor")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
        .getOrCreate()
    
    processor = SilverLayerProcessor(spark)
    processor.process_all()
    spark.stop()


if __name__ == "__main__":
    main()
