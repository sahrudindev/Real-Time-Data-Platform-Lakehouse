"""
=============================================================================
ENTERPRISE DATA PLATFORM - DATA QUALITY DAG
=============================================================================
Data quality validation using Great Expectations.
=============================================================================
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

GE_PROJECT_DIR = '/opt/great_expectations'


def run_checkpoint(checkpoint_name: str, **context):
    """Run a Great Expectations checkpoint."""
    import great_expectations as gx
    
    context_gx = gx.get_context(context_root_dir=GE_PROJECT_DIR)
    result = context_gx.run_checkpoint(checkpoint_name=checkpoint_name)
    
    if not result.success:
        raise ValueError(f"Checkpoint {checkpoint_name} failed!")
    
    return result.success


def send_quality_alert(message: str, **context):
    """Send data quality alert."""
    print(f"ALERT: {message}")
    # Add Slack/Email notification here


with DAG(
    dag_id='data_quality_validation',
    default_args=default_args,
    description='Run Great Expectations data quality checks',
    schedule_interval='0 */3 * * *',  # Every 3 hours
    catchup=False,
    tags=['quality', 'great_expectations', 'validation'],
    max_active_runs=1,
) as dag:
    
    start = BashOperator(
        task_id='start',
        bash_command='echo "Starting data quality validation at $(date)"'
    )
    
    # Bronze layer validation
    with TaskGroup(group_id='bronze_validation') as bronze_validation:
        validate_bronze_orders = PythonOperator(
            task_id='validate_bronze_orders',
            python_callable=run_checkpoint,
            op_kwargs={'checkpoint_name': 'bronze_orders_checkpoint'}
        )
        
        validate_bronze_customers = PythonOperator(
            task_id='validate_bronze_customers',
            python_callable=run_checkpoint,
            op_kwargs={'checkpoint_name': 'bronze_customers_checkpoint'}
        )
    
    # Silver layer validation
    with TaskGroup(group_id='silver_validation') as silver_validation:
        validate_silver_orders = PythonOperator(
            task_id='validate_silver_orders',
            python_callable=run_checkpoint,
            op_kwargs={'checkpoint_name': 'silver_orders_checkpoint'}
        )
        
        validate_silver_customers = PythonOperator(
            task_id='validate_silver_customers',
            python_callable=run_checkpoint,
            op_kwargs={'checkpoint_name': 'silver_customers_checkpoint'}
        )
    
    # Gold layer validation
    with TaskGroup(group_id='gold_validation') as gold_validation:
        validate_gold_sales = PythonOperator(
            task_id='validate_gold_sales',
            python_callable=run_checkpoint,
            op_kwargs={'checkpoint_name': 'gold_daily_sales_checkpoint'}
        )
    
    # Generate data docs
    generate_docs = BashOperator(
        task_id='generate_data_docs',
        bash_command=f'cd {GE_PROJECT_DIR} && great_expectations docs build --no-view'
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "Data quality validation completed at $(date)"'
    )
    
    start >> bronze_validation >> silver_validation >> gold_validation >> generate_docs >> end
