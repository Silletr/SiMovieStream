from core.vidfast import get_movie_url as search_movie

from textual.app import App, ComposeResult
from textual.widgets import Input, Button, Label


class MovieTUI(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter the movie title:",
                    type="text",
                    tooltip="Enter the movie title!")
        yield Button("Search", id="search")
        yield Label("", id="result")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        movie_title = self.query_one(Input).value
        url = search_movie(movie_title)

        if url:
            self.query_one("#result").update(f"URL: {url}")
        else:
            self.query_one("#result").update("Movie not found 🗿")


if __name__ == "__main__":
    app = MovieTUI()
    app.run()
