import requests
import os
from dotenv import load_dotenv
import re


load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")


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
    return (str(first["id"]), first["title"])  # pyright: ignore
