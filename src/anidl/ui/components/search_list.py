from collections.abc import Collection, Iterable
from typing import ClassVar, Self

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.reactive import Reactive, reactive
from textual.widget import Widget
from textual.widgets import Input, Label, OptionList, Rule
from textual.widgets.option_list import Option

SEARCH_CONTAINER_CLASS = "search-container"
SEARCH_LABEL_CLASS = "search-label"
SEARCH_INPUT_CLASS = "search-input"
INVALID_WARNING_CLASS = "invalid-warning"
NO_ITEM_WARNING_CLASS = "no-item-warning"
LIST_VIEW_CLASS = "list-view"


class ItemList(OptionList):
    BINDINGS = [
        Binding("up", "cursor_up", "Cursor up", show=False),
        Binding("down", "cursor_down", "Cursor down", show=False),
        Binding("j", "cursor_down", "Cursor down", show=False),
        Binding("k", "cursor_up", "Cursor up", show=False),
        Binding("alt+j", "cursor_down_5", "Cursor down 5", show=False),
        Binding("alt+k", "cursor_up_5", "Cursor up 5", show=False),
    ]

    def action_cursor_down_5(self):
        """Move cursor down by 5 items."""
        [self.action_cursor_down() for _ in range(5)]

    def action_cursor_up_5(self):
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

    def get_items(self) -> Collection[str | Option]:
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

    def search_items(self) -> Iterable[str | Option]:
        return filter(
            lambda item: (
                self.search_term.lower()
                in (item if isinstance(item, str) else str(item.prompt))
            ),
            self.items,
        )

    def set_items(self) -> None:
        displayed_items = self.search_items() if self.search_term else self.items

        item_list_widget = self.list_view
        item_list_widget.clear_options()
        item_list_widget.add_options(displayed_items)

    def compose(self) -> ComposeResult:
        with Vertical(classes=SEARCH_CONTAINER_CLASS):
            with Horizontal():
                yield Label("Search:", classes=SEARCH_LABEL_CLASS)
                yield Input(classes=SEARCH_INPUT_CLASS, placeholder="Filter by name")
            yield Rule()

        invalid_warning = Label(
            self.invalid_message,
            classes=INVALID_WARNING_CLASS,
        )
        no_item_warning = Label(
            self.no_item_message or "", classes=NO_ITEM_WARNING_CLASS
        )
        if self.invalid_check():
            invalid_warning.styles.display = "block"
        elif self.no_items_check():
            no_item_warning.styles.display = "block"
        yield invalid_warning
        yield no_item_warning

        yield ItemList(*self.items, classes=LIST_VIEW_CLASS)

    @property
    def invalid_warning(self) -> Label:
        return self.query_one("." + INVALID_WARNING_CLASS, Label)

    @property
    def no_item_warning(self) -> Label:
        return self.query_one("." + NO_ITEM_WARNING_CLASS, Label)

    @property
    def search_input(self) -> Input:
        return self.query_one("." + SEARCH_INPUT_CLASS, Input)

    @property
    def list_view(self) -> ItemList:
        return self.query_one("." + LIST_VIEW_CLASS, ItemList)

    @property
    def search_container(self) -> Vertical:
        return self.query_one("." + SEARCH_CONTAINER_CLASS, Vertical)

    def toggle_warnings(self) -> None:
        invalid_warning = self.invalid_warning
        no_item_warning = self.no_item_warning

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
        list_search_widget = self.search_container
        list_search_widget.styles.visibility = "visible"
        list_search_widget.styles.display = "block"

    def hide_search(self) -> None:
        list_search_widget = self.search_container
        list_search_widget.styles.visibility = "hidden"
        list_search_widget.styles.display = "none"

    def action_filter(self) -> None:
        self.show_search()
        self.search_input.focus()

    def action_focus_parent(self) -> None:
        if not self.search_input.value:
            self.hide_search()
        self.list_view.focus()

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self.action_focus_parent()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.search_term = event.value
        self.set_items()

    def focus(self, scroll_visible: bool = True) -> Self:
        list_view = self.list_view
        if list_view.styles.display == "none":
            super().focus(scroll_visible)
        else:
            list_view.focus(scroll_visible)
        return self
