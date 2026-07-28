# PACKAGE_ARCHITECTURE.md: EnhanceX Modular Ecosystem Specification

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. Modular Subpackage Strategy

EnhanceX is structured to support both monolithic installations (`pip install enhancex`) and lightweight domain-specific subpackages.

```text
packages/
├── enhancex-core/        # Minimal system config, logger, scheduler, cache
├── enhancex-image/       # Image processing algorithms & CLAHE pipeline
├── enhancex-video/       # Video reader/writer, stabilization, scene detection
├── enhancex-audio/       # Spectral noise suppression & peak gain normalization
├── enhancex-document/    # Binarization, deskew, shadow removal
├── enhancex-anime/       # Line-art preservation, anime super resolution
├── enhancex-medical/     # DICOM tissue contrast CLAHE & denoise
├── enhancex-satellite/   # Dark Channel Prior haze removal & spectral sharpening
├── enhancex-face/        # GFPGAN & CodeFormer restoration wrapper
├── enhancex-studio/      # Desktop Qt6 / PySide GUI
├── enhancex-server/      # FastAPI REST server & gRPC server
├── enhancex-sdk/         # Enterprise batch queue client & async streaming SDK
└── enhancex-cuda/        # Pybind11 C++ & CUDA acceleration kernels
```

---

## 2. Namespace & Dependency Isolation

Each domain module is isolated under the `enhancex.<domain>` namespace:
```python
import enhancex.image
import enhancex.video
import enhancex.audio
import enhancex.document
import enhancex.anime
import enhancex.medical
import enhancex.satellite
import enhancex.face
```
Subpackages import shared utilities from `enhancex.core` and `enhancex.gpu` without cyclic dependencies.
