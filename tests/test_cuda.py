import pytest
from enhancex.gpu.manager import GPUManager


def test_gpu_manager_singleton():
    mgr1 = GPUManager.get_instance()
    mgr2 = GPUManager.get_instance()
    assert mgr1 is mgr2


def test_gpu_manager_info():
    mgr = GPUManager.get_instance()
    info = mgr.get_device_info()
    assert "device" in info
    assert "is_cuda" in info
    assert "name" in info


def test_gpu_manager_synchronize():
    mgr = GPUManager.get_instance()
    mgr.synchronize()
