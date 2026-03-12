from typing import Dict
import requests
import json
import os
from dotenv import load_dotenv
from tmdbv3api import List, TMDb, Genre

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY


def get_genres() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "genres.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    genre = Genre()
    genres = genre.movie_list()

    if not genres:
        print("No genres retrieved from the API.")
        return {}

    with open(file_path, "w") as file:
        json.dump({"genres": [dict(g) for g in genres]},   # pyright: ignore
                  file, indent=2)   # pyright: ignore

    print(f"Genres written to {file_path}")
    return genres   # pyright: ignore


def build_genre_map() -> dict:
    genres = get_genres()
    return {g["id"]: g["name"] for g in genres["genres"]}


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

    # Convert genres ID to their names
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
    genre_map = build_genre_map()
    genre_names = [genre_map.get(id, "Unknown") for id in first["genre_ids"]]
    return (   # pyright: ignore
        str(first["id"]),
        first["title"],
        genre_names,
        f"https://image.tmdb.org/t/p/w500{first['poster_path']}",
        first.get("overview", "")
    )
