from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
from airflow.models.baseoperator import chain

default_args = {
    'owner': 'airflow',
    'start_date':datetime(2025, 3, 11),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    dag_id='run_users_activity_pipeline',
    default_args=default_args,
    description='Запуск всех DAG репликации перед формированием витрины пользовательской активности',
    schedule_interval=None,
    is_paused_upon_creation=False,
    catchup=False
)

# Запускаем необходимые DAG'и репликации данных
trigger_user_sessions = TriggerDagRunOperator(
    task_id='trigger_user_sessions_etl',
    trigger_dag_id='user_sessions_etl',
    wait_for_completion=True,
    dag=dag
)

trigger_search_queries = TriggerDagRunOperator(
    task_id='trigger_search_queries_etl',
    trigger_dag_id='search_queries_etl',
    wait_for_completion=True,
    dag=dag
)

trigger_support_tickets = TriggerDagRunOperator(
    task_id='trigger_support_tickets_etl',
    trigger_dag_id='support_tickets_etl',
    wait_for_completion=True,
    dag=dag
)

trigger_user_recommendations = TriggerDagRunOperator(
    task_id='trigger_user_recommendations_etl',
    trigger_dag_id='user_recommendations_etl',
    wait_for_completion=True,
    dag=dag
)


# Запускаем DAG витрины `users_activity_mart_create`
trigger_users_activity_mart = TriggerDagRunOperator(
    task_id='trigger_users_activity_mart',
    trigger_dag_id='users_activity_mart_create',
    wait_for_completion=True,
    dag=dag
)

# Определяем последовательность выполнения задач
chain(
    [trigger_user_sessions, trigger_search_queries, trigger_support_tickets, trigger_user_recommendations],
    trigger_users_activity_mart
)
