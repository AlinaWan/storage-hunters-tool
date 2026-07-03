import tkinter as tk
from typing import final as sealed

import cv2
import numpy as np

@sealed
class ImageConverter:
    @staticmethod
    def mat_to_tk_image(mat: np.ndarray) -> tk.PhotoImage | None:
        success, encoded_img = cv2.imencode(".png", mat)
        if not success:
            return None
            
        raw_bytes = encoded_img.tobytes()
        img_tk = tk.PhotoImage(data=raw_bytes)
        
        return img_tk