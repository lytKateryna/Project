# Импортируем нужные библиотеки

from pymongo import MongoClient
from datetime import datetime
from settings import settings
print("MONGO_URL used:", settings.MONGO_URL)
print("MONGO_DB:", settings.MONGO_DB)
print("COLLECTION:", settings.MONGO_LOG_COLLECTION)
client = MongoClient(settings.MONGO_URL, serverSelectionTimeoutMS=5000)
db = client[settings.MONGO_DB]
collection = db[settings.MONGO_LOG_COLLECTION]


def ping():
    client.admin.command("ping")

def save_search_query(query: str):
    if not query or not query.strip():
        return
    clean_query = query.strip().lower()

    try:
        ping() 
        collection.update_one(
            {"query": clean_query},
            {"$set": {"last_searched": datetime.utcnow()},
             "$inc": {"count": 1}},
            upsert=True
        )
    except Exception as e:
        print(f"Ошибка MongoDB: {e}")
def get_popular_queries(limit: int = 5):
    """Самые популярные (по количеству запросов через 'count')"""
    try:
        cursor = collection.find().sort("count", -1).limit(limit)
        return [doc["query"] for doc in cursor if "query" in doc]
    except Exception as error:
        print(f"Ошибка чтения популярных: {error}")
        return []


def get_recent_queries(limit: int = 5):
    """Часто ищут / Недавние """
    try:
        cursor = collection.find().sort("last_searched", -1).limit(limit)
        return [doc["query"] for doc in cursor if "query" in doc]
    except Exception as e:
        print(f"Ошибка чтения последних: {e}")
        return []


if __name__ == "__main__":
    print("Проверка подключения...")
    try:
        save_search_query("test_query")
        print(f"Запрос отправлен в коллекцию: {collection}")

        popular = get_popular_queries(5)
        recent = get_recent_queries(5)

        print(f"ТОП Популярных (по количеству): {popular}")
        print(f"ТОП Недавних (по времени): {recent}")
    except Exception as err:
        print(f"Ошибка при тестировании: {err}")