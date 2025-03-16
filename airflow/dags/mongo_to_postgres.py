from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
import psycopg2
from datetime import datetime, timezone

# Подключение к MongoDB и PostgreSQL
MONGO_CONN = "mongodb://mongodb:27017"
POSTGRES_CONN = {
    "host": "postgres",
    "database": "etl_project",
    "user": "airflow",
    "password": "airflow",
    "port": 5432
}

# Настройки имен коллекций и таблиц
MONGO_COLLECTION = "ModerationQueue"  # Название коллекции в MongoDB
POSTGRES_TABLE = "moderation_queue"  # Название таблицы в PostgreSQL

# Функция для извлечения данных из MongoDB
def extract_from_mongo():
    client = MongoClient(MONGO_CONN)
    db = client["etl_database"]
    collection = db[MONGO_COLLECTION]
    data = list(collection.find({}, {"_id": 0}))  # Игнорируем _id MongoDB
    client.close()
    return data

# Функция для загрузки данных в PostgreSQL
from datetime import datetime

def load_to_postgres(**kwargs):
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="extract")

    if not data:
        raise ValueError("Ошибка: XCom вернул None")

    conn = psycopg2.connect(**POSTGRES_CONN)
    cursor = conn.cursor()

    for row in data:
        # Преобразуем `submitted_at` из строки в нормальный datetime
        timestamp = row["submitted_at"]["timestamp"]
        submitted_at = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(f"""
            INSERT INTO {POSTGRES_TABLE} (user_id, product_id, review_text, rating, moderation_status, flags, submitted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row["user_id"],
            row["product_id"],
            row["review_text"],
            row["rating"],
            row["moderation_status"],
            row["flags"],
            submitted_at  # Теперь в формате TIMESTAMP
        ))

    conn.commit()
    cursor.close()
    conn.close()


# Определение DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 15),
    "retries": 1
}

dag = DAG(
    "mongo_to_postgres",
    default_args=default_args,
    schedule="@daily",
    catchup=False
)

# Операторы Airflow
extract = PythonOperator(
    task_id="extract",
    python_callable=extract_from_mongo,
    dag=dag
)

load = PythonOperator(
    task_id="load",
    python_callable=load_to_postgres,
    dag=dag
)

extract >> load  # Последовательность задач
