import flet as ft
from ..core.tmdb_parser import search_movie_by_name as search_film


class FilmCard:
    def __init__(self, film_name: str, film_id: int, film_genre: list, film_description: str, poster_url: str):
        self.name = film_name
        self.id = film_id
        self.genre = film_genre
        self.description = film_description
        self.poster = poster_url
