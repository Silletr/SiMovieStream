from difflib import SequenceMatcher
import json
import os

from dotenv import load_dotenv
from loguru import logger
import requests
from tmdbv3api import Genre, TMDb

#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃    All variables and API key    ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY


#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def get_genres() -> dict:
    file_path = os.path.join(os.path.dirname(__file__), "genres.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    genre = Genre()
    genres = genre.movie_list()

    if not genres:
        logger.warning("No genres retrieved from the API.")
        return {}

    with open(file_path, "w") as file:
        json.dump(
            {"genres": [dict(g) for g in genres]},
            file,
            indent=2,
        )
    logger.info("Genres written to {}", file_path)
    return genres


#  ────────────────────────────────────────────────────────────────
def build_genre_map() -> dict:
    genres = get_genres()
    return {g["id"]: g["name"] for g in genres["genres"]}


#  ────────────────────────────────────────────────────────────────
def normalize_title(title: str) -> str:
    conversions = {
        " 2": " II",
        " 3": " III",
        " 4": " IV",
        " 5": " V",
        " 6": " VI",
        " 7": " VII",
        " 8": " VIII",
        " 9": " IX",
        " 10": " X",
    }
    for arabic, roman in conversions.items():
        if title.endswith(arabic):
            title = title[: -len(arabic)] + roman
    return title


#  ────────────────────────────────────────────────────────────────
def search_movies_by_name(
    query: str,
) -> list[tuple[str, str, list[str], str, str, str, float]]:
    """
    Returns: (tmdb_id, title, genres, poster_url, overview, release_year, tmdb_rating)
    """
    normalized_query = normalize_title(query.strip())
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": normalized_query}
    r = requests.get(url, params=params)
    results = r.json().get("results", [])
    if not results:
        return []

    genre_map = build_genre_map()

    scored = []
    for movie in results:
        title = movie["title"].strip()
        score = SequenceMatcher(None, normalized_query.lower(), title.lower()).ratio()
        genre_names = [
            genre_map.get(id_, "Unknown") for id_ in movie.get("genre_ids", [])
        ]

        # Extract year from release_date (e.g. "2022-10-07" → "2022")
        release_date = movie.get("release_date", "")
        year = release_date.split("-")[0] if release_date else "Unknown"

        # TMDB rating (average vote)
        tmdb_rating = movie.get("vote_average", 0.0)

        scored.append(
            (
                movie["id"],
                title,
                genre_names,
                f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                if movie["poster_path"]
                else "",
                movie.get("overview", ""),
                year,
                tmdb_rating,
                score,
            )
        )

    # Sort by similarity score descending
    scored.sort(
        key=lambda x: (
            # 1. similarity score (high → low)
            x[-1],
            # 2. year (high → low, newer first)
            int(x[5]) if x[5].isdigit() else 0,
        ),
        reverse=True,
    )

    # Return list of tuples without the score
    return [  # pyright: ignore
        (
            str(id_),
            title,
            genres,
            poster_url,
            overview,
            year,
            tmdb_rating,
        )
        for id_, title, genres, poster_url, overview, year, tmdb_rating, score in scored
    ]
