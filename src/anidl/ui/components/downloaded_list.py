from typing import Iterable

from textual import log
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


def get_anime_list() -> list[str]:
    anime_dir = Config().get_anime_dir()
    return (
        [i.name for i in anime_dir.iterdir() if i.is_dir()]
        if anime_dir.exists()
        else []
    )


class DownloadedList(Vertical):
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("slash", "filter", "Filter"),
        Binding("escape", "focus_parent", "Focus parent", show=False),
    ]

    search_term: Reactive[str] = reactive("")
    animes: Reactive[list[str]] = reactive(get_anime_list, recompose=True)
    anime_list: Reactive[Iterable[str]] = reactive(tuple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_title = "Downloaded"

    def watch_anime_list(self, _: list[str], new: list[str]) -> None:
        list_widget = self.query_one("#download-list-view", DownloadedItemList)
        list_widget.clear_options()
        list_widget.add_options(new)

    def compose(self) -> ComposeResult:
        with Vertical(id="download-list-search"):
            with Horizontal():
                yield Label("Search:", id="search-label")
                yield Input(id="search-input", placeholder="Filter by name")
            yield Rule()

        no_anime_dir_warning_widget = Label(
            "Invalid anime directory. Please set it in setting or press 'r' to refresh.",
            id="no-anime-dir-warning",
        )
        no_anime_warning_widget = Label(
            "No downloaded anime found.", id="no-anime-warning"
        )
        if not Config().get_anime_dir().exists():
            no_anime_dir_warning_widget.styles.display = "block"
        elif len(self.animes) == 0:
            no_anime_warning_widget.styles.display = "block"
        yield no_anime_dir_warning_widget
        yield no_anime_warning_widget

        yield DownloadedItemList(
            id="download-list-view",
        )

    def display_warnings(self) -> None:
        if not Config().get_anime_dir().exists():
            self.query_one("#no-anime-dir-warning").styles.display = "block"
            self.query_one("#no-anime-warning").styles.display = "none"
        elif len(self.animes) == 0:
            self.query_one("#no-anime-dir-warning").styles.display = "none"
            self.query_one("#no-anime-warning").styles.display = "block"

    def action_refresh(self) -> None:
        self.animes = get_anime_list()
        self.display_warnings()

    def show_search(self) -> None:
        download_list_search_widget = self.query_one("#download-list-search")
        download_list_search_widget.styles.visibility = "visible"
        download_list_search_widget.styles.display = "block"

    def hide_search(self) -> None:
        download_list_search_widget = self.query_one("#download-list-search")
        download_list_search_widget.styles.visibility = "hidden"
        download_list_search_widget.styles.display = "none"

    def action_filter(self) -> None:
        self.show_search()
        self.query_one("#search-input").focus()

    def action_focus_parent(self) -> None:
        if not self.query_one("#search-input", Input).value:
            self.hide_search()
        self.query_one("#download-list-view").focus()

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self.action_focus_parent()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.search_term = event.value

    def on_downloaded_item_list_option_selected(
        self, event: DownloadedItemList.OptionSelected
    ) -> None:
        log("Option Selected", event.option)
