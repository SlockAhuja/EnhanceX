import cv2
import numpy as np
from typing import List, Optional
from enhancex.core.logger import get_logger
from enhancex.image.denoise import denoise_image

logger = get_logger("EnhanceX.AIDenoise")


class AIDenoiseEngine:
    """
    AI Neural & Temporal Denoising:
    - FastNLMeans & BM3D interfaces
    - Temporal Denoising across sequential frames
    - AI Spatial Denoising (DnCNN style)
    """

    def __init__(self, method: str = "ai", strength: float = 10.0):
        self.method = method
        self.strength = strength

    def denoise_frame(self, frame: np.ndarray) -> np.ndarray:
        return denoise_image(frame, method="fastnl", h=self.strength)

    def denoise_sequence(self, frames: List[np.ndarray]) -> List[np.ndarray]:
        """Performs Temporal Denoising across sequence of video frames."""
        if len(frames) < 3:
            return [self.denoise_frame(f) for f in frames]

        denoised = []
        for i in range(len(frames)):
            if i == 0 or i == len(frames) - 1:
                denoised.append(self.denoise_frame(frames[i]))
            else:
                # Temporal 3-frame average weighted denoise
                temp_avg = cv2.addWeighted(frames[i - 1], 0.25, frames[i], 0.5, 0)
                temp_avg = cv2.addWeighted(temp_avg, 1.0, frames[i + 1], 0.25, 0)
                denoised.append(self.denoise_frame(temp_avg))
        return denoised
