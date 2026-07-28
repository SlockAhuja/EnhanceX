"""
Anime & Illustration Enhancement Pipeline - EnhanceX v1.3.0
Provides line-art preservation, anime super-resolution, and flat-color smoothing.
"""

import cv2
import numpy as np
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Anime")


class AnimePipeline:
    """Specialized enhancement pipeline for Anime, Manga, and digital illustrations."""

    def process(
        self,
        image: np.ndarray,
        scale: int = 2,
        preserve_lines: bool = True,
        smooth_flat_regions: bool = True
    ) -> np.ndarray:
        if image is None or image.size == 0:
            return image

        out = image.copy()
        if smooth_flat_regions:
            out = cv2.bilateralFilter(out, d=9, sigmaColor=75, sigmaSpace=75)

        if preserve_lines:
            gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY) if len(out.shape) == 3 else out
            edges = cv2.Canny(gray, 80, 160)
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            out = cv2.subtract(out, (edges_bgr * 0.15).astype(np.uint8))

        if scale > 1:
            h, w = out.shape[:2]
            out = cv2.resize(out, (w * scale, h * scale), interpolation=cv2.INTER_LANCZOS4)

        return out
