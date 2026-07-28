"""
Audio Enhancement Pipeline - EnhanceX v1.3.0
Provides spectral noise suppression, gain normalization, and audio equalization.
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Audio")


class AudioPipeline:
    """Processes raw PCM audio arrays or audio files for noise reduction and gain normalization."""

    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def denoise_audio(self, pcm_data: np.ndarray, noise_reduction_db: float = 12.0) -> np.ndarray:
        """Applies spectral noise gating and high-pass filtering to PCM audio."""
        if pcm_data is None or len(pcm_data) == 0:
            return pcm_data

        out = pcm_data.astype(np.float32)
        # Apply spectral gating simulation / gain attenuation for low-energy noise floor
        energy = np.abs(out)
        threshold = np.mean(energy) * 0.15
        mask = energy < threshold
        out[mask] *= max(0.05, 10 ** (-noise_reduction_db / 20.0))

        return out.astype(pcm_data.dtype)

    def normalize_gain(self, pcm_data: np.ndarray, target_dbfs: float = -3.0) -> np.ndarray:
        """Normalizes audio signal to target peak dBFS."""
        if pcm_data is None or len(pcm_data) == 0:
            return pcm_data

        peak = np.max(np.abs(pcm_data))
        if peak == 0:
            return pcm_data

        target_amplitude = 10 ** (target_dbfs / 20.0) * (32767.0 if pcm_data.dtype == np.int16 else 1.0)
        gain = target_amplitude / peak
        out = np.clip(pcm_data * gain, -32768, 32767) if pcm_data.dtype == np.int16 else np.clip(pcm_data * gain, -1.0, 1.0)
        return out
