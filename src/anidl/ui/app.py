from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Label

from anidl.version import VERSION
from anidl.config import Config

from .components import SelectAnimeDir, DownloadedList, EpisodeList
from .ctx import Ctx


class AppHeader(Horizontal):
    def compose(self) -> ComposeResult:
        yield Label(f"[b]Anidl[/] [dim]{VERSION}[/]", id="app-title")


class AppBody(Horizontal):
    pass


class Anidl(App):
    CSS_PATH = Path(__file__).parent / "app.scss"

    def compose(self) -> ComposeResult:
        with Ctx():
            if not Config().anime_dir:
                yield SelectAnimeDir()

            yield AppHeader()
            with AppBody():
                yield DownloadedList(classes="window")
                yield EpisodeList(classes="window")
            yield Footer()
