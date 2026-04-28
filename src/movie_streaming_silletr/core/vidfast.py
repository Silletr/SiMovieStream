from tmdb_parser import search_movies_by_name  # Get actual function name


def get_movie_url(movie_title: str) -> dict | None:
    movies = search_movies_by_name(movie_title)  # Returns list
    if not movies:
        return None
    movie = movies[0]  # Take first result
    film_id, film_name, genres, poster, description, overview, release_year = movie
    return {
        "id": film_id,
        "title": film_name,
        "genres": genres,
        "poster": poster,
        "description": description,
        "overview": overview,
        "release_year": release_year,
        "url": f"https://vidfast.pro/movie/{film_id}",
    }

