"""
EnhanceX Python API Demonstration Script
"""
import numpy as np
import cv2
from enhancex import VideoEnhancer, ImageEnhancer, Stabilizer


def main():
    print("=== EnhanceX Python API Demo ===")

    # 1. Image Enhancement
    img_enhancer = ImageEnhancer()
    dummy_img = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.putText(dummy_img, "EnhanceX Demo", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    enhanced_img = img_enhancer.enhance(
        dummy_img,
        sharpen=1.5,
        clahe=True,
        white_balance=True,
        denoise=5.0
    )
    print(f"Enhanced Image Shape: {enhanced_img.shape}")

    # 2. Video Enhancer API
    enhancer = VideoEnhancer()
    print("VideoEnhancer API Initialized successfully.")


if __name__ == "__main__":
    main()
