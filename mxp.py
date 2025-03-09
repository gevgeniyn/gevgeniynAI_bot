from functools import wraps
from typing import Optional
import logging

from telegram import Update
from telegram.ext import CallbackContext

mixpanel_token = "1db6421f7bdd3468e57d28cc6800c079"


logger = logging.getLogger(__name__)


class MixpanelWrapper:
    def __init__(self, token: Optional[str] = None):
        if token:
            try:
                import mixpanel
                from mixpanel_async import AsyncBufferedConsumer
                self.mxp = mixpanel.Mixpanel(token, consumer=AsyncBufferedConsumer())
            except Exception:
                logger.error("Mixpanel init error")
        else:
            self.mxp = None

    def track(self, distinct_id, event_name, properties):
        emoji = "❌"
        if self.mxp is not None:
            try:
                self.mxp.track(distinct_id, event_name, properties)
                emoji = "✅"
            except Exception:
                logger.error("Mixpanel track error")

        logger.info(f"{emoji} [{distinct_id}] {event_name}: {properties}")

    def people_set(self, distinct_id, properties):
        emoji = "❌"
        if self.mxp is not None:
            try:
                self.mxp.people_set(distinct_id, properties)
                emoji = "✅"
            except Exception:
                logger.error("Mixpanel people_set error")
        logger.info(f"{emoji} [{distinct_id}] people set: {properties}")



mxp = MixpanelWrapper(mixpanel_token)

