import logging
from datetime import datetime, timezone
from typing import Dict as Dictionary

class DiscordWebhookLoggerPayloadFormatter():
    LEVEL_COLORS = {
        logging.DEBUG: 0x95A5A6,      # gray
        logging.INFO: 0x3498DB,       # blue
        logging.WARNING: 0xF1C40F,    # yellow
        logging.ERROR: 0xE74C3C,      # red
        logging.CRITICAL: 0x8E44AD    # purple
    }

    LEVEL_ICONS = {
        logging.DEBUG: "🔍",
        logging.INFO: "ℹ️",
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🚨"
    }

    def format(self, handler: logging.Handler, record: logging.LogRecord) -> Dictionary:
        return {
            "embeds": [{
                "title": (
                    f"{self.LEVEL_ICONS.get(record.levelno, '📝')} "
                    f"{record.levelname}"
                ),

                "description":
                    f"```{handler.format(record)}```",

                "color":
                    self.LEVEL_COLORS.get(
                        record.levelno,
                        0x3498DB
                    ),

                "fields": [
                    {
                        "name": "Identity",
                        "value": record.name.replace("_", "\\_"),
                        "inline": True
                    },
                    {
                        "name": "Method",
                        "value": record.funcName.replace("_", "\\_"),
                        "inline": True
                    }
                ],

                "timestamp":
                    datetime.now(timezone.utc).isoformat()
            }]
        }
