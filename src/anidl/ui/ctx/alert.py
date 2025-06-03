import asyncio
import uuid

from textual import work
from textual.widget import Widget

from anidl.ui.components import Alerts
from anidl.ui.components.alert import AlertMsg


class AlertCtx(Widget):
    @work()
    async def on_alert_msg(self, msg: AlertMsg) -> None:
        alerts_widget = self.query_one(Alerts)
        uuid_str = str(uuid.uuid4())
        alerts_widget.msgs[uuid_str] = msg
        alerts_widget.mutate_reactive(Alerts.msgs)

        await asyncio.sleep(1)

        alerts_widget.msgs.pop(uuid_str)
        alerts_widget.mutate_reactive(Alerts.msgs)
