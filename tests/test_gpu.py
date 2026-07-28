import pytest
from enhancex.gpu.manager import GPUManager


def test_gpu_manager_fallback():
    gpu = GPUManager.get_instance(preferred_device="cpu")
    assert gpu.device_type == "cpu"
    assert not gpu.is_cuda_available()
    info = gpu.get_device_info()
    assert "device" in info
    assert info["is_cuda"] is False
