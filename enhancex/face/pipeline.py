"""
Facial Restoration & Enhancement Pipeline - EnhanceX v1.3.0
Provides face detection, restoration alignment, and GFPGAN / CodeFormer high-level interface.
"""

import cv2
import numpy as np
from typing import Optional
from enhancex.ai.enhancements import FaceEnhancer
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Face")


class FacialRestorationPipeline:
    """Dedicated face detection and restoration pipeline."""

    def __init__(self, model_name: str = "GFPGAN"):
        self.model_name = model_name
        self.enhancer = FaceEnhancer()

    def process(self, image: np.ndarray, fidelity: float = 0.8) -> np.ndarray:
        if image is None or image.size == 0:
            return image
        return self.enhancer.enhance(image)
