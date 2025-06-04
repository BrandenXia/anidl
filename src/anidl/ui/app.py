from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Label

from anidl.version import VERSION
from anidl.config import Config

from .components import SelectAnimeDir, DownloadedList
from .ctx import Ctx


class AppHeader(Horizontal):
    def compose(self) -> ComposeResult:
        yield Label(f"[b]Anidl[/] [dim]{VERSION}[/]", id="app-title")


class AppBody(Vertical):
    pass


class Anidl(App):
    CSS_PATH = Path(__file__).parent / "app.scss"

    def compose(self) -> ComposeResult:
        with Ctx():
            if not Config().anime_dir:
                yield SelectAnimeDir()

            yield AppHeader()
            with AppBody():
                yield DownloadedList()
            yield Footer()
