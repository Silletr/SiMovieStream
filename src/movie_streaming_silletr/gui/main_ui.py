import flet as ft
import os
import sys
from core.tmdb_parser import search_movie_by_name as search_movie


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def main(page: ft.Page):
    page.title = "SiMovieStream"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"

    search_input = ft.TextField(
        hint_text="Enter movie title...",
        border_color="#333333",
        focused_border_color="#7c3aed",
    )
    result_title = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    result_genres = ft.Text("", color="#7c3aed")
    result_description = ft.Text("", color="#a0a0a0")
    result_button = ft.ElevatedButton("Transfer to film page", color="#e50914")
    # Define poster as ft.Image here
    poster = ft.Image(width=200, height=300, fit="contain", src="")

    def on_search(e):
        result = search_movie(search_input.value)
        if result:
            film_id, film_name, genres, poster_url, description = result
            result_title.value = f"🎬 {film_name}"
            result_genres.value = f"🎭 {', '.join(genres)}"
            result_description.value = description

            # Update src directly and refresh
            poster.src = poster_url
            poster.update()

            result_button.text = "🔗 Open film page"
            result_button.url = f"https://vidfast.pro/movie/{film_id}"
            page.update()
        else:
            result_title.value = "🗿 Movie not found"
            page.update()

    page.add(
        search_input,
        ft.ElevatedButton("Search", on_click=on_search),
        ft.Row(
            [
                poster,  # Now defined
                ft.Column(
                    [result_title, result_genres, result_description, result_button]
                ),
            ]
        ),
    )


ft.run(main=main)
