# EnhanceX Compatibility Report (v1.0.0)

---

## 1. Operating Systems & Hardware Platforms

| Platform | Arch | Python Versions | C++ Compiler | CUDA Toolkit | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Windows 10/11** | x86_64 | 3.8 - 3.12 | MSVC 2019/2022 | 11.8 / 12.1 / 12.4 | ✅ Fully Compatible |
| **Ubuntu / Debian Linux** | x86_64 / aarch64 | 3.8 - 3.12 | GCC 10+ / Clang 12+ | 11.8 / 12.1 / 12.4 | ✅ Fully Compatible |
| **macOS (Apple Silicon)** | arm64 | 3.9 - 3.12 | Apple Clang 13+ | MPS / CPU Fallback | ✅ Fully Compatible |

---

## 2. Deep Learning & Computer Vision Runtime Backends

| Framework / Runtime | Minimum Version | Recommended Version | Execution Mode |
| :--- | :--- | :--- | :--- |
| **PyTorch** | 2.0.0 | 2.3.0+ | CUDA / CPU / MPS |
| **ONNX Runtime** | 1.14.0 | 1.18.0+ | CUDAExecutionProvider / CPUExecutionProvider |
| **OpenCV (opencv-python)** | 4.6.0 | 4.10.0+ | Core Image & Video Processing |
| **PyQt6 / PySide6** | 6.2.0 | 6.7.0+ | EnhanceX Studio Desktop UI |
| **FastAPI / Uvicorn** | 0.95.0 | 0.111.0+ | Enterprise REST API Server |
| **gRPC (grpcio)** | 1.50.0 | 1.64.0+ | High-Throughput Remote RPC |
