import mysql.connector
from settings import settings


dbconfig = {
    'host': settings.MYSQL_HOST,
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
    'database': settings.MYSQL_DB,
}

_cfg = dbconfig.copy()

def query_all(sql: str, params: tuple=())->list[dict]:
    with mysql.connector.connect(**_cfg) as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()


def get_films(limit: int = 10, offset:int = 0)->list[dict]:
    sql = """
        SELECT film_id, title, release_year, length, rating, '/static/no-poster.png' AS poster_url
        FROM film
        ORDER BY release_year DESC, film_id DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql,(limit, offset))


def get_films_count() -> int:
    sql = "SELECT COUNT(*) AS total FROM film;"
    row = query_all(sql)
    return row[0]["total"] if row else 0



def search_films_by_keyword(keyword:str, limit: int = 10, offset:int = 0)->list[dict]:
    sql = """
      SELECT film_id, title, release_year, length, rating, '/static/no-poster.png' AS poster_url
      FROM film
      WHERE LOWER(title) LIKE %s
      ORDER BY release_year DESC, film_id DESC
      LIMIT %s OFFSET %s;
    """
    return query_all(sql, (f"%{keyword.strip().lower()}%", limit, offset))
def count_films_by_keyword(keyword: str) -> int:
    sql = """
        SELECT COUNT(*) AS total
        FROM film
        WHERE LOWER(title) LIKE %s;
    """
    row = query_all(sql, (f"%{keyword.lower()}%",))
    return row[0]["total"] if row else 0


def count_films_by_actor(full_name: str) -> int:
    sql = """
        SELECT COUNT(*) AS total
        FROM film AS f
        JOIN film_actor AS fa ON fa.film_id = f.film_id
        JOIN actor AS a ON a.actor_id = fa.actor_id
        WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s;
    """
    row = query_all(sql, (f"%{full_name}%",))
    return row[0]["total"] if row else 0


def count_films_by_genres_year_range(category_id: int, year_from: int, year_to: int) -> int:
    sql = """
        SELECT COUNT(*) AS total
        FROM film AS f
        JOIN film_category AS fc ON fc.film_id = f.film_id
        WHERE fc.category_id = %s AND f.release_year BETWEEN %s AND %s;
    """
    row = query_all(sql, (category_id, year_from, year_to))
    return row[0]["total"] if row else 0


def count_films_by_year(year: int) -> int:
    sql = """
        SELECT COUNT(*) AS total
        FROM film
        WHERE release_year = %s;
    """
    row = query_all(sql, (year,))
    return row[0]["total"] if row else 0


def count_films_by_year_range(year_from: int, year_to: int, category_id: int | None = None) -> int:
    if category_id is not None:
        sql = """
            SELECT COUNT(*) AS total
            FROM film AS f
            JOIN film_category AS fc ON fc.film_id = f.film_id
            WHERE f.release_year BETWEEN %s AND %s AND fc.category_id = %s;
        """
        row = query_all(sql, (year_from, year_to, category_id))
    else:
        sql = """
            SELECT COUNT(*) AS total
            FROM film
            WHERE release_year BETWEEN %s AND %s;
        """
        row = query_all(sql, (year_from, year_to))
    return row[0]["total"] if row else 0


def get_films_by_year_range(
    year_from: int,
    year_to: int,
    category_id: int | None = None,
    limit: int = 10,
    offset: int = 0
) -> list[dict]:

    if category_id is not None:
        sql = """
            SELECT f.film_id, f.title, f.release_year, f.length, f.rating,
                   '/static/no-poster.png' AS poster_url
            FROM film AS f
            JOIN film_category AS fc ON fc.film_id = f.film_id
            WHERE f.release_year BETWEEN %s AND %s
              AND fc.category_id = %s
            ORDER BY f.release_year DESC, f.film_id DESC
            LIMIT %s OFFSET %s;
        """
        return query_all(sql, (year_from, year_to, category_id, limit, offset))

    sql = """
        SELECT film_id, title, release_year, length, rating,
               '/static/no-poster.png' AS poster_url
        FROM film
        WHERE release_year BETWEEN %s AND %s
        ORDER BY release_year DESC, film_id DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql, (year_from, year_to, limit, offset))


def get_all_genres()->list[dict]:
    sql = """
          SELECT category_id, name, '/static/no-poster.png' AS poster_url 
          FROM category
          ORDER BY name;
          """
    return query_all(sql)

def get_years()->list[dict]:
    sql = """
    SELECT MIN(release_year) AS min_year,
    MAX(release_year) AS max_year
    FROM film;
     """
    return query_all(sql)

def search_films_by_year(year: int, offset: int = 0, limit: int = 10) -> list[dict]:
    sql = """
        SELECT film_id, title, release_year, rating, length
        FROM film
        WHERE release_year = %s
        ORDER BY rating DESC
        LIMIT %s OFFSET %s
    """
    return query_all(sql, params=(year, limit, offset))

def get_title_year_genres(category_id:int, year_from:int, year_to:int,limit:int = 10, offset:int = 0)->list[dict]:
    sql = """
          SELECT f.film_id, f.title, f.release_year, f.length, f.rating, c.name as genre, '/static/no-poster.png' AS poster_url
          FROM film as f
          JOIN film_category as fc
          on fc.film_id = f.film_id
          JOIN category as c
          on c.category_id = fc.category_id
          WHERE fc.category_id = %s
          AND f.release_year BETWEEN %s AND %s
          ORDER BY f.release_year DESC, f.film_id DESC
          LIMIT %s OFFSET %s;
          """
    return query_all(sql,(category_id, year_from, year_to, limit, offset))


def get_films_by_year(year: int, limit: int = 10, offset: int = 0) -> list[dict]:
    sql = """
        SELECT film_id, title, release_year, length, rating, '/static/no-poster.png' AS poster_url
        FROM film
        WHERE release_year = %s
        ORDER BY release_year DESC, film_id DESC
        LIMIT %s OFFSET %s;
    """
    return query_all(sql, (year, limit, offset))






def search_films_by_actor(full_name:str,limit:int = 10, offset:int = 0)->list[dict]:
    sql = """
          SELECT f.film_id, 
                 f.title, 
                 f.release_year, 
                 f.length, 
                 f.rating, 
                 '/static/no-poster.png' AS poster_url
          , CONCAT(a.first_name, ' ', a.last_name) AS actor_name
          FROM film AS f
          JOIN film_actor AS fa
          ON fa.film_id = f.film_id
          JOIN actor AS a
          ON a.actor_id = fa.actor_id
          WHERE CONCAT(a.first_name, ' ', a.last_name) LIKE %s
          ORDER BY f.release_year DESC, f.film_id DESC
          LIMIT %s 
          OFFSET %s; 
          """

    pattern = f"%{full_name}%"
    return query_all(sql, (pattern, limit, offset))
