import imdb


def search_movie_by_name(movie_name: str) -> tuple[str, str] | None:
    ia = imdb.Cinemagoer()
    movies = ia.search_movie(movie_name)
    if movies:
        first_movie = movies[0]
        film_id: int = "tt" + first_movie.getID()   # pyright: ignore
        film_name: str = first_movie['title']   # pyright: ignore
        print(f"Film ID: {film_id} | Film Title: {film_name}")
        return (film_id, film_name)   # pyright: ignore
        # Pyright is such bich
    return None


if __name__ == "__main__":
    # Because Pyright bich
    user_film: str = str(input("Please enter the movie TITLE:\n>> "))
    search_movie_by_name(user_film)
