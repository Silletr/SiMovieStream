# WILL BE USED FOR STREAMING WIDGET. LINK EXAMPLE:
# vidfast.pro/movie/tt27047903
# tt27047903 -> MOVIE ID FROM iMDB (./imdb.py FILE)
# Link example: https://vidfast.pro/movie/{id}
from requests import get
from imdb_parser import search_movie_by_name as search_movie

movie = input("Movie title: ")
movie = search_movie(movie)
if movie is None:
    print("Movie not found, check your input")

else:
    film_id, film_name = movie
    url = get(f"https://vidfast.pro/movie/{film_id}")
    print(f"Fetching: {url.url}")
