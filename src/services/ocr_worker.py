"""
This is launched as a subprocess with shared memory.

Depended by program.pyw
"""
import asyncio
from multiprocessing import shared_memory

import cv2
import numpy as np

from utils.ocr_engine import WindowsOCR
from utils.ocr_parser import OCRParser


class OCRWorker:
    def __init__(self, shm_name, shape, dtype, request_queue, result_queue, lock):
        self.shm = shared_memory.SharedMemory(name=shm_name)
        self.shape = shape
        self.dtype = dtype

        self.request_queue = request_queue
        self.result_queue = result_queue
        self.lock = lock

        self.frame = np.ndarray(shape, dtype=dtype, buffer=self.shm.buf)

    def run(self):
        ocr_engine = WindowsOCR()

        while True:
            msg = self.request_queue.get()
            if msg == "STOP": break
            if msg != "PROCESS": continue

            try:
                # Use a local copy to avoid shared memory mutation during processing
                with self.lock:
                    img = np.copy(self.frame)

                if img is None or img.size == 0:
                    continue

                if not img.flags['C_CONTIGUOUS']:
                    img = np.ascontiguousarray(img)

                rarity = OCRParser.detect_rarity_by_color(img)

                # Improved Pre-processing
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Resizing up 2x often significantly improves OCR accuracy for small text
                gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                
                # only keep text that is almost perfectly white
                _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
                thresh = cv2.bitwise_not(thresh) # inverting 
                kernel = np.ones((2,2), np.uint8)
                thresh = cv2.dilate(thresh, kernel, iterations=1)

                # debug
                # from datetime import datetime, timezone
                # from pathlib import Path

                # base_dir = Path(__file__).resolve().parent.parent 
                # debug_folder = base_dir / "ocr_debug"
                # timestamp = datetime.now().strftime("%y%m%d_%H%M%S")

                # if not debug_folder.exists():
                #     debug_folder.mkdir(parents=True, exist_ok=True)

                # filename = debug_folder / f"ocr_{timestamp}.png"
                # cv2.imwrite(str(filename), thresh)

                raw_text = asyncio.run(
                    ocr_engine.get_text_from_bytes(
                        cv2.imencode(".png", thresh)[1].tobytes()
                    )
                )

                bee_name, bee_weight = OCRParser.parse_bee_text(raw_text)

                self.result_queue.put({
                    "rarity": rarity,
                    "raw_text": raw_text,
                    "bee_name": bee_name,
                    "bee_weight": bee_weight
                })

            except Exception as e:
                self.result_queue.put({"error": str(e)})


def start_worker(shm_name, shape, dtype, request_queue, result_queue, lock):
    worker = OCRWorker(shm_name, shape, dtype, request_queue, result_queue, lock)
    worker.run()