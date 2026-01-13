from fastapi import APIRouter, Query
from db.my_mongo import (
    save_search_query,
    get_popular_queries,
    get_recent_queries
)

# Роутер для мета-информации (поисковые запросы)
router = APIRouter(prefix="/meta", tags=["meta"])


@router.post("/search")
def save_search(query: str = Query(..., min_length=1)):
    """
    Сохранить поисковый запрос в MongoDB
    """
    save_search_query(query)
    return {
        "status": "ok",
        "query": query
    }


@router.get("/popular")
def popular_queries(limit: int = Query(5, ge=1, le=20)):
    """
    Получить самые популярные поисковые запросы
    """
    items = get_popular_queries(limit)
    return {
        "items": items,
        "count": len(items)
    }


@router.get("/recent")
def recent_queries(limit: int = Query(5, ge=1, le=20)):
    """
    Получить последние поисковые запросы
    """
    items = get_recent_queries(limit)
    return {
        "items": items,
        "count": len(items)
    }

