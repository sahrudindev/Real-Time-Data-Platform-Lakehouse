"""
=============================================================================
ENTERPRISE DATA PLATFORM - STREAMING ORCHESTRATION DAG
=============================================================================
Manages Spark Structured Streaming jobs lifecycle.
=============================================================================
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.sensors.python import PythonSensor

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}


def check_streaming_health(**context):
    """Check if streaming jobs are healthy."""
    import requests
    try:
        response = requests.get('http://spark-master:8080/api/v1/applications')
        apps = response.json()
        running_apps = [app for app in apps if app.get('state') == 'RUNNING']
        return len(running_apps) > 0
    except Exception as e:
        print(f"Error checking streaming health: {e}")
        return False


with DAG(
    dag_id='streaming_orchestration',
    default_args=default_args,
    description='Manage Spark Streaming jobs',
    schedule_interval='@daily',
    catchup=False,
    tags=['streaming', 'spark', 'kafka'],
    max_active_runs=1,
) as dag:
    
    start = BashOperator(
        task_id='start',
        bash_command='echo "Starting streaming orchestration at $(date)"'
    )
    
    # Check Kafka connectivity
    check_kafka = BashOperator(
        task_id='check_kafka',
        bash_command='kafka-topics --bootstrap-server kafka:9092 --list || exit 1'
    )
    
    # Start Bronze ingestion streaming
    start_bronze_streaming = SparkSubmitOperator(
        task_id='start_bronze_streaming',
        application='/opt/spark/jobs/streaming_ingestion.py',
        conn_id='spark_default',
        conf={
            'spark.master': 'spark://spark-master:7077',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
            'spark.sql.catalog.spark_catalog': 'org.apache.spark.sql.delta.catalog.DeltaCatalog',
            'spark.streaming.stopGracefullyOnShutdown': 'true',
        },
        packages='io.delta:delta-core_2.12:2.4.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0',
        verbose=True,
    )
    
    # Monitor streaming health
    monitor_streaming = PythonSensor(
        task_id='monitor_streaming',
        python_callable=check_streaming_health,
        poke_interval=60,
        timeout=300,
        mode='poke',
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "Streaming orchestration completed at $(date)"'
    )
    
    start >> check_kafka >> start_bronze_streaming >> monitor_streaming >> end
