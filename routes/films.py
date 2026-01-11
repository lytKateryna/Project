from fastapi import APIRouter, Query
from db.my_sql import (
    get_films as db_get_films,
    search_films_by_keyword as db_search_films_by_keyword,
    search_films_by_actor as db_search_films_by_actor,
    get_title_year_genres as db_get_title_year_genres,
    get_films_by_year as db_get_films_by_year,
    get_films_by_year_range as db_get_films_by_year_range,
    get_all_genres as db_get_all_genres,
    get_years
)
from utils.tmdb import get_poster_by_title
from utils.log_writer import log_search_keyword, log_films_id
from fastapi import HTTPException

router = APIRouter(prefix='/films', tags=['films'])

# -----------------------------
# Вспомогательная функция для добавления постеров
# -----------------------------
def add_posters(films: list[dict]) -> list[dict]:
    for film in films:
        try:
            film["poster_url"] = get_poster_by_title(film.get("title", "")) or "/static/no-poster.png"
        except Exception:
            film["poster_url"] = "/static/no-poster.png"
    return films

# -----------------------------
# Маршруты
# -----------------------------
@router.get('/latest')
def get_latest_films_route(offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = db_get_films(offset=offset, limit=limit)
    items = add_posters(items)
    return {
        "items": items,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }

@router.get('/search/keyword')
def search_films_by_keyword_route(query: str, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = db_search_films_by_keyword(query, offset=offset, limit=limit)
    items = add_posters(items)
    log_search_keyword(search_type='keyword', params={"query": query})
    log_films_id([item["film_id"] for item in items])
    return {
        "query": query,
        "items": items,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }

@router.get('/search/actor')
def search_films_by_actor(full_name: str, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = db_search_films_by_actor(full_name, offset=offset, limit=limit)
    items = add_posters(items)
    return {
        "full_name": full_name,
        "items": items,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }

@router.get('/search/genres')
def get_title_year_genres_route(category_id: int, year_from: int, year_to: int, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = db_get_title_year_genres(category_id=category_id, year_from=year_from, year_to=year_to, offset=offset, limit=limit)
    items = add_posters(items)
    return {
        "category_id": category_id,
        "year_from": year_from,
        "year_to": year_to,
        "items": items,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }

@router.get('/genres')
def get_all_genres_route():
    items = db_get_all_genres()
    # Для жанров постеры не нужны, так как нет поля title
    return {
        "items": items,
        "count": len(items)
    }

@router.get('/min_max_year/keyword')
def get_min_max_year_route():
    items = get_years()
    return items

@router.get('/search/year_range')
def search_films_by_year_range_route(year_from: int, year_to: int, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    items = db_get_films_by_year_range(year_from=year_from, year_to=year_to, offset=offset, limit=limit)
    items = add_posters(items)
    return {
        "year_from": year_from,
        "year_to": year_to,
        "items": items,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }

@router.get('/search/year')
def search_films_by_year_route(year: int, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    print(f"/films/search/year called with year={year} offset={offset} limit={limit}")
    error_msg = None
    try:
        items = db_get_films_by_year(year=year, offset=offset, limit=limit)
    except Exception as e:
        print("DB error in get_films_by_year:", e)
        error_msg = "database_error"
        items = []

    try:
        items = add_posters(items)
    except Exception as e:
        print("Poster add error:", e)

    resp = {
        "year": year,
        "items": items,
        "offset": offset,
        "limit": limit,
        "count": len(items)
    }
    if error_msg:
        resp["error"] = error_msg

    return resp




