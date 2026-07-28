import cv2
import numpy as np
from typing import Tuple


def histogram_equalization(image: np.ndarray) -> np.ndarray:
    """Performs Histogram Equalization on single-channel or YCrCb color channels."""
    if len(image.shape) == 2:
        return cv2.equalizeHist(image)
    
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)


def apply_clahe(
    image: np.ndarray,
    clip_limit: float = 2.0,
    tile_grid_size: Tuple[int, int] = (8, 8)
) -> np.ndarray:
    """Applies Contrast Limited Adaptive Histogram Equalization (CLAHE)."""
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    if len(image.shape) == 2:
        return clahe.apply(image)
    
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    return cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)


def white_balance(image: np.ndarray, method: str = "gray_world") -> np.ndarray:
    """
    Automatic White Balance correction (Gray World or White Patch).
    """
    result = image.astype(np.float32)
    if method == "white_patch":
        max_b = np.percentile(result[:, :, 0], 99) or 1.0
        max_g = np.percentile(result[:, :, 1], 99) or 1.0
        max_r = np.percentile(result[:, :, 2], 99) or 1.0
        result[:, :, 0] = np.clip(result[:, :, 0] * (255.0 / max_b), 0, 255)
        result[:, :, 1] = np.clip(result[:, :, 1] * (255.0 / max_g), 0, 255)
        result[:, :, 2] = np.clip(result[:, :, 2] * (255.0 / max_r), 0, 255)
    else:  # gray_world
        avg_b = np.mean(result[:, :, 0]) or 1.0
        avg_g = np.mean(result[:, :, 1]) or 1.0
        avg_r = np.mean(result[:, :, 2]) or 1.0
        avg_gray = (avg_b + avg_g + avg_r) / 3.0
        result[:, :, 0] = np.clip(result[:, :, 0] * (avg_gray / avg_b), 0, 255)
        result[:, :, 1] = np.clip(result[:, :, 1] * (avg_gray / avg_g), 0, 255)
        result[:, :, 2] = np.clip(result[:, :, 2] * (avg_gray / avg_r), 0, 255)
    return result.astype(np.uint8)


def adjust_color(
    image: np.ndarray,
    brightness: float = 0.0,
    contrast: float = 1.0,
    gamma: float = 1.0,
    saturation: float = 1.0
) -> np.ndarray:
    """Adjusts brightness, contrast, gamma, and color saturation."""
    res = image.astype(np.float32)

    # Brightness & Contrast
    if brightness != 0.0 or contrast != 1.0:
        res = res * contrast + brightness

    # Gamma correction
    if gamma != 1.0 and gamma > 0:
        inv_gamma = 1.0 / gamma
        res = np.power(np.clip(res / 255.0, 0, 1), inv_gamma) * 255.0

    res = np.clip(res, 0, 255).astype(np.uint8)

    # Saturation adjustment
    if saturation != 1.0 and len(res.shape) == 3:
        hsv = cv2.cvtColor(res, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 255)
        res = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    return res
