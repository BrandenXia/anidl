from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Label


class EpisodeList(Vertical):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = "Episode"

    def compose(self) -> ComposeResult:
        yield Label("Nothing selected", id="nothing-selected-warning")
        yield Label("No episodes to preview", id="no-episodes-warning")
