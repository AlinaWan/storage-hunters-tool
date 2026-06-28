import numpy as np
import re
from typing import final as sealed

from core.config import Config
from core.constants import Constants

@sealed
class OCRParser:
    @staticmethod
    def _find_color_hit(img_bgr, target_bgr, tolerance=10, strip=100):
        diff = np.abs(img_bgr.astype(np.int16) - np.array(target_bgr, dtype=np.int16))
        mask = np.all(diff <= tolerance, axis=2) # per channel

        # we look for strip number of True values in a row
        for row in mask[::-1]: # [::-1] to reverse the rows (iterate bottom to top)
            count = 0
            for hit in row: # left to right
                if hit:
                    count += 1
                    if count >= strip:
                        return True
                else:
                    count = 0
        return False

    def parse_bee_text(text: str):
        clean = text.replace("\n", " ").strip()

        # --- Normalize OCR noise ---
        clean = re.sub(r"\.\.+", ".", clean)
        clean = re.sub(r"(\d)\s+(\d)", r"\1\2", clean)
        clean = re.sub(r"(?<=\d)\s*[:;,]\s*(?=\d)", ".", clean)

        # --- Fix OCR unit corruption ---
        clean = re.sub(r"kq\b", "kg", clean, flags=re.IGNORECASE) # fix kq -> kg
        clean = re.sub(r"\bk g\b", "kg", clean, flags=re.IGNORECASE)

        # --- Bee detection & Name extraction ---
        has_bee_word = bool(re.search(r"\bBee\b", clean, re.IGNORECASE)) 
        ends_with_stuck_bee = re.search(r"[A-Za-z]+Bee\b", clean) # IMPORTANT: B must be capital or else
                                                                  # it will split things like Zombee
        if ends_with_stuck_bee and not has_bee_word: # Fix missing space before 'Bee'
            clean = re.sub(r"([A-Za-z]+)Bee\b", r"\1 Bee", clean)

        # recompute after modification
        has_bee_word = re.search(r"\bBee\b", clean, re.IGNORECASE)

        name_match = re.search(r"([A-Za-z]+(?:\s?[A-Za-z]+)*\s?Bee)", clean)

        if name_match:
            raw_name = name_match.group(1)
            bee_name = raw_name if has_bee_word else re.sub(r"\s*Bee$", "", raw_name, flags=re.IGNORECASE)
        else:
            fallback_match = re.search(r"^([A-Za-z]+(?:\s[A-Za-z]+)*)", clean)
            bee_name = fallback_match.group(1) if fallback_match else "unknown Bee"
        
        bee_name = bee_name.title().strip()

        weight_match = re.search(r"([0-9SlIOQ]+(?:\.[0-9SlIOQ]+)?\s*[kK][gG])", clean)
        
        if weight_match:
            raw_weight = weight_match.group(1).lower()
            
            # 2. Map look-alikes to numbers
            mapping = {
                's': '5',
                'i': '1',
                'l': '1',
                'o': '0',
                'q': '0'
            }
            
            # Apply mapping only to the numbers part
            for char, replacement in mapping.items():
                raw_weight = raw_weight.replace(char, replacement)
            
            bee_weight = raw_weight.replace(" ", "")
        else:
            bee_weight = "unknown"

        return bee_name, bee_weight

    @staticmethod
    def detect_rarity_by_color(img_bgr):

        # h = img_bgr.shape[0]

        # take bottom half of OCR ROI
        # img_bgr = img_bgr[h // 2:, :]

        # import cv2
        # cv2.imshow("rarity_roi", img_bgr)
        # cv2.waitKey(1)

        best_match = "Common"

        for name, data in Constants.RARITY_DATA.items():
            if OCRParser._find_color_hit(img_bgr, data["color_bgr"], Config.DISCORD_WEBHOOK_RARITY_TOLERANCE, int(Config.DRAG_STEP//4)):
                return name

        return best_match
