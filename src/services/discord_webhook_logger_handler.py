import json
import logging
import queue
import threading
import urllib.request
from datetime import datetime, timezone

from core.interfaces import IDisposable

class DiscordWebhookLoggerHandler(logging.Handler, IDisposable):
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

    def __init__(self, webhook_url: str):
        super().__init__()
        self.url = webhook_url
        self.queue = queue.Queue()
        self._cts = threading.Event()

        self.worker = threading.Thread(
            target=self._processor,
            daemon=True
        )
        self.worker.start()

    def emit(self, record: logging.LogRecord) -> None:
        payload = {
                "embeds": [{
                    "title": (
                        f"{self.LEVEL_ICONS.get(record.levelno, '📝')} "
                        f"{record.levelname}"
                    ),

                    "description":
                        f"```{self.format(record)}```",

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

        self.queue.put(payload)

    def _processor(self):
        while not self._cts.is_set():
            try:
                payload = self.queue.get(timeout=1)

                req = urllib.request.Request(
                    self.url,
                    data=json.dumps(payload).encode("utf-8"),
                    method="POST"
                )
                req.add_header(
                    "Content-Type",
                    "application/json"
                )
                req.add_header(
                    "User-Agent",
                    "StorageHuntersToolLogger/1.0"
                )

                with urllib.request.urlopen(req, timeout=15) as response:
                    response.read()

                self.queue.task_done()

            except queue.Empty:
                continue

            except Exception as e:
                pass

    def stop(self) -> None:
        self._cts.set()

    def close(self) -> None:
        if self.worker.is_alive():
            self.worker.join(timeout=2)
        super().close()

    def dispose(self) -> None:
        self.stop()
        self.close()

        self.url = ""
        self.worker = None