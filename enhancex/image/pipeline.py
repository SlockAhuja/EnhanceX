import numpy as np
from typing import Optional, Dict, Any
from enhancex.image.resize import resize_image
from enhancex.image.sharpen import sharpen_image
from enhancex.image.denoise import denoise_image
from enhancex.image.color import apply_clahe, white_balance, adjust_color, histogram_equalization


class ImagePipeline:
    """Configurable pipeline for executing sequence of traditional image enhancements."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def process(
        self,
        image: np.ndarray,
        use_clahe: bool = False,
        use_white_balance: bool = False,
        sharpen_strength: float = 0.0,
        denoise_strength: float = 0.0,
        resize_factor: Optional[float] = None
    ) -> np.ndarray:
        out = image.copy()

        if use_white_balance:
            out = white_balance(out, method=self.config.get("white_balance_method", "gray_world"))

        if use_clahe:
            out = apply_clahe(out, clip_limit=self.config.get("clahe_clip_limit", 2.0))

        if denoise_strength > 0:
            out = denoise_image(out, method="fastnl", h=denoise_strength)

        if sharpen_strength > 0:
            out = sharpen_image(out, strength=sharpen_strength)

        if resize_factor is not None and resize_factor != 1.0:
            out = resize_image(out, size=resize_factor)

        return out
