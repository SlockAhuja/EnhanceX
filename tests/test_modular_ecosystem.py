import pytest
import numpy as np
from enhancex.audio import AudioPipeline
from enhancex.document import DocumentPipeline
from enhancex.anime import AnimePipeline
from enhancex.medical import MedicalPipeline
from enhancex.satellite import SatellitePipeline
from enhancex.face import FacialRestorationPipeline


def test_audio_pipeline():
    pipeline = AudioPipeline()
    pcm = np.random.randint(-10000, 10000, 44100, dtype=np.int16)
    denoised = pipeline.denoise_audio(pcm)
    assert denoised.shape == pcm.shape

    normalized = pipeline.normalize_gain(pcm)
    assert normalized.shape == pcm.shape


def test_document_pipeline():
    pipeline = DocumentPipeline()
    img = np.ones((400, 400, 3), dtype=np.uint8) * 200
    res = pipeline.process(img, binarize=True, deskew=True, remove_shadows=True)
    assert res.shape == img.shape


def test_anime_pipeline():
    pipeline = AnimePipeline()
    img = np.ones((200, 200, 3), dtype=np.uint8) * 150
    res = pipeline.process(img, scale=2)
    assert res.shape == (400, 400, 3)


def test_medical_pipeline():
    pipeline = MedicalPipeline()
    img = np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8)
    res = pipeline.process(img)
    assert res.shape == img.shape


def test_satellite_pipeline():
    pipeline = SatellitePipeline()
    img = np.random.randint(50, 200, (200, 200, 3), dtype=np.uint8)
    res = pipeline.process(img)
    assert res.shape == img.shape


def test_face_pipeline():
    pipeline = FacialRestorationPipeline()
    img = np.ones((200, 200, 3), dtype=np.uint8) * 128
    res = pipeline.process(img)
    assert res.shape == img.shape
