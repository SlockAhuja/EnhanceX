import cv2
import numpy as np
from typing import List, Tuple
from enhancex.video.io import VideoReader


def detect_scenes(input_path: str, threshold: float = 30.0) -> List[Tuple[int, float]]:
    """
    Detect scene changes in video using HSV color histogram differences.
    Returns list of (frame_index, scene_change_score).
    """
    scene_cuts = []
    prev_hist = None

    with VideoReader(input_path) as reader:
        for idx, frame in enumerate(reader):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)

            if prev_hist is not None:
                score = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA) * 100.0
                if score > threshold:
                    scene_cuts.append((idx, score))
            prev_hist = hist

    return scene_cuts
