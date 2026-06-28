import json
import time
import threading
import queue
import urllib.request
import uuid
from typing import final as sealed

from core.config import Config
from core.constants import Constants

@sealed
class WebhookManager:
    def __init__(self):
        self.msg_queue = queue.Queue()
        self.enabled = False
        self.url = ""
        self.interval = 50

        self._stop_event = threading.Event()
        self._worker_thread = threading.Thread(target=self._processor, daemon=True)
        self._worker_thread.start()

    def update_config(self):
        self.enabled = getattr(Config, "DISCORD_WEBHOOK_ENABLED", False)
        self.url = getattr(Config, "DISCORD_WEBHOOK_URL", "")
        self.interval = getattr(Config, "DISCORD_WEBHOOK_INTERVAL", 50)

    def send_alert(self, message: str, count: int, image_bytes=None, rarity="Common", weight="0kg"):
        if message.strip().lower() == "Unknown Bee" and weight.lower() == "unknown": # if only one is unknown send it anyways as
            return                                                                   # it's probably valid, just couldn't extract
                                                                                     # one of the parts well
        if self.enabled and self.url:
            data = Constants.RARITY_DATA.get(rarity, Constants.RARITY_DATA["Common"])
            payload = {
                "embeds": [{
                    "title": f"✨ {rarity} Catch!",
                    "color": data["embed_color"],
                    "fields": [
                        {"name": "Bee", "value": message, "inline": True},
                        {"name": "Weight", "value": weight, "inline": True},
                        {"name": "Total", "value": str(count), "inline": True}
                    ],
                    "image": {"url": "attachment://catch.png"} if image_bytes else None,
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                }]
            }
            self.msg_queue.put({"payload": payload, "img": image_bytes})

    def send_status(self, message: str, image_bytes=None):
        if not self.enabled or not self.url:
            return

        payload = {
            "embeds": [{
                "title": "📊 Session Status",
                "description": message,
                "color": 0x3498db,  # blue
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                "image": {"url": "attachment://status.png"} if image_bytes else None
            }]
        }

        self.msg_queue.put({
            "payload": payload,
            "img": image_bytes
        })

    def _processor(self):
        while not self._stop_event.is_set():
            try:
                item = self.msg_queue.get(timeout=1.0)
                boundary = uuid.uuid4().hex
                payload = item["payload"]
                img_bytes = item["img"]

                parts = []
                # JSON Payload
                parts.append(f'--{boundary}\r\n'.encode())
                parts.append(f'Content-Disposition: form-data; name="payload_json"\r\n'.encode())
                parts.append(f'Content-Type: application/json\r\n\r\n'.encode())
                parts.append(f'{json.dumps(payload)}\r\n'.encode())
            
                # Image
                if img_bytes:
                    parts.append(f'--{boundary}\r\n'.encode())
                    parts.append(f'Content-Disposition: form-data; name="files[0]"; filename="catch.png"\r\n'.encode())
                    parts.append(f'Content-Type: image/png\r\n\r\n'.encode())
                    parts.append(img_bytes)
                    parts.append(b'\r\n')
            
                # Final boundary
                parts.append(f'--{boundary}--\r\n'.encode())
                body = b''.join(parts)

                req = urllib.request.Request(self.url, data=body, method='POST')
                req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
                req.add_header('User-Agent', 'BeesTool/1.0')

                try:
                    with urllib.request.urlopen(req, timeout=15) as _: pass
                except Exception as e: 
                    print(f"[Webhook::Processor] Failed: {e}")
            
                self.msg_queue.task_done()
            except queue.Empty: 
                continue

    def stop(self):
        self._stop_event.set()