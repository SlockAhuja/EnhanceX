# Changelog

All notable changes to the EnhanceX project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-25

### Added
- **C++ Engine**: Modern C++20 framework with `GPUManager`, `ModelManager`, `ImageEnhancer`, `VideoEnhancer`, `FrameInterpolator`, and `Stabilizer`.
- **CUDA Kernels**: 2D Laplacian Sharpening kernel and Spatial Bilateral Denoising CUDA kernel (`cpp/src/gpu/cuda_kernels.cu`).
- **Python API**: High-level classes (`VideoEnhancer`, `ImageEnhancer`, `Stabilizer`, `FrameInterpolator`, `SuperResolutionEngine`).
- **CLI Utility**: Command line tool supporting `enhance`, `stabilize`, `upscale`, `interpolate`, and `live`.
- **AI Acceleration Engine**: Tile-Inference engine supporting Real-ESRGAN, EDSR, SRCNN, and RIFE frame interpolation with ONNX Runtime, PyTorch, TensorRT, and CPU Fallback.
- **Security Hardening**: Path traversal protection across all file I/O operations and model weight loading.
- **Packaging & CI**: Full multi-stage `Dockerfile`, `environment.yml`, `requirements.txt`, and GitHub Actions workflow.
