"""
=============================================================================
ENTERPRISE DATA PLATFORM - BATCH INGESTION DAG
=============================================================================
Batch data ingestion from external sources to Delta Lake Bronze layer.
=============================================================================
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.sensors.filesystem import FileSensor
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

with DAG(
    dag_id='batch_ingestion',
    default_args=default_args,
    description='Batch data ingestion to Bronze layer',
    schedule_interval='0 */4 * * *',  # Every 4 hours
    catchup=False,
    tags=['ingestion', 'bronze', 'batch'],
    max_active_runs=1,
) as dag:
    
    # Start task
    start = BashOperator(
        task_id='start',
        bash_command='echo "Starting batch ingestion at $(date)"'
    )
    
    # Check for new data files
    check_data_files = BashOperator(
        task_id='check_data_files',
        bash_command='ls -la /data/raw/ 2>/dev/null || echo "No files found"'
    )
    
    # Spark job for batch ingestion
    ingest_batch_data = SparkSubmitOperator(
        task_id='ingest_batch_data',
        application='/opt/spark/jobs/batch_ingestion.py',
        conn_id='spark_default',
        conf={
            'spark.master': 'spark://spark-master:7077',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
        },
        packages='io.delta:delta-core_2.12:2.4.0',
        verbose=True,
    )
    
    # Validate ingested data
    validate_ingestion = BashOperator(
        task_id='validate_ingestion',
        bash_command='echo "Validating ingested data..."'
    )
    
    # End task
    end = BashOperator(
        task_id='end',
        bash_command='echo "Batch ingestion completed at $(date)"'
    )
    
    start >> check_data_files >> ingest_batch_data >> validate_ingestion >> end
