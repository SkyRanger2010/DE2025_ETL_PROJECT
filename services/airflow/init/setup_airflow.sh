#!/bin/bash

# Запуск Airflow
airflow db migrate

# Создание юзеров
airflow users create \
    --username "$_AIRFLOW_WWW_USER_USERNAME" \
    --password "$_AIRFLOW_WWW_USER_PASSWORD" \
    --firstname Admin \
    --lastname Adminov \
    --role Admin \
    --email admin@administration.info

# Создание коннектов
airflow connections add 'etl_postgres' \
    --conn-json '{
        "conn_type": "postgres",
        "login": "'"$POSTGRESQL_APP_USER"'",
        "password": "'"$POSTGRESQL_APP_PASSWORD"'",
        "host": "'"$POSTGRESQL_APP_HOST"'",
        "port": 5432,
        "schema": "'"$POSTGRESQL_APP_DB"'",
        "extra": {
            "currentSchema": "'"$POSTGRESQL_APP_SCHEMA"'"
        }
    }'


airflow version