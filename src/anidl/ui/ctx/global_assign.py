from typing import Any

from textual.css.query import QueryType
from textual.message import Message
from textual.widget import Widget


class AssignCtx(Widget):
    class Assign(Message):
        def __init__(
            self,
            selector: str,
            expect: type[QueryType],
            attr: str,
            value: Any,
        ) -> None:
            assert attr in expect.__dict__.keys(), f"Invalid attribute: {attr}"
            self.attr = attr
            self.value = value
            self.selector = selector
            self.expect = expect
            super().__init__()

    def on_global_ctx_assign(self, assign: Assign) -> None:
        setattr(
            self.query_one(assign.selector, assign.expect), assign.attr, assign.value
        )
