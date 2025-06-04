from pathlib import Path
from typing import Iterable

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.reactive import Reactive, reactive
from textual.widgets import Input, Label, OptionList, Rule

from anidl.config import Config


class DownloadedItemList(OptionList):
    BINDINGS = [
        Binding("up", "cursor_up", "Cursor up", show=False),
        Binding("down", "cursor_down", "Cursor down", show=False),
        Binding("j", "cursor_down", "Cursor down", show=False),
        Binding("k", "cursor_up", "Cursor up", show=False),
        Binding("alt+j", "cursor_down_5", "Cursor down 5", show=False),
        Binding("alt+k", "cursor_up_5", "Cursor up 5", show=False),
    ]

    def action_cursor_down_5(self) -> None:
        """Move cursor down by 5 items."""
        [self.action_cursor_down() for _ in range(5)]

    def action_cursor_up_5(self) -> None:
        """Move cursor up by 5 items."""
        [self.action_cursor_up() for _ in range(5)]


class DownloadedList(Vertical):
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("slash", "filter", "Filter"),
        Binding("escape", "focus_parent", "Focus parent", show=False),
    ]

    search_term: Reactive[str] = reactive("")
    anime_list: Reactive[Iterable[str]] = reactive(tuple, layout=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "Downloaded"
        self.refresh_anime_list()

    def refresh_anime_list(self) -> None:
        self.anime_dir = Path(Config().anime_dir)
        self.animes = (
            [i.name for i in self.anime_dir.iterdir() if i.is_dir()]
            if self.anime_dir.exists()
            else []
        )

    def show_search(self) -> None:
        download_list_search_widget = self.query_one("#download-list-search")
        download_list_search_widget.styles.visibility = "visible"
        download_list_search_widget.styles.display = "block"

    def hide_search(self) -> None:
        download_list_search_widget = self.query_one("#download-list-search")
        download_list_search_widget.styles.visibility = "hidden"
        download_list_search_widget.styles.display = "none"

    def compute_anime_list(self) -> Iterable[str]:
        return (
            filter(
                lambda item: self.search_term.lower() in item.lower(),
                self.animes,
            )
            if self.search_term
            else self.animes
        )

    def watch_anime_list(self, _: Iterable[str], new: Iterable[str]) -> None:

        list_widget = self.query_one("#downloaded-list-view", DownloadedItemList)
        list_widget.clear_options()
        list_widget.add_options(new)

    def compose(self) -> ComposeResult:
        with Vertical(id="download-list-search"):
            with Horizontal():
                yield Label("Search:", id="search-label")
                yield Input(id="search-input", placeholder="Filter by name")
            yield Rule()

        if not self.anime_dir.exists():
            yield Label(
                "Invalid anime directory. Please set it in setting or press 'r' to refresh."
            )

        yield DownloadedItemList(
            id="downloaded-list-view",
        )

    async def action_refresh(self) -> None:
        self.refresh_anime_list()
        await self.recompose()
        self.query_one("#downloaded-list-view").focus()

    def action_filter(self) -> None:
        self.show_search()
        self.query_one("#search-input").focus()

    def action_focus_parent(self) -> None:
        if not self.query_one("#search-input", Input).value:
            self.hide_search()
        self.query_one("#downloaded-list-view").focus()

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self.action_focus_parent()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.search_term = event.value
