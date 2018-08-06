# This file is used for logging errors and
# sending them to sentry.io for helping retke
# in fixing bugs.
#
# This will only be enabled if the main Sentry
# (for Red) is enabled.
#
# This file is 95% from Cog-Creators for core Red

import logging
import platform

from raven import Client
from raven.handlers.logging import SentryHandler
from redbot.core.bot import RedBase
from distutils.version import StrictVersion


class Sentry:
    """
    Automatically send errors to the cog author
    """

    def __init__(self, logger: logging.Logger, version: StrictVersion, bot: RedBase):
        self.client = Client(
            dsn=(
                "https://569a1369052245218133d2157028e6f6:bea00ed8961e408d8a7988628fe59607"
                "@sentry.io/1256931"
            ),
            release=version,
        )
        self.client.environment = f"{platform.system()} ({platform.release()})"
        self.client.user_context({"id": bot.user.id, "name": str(bot.user)})

        self.handler = SentryHandler(self.client)
        self.logger = logger

    def enable(self):
        """Enable error reporting for Sentry."""
        self.logger.addHandler(self.handler)

    def disable(self):
        """Disable error reporting for Sentry."""
        self.logger.removeHandler(self.handler)
