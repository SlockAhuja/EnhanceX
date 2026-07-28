"""
EnhanceX Exception Hierarchy.
Provides clear, structured, domain-specific exception types for error handling and reporting.
"""

class EnhanceXError(Exception):
    """Base exception for all errors raised by the EnhanceX framework."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ModelNotFoundError(EnhanceXError):
    """Raised when a requested AI model or weight file cannot be located or downloaded."""
    pass


class ModelLoadError(EnhanceXError):
    """Raised when model weights fail to deserialize or load into network state dict."""
    pass


class InferenceError(EnhanceXError):
    """Raised when tensor inference fails during execution across PyTorch, ONNX, or TensorRT."""
    pass


class CUDAError(EnhanceXError):
    """Raised when CUDA device initialization, stream management, or kernel launch fails."""
    pass


class VideoIOError(EnhanceXError):
    """Raised when reading, decoding, or encoding video streams encounters an I/O failure."""
    pass


class SecurityError(EnhanceXError):
    """Raised when path traversal, invalid paths, or insecure subprocess calls are detected."""
    pass


class ValidationError(EnhanceXError):
    """Raised when input parameters, frame shapes, or config options violate validation bounds."""
    pass
