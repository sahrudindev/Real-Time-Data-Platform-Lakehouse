"""
=============================================================================
ENTERPRISE DATA PLATFORM - DELTA LAKE UTILITIES
=============================================================================
Delta Lake maintenance and optimization utilities.
=============================================================================
"""

import os
import logging
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from delta.tables import DeltaTable

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DeltaLakeUtils:
    """Utilities for Delta Lake table management and optimization."""
    
    def __init__(self, spark):
        self.spark = spark
        self.base_path = os.getenv('DELTA_LAKE_PATH', '/data/delta')
    
    def vacuum(self, table_path, retention_hours=168):
        """Remove old files from Delta table."""
        logger.info(f"Vacuuming {table_path} with {retention_hours}h retention")
        delta_table = DeltaTable.forPath(self.spark, table_path)
        delta_table.vacuum(retention_hours)
        logger.info(f"Vacuum completed for {table_path}")
    
    def optimize(self, table_path, z_order_columns=None):
        """Optimize Delta table by compacting small files."""
        logger.info(f"Optimizing {table_path}")
        delta_table = DeltaTable.forPath(self.spark, table_path)
        
        if z_order_columns:
            delta_table.optimize().executeZOrderBy(z_order_columns)
            logger.info(f"Optimized with Z-ORDER on {z_order_columns}")
        else:
            delta_table.optimize().executeCompaction()
            logger.info(f"Compaction completed for {table_path}")
    
    def get_history(self, table_path, limit=10):
        """Get table history for auditing."""
        delta_table = DeltaTable.forPath(self.spark, table_path)
        return delta_table.history(limit)
    
    def time_travel(self, table_path, version=None, timestamp=None):
        """Read table at a specific version or timestamp."""
        reader = self.spark.read.format("delta")
        if version is not None:
            return reader.option("versionAsOf", version).load(table_path)
        elif timestamp:
            return reader.option("timestampAsOf", timestamp).load(table_path)
        return reader.load(table_path)
    
    def restore_table(self, table_path, version):
        """Restore table to a previous version."""
        logger.info(f"Restoring {table_path} to version {version}")
        delta_table = DeltaTable.forPath(self.spark, table_path)
        delta_table.restoreToVersion(version)
        logger.info(f"Restored {table_path} to version {version}")
    
    def get_table_details(self, table_path):
        """Get detailed information about a Delta table."""
        delta_table = DeltaTable.forPath(self.spark, table_path)
        return delta_table.detail()
    
    def generate_manifest(self, table_path):
        """Generate manifest files for external integrations."""
        delta_table = DeltaTable.forPath(self.spark, table_path)
        delta_table.generate("symlink_format_manifest")
        logger.info(f"Manifest generated for {table_path}")
    
    def run_maintenance(self, table_paths=None):
        """Run maintenance on all or specified tables."""
        if table_paths is None:
            table_paths = [
                f"{self.base_path}/bronze/orders",
                f"{self.base_path}/bronze/customers",
                f"{self.base_path}/bronze/products",
                f"{self.base_path}/bronze/clickstream",
                f"{self.base_path}/silver/orders",
                f"{self.base_path}/silver/customers",
                f"{self.base_path}/silver/products",
                f"{self.base_path}/gold/fact_daily_sales",
                f"{self.base_path}/gold/fact_customer_orders"
            ]
        
        for path in table_paths:
            try:
                if DeltaTable.isDeltaTable(self.spark, path):
                    self.optimize(path)
                    self.vacuum(path)
            except Exception as e:
                logger.error(f"Maintenance failed for {path}: {e}")


def main():
    spark = SparkSession.builder.appName("DeltaLakeUtils")\
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
        .getOrCreate()
    
    utils = DeltaLakeUtils(spark)
    utils.run_maintenance()
    spark.stop()


if __name__ == "__main__":
    main()
