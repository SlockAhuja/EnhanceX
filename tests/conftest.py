import pytest
import os
import cv2
import numpy as np


@pytest.fixture
def sample_image():
    """Generates a 256x256 test image fixture."""
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    cv2.circle(img, (128, 128), 50, (255, 128, 0), -1)
    cv2.rectangle(img, (20, 20), (80, 80), (0, 255, 255), -1)
    return img


@pytest.fixture
def temp_media_dir(tmp_path):
    """Creates temporary video and image files for testing."""
    img_path = str(tmp_path / "test_input.jpg")
    vid_path = str(tmp_path / "test_input.mp4")

    # Save test image
    img = np.zeros((128, 128, 3), dtype=np.uint8)
    cv2.circle(img, (64, 64), 30, (255, 255, 255), -1)
    cv2.imwrite(img_path, img)

    # Save test video (10 frames)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(vid_path, fourcc, 10.0, (128, 128))
    for i in range(10):
        f = np.zeros((128, 128, 3), dtype=np.uint8)
        cv2.circle(f, (64 + i * 2, 64), 20, (0, 255, 0), -1)
        writer.write(f)
    writer.release()

    return {"image": img_path, "video": vid_path, "dir": str(tmp_path)}
