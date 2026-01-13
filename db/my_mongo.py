# Импортируем нужные библиотеки

from pymongo import MongoClient
from datetime import datetime
from settings import settings

# Подключаемся к DB
MONGO_DB = MongoClient(settings.MONGO_URL)
COLLECTION_NAME = settings.MONGO_LOG_COLLECTION
MONGO_DB = MONGO_DB[settings.MONGO_DB]


def save_search_query(query: str):
    """Сохранение запроса."""
    if not query or not query.strip():
        return
    clean_query = query.strip().lower()
    try:
        MONGO_DB[COLLECTION_NAME].update_one(
            {"query": clean_query},
            {
                "$set": {"last_searched": datetime.now()},
                "$inc": {"count": 1}
            },
            upsert=True
        )
    except Exception as e:
        print(f"Ошибка записи в MongoDB: {e}")

# для отображения на фронтенде
def get_popular_queries(limit: int = 5):
    """Самые популярные (по количеству запросов через 'count')"""
    try:
        # Сортируем по count
        cursor = MONGO_DB[COLLECTION_NAME].find().sort("count", -1).limit(limit)
        return [doc["query"] for doc in cursor if "query" in doc]
    except Exception as error:
        print(f"Ошибка чтения популярных: {error}")
        return []


def get_recent_queries(limit: int = 5):
    """Часто ищут / Недавние """
    try:
        # Сортируем по дате
        cursor = MONGO_DB[COLLECTION_NAME].find().sort("last_searched", -1).limit(limit)
        return [doc["query"] for doc in cursor if "query" in doc]
    except Exception as e:
        print(f"Ошибка чтения последних: {e}")
        return []


if __name__ == "__main__":
    print("Проверка подключения...")
    try:
        save_search_query("test_query")
        print(f"Запрос отправлен в коллекцию: {COLLECTION_NAME}")

        popular = get_popular_queries(5)
        recent = get_recent_queries(5)

        print(f"ТОП Популярных (по количеству): {popular}")
        print(f"ТОП Недавних (по времени): {recent}")
    except Exception as err:
        print(f"Ошибка при тестировании: {err}")