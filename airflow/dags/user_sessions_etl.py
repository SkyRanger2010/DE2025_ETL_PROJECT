import logging
import os
from datetime import datetime
from typing import List, Tuple

from airflow.decorators import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Определение DAG
    @dag(
        start_date=datetime(2024, 3, 1),
        schedule_interval="@daily",
        catchup=False
    )
    def my_etl():
        @task()
        def extract() -> List[dict]:
            try:
                # Используем Airflow Connection
                mongo_hook = MongoHook(mongo_conn_id='etl_mongo')
                client = mongo_hook.get_conn()
                # Получаем название БД из переменной окружения (если нет, то "source_db")
                db_name = os.getenv("MONGO_DB", "source_db")
                collection_name = "user_sessions"
                db = client[db_name]
                collection = db[collection_name]

                # Правильный запрос с исключением _id
                sessions = list(collection.find({}, {"_id": 0}))
                logging.info(f"Извлечено {len(sessions)} записей")
                return sessions
            except Exception as e:
                logging.error(f"Ошибка при извлечении данных: {e}")
                raise


        @task()
        def transform(sessions: List[dict]) -> List[Tuple]:
            """Трансформирует данные для PostgreSQL."""
            logging.info("Запуск transform")
            if not sessions:
                logging.warning("Нет данных для трансформации")
                return []

            transformed = [
                (
                    session["session_id"],
                    session["user_id"],
                    session.get("start_time"),
                    session.get("end_time"),
                    session.get("pages_visited", []),
                    session.get("device", ""),
                    session.get("actions", [])
                ) for session in sessions
            ]

            logging.info(f"Трансформировано {len(transformed)} записей")
            return transformed


        @task()
        def load(transformed_sessions: List[Tuple]):
            """Загружает данные в PostgreSQL через Airflow Connection."""
            logging.info("Запуск load")

            if not transformed_sessions:
                logging.warning("Нет данных для загрузки в PostgreSQL")
                return

            try:
                pg_hook = PostgresHook(postgres_conn_id="etl_postgres")  # Используем Airflow Connection
                conn = pg_hook.get_conn()
                cur = conn.cursor()
                cur
                # Создание схемы и таблицы, если их нет
                cur.execute("CREATE SCHEMA IF NOT EXISTS source;")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS source.user_sessions (
                        session_id VARCHAR PRIMARY KEY,
                        user_id VARCHAR NOT NULL,
                        start_time TIMESTAMP,
                        end_time TIMESTAMP,
                        pages_visited JSONB,
                        device TEXT,
                        actions JSONB
                    );
                """)

                # Вставка данных
                cur.executemany("""
                    INSERT INTO source.user_sessions (session_id, user_id, start_time, end_time, pages_visited, device, actions)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (session_id) DO NOTHING;
                """, transformed_sessions)

                conn.commit()
                cur.close()
                conn.close()

                logging.info(f"Загружено {len(transformed_sessions)} записей в PostgreSQL")

            except Exception as e:
                logging.error(f"Ошибка при загрузке данных: {e}")
                raise

        extracted_data = extract()
        transformed_data = transform(extracted_data)
        load(transformed_data)
my_etl()