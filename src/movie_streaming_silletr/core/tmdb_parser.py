import requests
import json
import os
from dotenv import load_dotenv
from tmdbv3api import TMDb, Genre

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY


def normalize_title(title: str) -> str:
    # Convert arabic to roman for common numbers
    conversions = {
        " 2": " II", " 3": " III", " 4": " IV",
        " 5": " V", " 6": " VI", " 7": " VII",
        " 8": " VIII", " 9": " IX", " 10": " X"
    }
    for arabic, roman in conversions.items():
        if title.endswith(arabic):
            title = title[:-len(arabic)] + roman
    return title


def search_movie_by_name(movie_name: str) -> tuple[str, str] | None:
    movie_name = normalize_title(movie_name)
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name
    }
    r = requests.get(url, params=params)
    results = r.json().get("results", [])
    if not results:
        return None
    first = results[0]
    print(first)
    return (str(first["id"]), first["title"], first["genre_ids"])


def get_genres() -> dict:
    if os.path.exists("genres.json"):
        with open("genres.json", "r") as file:
            return json.load(file)

    genre = Genre()
    genres = genre.movie_list()
    with open(file="genres.json", mode="w") as file:
        json.dump({"genres": [dict(g) for g in genres]}, file, indent=2)

    print(genres)
    return genres   # pyright: ignore
    # pyright is the most bitch, that I ever saw
