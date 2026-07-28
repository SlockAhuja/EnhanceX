import cv2
import numpy as np
from typing import Optional, Dict, Any, Union
from enhancex.core.logger import get_logger
from enhancex.core.config import ConfigManager
from enhancex.image.pipeline import ImagePipeline
from enhancex.video.io import VideoReader, VideoWriter
from enhancex.video.stabilization import VideoStabilizer
from enhancex.ai.super_resolution import SuperResolutionEngine
from enhancex.ai.interpolation import FrameInterpolatorEngine
from enhancex.ai.denoise import AIDenoiseEngine
from enhancex.ai.enhancements import FaceEnhancer, HDREnhancer

logger = get_logger("EnhanceX.API")


class ImageEnhancer:
    """High-level Python API for Image Enhancement."""

    def __init__(self, device: str = "auto", config_path: Optional[str] = None):
        self.config = ConfigManager.get_instance(config_path)
        self.pipeline = ImagePipeline(self.config.get("image", {}))
        self.face_enhancer = FaceEnhancer()
        self.hdr_enhancer = HDREnhancer()

    def enhance(
        self,
        image_input: Union[str, np.ndarray],
        output_path: Optional[str] = None,
        sharpen: float = 1.0,
        denoise: float = 0.0,
        clahe: bool = True,
        white_balance: bool = True,
        face_enhance: bool = False,
        hdr: bool = False
    ) -> np.ndarray:
        if isinstance(image_input, str):
            image = cv2.imread(image_input)
            if image is None:
                raise FileNotFoundError(f"Image not found at {image_input}")
        else:
            image = image_input

        out = self.pipeline.process(
            image,
            use_clahe=clahe,
            use_white_balance=white_balance,
            sharpen_strength=sharpen,
            denoise_strength=denoise
        )

        if face_enhance:
            out = self.face_enhancer.enhance(out)

        if hdr:
            out = self.hdr_enhancer.enhance(out)

        if output_path and isinstance(image_input, str):
            cv2.imwrite(output_path, out)

        return out


class Stabilizer:
    """High-level Python API for Video Stabilization."""

    def __init__(self, smoothing_radius: int = 30, border_mode: str = "reflect"):
        self.stabilizer_engine = VideoStabilizer(
            smoothing_radius=smoothing_radius,
            border_mode=border_mode
        )

    def process(self, input_path: str, output_path: str) -> str:
        return self.stabilizer_engine.stabilize(input_path, output_path)


class FrameInterpolator:
    """High-level Python API for Frame Interpolation."""

    def __init__(self, engine: str = "rife", device: str = "auto"):
        self.interpolator = FrameInterpolatorEngine(engine=engine, device=device)

    def process_video(self, input_path: str, output_path: str, target_fps: float = 60.0) -> str:
        with VideoReader(input_path) as reader:
            src_fps = reader.fps
            width, height = reader.width, reader.height
            frames = list(reader)

        if len(frames) < 2:
            raise ValueError("Video has insufficient frames for interpolation.")

        multiplier = max(1, int(round(target_fps / src_fps)))

        with VideoWriter(output_path, target_fps, (width, height)) as writer:
            for i in range(len(frames) - 1):
                writer.write(frames[i])
                if multiplier > 1:
                    interp_frames = self.interpolator.interpolate_frames(frames[i], frames[i + 1], num_intermediate=multiplier - 1)
                    for frame_idx in range(1, len(interp_frames)):
                        writer.write(interp_frames[frame_idx])
            writer.write(frames[-1])

        return output_path


class VideoEnhancer:
    """
    Universal High-Level Python API for Video Enhancement.
    Provides stabilize(), upscale(), denoise(), and interpolate() methods.
    """

    def __init__(self, device: str = "auto", backend: str = "auto", config_path: Optional[str] = None):
        self.device = device
        self.backend = backend
        self.config = ConfigManager.get_instance(config_path)
        self.image_enhancer = ImageEnhancer(device=device, config_path=config_path)

    def enhance(
        self,
        input_path: str,
        output_path: str,
        sharpen: float = 1.0,
        denoise: float = 0.0,
        clahe: bool = False,
        white_balance: bool = False,
        face_enhance: bool = False,
        hdr: bool = False
    ) -> str:
        with VideoReader(input_path) as reader:
            fps = reader.fps
            width, height = reader.width, reader.height

            with VideoWriter(output_path, fps, (width, height)) as writer:
                for frame in reader:
                    enhanced = self.image_enhancer.enhance(
                        frame,
                        sharpen=sharpen,
                        denoise=denoise,
                        clahe=clahe,
                        white_balance=white_balance,
                        face_enhance=face_enhance,
                        hdr=hdr
                    )
                    writer.write(enhanced)
        return output_path

    def stabilize(self, input_path: str, output_path: str, smoothing_radius: int = 30, border_mode: str = "reflect") -> str:
        stabilizer = Stabilizer(smoothing_radius=smoothing_radius, border_mode=border_mode)
        return stabilizer.process(input_path, output_path)

    def upscale(
        self,
        input_path: str,
        output_path: str,
        model_name: str = "real-esrgan",
        scale: int = 4,
        tile_size: int = 512
    ) -> str:
        sr_engine = SuperResolutionEngine(
            model_name=model_name,
            scale=scale,
            device=self.device,
            backend=self.backend,
            tile_size=tile_size
        )

        with VideoReader(input_path) as reader:
            fps = reader.fps
            target_w = reader.width * scale
            target_h = reader.height * scale

            with VideoWriter(output_path, fps, (target_w, target_h)) as writer:
                for frame in reader:
                    upscaled = sr_engine.upscale(frame)
                    writer.write(upscaled)

        return output_path

    def denoise(self, input_path: str, output_path: str, method: str = "fastnl", strength: float = 10.0) -> str:
        denoise_engine = AIDenoiseEngine(method=method, strength=strength)
        with VideoReader(input_path) as reader:
            fps = reader.fps
            width, height = reader.width, reader.height

            with VideoWriter(output_path, fps, (width, height)) as writer:
                frames_buffer = []
                for frame in reader:
                    frames_buffer.append(frame)
                    if len(frames_buffer) >= 10:
                        denoised_batch = denoise_engine.denoise_sequence(frames_buffer)
                        for d_frame in denoised_batch:
                            writer.write(d_frame)
                        frames_buffer = []

                if frames_buffer:
                    denoised_batch = denoise_engine.denoise_sequence(frames_buffer)
                    for d_frame in denoised_batch:
                        writer.write(d_frame)

        return output_path

    def interpolate(self, input_path: str, output_path: str, target_fps: float = 60.0, engine: str = "rife") -> str:
        interpolator = FrameInterpolator(engine=engine, device=self.device)
        return interpolator.process_video(input_path, output_path, target_fps=target_fps)
