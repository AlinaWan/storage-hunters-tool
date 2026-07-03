import tkinter as tk
from typing import final as sealed

import cv2
import numpy as np

@sealed
class ImageConverter:
    @staticmethod
    def mat_to_tk_image(mat: np.ndarray) -> tk.PhotoImage | None:
        if mat is None or mat.size == 0:
            return None

        h, w = mat.shape[:2]
            
        if mat.ndim == 2:
            rgb_mat = cv2.cvtColor(mat, cv2.COLOR_GRAY2RGB)
        elif mat.shape[2] == 3:
            rgb_mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
        elif mat.shape[2] == 4:
            rgb_mat = cv2.cvtColor(mat, cv2.COLOR_BGRA2RGB)
        if not rgb_mat.flags['C_CONTIGUOUS']:
            rgb_mat = np.ascontiguousarray(rgb_mat)
            
        # P6, Width, Height, MaxVal, single whitespace -> bytes start
        header = f"P6\n{w} {h}\n255\n".encode("ascii")
        ppm_data = header + rgb_mat.tobytes()
        img_tk = tk.PhotoImage(data=ppm_data)
            
        return img_tk
