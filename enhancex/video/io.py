import os
import cv2
import numpy as np
from typing import Generator, Tuple, Optional
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.VideoIO")


def _sanitize_path(filepath: str) -> str:
    """Sanitizes filepath preventing path traversal attacks."""
    if not isinstance(filepath, str):
        return filepath
    clean_path = os.path.realpath(os.path.abspath(filepath))
    return clean_path


class VideoReader:
    """High-performance frame iterator for video files and live camera streams."""

    def __init__(self, source: str):
        self.source = source
        self.is_stream = isinstance(source, int) or (isinstance(source, str) and source.isdigit())

        if not self.is_stream:
            self.source = _sanitize_path(str(source))
            if not os.path.exists(self.source):
                raise FileNotFoundError(f"Video file not found: {self.source}")

        self.cap = cv2.VideoCapture(int(source) if self.is_stream else self.source)
        if not self.cap.isOpened():
            raise ValueError(f"Failed to open video source: {source}")

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) if not self.is_stream else -1

    def __iter__(self) -> Generator[np.ndarray, None, None]:
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret or frame is None:
                break
            yield frame

    def read_all(self) -> list:
        return [frame for frame in self]

    def release(self) -> None:
        if self.cap:
            self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


class VideoWriter:
    """Video writer wrapper for encoding enhanced frames."""

    def __init__(self, output_path: str, fps: float, size: Tuple[int, int], codec: str = "mp4v"):
        self.output_path = _sanitize_path(output_path)
        out_dir = os.path.dirname(self.output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        self.fps = max(1.0, float(fps))
        self.size = size
        fourcc = cv2.VideoWriter_fourcc(*codec)
        self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, size)
        if not self.writer.isOpened():
            raise RuntimeError(f"Failed to initialize VideoWriter for {self.output_path}")

    def write(self, frame: np.ndarray) -> None:
        if (frame.shape[1], frame.shape[0]) != self.size:
            frame = cv2.resize(frame, self.size)
        self.writer.write(frame)

    def release(self) -> None:
        if self.writer:
            self.writer.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
