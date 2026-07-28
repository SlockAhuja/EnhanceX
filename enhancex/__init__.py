"""
EnhanceX: Universal AI-Powered Image & Video Enhancement Framework
Created by Slock Ahuja
GitHub: https://github.com/SlockAhuja/EnhanceX
"""

__version__ = "2.0.0"
__author__ = "Slock Ahuja"

from enhancex.api.high_level import (
    VideoEnhancer,
    ImageEnhancer,
    Stabilizer,
    FrameInterpolator,
    SuperResolutionEngine
)
from enhancex.core.config import ConfigManager
from enhancex.core.logger import get_logger

__all__ = [
    "VideoEnhancer",
    "ImageEnhancer",
    "Stabilizer",
    "FrameInterpolator",
    "SuperResolutionEngine",
    "ConfigManager",
    "get_logger"
]
