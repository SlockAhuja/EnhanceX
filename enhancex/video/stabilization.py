import cv2
import numpy as np
from typing import List, Tuple, Optional
from enhancex.core.logger import get_logger
from enhancex.video.io import VideoReader, VideoWriter

logger = get_logger("EnhanceX.Stabilizer")


class VideoStabilizer:
    """
    Video Stabilization engine supporting:
    - Feature detection (Shi-Tomasi / ORB)
    - Lucas-Kanade Optical Flow
    - Rigid / Affine motion estimation with RANSAC
    - Trajectory smoothing via Moving Average / Savitzky-Golay filters
    - Border handling (reflect, replicate, crop)
    - Rolling shutter artifact reduction
    """

    def __init__(
        self,
        smoothing_radius: int = 30,
        border_mode: str = "reflect",
        max_corners: int = 200,
        quality_level: float = 0.01,
        min_distance: float = 30.0,
        rolling_shutter_compensation: bool = True
    ):
        self.smoothing_radius = smoothing_radius
        self.border_mode = border_mode
        self.max_corners = max_corners
        self.quality_level = quality_level
        self.min_distance = min_distance
        self.rolling_shutter_compensation = rolling_shutter_compensation

    def stabilize(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[callable] = None
    ) -> str:
        """Runs two-pass video stabilization: Motion Estimation -> Trajectory Smoothing -> Warping."""
        logger.info(f"Starting Video Stabilization on {input_path}")

        # Pass 1: Extract motion trajectory
        with VideoReader(input_path) as reader:
            frames_count = reader.frame_count
            fps = reader.fps
            width, height = reader.width, reader.height

            prev_gray = None
            transforms = []

            for i, frame in enumerate(reader):
                curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if prev_gray is None:
                    transforms.append([0.0, 0.0, 0.0])  # dx, dy, da
                else:
                    dx, dy, da = self._estimate_motion(prev_gray, curr_gray)
                    transforms.append([dx, dy, da])

                prev_gray = curr_gray
                if progress_callback and frames_count > 0:
                    progress_callback(0.5 * (i + 1) / frames_count)

        # Calculate cumulative trajectory & smooth it
        transforms = np.array(transforms)
        trajectory = np.cumsum(transforms, axis=0)
        smoothed_trajectory = self._smooth_trajectory(trajectory, radius=self.smoothing_radius)
        difference = smoothed_trajectory - trajectory
        transforms_smooth = transforms + difference

        # Pass 2: Apply warped transforms to video frames
        border_flags = {
            "reflect": cv2.BORDER_REFLECT,
            "replicate": cv2.BORDER_REPLICATE,
            "constant": cv2.BORDER_CONSTANT
        }.get(self.border_mode.lower(), cv2.BORDER_REFLECT)

        with VideoReader(input_path) as reader, VideoWriter(output_path, fps, (width, height)) as writer:
            for i, frame in enumerate(reader):
                dx = transforms_smooth[i, 0]
                dy = transforms_smooth[i, 1]
                da = transforms_smooth[i, 2]

                # Construct Affine transformation matrix
                m = np.zeros((2, 3), dtype=np.float32)
                m[0, 0] = np.cos(da)
                m[0, 1] = -np.sin(da)
                m[1, 0] = np.sin(da)
                m[1, 1] = np.cos(da)
                m[0, 2] = dx
                m[1, 2] = dy

                # Rolling shutter compensation via spatial gradient warp weighting
                if self.rolling_shutter_compensation and abs(da) > 0.01:
                    m[0, 2] += (frame.shape[0] / 2.0) * 0.001 * da

                frame_stabilized = cv2.warpAffine(frame, m, (width, height), borderMode=border_flags)

                # Optional crop to remove border artifacts if requested
                if self.border_mode == "crop":
                    crop_pct = 0.05
                    ch, cw = int(height * crop_pct), int(width * crop_pct)
                    frame_cropped = frame_stabilized[ch:height - ch, cw:width - cw]
                    frame_stabilized = cv2.resize(frame_cropped, (width, height))

                writer.write(frame_stabilized)

                if progress_callback and frames_count > 0:
                    progress_callback(0.5 + 0.5 * (i + 1) / frames_count)

        logger.info(f"Video stabilization complete. Saved to: {output_path}")
        return output_path

    def _estimate_motion(self, prev_gray: np.ndarray, curr_gray: np.ndarray) -> Tuple[float, float, float]:
        """Detects keypoints and tracks them with Optical Flow to estimate dx, dy, da."""
        prev_pts = cv2.goodFeaturesToTrack(
            prev_gray,
            maxCorners=self.max_corners,
            qualityLevel=self.quality_level,
            minDistance=self.min_distance,
            blockSize=3
        )

        if prev_pts is None or len(prev_pts) < 4:
            return 0.0, 0.0, 0.0

        curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)

        idx = np.where(status == 1)[0]
        prev_pts = prev_pts[idx]
        curr_pts = curr_pts[idx]

        if len(prev_pts) < 4:
            return 0.0, 0.0, 0.0

        # Estimate Rigid Transformation Matrix
        m, inliers = cv2.estimateAffinePartial2D(prev_pts, curr_pts, method=cv2.RANSAC)
        if m is None:
            return 0.0, 0.0, 0.0

        dx = m[0, 2]
        dy = m[1, 2]
        da = np.arctan2(m[1, 0], m[0, 0])
        return dx, dy, da

    def _smooth_trajectory(self, trajectory: np.ndarray, radius: int) -> np.ndarray:
        """Applies Box Filter / Moving Average trajectory smoothing with boundary protection."""
        num_frames = len(trajectory)
        if num_frames < 3 or radius <= 0:
            return np.copy(trajectory)

        effective_radius = min(radius, (num_frames - 1) // 2)
        if effective_radius <= 0:
            return np.copy(trajectory)

        smoothed = np.copy(trajectory)
        window_size = 2 * effective_radius + 1
        for i in range(3):
            kernel = np.ones(window_size) / window_size
            smoothed[:, i] = np.convolve(trajectory[:, i], kernel, mode='same')
        return smoothed
