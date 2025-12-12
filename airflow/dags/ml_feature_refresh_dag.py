"""
=============================================================================
ENTERPRISE DATA PLATFORM - ML FEATURE REFRESH DAG
=============================================================================
Refreshes ML feature store with latest data.
=============================================================================
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=10),
}

FEATURE_STORE_DIR = '/opt/feature_store'


def materialize_features(**context):
    """Materialize features to online and offline stores."""
    import subprocess
    result = subprocess.run(
        ['feast', 'materialize-incremental', datetime.now().isoformat()],
        cwd=FEATURE_STORE_DIR,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise ValueError(f"Feature materialization failed: {result.stderr}")
    return result.stdout


with DAG(
    dag_id='ml_feature_refresh',
    default_args=default_args,
    description='Refresh ML feature store',
    schedule_interval='0 */6 * * *',  # Every 6 hours
    catchup=False,
    tags=['ml', 'feature_store', 'feast'],
    max_active_runs=1,
) as dag:
    
    start = BashOperator(
        task_id='start',
        bash_command='echo "Starting ML feature refresh at $(date)"'
    )
    
    # Build feature views from Gold layer
    build_feature_views = SparkSubmitOperator(
        task_id='build_feature_views',
        application='/opt/spark/jobs/feature_engineering.py',
        conn_id='spark_default',
        conf={
            'spark.master': 'spark://spark-master:7077',
            'spark.sql.extensions': 'io.delta.sql.DeltaSparkSessionExtension',
        },
        packages='io.delta:delta-core_2.12:2.4.0',
    )
    
    # Apply feast feature definitions
    apply_feast = BashOperator(
        task_id='apply_feast',
        bash_command=f'cd {FEATURE_STORE_DIR} && feast apply'
    )
    
    # Materialize features
    materialize = PythonOperator(
        task_id='materialize_features',
        python_callable=materialize_features
    )
    
    # Validate features
    validate_features = BashOperator(
        task_id='validate_features',
        bash_command=f'cd {FEATURE_STORE_DIR} && feast feature-views list'
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "ML feature refresh completed at $(date)"'
    )
    
    start >> build_feature_views >> apply_feast >> materialize >> validate_features >> end
