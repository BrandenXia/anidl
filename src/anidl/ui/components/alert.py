from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive, Reactive
from textual.widgets import Static

from anidl.ui.msgs.alert import AlertMsg, MsgType


msg_type_2_color: dict[MsgType, str] = {
    "Info": "lightseagreen",
    "Warning": "gold",
    "Error": "crimson",
}


class Alerts(Vertical):
    msgs: Reactive[dict[str, AlertMsg]] = reactive(dict, recompose=True)

    def compose(self) -> ComposeResult:
        for msg in self.msgs.values():
            color = msg_type_2_color[msg.msg_type]
            msg_widget = Static(f"[bold][{color}]{msg.title}[/]: {msg.content}")
            msg_widget.border_title = msg.msg_type
            msg_widget.styles.border = ("round", color)

            yield msg_widget
