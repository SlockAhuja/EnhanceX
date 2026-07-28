import os
import pytest
from enhancex.video.io import _sanitize_path, VideoReader, VideoWriter
from enhancex.ai.model_loader import ModelLoader
from enhancex.core.exceptions import SecurityError, ValidationError


def test_path_sanitization():
    clean = _sanitize_path("tests/../tests/test_ai.py")
    assert os.path.exists(clean)


def test_invalid_model_names():
    loader = ModelLoader()
    with pytest.raises(ValidationError):
        loader.get_model_path("")

    with pytest.raises(ValidationError):
        loader.get_model_path("../../../etc/passwd")


def test_video_reader_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        VideoReader("non_existent_file_12345.mp4")
