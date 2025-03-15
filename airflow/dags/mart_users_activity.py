from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

name_mart = 'users_activity_mart'

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
    description='Создание витрины пользовательской активности',
    schedule_interval='@daily',
    catchup=False
)

# Путь к SQL-файлу
sql_file_path = f'./sql/{name_mart}.sql'

# SQLExecuteQueryOperator выполняет SQL из файла
create_user_activity_mart = SQLExecuteQueryOperator(
    task_id=f'create_{name_mart}',
    conn_id='etl_postgres',
    sql=sql_file_path,
    autocommit=True,
    dag=dag
)

create_user_activity_mart
