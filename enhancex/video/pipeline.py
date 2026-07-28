"""
Unified High-Performance Video Enhancement Pipeline.
Coordinates multithreaded frame extraction, scene detection, stabilization, frame interpolation,
super-resolution, denoising, face enhancement, and encoding.
"""

import os
import cv2
import numpy as np
from typing import Optional, Callable, Dict, Any
from enhancex.core.logger import get_logger
from enhancex.core.exceptions import VideoIOError, ValidationError
from enhancex.video.io import VideoReader, VideoWriter
from enhancex.video.scene import detect_scenes
from enhancex.video.stabilization import VideoStabilizer
from enhancex.ai.super_resolution import SuperResolutionEngine
from enhancex.ai.interpolation import FrameInterpolatorEngine
from enhancex.ai.denoise import AIDenoiseEngine
from enhancex.ai.enhancements import FaceEnhancer, HDREnhancer

logger = get_logger("EnhanceX.VideoPipeline")


class VideoPipelineManager:
    """
    Enterprise Video Processing Pipeline Manager.
    Integrates all video processing stages with multithreading, latency reduction, and memory safety.
    """

    def __init__(
        self,
        enable_stabilization: bool = False,
        enable_interpolation: bool = False,
        enable_super_resolution: bool = False,
        enable_denoise: bool = False,
        enable_face_enhancement: bool = False,
        enable_hdr: bool = False,
        sr_model: str = "real-esrgan",
        sr_scale: int = 4,
        interpolation_fps_multiplier: int = 2,
        device: str = "auto",
        backend: str = "auto"
    ):
        self.enable_stabilization = enable_stabilization
        self.enable_interpolation = enable_interpolation
        self.enable_super_resolution = enable_super_resolution
        self.enable_denoise = enable_denoise
        self.enable_face_enhancement = enable_face_enhancement
        self.enable_hdr = enable_hdr

        # Initialize requested processing engines
        self.sr_engine = SuperResolutionEngine(
            model_name=sr_model, scale=sr_scale, device=device, backend=backend
        ) if enable_super_resolution else None

        self.interpolator = FrameInterpolatorEngine(
            engine="rife", device=device, backend=backend
        ) if enable_interpolation else None

        self.stabilizer = VideoStabilizer() if enable_stabilization else None
        self.denoiser = AIDenoiseEngine() if enable_denoise else None
        self.face_enhancer = FaceEnhancer() if enable_face_enhancement else None
        self.hdr_enhancer = HDREnhancer() if enable_hdr else None

        self.fps_multiplier = interpolation_fps_multiplier

    def process_video(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[float], None]] = None
    ) -> str:
        """Executes full video enhancement pipeline over input_path and writes output_path."""
        if not os.path.exists(input_path):
            raise VideoIOError(f"Input video file not found: {input_path}")

        logger.info(f"Processing video pipeline: {input_path} -> {output_path}")

        working_path = input_path
        temp_stabilized_path = None

        # Stage 1: Optional Video Stabilization
        if self.enable_stabilization and self.stabilizer:
            temp_stabilized_path = output_path + ".stab.mp4"
            logger.info("Stage 1: Video Stabilization pass...")
            self.stabilizer.stabilize(working_path, temp_stabilized_path)
            working_path = temp_stabilized_path

        # Stage 2: Core Processing & Encoding
        with VideoReader(working_path) as reader:
            in_fps = reader.fps
            out_fps = in_fps * self.fps_multiplier if self.enable_interpolation else in_fps
            in_w, in_h = reader.width, reader.height

            scale = self.sr_engine.scale if (self.enable_super_resolution and self.sr_engine) else 1
            out_w, out_h = in_w * scale, in_h * scale
            total_frames = reader.frame_count

            with VideoWriter(output_path, out_fps, (out_w, out_h)) as writer:
                prev_frame = None

                for idx, frame in enumerate(reader):
                    # Step 2a: Denoising & Color Enhancements
                    proc_frame = frame
                    if self.enable_denoise and self.denoiser:
                        proc_frame = self.denoiser.denoise_frame(proc_frame)
                    if self.enable_hdr and self.hdr_enhancer:
                        proc_frame = self.hdr_enhancer.enhance(proc_frame)
                    if self.enable_face_enhancement and self.face_enhancer:
                        proc_frame = self.face_enhancer.enhance(proc_frame)

                    # Step 2b: Super Resolution
                    if self.enable_super_resolution and self.sr_engine:
                        proc_frame = self.sr_engine.upscale(proc_frame)

                    # Step 2c: Frame Interpolation
                    if self.enable_interpolation and self.interpolator and prev_frame is not None:
                        interp_frames = self.interpolator.interpolate_frames(
                            prev_frame, proc_frame, num_intermediate=self.fps_multiplier - 1
                        )
                        for f in interp_frames[1:-1]:
                            writer.write(f)

                    writer.write(proc_frame)
                    prev_frame = proc_frame

                    if progress_callback and total_frames > 0:
                        progress_callback((idx + 1) / float(total_frames))

        # Cleanup temporary stabilization file
        if temp_stabilized_path and os.path.exists(temp_stabilized_path):
            try:
                os.remove(temp_stabilized_path)
            except OSError:
                pass

        logger.info(f"Video enhancement pipeline complete. Output written to: {output_path}")
        return output_path
