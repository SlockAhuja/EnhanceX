import pytest
import numpy as np
from enhancex.ai.model_loader import ModelLoader
from enhancex.ai.inference import InferenceEngine
from enhancex.ai.super_resolution import SuperResolutionEngine
from enhancex.ai.interpolation import FrameInterpolatorEngine
from enhancex.ai.denoise import AIDenoiseEngine
from enhancex.ai.enhancements import FaceEnhancer, HDREnhancer


def test_model_loader():
    loader = ModelLoader()
    path = loader.get_model_path("real-esrgan")
    assert path is not None


def test_inference_engine():
    engine = InferenceEngine(device="cpu")
    dummy_input = np.ones((1, 3, 64, 64), dtype=np.float32)
    output = engine.predict(dummy_input)
    assert output is not None


def test_super_resolution(sample_image):
    sr = SuperResolutionEngine(model_name="real-esrgan", scale=2, device="cpu", tile_size=128)
    upscaled = sr.upscale(sample_image)
    assert upscaled.shape == (512, 512, 3)


def test_frame_interpolation(sample_image):
    engine = FrameInterpolatorEngine(device="cpu")
    frames = engine.interpolate_frames(sample_image, sample_image, num_intermediate=2)
    assert len(frames) == 3


def test_ai_denoise(sample_image):
    ai_denoise = AIDenoiseEngine(strength=5.0)
    res = ai_denoise.denoise_frame(sample_image)
    assert res.shape == sample_image.shape
    seq_res = ai_denoise.denoise_sequence([sample_image, sample_image, sample_image])
    assert len(seq_res) == 3


def test_enhancements(sample_image):
    face = FaceEnhancer()
    f_res = face.enhance(sample_image)
    assert f_res.shape == sample_image.shape

    hdr = HDREnhancer()
    hdr_res = hdr.enhance(sample_image)
    assert hdr_res.shape == sample_image.shape
