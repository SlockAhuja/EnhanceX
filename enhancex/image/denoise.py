import cv2
import numpy as np


def denoise_image(
    image: np.ndarray,
    method: str = "fastnl",
    h: float = 10.0,
    template_window_size: int = 7,
    search_window_size: int = 21
) -> np.ndarray:
    """
    Denoise image using Fast Non-Local Means, Bilateral, or Gaussian filtering.
    :param image: Input HWC uint8 image array.
    :param method: 'fastnl', 'bilateral', or 'gaussian'.
    :param h: Filter strength parameter for FastNLMeans / Bilateral sigmaColor.
    :param template_window_size: Size in pixels of template patch for FastNLMeans.
    :param search_window_size: Size in pixels of window to search for patch matches.
    :return: Denoised uint8 image array.
    """
    if method == "bilateral":
        d = 9
        sigma_color = float(h)
        sigma_space = float(h)
        return cv2.bilateralFilter(image, d, sigma_color, sigma_space)
    elif method == "gaussian":
        k_size = int(h) if int(h) % 2 == 1 else int(h) + 1
        return cv2.GaussianBlur(image, (k_size, k_size), 0)
    else:  # 'fastnl'
        if len(image.shape) == 2:
            return cv2.fastNlMeansDenoising(
                image, None, h, template_window_size, search_window_size
            )
        else:
            return cv2.fastNlMeansDenoisingColored(
                image, None, h, h, template_window_size, search_window_size
            )
