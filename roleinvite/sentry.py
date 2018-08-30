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
from redbot.core.data_manager import cog_data_path
from distutils.version import StrictVersion


class Sentry:
    """
    Automatically send errors to the cog author
    """

    def __init__(self, logger: logging.Logger, version: StrictVersion, bot: RedBase):
        self.bot = bot
        self.client = Client(
            dsn=(
                "https://569a1369052245218133d2157028e6f6:bea00ed8961e408d8a7988628fe59607"
                "@sentry.io/1256931"
            ),
            release=version,
        )
        self.format = logging.Formatter(
            "%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: %(message)s",
            datefmt="[%d/%m/%Y %H:%M]",
        )
        self.logger = logger

        self.handler = self.sentry_log_init()
        self.file_handler_init()

    def sentry_log_init(self):
        """Initialize Sentry logger"""
        self.client.environment = f"{platform.system()} ({platform.release()})"
        self.client.user_context({"id": self.bot.user.id, "name": str(self.bot.user)})
        handler = SentryHandler(self.client)
        handler.setFormatter(self.format)
        return handler

    def file_handler_init(self):
        """Initialize file handlers"""
        error_log = logging.FileHandler(cog_data_path(self.bot) / "logs/error.log")
        error_log.setLevel(logging.ERROR)
        error_log.setFormatter(self.format)
        debug_log = logging.FileHandler(cog_data_path(self.bot) / "logs/debug.log")
        debug_log.setLevel(logging.DEBUG)
        debug_log.setFormatter(self.format)
        self.logger.addHandler(error_log)
        self.logger.addHandler(debug_log)

    def enable(self):
        """Enable error reporting for Sentry."""
        self.logger.addHandler(self.handler)

    def disable(self):
        """Disable error reporting for Sentry."""
        self.logger.removeHandler(self.handler)
