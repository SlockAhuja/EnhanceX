import pytest
from pathlib import Path
from enhancex.models.manager import ModelManager, ModelInfo


def test_model_manager_list():
    mgr = ModelManager()
    models = mgr.list_models()
    assert len(models) >= 5
    names = [m.name for m in models]
    assert "RealESRGAN" in names
    assert "GFPGAN" in names
    assert "CodeFormer" in names


def test_model_manager_install_remove_verify():
    mgr = ModelManager()
    info = mgr.install_model("RealESRGAN")
    assert info.status == "installed"
    assert Path(info.local_path).exists()

    verification = mgr.verify_models()
    assert verification.get("RealESRGAN") is True

    removed = mgr.remove_model("RealESRGAN")
    assert removed is True
    assert Path(info.local_path).exists() is False
