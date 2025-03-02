from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pymongo import MongoClient
import psycopg2

MONGO_URI = "mongodb://admin:admin@etl_mongo:27017/"
POSTGRES_CONN = "dbname='etl_database' user='postgres' host='etl_postgres' password='postgres'"

def extract():
    client = MongoClient(MONGO_URI)
    db = client["etl_database"]
    sessions = list(db["UserSessions"].find())
    return sessions

def transform(sessions):
    transformed = [
        (
            session["session_id"],
            session["user_id"],
            session["start_time"],
            session["end_time"],
            session["pages_visited"],
            session["device"],
            session["actions"]
        ) for session in sessions
    ]
    return transformed

def load(transformed_sessions):
    conn = psycopg2.connect(POSTGRES_CONN)
    cur = conn.cursor()
    for session in transformed_sessions:
        cur.execute("""
            INSERT INTO user_sessions (session_id, user_id, start_time, end_time, pages_visited, device, actions)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, session)
    conn.commit()
    cur.close()
    conn.close()

with DAG(
    dag_id="etl_pipeline",
    start_date=datetime(2024, 3, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform,
        provide_context=True
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load,
        provide_context=True
    )

    extract_task >> transform_task >> load_task
