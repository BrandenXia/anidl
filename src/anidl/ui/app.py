from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Label, ListItem, ListView

from anidl.version import VERSION
from anidl.config import Config

from .components.select_anime_dir import SelectAnimeDir
from .ctx import Ctx


class Alerts(Vertical):
    pass


class AppHeader(Horizontal):
    def compose(self) -> ComposeResult:
        yield Label(f"[b]Anidl[/] [dim]{VERSION}[/]", id="app-title")


class AppBody(Vertical):
    pass


class DownloadedList(Vertical):
    def compose(self) -> ComposeResult:
        self.border_title = "Downloaded"
        items = [f"Item {i}" for i in range(1, 100)]
        yield ListView(*(ListItem(Label(item)) for item in items))


class Anidl(App):
    CSS_PATH = Path(__file__).parent / "app.scss"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config = Config()

    def compose(self) -> ComposeResult:
        with Ctx():
            yield Alerts()

            if not self.config.anime_dir:
                yield SelectAnimeDir()

            yield AppHeader()
            with AppBody():
                yield DownloadedList()
            yield Footer()
