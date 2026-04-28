from movie_streaming_silletr.core.tmdb_parser import (
    search_movies_by_name as search_movie,
)
import sys
import os
import flet as ft
import webbrowser


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        # Fix for PyInstaller
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "movie_streaming_silletr", relative_path)


#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def make_click_handler(fid):
    def handler(e):
        webbrowser.open(f"https://vidfast.pro/movie/{fid}")

    return handler


#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main(page: ft.Page):
    page.title = "SiMovieStream"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"
    page.scroll = ft.ScrollMode.AUTO

    search_input = ft.TextField(
        hint_text="Enter movie title...",
        border_color="#333333",
        focused_border_color="#7c3aed",
    )

    results_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def on_search(e):
        movies = search_movie(search_input.value)
        results_list.controls.clear()

        if not movies:
            results_list.controls.append(ft.Text("🗿 No movies found", color="#a0a0a0"))
        else:
            for movie in movies:
                title = movie.get("title", "N/A")
                year = movie.get("year", "N/A")
                poster_url = movie.get("poster", "")
                genres = movie.get("genres", [])
                tmdb_rating = movie.get("rating", 0)
                film_id = movie.get("id", "")

                card = ft.Row(
                    [
                        ft.Image(
                            src=poster_url,
                            width=60,
                            height=90,
                            fit=ft.ImageFit.COVER,
                            border_radius=5,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    f"{title} ({year})",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"{', '.join(genres[:2])}", color="#7c3aed", size=12
                                ),
                                ft.Text(
                                    f"★ {tmdb_rating:.1f}", color="#a0a0a0", size=12
                                ),
                            ],
                            spacing=1,
                            expand=True,
                        ),
                        ft.CupertinoButton(
                            "Open",
                            color="#e50914",
                            on_click=make_click_handler(film_id),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                )
                results_list.controls.append(card)

        page.update()

    page.add(
        ft.Container(
            ft.Column(
                [
                    search_input,
                    ft.CupertinoButton("Search", on_click=on_search),
                    results_list,
                ],
                spacing=15,
                expand=True,
            ),
            padding=10,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
