from textual.widget import Widget
from textual.visual import VisualType
from textual.message import Message
from textual import log


class AlertCtx(Widget):
    class Msg(Message):
        def __init__(self, content: VisualType) -> None:
            self.content = content
            super().__init__()

    def on_alert_ctx_msg(self, msg: Msg) -> None:
        log("AlertCtx received message:", msg.content)
