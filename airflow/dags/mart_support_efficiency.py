from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

name_mart = 'support_efficiency_mart'

# Определяем параметры DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 11),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    dag_id=f'{name_mart}_create',
    default_args=default_args,
    description='Создание витрины эффективности поддержки',
    schedule_interval=None,
    is_paused_upon_creation=False,
    catchup=False
)

# Путь к SQL-файлу
sql_file_path = f'./sql/{name_mart}.sql'

# SQLExecuteQueryOperator выполняет SQL из файла
create_support_efficiency_mart = SQLExecuteQueryOperator(
    task_id=f'create_{name_mart}',
    conn_id='etl_postgres',
    sql=sql_file_path,
    autocommit=True,
    dag=dag
)

create_support_efficiency_mart
