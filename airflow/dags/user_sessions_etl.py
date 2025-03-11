import logging
import os
from datetime import datetime
import pandas as pd

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Настройка логирования
logging.basicConfig(level=logging.INFO)

DAG_NAME = 'user_sessions_etl'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 11),
    'retries': 1,
}

dag = DAG(DAG_NAME,
          default_args=default_args,
          schedule_interval="@daily",
          catchup=False
          )

def extract(**kwargs):
    """Извлекает данные из MongoDB"""
    try:
        mongo_hook = MongoHook(mongo_conn_id='etl_mongo')
        client = mongo_hook.get_conn()
        db_name = os.getenv("MONGO_DB", "source_db")
        collection_name = "user_sessions"
        db = client[db_name]
        collection = db[collection_name]

        sessions = list(collection.find({}, {"_id": 0}))
        logging.info(f"Извлечено {len(sessions)} записей")

        # Отправляем данные в XCom
        kwargs['ti'].xcom_push(key='sessions', value=sessions)
    except Exception as e:
        logging.error(f"Ошибка при извлечении данных: {e}")
        raise

def transform(**kwargs):
    """Трансформирует данные для PostgreSQL"""
    logging.info("Запуск transform")

    ti = kwargs['ti']
    sessions = ti.xcom_pull(task_ids='extract', key='sessions')

    if not sessions:
        logging.warning("Нет данных для трансформации")
        return

    # Загружаем данные в DataFrame
    transformed = pd.DataFrame(sessions)

    # 1. Заменяем NaN на пустые списки, чтобы избежать ошибок при join()
    transformed['pages_visited'] = transformed['pages_visited'].apply(lambda x: x if isinstance(x, list) else [])
    transformed['actions'] = transformed['actions'].apply(lambda x: x if isinstance(x, list) else [])

    # 2. Соединяем списки в строку через ", "
    transformed['pages_visited'] = transformed['pages_visited'].apply(', '.join)
    transformed['actions'] = transformed['actions'].apply(', '.join)

    # 3. Очищаем остальные NaN (если остались) и приводим все пустые значения к ""
    transformed.fillna("", inplace=True)

    # 4. Удаляем дубликаты по session_id
    transformed.drop_duplicates(subset=["session_id"], inplace=True)

    logging.info(f"Трансформировано {len(transformed)} записей")

    # Преобразуем DataFrame в список кортежей для XCom
    transformed_records = transformed.to_records(index=False).tolist()

    # Отправляем трансформированные данные в XCom
    ti.xcom_push(key='transformed_sessions', value=transformed_records)

def load(**kwargs):
    """Загружает данные в PostgreSQL через Airflow Connection"""
    logging.info("Запуск load")

    ti = kwargs['ti']
    transformed_sessions = ti.xcom_pull(task_ids='transform', key='transformed_sessions')

    if not transformed_sessions:
        logging.warning("Нет данных для загрузки в PostgreSQL")
        return

    try:
        pg_hook = PostgresHook(postgres_conn_id="etl_postgres")
        engine = pg_hook.get_sqlalchemy_engine()

        # Создаём DataFrame обратно
        columns = ["session_id", "user_id", "start_time", "end_time", "pages_visited", "device", "actions"]
        transformed_df = pd.DataFrame(transformed_sessions, columns=columns)

        # Загружаем данные в PostgreSQL
        transformed_df.to_sql(name="user_sessions", schema="source", con=engine, if_exists='append', index=False)

        logging.info(f"Загружено {len(transformed_df)} записей в PostgreSQL")

    except Exception as e:
        logging.error(f"Ошибка при загрузке данных: {e}")
        raise

# Заглушки
task_start = DummyOperator(
    task_id='start',
    dag=dag
)

task_finish = DummyOperator(
    task_id='finish',
    dag=dag
)

task_extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    provide_context=True,
    dag=dag
)

task_transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    provide_context=True,
    dag=dag
)

task_load = PythonOperator(
    task_id='load',
    python_callable=load,
    provide_context=True,
    dag=dag
)

# Определяем порядок выполнения
task_start >> task_extract >> task_transform >> task_load >> task_finish
