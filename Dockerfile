FROM apache/airflow:latest

USER airflow
RUN pip install --no-cache-dir pymongo
