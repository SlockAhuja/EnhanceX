import cv2
import numpy as np


def sharpen_image(
    image: np.ndarray,
    strength: float = 1.0,
    radius: int = 1,
    method: str = "unsharp_mask"
) -> np.ndarray:
    """
    Sharpen input image using unsharp masking or Laplacian kernel.
    :param image: Input HWC image array (uint8).
    :param strength: Sharpening strength factor (1.0 = standard).
    :param radius: Gaussian blur radius for unsharp mask.
    :param method: 'unsharp_mask' or 'laplacian'.
    :return: Sharpened image array (uint8).
    """
    if strength <= 0:
        return image.copy()

    if method == "laplacian":
        kernel = np.array([[0, -1, 0],
                           [-1, 4 + strength, -1],
                           [0, -1, 0]], dtype=np.float32)
        sharpened = cv2.filter2D(image, -1, kernel)
        return np.clip(sharpened, 0, 255).astype(np.uint8)

    # Default: unsharp mask
    kernel_size = radius * 2 + 1
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), radius)
    sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)
