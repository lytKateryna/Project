# Tasks for Adding Year Range Search

- [x] Add "Year Range" section in templates/index.html after the search box and before genres, with inputs for "From year" and "To year" and a search button.
- [x] Add get_min_max_year_route endpoint in routes/films.py if not present (already exists).
- [x] Add get_films_by_year_range function in db/my_sql.py to query films within a year range.
- [x] Add /films/search/year_range endpoint in routes/films.py to handle year range queries.
- [x] Add searchByYearRange() function in static/app.js to handle the year range search, calling the new endpoint.
- [x] Test the new year range search functionality.
