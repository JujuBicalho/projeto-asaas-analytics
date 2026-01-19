from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    'pipeline_pagamentos_asaas',
    start_date=datetime(2023, 1, 1),
    schedule=None, 
    catchup=False
) as dag:
    
    rodar_modelos = BashOperator(
        task_id='dbt_run',
        bash_command='cd /usr/local/airflow/include/transformacoes_asaas && dbt run --profiles-dir .'
    )

    testar_dados = BashOperator(
        task_id='dbt_test',
        bash_command='cd /usr/local/airflow/include/transformacoes_asaas && dbt test --profiles-dir .'
    )

    rodar_modelos >> testar_dados