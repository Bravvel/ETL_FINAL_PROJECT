from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime, timedelta

# Подключаемся к MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["etl_database"]

fake = Faker()

# Функция для генерации UserSessions
def generate_user_sessions(n=10):
    sessions = []
    for _ in range(n):
        sessions.append({
            "session_id": fake.uuid4(),
            "user_id": random.randint(1, 100),
            "start_time": fake.date_time_between(start_date="-1y", end_date="now"),
            "end_time": fake.date_time_between(start_date="now", end_date="+1y"),
            "pages_visited": [fake.uri_path() for _ in range(random.randint(1, 5))],
            "device": random.choice(["Windows PC", "MacBook", "iPhone", "Android"]),
            "actions": random.choices(["click", "scroll", "purchase", "logout"], k=random.randint(1, 5))
        })
    db.UserSessions.insert_many(sessions)

# Функция для генерации ProductPriceHistory
def generate_product_price_history(n=10):
    products = []
    for _ in range(n):
        products.append({
            "product_id": fake.uuid4(),
            "price_changes": [
                {"date": fake.date_this_year().isoformat(), "price": round(random.uniform(10, 500), 2)}
                for _ in range(5)
            ],
            "current_price": round(random.uniform(10, 500), 2),
            "currency": "USD"
        })
    db.ProductPriceHistory.insert_many(products)

# Функция для генерации EventLogs
def generate_event_logs(n=10):
    events = []
    for _ in range(n):
        events.append({
            "event_id": fake.uuid4(),
            "timestamp": fake.date_time_this_year(),
            "event_type": random.choice(["login", "logout", "error", "purchase"]),
            "details": fake.sentence()
        })
    db.EventLogs.insert_many(events)

# Функция для генерации SupportTickets
def generate_support_tickets(n=10):
    tickets = []
    for _ in range(n):
        tickets.append({
            "ticket_id": fake.uuid4(),
            "user_id": random.randint(1, 100),
            "status": random.choice(["open", "closed", "pending"]),
            "issue_type": random.choice(["billing", "technical", "account"]),
            "messages": [fake.text() for _ in range(random.randint(1, 5))],
            "created_at": fake.date_time_this_year(),
            "updated_at": fake.date_time_this_year()
        })
    db.SupportTickets.insert_many(tickets)

# Функция для генерации UserRecommendations
def generate_user_recommendations(n=10):
    recommendations = []
    for _ in range(n):
        recommendations.append({
            "user_id": random.randint(1, 100),
            "recommended_products": [fake.uuid4() for _ in range(random.randint(1, 5))],
            "last_updated": fake.date_time_this_year()
        })
    db.UserRecommendations.insert_many(recommendations)

# Функция для генерации ModerationQueue
def generate_moderation_queue(n=10):
    reviews = []
    for _ in range(n):
        reviews.append({
            "review_id": fake.uuid4(),
            "user_id": random.randint(1, 100),
            "product_id": fake.uuid4(),
            "review_text": fake.text(),
            "rating": random.randint(1, 5),
            "moderation_status": random.choice(["pending", "approved", "rejected"]),
            "flags": random.choices(["spam", "offensive", "irrelevant"], k=random.randint(0, 2)),
            "submitted_at": fake.date_time_this_year()
        })
    db.ModerationQueue.insert_many(reviews)

# Функция для генерации SearchQueries
def generate_search_queries(n=10):
    queries = []
    for _ in range(n):
        queries.append({
            "query_id": fake.uuid4(),
            "user_id": random.randint(1, 100),
            "query_text": fake.word(),
            "timestamp": fake.date_time_this_year(),
            "filters": {"category": fake.word(), "price_range": f"{random.randint(10, 100)}-{random.randint(101, 500)}"},
            "results_count": random.randint(0, 100)
        })
    db.SearchQueries.insert_many(queries)

# Генерируем тестовые данные
generate_user_sessions(20)
generate_product_price_history(20)
generate_event_logs(20)
generate_support_tickets(20)
generate_user_recommendations(20)
generate_moderation_queue(20)
generate_search_queries(20)

print("Данные успешно добавлены в MongoDB!")
