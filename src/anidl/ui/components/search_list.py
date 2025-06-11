from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal
from textual.reactive import Reactive, reactive
from textual.widgets import Input, Label, OptionList, Rule
from textual.widget import Widget


class ItemList(OptionList):
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


class SearchList(Vertical):
    BINDINGS = [
        ("r", "refresh", "Refresh"),
        ("slash", "filter", "Filter"),
        Binding("escape", "focus_parent", "Focus parent", show=False),
    ]

    search_term: Reactive[str] = reactive("")

    invalid_message: ClassVar[str] = "Invalid items found."
    no_item_message: ClassVar[str | None] = "No items found."

    def get_items(self) -> list[str]:
        return []

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.items = self.get_items()

    def invalid_check(self) -> bool:
        return False

    def no_items_check(self) -> bool:
        return len(self.items) == 0 and self.no_item_message is not None

    def set_items(self) -> None:
        displayed_items = (
            filter(
                lambda item: self.search_term.lower() in item.lower(),
                self.items,
            )
            if self.search_term
            else self.items
        )

        item_list_widget = self.query_one(ItemList)
        item_list_widget.clear_options()
        item_list_widget.add_options(displayed_items)

    def compose(self) -> ComposeResult:
        with Vertical(classes="list-search"):
            with Horizontal():
                yield Label("Search:", classes="search-label")
                yield Input(classes="search-input", placeholder="Filter by name")
            yield Rule()

        invalid_warning = Label(
            self.invalid_message,
            classes="invalid-warning",
        )
        no_item_warning = Label(self.no_item_message or "", classes="no-item-warning")
        if self.invalid_check():
            invalid_warning.styles.display = "block"
        elif self.no_items_check():
            no_item_warning.styles.display = "block"
        yield invalid_warning
        yield no_item_warning

        yield ItemList(*self.items, classes="list-view")

    def toggle_warnings(self) -> None:
        invalid_warning = self.query_one(".invalid-warning", Label)
        no_item_warning = self.query_one(".no-item-warning", Label)

        def show(widget: Widget):
            widget.styles.display = "block"

        def hide(widget: Widget):
            widget.styles.display = "none"

        if self.invalid_check():
            show(invalid_warning)
            hide(no_item_warning)
        elif self.no_items_check():
            hide(invalid_warning)
            show(no_item_warning)
        else:
            hide(invalid_warning)
            hide(no_item_warning)

    def action_refresh(self) -> None:
        self.items = self.get_items()
        self.toggle_warnings()
        self.set_items()

    def show_search(self) -> None:
        download_list_search_widget = self.query_one(".list-search")
        download_list_search_widget.styles.visibility = "visible"
        download_list_search_widget.styles.display = "block"

    def hide_search(self) -> None:
        download_list_search_widget = self.query_one(".list-search")
        download_list_search_widget.styles.visibility = "hidden"
        download_list_search_widget.styles.display = "none"

    def action_filter(self) -> None:
        self.show_search()
        self.query_one(".search-input").focus()

    def action_focus_parent(self) -> None:
        if not self.query_one(".search-input", Input).value:
            self.hide_search()
        self.query_one(".list-view").focus()

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self.action_focus_parent()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.search_term = event.value
        self.set_items()
