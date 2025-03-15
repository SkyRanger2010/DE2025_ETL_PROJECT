from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date':datetime(2025, 3, 11),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    dag_id='run_support_efficiency_pipeline',
    default_args=default_args,
    description='Запуск всех DAG репликации перед формированием витрины эффективности поддержки',
    schedule_interval=None,
    is_paused_upon_creation=False,
    catchup=False
)

#  Запускаем необходимые DAG'и репликации данных
trigger_support_tickets = TriggerDagRunOperator(
    task_id='trigger_support_tickets_etl',
    trigger_dag_id='support_tickets_etl',
    wait_for_completion=True,
    dag=dag
)


#  Запускаем DAG витрины `support_efficiency_mart_create`
trigger_users_activity_mart = TriggerDagRunOperator(
    task_id='trigger_support_efficiency_mart',
    trigger_dag_id='support_efficiency_mart_create',
    wait_for_completion=True,
    dag=dag
)

trigger_support_tickets >> trigger_users_activity_mart