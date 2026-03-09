from core.tmdb_parser import search_movie_by_name as search_movie


def get_movie_url(movie_title: str) -> str | None:
    movie = search_movie(movie_title)
    if movie is None:
        return None
    film_id, film_name = movie
    url = f"https://vidfast.pro/movie/{film_id}"
    return url
