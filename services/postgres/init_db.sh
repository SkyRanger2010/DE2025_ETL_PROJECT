#!/bin/bash

# Создание временной директории
mkdir -p /tmp/sql

# Подстановка ENV VARS в шаблон SQL
envsubst < /sql/init_db_template.sql > /tmp/sql/init_db.sql

# Подключение к PG, создание БД, юзера, выдача прав и создание таблиц
psql -v ON_ERROR_STOP=1 -U "postgresuser" -f /tmp/sql/init_db.sql

psql -v ON_ERROR_STOP=1 -U "postgresuser" -f /sql/airflow_db.sql

# Удаление временной директории
rm -rf /tmp/sql