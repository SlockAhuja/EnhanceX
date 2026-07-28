"""
Document Processing & Enhancement Pipeline - EnhanceX v1.3.0
Provides adaptive binarization, document deskew, shadow removal, and contrast enhancement.
"""

import cv2
import numpy as np
from typing import Optional, Tuple
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Document")


class DocumentPipeline:
    """Specialized document image enhancement pipeline."""

    def process(
        self,
        image: np.ndarray,
        binarize: bool = False,
        deskew: bool = True,
        remove_shadows: bool = True
    ) -> np.ndarray:
        if image is None or image.size == 0:
            return image

        out = image.copy()
        if remove_shadows:
            out = self.remove_shadows(out)

        if deskew:
            out = self.deskew_document(out)

        if binarize:
            out = self.adaptive_binarize(out)

        return out

    def remove_shadows(self, image: np.ndarray) -> np.ndarray:
        rgb_planes = cv2.split(image)
        result_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(norm_img)
        return cv2.merge(result_planes)

    def deskew_document(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

        if lines is None or len(lines) == 0:
            return image

        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
            if abs(angle) < 45.0:
                angles.append(angle)

        if not angles:
            return image

        median_angle = float(np.median(angles))
        if abs(median_angle) < 0.5:
            return image

        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def adaptive_binarize(self, image: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8
        )
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR) if len(image.shape) == 3 else binary
