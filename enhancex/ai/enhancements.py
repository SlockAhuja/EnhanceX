import cv2
import numpy as np
from enhancex.image.color import apply_clahe, adjust_color
from enhancex.image.sharpen import sharpen_image


class FaceEnhancer:
    """Detects and enhances facial regions in images and videos."""

    def __init__(self):
        self.face_cascade = None
        if hasattr(cv2, 'CascadeClassifier') and hasattr(cv2, 'data'):
            cascade_path = getattr(cv2.data, 'haarcascades', '') + 'haarcascade_frontalface_default.xml'
            try:
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
            except Exception:
                self.face_cascade = None

    def enhance(self, image: np.ndarray) -> np.ndarray:
        out = image.copy()
        if self.face_cascade is not None and not self.face_cascade.empty():
            try:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    roi = out[y:y + h, x:x + w]
                    roi_enhanced = sharpen_image(roi, strength=0.8)
                    roi_enhanced = adjust_color(roi_enhanced, contrast=1.1, brightness=5.0)
                    out[y:y + h, x:x + w] = roi_enhanced
                return out
            except Exception:
                pass

        # Center patch enhancement fallback if CascadeClassifier is unavailable
        h, w = out.shape[:2]
        ch, cw = int(h * 0.4), int(w * 0.4)
        cy, cx = h // 2, w // 2
        roi = out[cy - ch // 2:cy + ch // 2, cx - cw // 2:cx + cw // 2]
        if roi.size > 0:
            roi_enhanced = sharpen_image(roi, strength=0.6)
            out[cy - ch // 2:cy + ch // 2, cx - cw // 2:cx + cw // 2] = roi_enhanced

        return out


class HDREnhancer:
    """HDR Tone mapping and dynamic range expansion."""

    def enhance(self, image: np.ndarray) -> np.ndarray:
        # Multi-scale Retinex HDR effect approximation
        clahe_img = apply_clahe(image, clip_limit=3.0)
        hdr_blend = cv2.addWeighted(image, 0.4, clahe_img, 0.6, 0)
        return adjust_color(hdr_blend, saturation=1.25, contrast=1.15)
