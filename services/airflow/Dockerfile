FROM apache/airflow:2.5.1
USER root
RUN mkdir -p /opt/airflow/dags
RUN chown -R airflow: /opt/airflow/dags
USER airflow
WORKDIR /opt/airflow
COPY ../../python-scripts/dags /opt/airflow/dags
