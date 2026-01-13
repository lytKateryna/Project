from fastapi import APIRouter, Query
from db.my_sql import (
    get_films as db_get_films,
    get_films_count,
    search_films_by_keyword as db_search_films_by_keyword,
    count_films_by_keyword,
    search_films_by_actor as db_search_films_by_actor,
    count_films_by_actor,
    get_title_year_genres as db_get_title_year_genres,
    count_films_by_genres_year_range,
    get_films_by_year as db_get_films_by_year,
    count_films_by_year,
    get_films_by_year_range as db_get_films_by_year_range,
    count_films_by_year_range,
    get_all_genres as db_get_all_genres,
    get_years
)
from utils.tmdb import get_poster_by_title
from utils.log_writer import log_search_keyword, log_films_id
from utils.pagination import paginate
from db import my_sql as db
# from fastapi import HTTPException


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
    result = paginate(
        fetch_items=db_get_films,
        fetch_total=get_films_count,
        limit=limit,
        offset=offset
    )
    result["items"] = add_posters(result["items"])
    return result


@router.get('/search/keyword')
def search_films_by_keyword_route(query: str, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    result = paginate(
        fetch_items=db_search_films_by_keyword,
        fetch_total=count_films_by_keyword,
        keyword=query,
        limit=limit,
        offset=offset
    )
    result["query"] = query
    result["items"] = add_posters(result["items"])
    log_search_keyword(search_type='keyword', params={"query": query})
    log_films_id([item["film_id"] for item in result["items"]])
    return result


@router.get('/search/actor')
def search_films_by_actor(full_name: str, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    result = paginate(
        fetch_items=db_search_films_by_actor,
        fetch_total=count_films_by_actor,
        full_name=full_name,
        limit=limit,
        offset=offset
    )
    result["full_name"] = full_name
    result["items"] = add_posters(result["items"])
    return result


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
def search_films_by_year_range_route(
    year_from: int,
    year_to: int,
    category_id: int | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
):
    result = paginate(
        fetch_items=db_get_films_by_year_range,
        fetch_total=count_films_by_year_range,
        year_from=year_from,
        year_to=year_to,
        category_id=category_id,
        limit=limit,
        offset=offset
    )
    result["year_from"] = year_from
    result["year_to"] = year_to
    result["category_id"] = category_id
    result["items"] = add_posters(result["items"])
    return result


@router.get('/search/year')
def search_films_by_year_route(year: int, offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    print(f"/films/search/year called with year={year} offset={offset} limit={limit}")
    error_msg = None
    try:
        result = paginate(
            fetch_items=db_get_films_by_year,
            fetch_total=count_films_by_year,
            year=year,
            limit=limit,
            offset=offset
        )
        result["year"] = year
        result["items"] = add_posters(result["items"])
    except Exception as e:
        print("DB error in get_films_by_year:", e)
        error_msg = "database_error"
        result = {
            "year": year,
            "items": [],
            "offset": offset,
            "limit": limit,
            "total": 0,
            "count": 0
        }

    if error_msg:
        result["error"] = error_msg

    return result


