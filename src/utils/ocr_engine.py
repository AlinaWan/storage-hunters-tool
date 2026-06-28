from typing import final as sealed

from winsdk.windows.media.ocr import OcrEngine
from winsdk.windows.graphics.imaging import BitmapDecoder
from winsdk.windows.storage.streams import DataWriter, InMemoryRandomAccessStream

@sealed
class WindowsOCR:
    def __init__(self):
        self.engine = OcrEngine.try_create_from_user_profile_languages()

    async def get_text_from_bytes(self, image_bytes):
        """Uses native Windows OCR to read text from raw image bytes."""
        # Convert bytes to Windows Stream
        stream = InMemoryRandomAccessStream()
        writer = DataWriter(stream)
        writer.write_bytes(image_bytes)
        await writer.store_async()
        stream.seek(0)

        # Process OCR
        decoder = await BitmapDecoder.create_async(stream)
        bitmap = await decoder.get_software_bitmap_async()
        result = await self.engine.recognize_async(bitmap)
        return result.text