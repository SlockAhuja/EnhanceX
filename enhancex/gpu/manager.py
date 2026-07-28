from typing import Dict, Any, Optional
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.GPU")


class GPUManager:
    """Manages GPU devices, streams, memory allocation, and CPU fallback states."""

    _instance: Optional['GPUManager'] = None

    def __init__(self, preferred_device: str = "auto"):
        self.device_type = self._detect_device(preferred_device)
        self.stream_pool = []
        logger.info(f"GPUManager initialized on active device: {self.device_type}")

    @classmethod
    def get_instance(cls, preferred_device: str = "auto") -> 'GPUManager':
        if cls._instance is None:
            cls._instance = GPUManager(preferred_device)
        return cls._instance

    def _detect_device(self, preferred: str) -> str:
        if preferred == "cpu":
            return "cpu"

        # Check PyTorch CUDA availability
        try:
            import torch
            if torch.cuda.is_available():
                return f"cuda:{torch.cuda.current_device()}"
        except ImportError:
            pass

        # Check CuPy availability
        try:
            import cupy
            return "cuda:0"
        except ImportError:
            pass

        return "cpu"

    def is_cuda_available(self) -> bool:
        return self.device_type.startswith("cuda")

    def get_device_info(self) -> Dict[str, Any]:
        info = {
            "device": self.device_type,
            "is_cuda": self.is_cuda_available(),
            "name": "CPU Fallback Engine"
        }
        if self.is_cuda_available():
            try:
                import torch
                dev_id = torch.cuda.current_device()
                info["name"] = torch.cuda.get_device_name(dev_id)
                info["memory_allocated_mb"] = torch.cuda.memory_allocated(dev_id) / (1024 * 1024)
                info["memory_total_mb"] = torch.cuda.get_device_properties(dev_id).total_memory / (1024 * 1024)
            except Exception:
                info["name"] = "NVIDIA CUDA GPU"
        return info

    def synchronize(self) -> None:
        if self.is_cuda_available():
            try:
                import torch
                torch.cuda.synchronize()
            except Exception:
                pass

