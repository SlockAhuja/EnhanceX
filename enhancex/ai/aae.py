"""
Adaptive AI Enhancement Engine (AAE) - EnhanceX v1.2.0
Provides automated category detection, quality defect analysis, and adaptive pipeline construction.
"""

import cv2
import numpy as np
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Union
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.AAE")


class MediaCategory(str, Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    ANIME = "anime"
    DOCUMENT = "document"
    NIGHT = "night"
    MEDICAL = "medical"
    SATELLITE = "satellite"
    ARTWORK = "artwork"
    SCREENSHOT = "screenshot"
    GENERAL = "general"


class QualityDefect(str, Enum):
    BLUR = "blur"
    NOISE = "noise"
    COMPRESSION = "compression"
    LOW_RES = "low_resolution"
    SCRATCHES = "scratches"
    COLOR_IMBALANCE = "color_imbalance"
    MOTION_BLUR = "motion_blur"
    LOW_LIGHT = "low_light"


@dataclass
class MediaAnalysis:
    category: MediaCategory
    category_confidence: float
    defects: List[QualityDefect]
    metrics: Dict[str, float] = field(default_factory=dict)
    recommended_pipeline: List[str] = field(default_factory=list)


class CategoryDetector:
    """Detects image category using computer vision metrics and signal analysis."""

    def detect(self, image: np.ndarray) -> Tuple[MediaCategory, float]:
        if image is None or image.size == 0:
            return MediaCategory.GENERAL, 0.5

        h, w, c = image.shape if len(image.shape) == 3 else (image.shape[0], image.shape[1], 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if c == 3 else image

        # 1. Document detection check
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        white_ratio = np.mean(binary == 255)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.mean(edges > 0)
        if white_ratio > 0.60 and edge_density > 0.01:
            return MediaCategory.DOCUMENT, 0.88

        # 2. Night detection check
        mean_lum = np.mean(gray)
        if mean_lum < 55.0:
            return MediaCategory.NIGHT, 0.90

        # 3. Medical detection check (grayscale / DICOM uniform spectrum with low color channels diff)
        if c == 3:
            b, g, r = cv2.split(image)
            diff_bg = np.mean(np.abs(b.astype(float) - g.astype(float)))
            diff_gr = np.mean(np.abs(g.astype(float) - r.astype(float)))
            if diff_bg < 1.0 and diff_gr < 1.0 and 20.0 < mean_lum < 200.0 and white_ratio < 0.50:
                return MediaCategory.MEDICAL, 0.92

        # 4. Portrait face detection check
        if hasattr(cv2, "CascadeClassifier") and hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
            try:
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                if len(faces) > 0:
                    return MediaCategory.PORTRAIT, 0.95
            except Exception:
                pass

        # 5. Screenshot detection check (flat areas + sharp font edges)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap_var = lap.var()
        if c == 3:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            sat = hsv[:, :, 1]
            sat_std = np.std(sat)
            if sat_std < 35.0 and lap_var > 300.0:
                return MediaCategory.SCREENSHOT, 0.85

        # 6. Anime / Illustration detection check
        if c == 3:
            # Anime has sharp contours, high saturation, flat region blocks
            blur_img = cv2.bilateralFilter(image, 9, 75, 75)
            diff = np.mean(np.abs(image.astype(float) - blur_img.astype(float)))
            if diff < 8.0 and sat_std > 50.0:
                return MediaCategory.ANIME, 0.87

        # 7. Satellite image check (high resolution spatial texture variance)
        if w >= 1000 and h >= 1000:
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            grad_mag = np.sqrt(sobelx**2 + sobely**2)
            if np.mean(grad_mag) > 45.0 and lap_var > 600.0:
                return MediaCategory.SATELLITE, 0.80

        # 8. Landscape vs Artwork
        if c == 3:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hue = hsv[:, :, 0]
            # Green (35-85) and Blue (90-130) dominant tones
            green_blue = np.mean((hue >= 35) & (hue <= 130))
            if green_blue > 0.40:
                return MediaCategory.LANDSCAPE, 0.82
            elif np.std(hsv[:, :, 0]) > 40.0:
                return MediaCategory.ARTWORK, 0.78

        return MediaCategory.GENERAL, 0.70


class QualityAnalyzer:
    """Analyzes quality defects in media inputs using digital signal processing."""

    def analyze(self, image: np.ndarray) -> Tuple[List[QualityDefect], Dict[str, float]]:
        if image is None or image.size == 0:
            return [], {}

        h, w, c = image.shape if len(image.shape) == 3 else (image.shape[0], image.shape[1], 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if c == 3 else image

        defects = []
        metrics = {}

        # 1. Blur Analysis
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        metrics["blur_score"] = blur_score
        if blur_score < 100.0:
            defects.append(QualityDefect.BLUR)

        # 2. Motion Blur Analysis
        sobelx = np.abs(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3))
        sobely = np.abs(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3))
        ratio_xy = np.mean(sobelx) / (np.mean(sobely) + 1e-5)
        metrics["motion_ratio"] = float(ratio_xy)
        if ratio_xy > 2.5 or ratio_xy < 0.4:
            defects.append(QualityDefect.MOTION_BLUR)

        # 3. Noise Analysis
        med = cv2.medianBlur(gray, 3)
        noise_variance = float(np.mean(np.abs(gray.astype(float) - med.astype(float))))
        metrics["noise_variance"] = noise_variance
        if noise_variance > 5.0:
            defects.append(QualityDefect.NOISE)

        # 4. Compression Artifacts (8x8 block boundary discontinuities)
        if h >= 16 and w >= 16:
            r7 = gray[7:-1:8, :]
            r8 = gray[8::8, :]
            min_r = min(r7.shape[0], r8.shape[0])
            block_diff_h = np.mean(np.abs(r7[:min_r, :].astype(float) - r8[:min_r, :].astype(float)))

            r3 = gray[3:-1:8, :]
            r4 = gray[4::8, :]
            min_rm = min(r3.shape[0], r4.shape[0])
            normal_diff_h = np.mean(np.abs(r3[:min_rm, :].astype(float) - r4[:min_rm, :].astype(float)))
            block_score = float(block_diff_h / (normal_diff_h + 1e-5))
            metrics["compression_score"] = block_score
            if block_score > 1.35:
                defects.append(QualityDefect.COMPRESSION)

        # 5. Low Resolution
        metrics["resolution_pixels"] = float(w * h)
        if w < 1280 or h < 720:
            defects.append(QualityDefect.LOW_RES)

        # 6. Low Light
        mean_lum = float(np.mean(gray))
        metrics["mean_luminance"] = mean_lum
        if mean_lum < 60.0:
            defects.append(QualityDefect.LOW_LIGHT)

        # 7. Color Imbalance
        if c == 3:
            b, g, r = cv2.split(image)
            ch_means = [float(np.mean(b)), float(np.mean(g)), float(np.mean(r))]
            channel_divergence = float(np.std(ch_means))
            metrics["channel_divergence"] = channel_divergence
            if channel_divergence > 18.0:
                defects.append(QualityDefect.COLOR_IMBALANCE)

        # 8. Scratches / Line Streaks
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=5)
        scratch_count = len(lines) if lines is not None else 0
        metrics["scratch_count"] = float(scratch_count)
        if scratch_count > 12:
            defects.append(QualityDefect.SCRATCHES)

        return defects, metrics


class AdaptiveAIEngine:
    """Adaptive AI Enhancement Engine main coordinator."""

    def __init__(self):
        self.detector = CategoryDetector()
        self.analyzer = QualityAnalyzer()

    def analyze(self, image_input: Union[str, np.ndarray]) -> MediaAnalysis:
        if isinstance(image_input, str):
            image = cv2.imread(image_input)
            if image is None:
                raise FileNotFoundError(f"Failed to read image at {image_input}")
        else:
            image = image_input

        category, confidence = self.detector.detect(image)
        defects, metrics = self.analyzer.analyze(image)
        recommended_pipeline = self.build_pipeline(category, defects)

        return MediaAnalysis(
            category=category,
            category_confidence=confidence,
            defects=defects,
            metrics=metrics,
            recommended_pipeline=recommended_pipeline
        )

    def build_pipeline(self, category: MediaCategory, defects: List[QualityDefect]) -> List[str]:
        pipeline = []

        # Category-driven base selection
        if category == MediaCategory.DOCUMENT:
            pipeline.extend(["document_binarize", "contrast_clahe", "unsharp_mask"])
        elif category == MediaCategory.PORTRAIT:
            pipeline.extend(["face_enhance", "color_balance", "denoise"])
        elif category == MediaCategory.ANIME:
            pipeline.extend(["anime_super_res", "edge_preserve_sharpen"])
        elif category == MediaCategory.MEDICAL:
            pipeline.extend(["histogram_equalize", "grayscale_contrast"])
        elif category == MediaCategory.SATELLITE:
            pipeline.extend(["multi_spectral_sharpen", "haze_removal"])
        elif category == MediaCategory.NIGHT:
            pipeline.extend(["low_light_boost", "denoise", "hdr_tone_map"])

        # Defect-driven stage additions
        if QualityDefect.BLUR in defects and "unsharp_mask" not in pipeline:
            pipeline.append("unsharp_mask")
        if QualityDefect.NOISE in defects and "denoise" not in pipeline:
            pipeline.append("denoise")
        if QualityDefect.COLOR_IMBALANCE in defects and "color_balance" not in pipeline:
            pipeline.append("color_balance")
        if QualityDefect.LOW_LIGHT in defects and "low_light_boost" not in pipeline:
            pipeline.append("low_light_boost")
        if QualityDefect.LOW_RES in defects and "super_resolution" not in pipeline and "anime_super_res" not in pipeline:
            pipeline.append("super_resolution")

        if not pipeline:
            pipeline = ["contrast_clahe", "sharpen"]

        return pipeline
