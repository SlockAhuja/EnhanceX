"""
Satellite & Aerial Imagery Pipeline - EnhanceX v1.3.0
Provides multi-band spectral sharpening, atmospheric haze removal, and spatial detail boost.
"""

import cv2
import numpy as np
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Satellite")


class SatellitePipeline:
    """Enhancement pipeline for satellite, drone, and aerial Remote Sensing imagery."""

    def process(
        self,
        image: np.ndarray,
        remove_haze: bool = True,
        sharpen_strength: float = 1.5
    ) -> np.ndarray:
        if image is None or image.size == 0:
            return image

        out = image.copy()
        if remove_haze:
            out = self.remove_atmospheric_haze(out)

        if sharpen_strength > 0:
            out = self.multi_band_sharpen(out, strength=sharpen_strength)

        return out

    def remove_atmospheric_haze(self, image: np.ndarray) -> np.ndarray:
        # Dark Channel Prior haze reduction
        dark_channel = np.min(image, axis=2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        dark_channel = cv2.erode(dark_channel, kernel)
        atmosphere = float(np.percentile(dark_channel, 99))
        transmission = 1.0 - 0.95 * (dark_channel.astype(float) / max(atmosphere, 1.0))
        transmission = np.clip(transmission, 0.1, 1.0)
        
        res = np.zeros_like(image, dtype=np.float32)
        for i in range(3):
            res[:, :, i] = (image[:, :, i].astype(float) - atmosphere) / transmission + atmosphere

        return np.clip(res, 0, 255).astype(np.uint8)

    def multi_band_sharpen(self, image: np.ndarray, strength: float = 1.5) -> np.ndarray:
        blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=3)
        sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
        return np.clip(sharpened, 0, 255).astype(np.uint8)
