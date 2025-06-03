from contextlib import ExitStack
from typing import Self

from textual.widget import Widget


class ScreenCtx(Widget):
    pass


ctxs: list[type] = []
_ctxs = [*ctxs, ScreenCtx]  # keep ScreenCtx at the end to emulate `Screen` in CSS


class Ctx(Widget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stack = ExitStack()

    def __enter__(self) -> Self:
        super().__enter__()
        [self.stack.enter_context(ctx()) for ctx in _ctxs]
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        super().__exit__(exc_type, exc_value, traceback)
        self.stack.close()
