import sys
import os
from textual.widgets import Input, Button, Label
from textual.app import App, ComposeResult
from textual.containers import Vertical
from movie_streaming_silletr.core.vidfast import get_movie_url as search_movie


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)  # pyright: ignore
    return os.path.join(os.path.dirname(__file__), relative_path)


class MovieTUI(App):
    def on_mount(self) -> None:
        self.stylesheet.read(resource_path(("styles.tcss")))

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter the movie title:", id="search-input")
        yield Button("Search", id="search")
        yield Vertical(
            Label("", id="title"),
            Label("", id="genres"),
            Label("", id="description"),
            Label("", id="url"),
            id="result-card",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        movie_title = self.query_one("#search-input", Input).value
        result = search_movie(movie_title)

        if result:
            self.query_one("#title", Label).update(f"🎬 {result['title']}")
            self.query_one("#genres", Label).update(f"🎭 {', '.join(result['genres'])}")
            self.query_one("#description", Label).update(f"📖 {result['description']}")
            self.query_one("#url", Label).update(f"🔗 {result['url']}")
        else:
            self.query_one("#title", Label).update("Movie not found 🗿")


if __name__ == "__main__":
    movie = MovieTUI()
    movie.run()
