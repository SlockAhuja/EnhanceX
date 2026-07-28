"""
Video Processing & Stabilization Module: Frame IO, Stabilization, Scene Detection, Trimming.
"""

from enhancex.video.io import VideoReader, VideoWriter
from enhancex.video.stabilization import VideoStabilizer
from enhancex.video.scene import detect_scenes
from enhancex.video.trim import trim_video
from enhancex.video.pipeline import VideoPipelineManager

__all__ = [
    "VideoReader",
    "VideoWriter",
    "VideoStabilizer",
    "detect_scenes",
    "trim_video",
    "VideoPipelineManager"
]

