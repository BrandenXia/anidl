from typing import Literal

from textual.visual import VisualType
from textual.message import Message

type MsgType = Literal["Info", "Warning", "Error"]


class AlertMsg(Message):
    def __init__(
        self,
        msg_type: MsgType,
        title: str,
        content: VisualType,
    ) -> None:
        self.msg_type: MsgType = msg_type
        self.title = title
        self.content = content
        super().__init__()
