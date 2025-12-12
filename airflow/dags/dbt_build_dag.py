"""
=============================================================================
ENTERPRISE DATA PLATFORM - DBT BUILD DAG
=============================================================================
Orchestrates dbt runs for data transformations.
=============================================================================
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.task_group import TaskGroup

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

DBT_PROJECT_DIR = '/opt/dbt'

with DAG(
    dag_id='dbt_build',
    default_args=default_args,
    description='Run dbt transformations',
    schedule_interval='0 */2 * * *',  # Every 2 hours
    catchup=False,
    tags=['dbt', 'transformation', 'silver', 'gold'],
    max_active_runs=1,
) as dag:
    
    start = BashOperator(
        task_id='start',
        bash_command=f'echo "Starting dbt build at $(date)"'
    )
    
    # dbt deps
    dbt_deps = BashOperator(
        task_id='dbt_deps',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt deps'
    )
    
    # dbt run staging models
    with TaskGroup(group_id='staging_models') as staging:
        dbt_run_staging = BashOperator(
            task_id='dbt_run_staging',
            bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select staging'
        )
        
        dbt_test_staging = BashOperator(
            task_id='dbt_test_staging',
            bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --select staging'
        )
        
        dbt_run_staging >> dbt_test_staging
    
    # dbt run intermediate models
    with TaskGroup(group_id='intermediate_models') as intermediate:
        dbt_run_intermediate = BashOperator(
            task_id='dbt_run_intermediate',
            bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select intermediate'
        )
        
        dbt_test_intermediate = BashOperator(
            task_id='dbt_test_intermediate',
            bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --select intermediate'
        )
        
        dbt_run_intermediate >> dbt_test_intermediate
    
    # dbt run marts models
    with TaskGroup(group_id='marts_models') as marts:
        dbt_run_marts = BashOperator(
            task_id='dbt_run_marts',
            bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select marts'
        )
        
        dbt_test_marts = BashOperator(
            task_id='dbt_test_marts',
            bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --select marts'
        )
        
        dbt_run_marts >> dbt_test_marts
    
    # Generate docs
    dbt_docs = BashOperator(
        task_id='dbt_docs_generate',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt docs generate'
    )
    
    # Freshness check
    dbt_source_freshness = BashOperator(
        task_id='dbt_source_freshness',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt source freshness || true'
    )
    
    end = BashOperator(
        task_id='end',
        bash_command='echo "dbt build completed at $(date)"'
    )
    
    start >> dbt_deps >> staging >> intermediate >> marts >> [dbt_docs, dbt_source_freshness] >> end
