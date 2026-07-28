import cv2
import numpy as np
from typing import Tuple, Union


def resize_image(
    image: np.ndarray,
    size: Union[Tuple[int, int], float],
    interpolation: str = "bicubic"
) -> np.ndarray:
    """
    Resize image using specified interpolation algorithm.
    :param image: Input HWC image array.
    :param size: Tuple (width, height) or float scale factor.
    :param interpolation: 'bicubic', 'lanczos', 'bilinear', or 'nearest'.
    :return: Resized HWC image array.
    """
    interp_map = {
        "bicubic": cv2.INTER_CUBIC,
        "lanczos": cv2.INTER_LANCZOS4,
        "bilinear": cv2.INTER_LINEAR,
        "nearest": cv2.INTER_NEAREST,
        "area": cv2.INTER_AREA
    }
    flag = interp_map.get(interpolation.lower(), cv2.INTER_CUBIC)

    if isinstance(size, float) or isinstance(size, int):
        scale = float(size)
        return cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=flag)
    else:
        w, h = size
        return cv2.resize(image, (w, h), interpolation=flag)
