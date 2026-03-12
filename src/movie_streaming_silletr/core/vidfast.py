from core.tmdb_parser import search_movie_by_name as search_movie


def get_movie_url(movie_title: str) -> dict | None:
    movie = search_movie(movie_title)
    if movie is None:
        return None
    film_id, film_name, genres, poster, description = movie
    return {
        "id": film_id,
        "title": film_name,
        "genres": genres,
        "poster": poster,
        "description": description,
        "url": f"https://vidfast.pro/movie/{film_id}"
    }
