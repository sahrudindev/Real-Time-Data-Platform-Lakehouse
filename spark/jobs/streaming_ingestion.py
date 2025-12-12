"""
=============================================================================
ENTERPRISE DATA PLATFORM - SPARK STREAMING INGESTION
=============================================================================
Real-time Kafka to Delta Lake ingestion with:
- Exactly-once semantics
- Watermarking
- Deduplication
- Checkpointing
- Schema enforcement
- Fault tolerance
=============================================================================
"""

import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, from_json, to_timestamp, window, lit,
    current_timestamp, expr, sha2, concat_ws,
    when, coalesce, struct, to_json, count,
    sum as spark_sum, avg, max as spark_max, min as spark_min
)
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    IntegerType, TimestampType, ArrayType, MapType,
    BooleanType, LongType
)
from delta.tables import DeltaTable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# CONFIGURATION
# =============================================================================

class StreamingConfig:
    """Streaming job configuration."""
    
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
    
    # Input Topics
    ORDERS_TOPIC = 'raw.ecommerce.orders'
    CUSTOMERS_TOPIC = 'raw.ecommerce.customers'
    PRODUCTS_TOPIC = 'raw.ecommerce.products'
    CLICKSTREAM_TOPIC = 'raw.ecommerce.clickstream'
    INVENTORY_TOPIC = 'raw.ecommerce.inventory'
    PAYMENTS_TOPIC = 'raw.ecommerce.payments'
    
    # Delta Lake Paths
    DELTA_BASE_PATH = os.getenv('DELTA_LAKE_PATH', '/data/delta')
    BRONZE_PATH = os.path.join(DELTA_BASE_PATH, 'bronze')
    SILVER_PATH = os.path.join(DELTA_BASE_PATH, 'silver')
    GOLD_PATH = os.path.join(DELTA_BASE_PATH, 'gold')
    
    # Checkpoint Paths
    CHECKPOINT_BASE_PATH = os.getenv('CHECKPOINT_PATH', '/data/checkpoints')
    
    # Streaming Configuration
    TRIGGER_INTERVAL = '10 seconds'
    WATERMARK_DELAY = '1 hour'
    MAX_OFFSETS_PER_TRIGGER = 10000
    
    # MinIO/S3 Configuration
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'http://minio:9000')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin123')


# =============================================================================
# SCHEMAS
# =============================================================================

class EventSchemas:
    """Schema definitions for all event types."""
    
    # Common event fields
    BASE_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_timestamp", StringType(), False),
        StructField("event_source", StringType(), True),
        StructField("event_version", StringType(), True),
        StructField("correlation_id", StringType(), True),
    ])
    
    # Order event schema
    ORDER_ITEM_SCHEMA = StructType([
        StructField("product_id", StringType(), False),
        StructField("name", StringType(), True),
        StructField("quantity", IntegerType(), False),
        StructField("unit_price", DoubleType(), False),
        StructField("total_price", DoubleType(), False),
    ])
    
    ADDRESS_SCHEMA = StructType([
        StructField("street", StringType(), True),
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("zip", StringType(), True),
        StructField("country", StringType(), True),
    ])
    
    ORDER_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_timestamp", StringType(), False),
        StructField("event_source", StringType(), True),
        StructField("event_version", StringType(), True),
        StructField("correlation_id", StringType(), True),
        StructField("order_id", StringType(), False),
        StructField("customer_id", StringType(), False),
        StructField("items", ArrayType(ORDER_ITEM_SCHEMA), False),
        StructField("total_amount", DoubleType(), False),
        StructField("currency", StringType(), True),
        StructField("status", StringType(), False),
        StructField("shipping_address", ADDRESS_SCHEMA, True),
        StructField("payment_method", StringType(), True),
        StructField("created_at", StringType(), True),
        StructField("updated_at", StringType(), True),
    ])
    
    # Customer event schema
    CUSTOMER_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_timestamp", StringType(), False),
        StructField("event_source", StringType(), True),
        StructField("event_version", StringType(), True),
        StructField("correlation_id", StringType(), True),
        StructField("customer_id", StringType(), False),
        StructField("email", StringType(), False),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("address", ADDRESS_SCHEMA, True),
        StructField("segment", StringType(), True),
        StructField("lifetime_value", DoubleType(), True),
        StructField("created_at", StringType(), True),
        StructField("updated_at", StringType(), True),
    ])
    
    # Clickstream event schema
    PROPERTIES_SCHEMA = MapType(StringType(), StringType())
    
    CLICKSTREAM_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_timestamp", StringType(), False),
        StructField("event_source", StringType(), True),
        StructField("event_version", StringType(), True),
        StructField("correlation_id", StringType(), True),
        StructField("session_id", StringType(), False),
        StructField("user_id", StringType(), True),
        StructField("anonymous_id", StringType(), True),
        StructField("page_url", StringType(), True),
        StructField("page_title", StringType(), True),
        StructField("referrer", StringType(), True),
        StructField("user_agent", StringType(), True),
        StructField("ip_address", StringType(), True),
        StructField("device_type", StringType(), True),
        StructField("country", StringType(), True),
        StructField("city", StringType(), True),
        StructField("action", StringType(), True),
        StructField("properties", PROPERTIES_SCHEMA, True),
    ])
    
    # Product event schema
    PRODUCT_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_timestamp", StringType(), False),
        StructField("event_source", StringType(), True),
        StructField("event_version", StringType(), True),
        StructField("correlation_id", StringType(), True),
        StructField("product_id", StringType(), False),
        StructField("name", StringType(), False),
        StructField("description", StringType(), True),
        StructField("category", StringType(), True),
        StructField("subcategory", StringType(), True),
        StructField("price", DoubleType(), False),
        StructField("currency", StringType(), True),
        StructField("sku", StringType(), True),
        StructField("brand", StringType(), True),
        StructField("attributes", MapType(StringType(), StringType()), True),
        StructField("is_active", BooleanType(), True),
        StructField("created_at", StringType(), True),
        StructField("updated_at", StringType(), True),
    ])
    
    # Inventory event schema
    INVENTORY_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_timestamp", StringType(), False),
        StructField("event_source", StringType(), True),
        StructField("event_version", StringType(), True),
        StructField("correlation_id", StringType(), True),
        StructField("product_id", StringType(), False),
        StructField("warehouse_id", StringType(), False),
        StructField("quantity_available", IntegerType(), False),
        StructField("quantity_reserved", IntegerType(), True),
        StructField("reorder_level", IntegerType(), True),
        StructField("reorder_quantity", IntegerType(), True),
        StructField("last_restock_date", StringType(), True),
    ])
    
    # Payment event schema
    PAYMENT_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_timestamp", StringType(), False),
        StructField("event_source", StringType(), True),
        StructField("event_version", StringType(), True),
        StructField("correlation_id", StringType(), True),
        StructField("payment_id", StringType(), False),
        StructField("order_id", StringType(), False),
        StructField("customer_id", StringType(), False),
        StructField("amount", DoubleType(), False),
        StructField("currency", StringType(), True),
        StructField("payment_method", StringType(), True),
        StructField("payment_provider", StringType(), True),
        StructField("status", StringType(), False),
        StructField("transaction_id", StringType(), True),
        StructField("error_code", StringType(), True),
        StructField("error_message", StringType(), True),
        StructField("processed_at", StringType(), True),
    ])


# =============================================================================
# SPARK SESSION BUILDER
# =============================================================================

def create_spark_session(app_name: str = "StreamingIngestion") -> SparkSession:
    """
    Create a configured Spark session with Delta Lake support.
    """
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master(os.getenv('SPARK_MASTER', 'spark://spark-master:7077'))
        
        # Delta Lake configuration
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        
        # Kafka configuration
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                "io.delta:delta-core_2.12:2.4.0")
        
        # S3/MinIO configuration
        .config("spark.hadoop.fs.s3a.endpoint", StreamingConfig.MINIO_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", StreamingConfig.MINIO_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", StreamingConfig.MINIO_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        
        # Performance tuning
        .config("spark.sql.shuffle.partitions", "10")
        .config("spark.default.parallelism", "10")
        .config("spark.streaming.backpressure.enabled", "true")
        .config("spark.streaming.kafka.maxRatePerPartition", "1000")
        
        # Checkpoint configuration
        .config("spark.sql.streaming.checkpointLocation", StreamingConfig.CHECKPOINT_BASE_PATH)
        
        .getOrCreate()
    )
    
    spark.sparkContext.setLogLevel("WARN")
    logger.info(f"Spark session created: {app_name}")
    
    return spark


# =============================================================================
# STREAMING PROCESSOR
# =============================================================================

class StreamingProcessor:
    """
    Enterprise streaming processor for Kafka to Delta Lake ingestion.
    
    Features:
    - Exactly-once semantics with checkpointing
    - Watermarking for late data handling
    - Deduplication based on event_id
    - Schema validation
    - Automatic partitioning
    - Fault tolerance
    """
    
    def __init__(self, spark: SparkSession, config: StreamingConfig = None):
        self.spark = spark
        self.config = config or StreamingConfig()
        
    def read_kafka_stream(
        self,
        topic: str,
        starting_offsets: str = "latest"
    ) -> DataFrame:
        """
        Read streaming data from Kafka topic.
        
        Args:
            topic: Kafka topic name
            starting_offsets: Starting offset (earliest/latest)
            
        Returns:
            Streaming DataFrame
        """
        logger.info(f"Reading from Kafka topic: {topic}")
        
        df = (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", self.config.KAFKA_BOOTSTRAP_SERVERS)
            .option("subscribe", topic)
            .option("startingOffsets", starting_offsets)
            .option("maxOffsetsPerTrigger", self.config.MAX_OFFSETS_PER_TRIGGER)
            .option("failOnDataLoss", "false")
            .option("kafka.session.timeout.ms", "30000")
            .option("kafka.request.timeout.ms", "60000")
            .load()
        )
        
        return df
    
    def parse_json_with_schema(
        self,
        df: DataFrame,
        schema: StructType,
        timestamp_column: str = "event_timestamp"
    ) -> DataFrame:
        """
        Parse JSON events with schema validation.
        
        Args:
            df: Input streaming DataFrame
            schema: Expected schema
            timestamp_column: Column to use for watermarking
            
        Returns:
            Parsed DataFrame
        """
        parsed = (
            df
            # Parse value as string
            .selectExpr("CAST(value AS STRING) as json_data", "timestamp as kafka_timestamp")
            # Parse JSON with schema
            .select(
                from_json(col("json_data"), schema).alias("data"),
                col("kafka_timestamp")
            )
            # Flatten structure
            .select("data.*", "kafka_timestamp")
            # Cast event timestamp
            .withColumn(
                "event_ts",
                to_timestamp(col(timestamp_column))
            )
            # Add processing metadata
            .withColumn("_ingested_at", current_timestamp())
            .withColumn("_partition_date", expr("date(event_ts)"))
        )
        
        return parsed
    
    def apply_deduplication(
        self,
        df: DataFrame,
        id_columns: list,
        watermark_column: str = "event_ts",
        watermark_delay: str = None
    ) -> DataFrame:
        """
        Apply deduplication with watermarking.
        
        Args:
            df: Input DataFrame
            id_columns: Columns to use for deduplication
            watermark_column: Timestamp column for watermarking
            watermark_delay: Watermark delay threshold
            
        Returns:
            Deduplicated DataFrame
        """
        delay = watermark_delay or self.config.WATERMARK_DELAY
        
        deduped = (
            df
            .withWatermark(watermark_column, delay)
            .dropDuplicates(id_columns)
        )
        
        return deduped
    
    def write_to_delta(
        self,
        df: DataFrame,
        table_path: str,
        partition_columns: list = None,
        checkpoint_location: str = None,
        output_mode: str = "append",
        trigger_interval: str = None
    ):
        """
        Write streaming data to Delta Lake.
        
        Args:
            df: Streaming DataFrame
            table_path: Delta table path
            partition_columns: Columns for partitioning
            checkpoint_location: Checkpoint path
            output_mode: append/update/complete
            trigger_interval: Processing interval
            
        Returns:
            Streaming query
        """
        interval = trigger_interval or self.config.TRIGGER_INTERVAL
        checkpoint = checkpoint_location or f"{self.config.CHECKPOINT_BASE_PATH}/{table_path.split('/')[-1]}"
        
        writer = (
            df.writeStream
            .format("delta")
            .outputMode(output_mode)
            .option("checkpointLocation", checkpoint)
            .trigger(processingTime=interval)
        )
        
        if partition_columns:
            writer = writer.partitionBy(*partition_columns)
        
        query = writer.start(table_path)
        
        logger.info(f"Started streaming to Delta: {table_path}")
        return query
    
    def upsert_to_delta(
        self,
        df: DataFrame,
        table_path: str,
        merge_keys: list,
        partition_columns: list = None,
        checkpoint_location: str = None
    ):
        """
        Upsert (merge) streaming data to Delta Lake.
        
        Args:
            df: Streaming DataFrame
            table_path: Delta table path
            merge_keys: Columns to use for matching
            partition_columns: Columns for partitioning
            checkpoint_location: Checkpoint path
            
        Returns:
            Streaming query
        """
        checkpoint = checkpoint_location or f"{self.config.CHECKPOINT_BASE_PATH}/{table_path.split('/')[-1]}_upsert"
        
        def upsert_batch(batch_df: DataFrame, batch_id: int):
            """Process each micro-batch with upsert logic."""
            if batch_df.count() == 0:
                return
            
            # Check if table exists
            if DeltaTable.isDeltaTable(self.spark, table_path):
                delta_table = DeltaTable.forPath(self.spark, table_path)
                
                # Build merge condition
                merge_condition = " AND ".join([
                    f"target.{key} = source.{key}" for key in merge_keys
                ])
                
                # Perform merge
                (
                    delta_table.alias("target")
                    .merge(
                        batch_df.alias("source"),
                        merge_condition
                    )
                    .whenMatchedUpdateAll()
                    .whenNotMatchedInsertAll()
                    .execute()
                )
                
                logger.info(f"Batch {batch_id}: Upserted to {table_path}")
            else:
                # Create table if doesn't exist
                write_options = {"path": table_path}
                writer = batch_df.write.format("delta")
                
                if partition_columns:
                    writer = writer.partitionBy(*partition_columns)
                
                writer.mode("overwrite").save(table_path)
                logger.info(f"Batch {batch_id}: Created table {table_path}")
        
        query = (
            df.writeStream
            .foreachBatch(upsert_batch)
            .option("checkpointLocation", checkpoint)
            .trigger(processingTime=self.config.TRIGGER_INTERVAL)
            .start()
        )
        
        return query


# =============================================================================
# BRONZE LAYER PROCESSOR
# =============================================================================

class BronzeLayerProcessor:
    """
    Bronze layer processor for raw data landing.
    
    Responsibilities:
    - Ingest raw events from Kafka
    - Minimal transformation (parsing)
    - Full history preservation
    - Schema-on-read support
    """
    
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.processor = StreamingProcessor(spark)
        self.config = StreamingConfig()
        self.queries = {}
    
    def ingest_orders(self) -> None:
        """Ingest order events to Bronze layer."""
        logger.info("Starting Orders Bronze ingestion...")
        
        # Read from Kafka
        raw_df = self.processor.read_kafka_stream(self.config.ORDERS_TOPIC)
        
        # Parse with schema
        parsed_df = self.processor.parse_json_with_schema(
            raw_df, 
            EventSchemas.ORDER_SCHEMA
        )
        
        # Deduplicate
        deduped_df = self.processor.apply_deduplication(
            parsed_df,
            id_columns=["event_id"]
        )
        
        # Write to Bronze
        table_path = f"{self.config.BRONZE_PATH}/orders"
        query = self.processor.write_to_delta(
            deduped_df,
            table_path,
            partition_columns=["_partition_date"]
        )
        
        self.queries["orders"] = query
    
    def ingest_customers(self) -> None:
        """Ingest customer events to Bronze layer."""
        logger.info("Starting Customers Bronze ingestion...")
        
        raw_df = self.processor.read_kafka_stream(self.config.CUSTOMERS_TOPIC)
        
        parsed_df = self.processor.parse_json_with_schema(
            raw_df,
            EventSchemas.CUSTOMER_SCHEMA
        )
        
        deduped_df = self.processor.apply_deduplication(
            parsed_df,
            id_columns=["event_id"]
        )
        
        table_path = f"{self.config.BRONZE_PATH}/customers"
        query = self.processor.write_to_delta(
            deduped_df,
            table_path,
            partition_columns=["_partition_date"]
        )
        
        self.queries["customers"] = query
    
    def ingest_clickstream(self) -> None:
        """Ingest clickstream events to Bronze layer."""
        logger.info("Starting Clickstream Bronze ingestion...")
        
        raw_df = self.processor.read_kafka_stream(self.config.CLICKSTREAM_TOPIC)
        
        parsed_df = self.processor.parse_json_with_schema(
            raw_df,
            EventSchemas.CLICKSTREAM_SCHEMA
        )
        
        deduped_df = self.processor.apply_deduplication(
            parsed_df,
            id_columns=["event_id"]
        )
        
        table_path = f"{self.config.BRONZE_PATH}/clickstream"
        query = self.processor.write_to_delta(
            deduped_df,
            table_path,
            partition_columns=["_partition_date"]
        )
        
        self.queries["clickstream"] = query
    
    def ingest_products(self) -> None:
        """Ingest product events to Bronze layer."""
        logger.info("Starting Products Bronze ingestion...")
        
        raw_df = self.processor.read_kafka_stream(self.config.PRODUCTS_TOPIC)
        
        parsed_df = self.processor.parse_json_with_schema(
            raw_df,
            EventSchemas.PRODUCT_SCHEMA
        )
        
        deduped_df = self.processor.apply_deduplication(
            parsed_df,
            id_columns=["event_id"]
        )
        
        table_path = f"{self.config.BRONZE_PATH}/products"
        query = self.processor.write_to_delta(
            deduped_df,
            table_path,
            partition_columns=["_partition_date"]
        )
        
        self.queries["products"] = query
    
    def ingest_inventory(self) -> None:
        """Ingest inventory events to Bronze layer."""
        logger.info("Starting Inventory Bronze ingestion...")
        
        raw_df = self.processor.read_kafka_stream(self.config.INVENTORY_TOPIC)
        
        parsed_df = self.processor.parse_json_with_schema(
            raw_df,
            EventSchemas.INVENTORY_SCHEMA
        )
        
        deduped_df = self.processor.apply_deduplication(
            parsed_df,
            id_columns=["event_id"]
        )
        
        table_path = f"{self.config.BRONZE_PATH}/inventory"
        query = self.processor.write_to_delta(
            deduped_df,
            table_path,
            partition_columns=["_partition_date"]
        )
        
        self.queries["inventory"] = query
    
    def ingest_payments(self) -> None:
        """Ingest payment events to Bronze layer."""
        logger.info("Starting Payments Bronze ingestion...")
        
        raw_df = self.processor.read_kafka_stream(self.config.PAYMENTS_TOPIC)
        
        parsed_df = self.processor.parse_json_with_schema(
            raw_df,
            EventSchemas.PAYMENT_SCHEMA
        )
        
        deduped_df = self.processor.apply_deduplication(
            parsed_df,
            id_columns=["event_id"]
        )
        
        table_path = f"{self.config.BRONZE_PATH}/payments"
        query = self.processor.write_to_delta(
            deduped_df,
            table_path,
            partition_columns=["_partition_date"]
        )
        
        self.queries["payments"] = query
    
    def start_all(self) -> Dict[str, Any]:
        """Start all Bronze layer ingestion streams."""
        logger.info("Starting all Bronze layer ingestion streams...")
        
        self.ingest_orders()
        self.ingest_customers()
        self.ingest_clickstream()
        self.ingest_products()
        self.ingest_inventory()
        self.ingest_payments()
        
        logger.info(f"Started {len(self.queries)} streaming queries")
        return self.queries
    
    def await_termination(self):
        """Wait for all queries to terminate."""
        for name, query in self.queries.items():
            logger.info(f"Awaiting termination: {name}")
            query.awaitTermination()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution entry point."""
    logger.info("=" * 60)
    logger.info("ENTERPRISE DATA PLATFORM - STREAMING INGESTION")
    logger.info("=" * 60)
    
    # Create Spark session
    spark = create_spark_session("EnterpriseStreamingIngestion")
    
    # Initialize Bronze processor
    bronze_processor = BronzeLayerProcessor(spark)
    
    # Start all ingestion streams
    queries = bronze_processor.start_all()
    
    # Log active queries
    logger.info("Active streaming queries:")
    for name, query in queries.items():
        logger.info(f"  - {name}: {query.status}")
    
    # Await termination
    bronze_processor.await_termination()


if __name__ == "__main__":
    main()
