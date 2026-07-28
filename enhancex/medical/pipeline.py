"""
Medical Image Processing Pipeline - EnhanceX v1.3.0
Provides DICOM/grayscale histogram equalization, tissue contrast enhancement, and noise reduction.
"""

import cv2
import numpy as np
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Medical")


class MedicalPipeline:
    """Enhancement pipeline for medical imagery (X-ray, CT, MRI, Ultrasound)."""

    def process(
        self,
        image: np.ndarray,
        clahe_clip: float = 3.0,
        denoise_strength: float = 5.0
    ) -> np.ndarray:
        if image is None or image.size == 0:
            return image

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()

        # Medical CLAHE tissue contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(gray)

        # Non-Local Means Denoising tailored for medical noise
        if denoise_strength > 0:
            enhanced_gray = cv2.fastNlMeansDenoising(enhanced_gray, None, h=denoise_strength, templateWindowSize=7, searchWindowSize=21)

        return cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR) if len(image.shape) == 3 else enhanced_gray
