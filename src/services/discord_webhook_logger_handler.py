import json
import logging
import queue
import threading
import urllib.request
from typing import Dict as Dictionary

from src.core.interfaces import IDisposable
from src.utils.discord_webhook_payload_formatter import DiscordWebhookPayloadFormatter

class DiscordWebhookLoggerHandler(logging.Handler, IDisposable):
    def __init__(self, webhook_url: str, formatter: DiscordWebhookPayloadFormatter):
        super().__init__()
        self.url = webhook_url
        self.payload_formatter = formatter

        self.queue = queue.Queue[Dictionary]()
        self._cts = threading.Event()

        self.worker = threading.Thread(
            target=self._processor,
            daemon=True
        )
        self.worker.start()

    def emit(self, record: logging.LogRecord) -> None:
        payload = self.payload_formatter.format(
            self,
            record
        )

        self.queue.put(payload)

    def _processor(self):
        while not self._cts.is_set() or not self.queue.empty():
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

            except Exception:
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