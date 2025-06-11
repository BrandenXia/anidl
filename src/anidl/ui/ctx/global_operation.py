from collections.abc import Callable

from textual import on
from textual.css.query import QueryType
from textual.message import Message
from textual.widget import Widget


class OperationCtx(Widget):
    class Operation(Message):
        def __init__(
            self,
            selector: str,
            expect: type[QueryType],
            operation: Callable[[QueryType], None],
        ) -> None:
            self.selector = selector
            self.expect = expect
            self.op = operation
            super().__init__()

    @on(Operation)
    def on_operation(self, assign: Operation) -> None:
        widget = self.query_one(assign.selector, assign.expect)
        (assign.op)(widget)
