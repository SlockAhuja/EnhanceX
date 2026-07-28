# EnhanceX Developer Guide (v2.0.0)

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SlockAhuja/EnhanceX.git
   cd EnhanceX
   ```

2. **Install in editable mode with development dependencies:**
   ```bash
   pip install -e ".[dev,ai,gpu]"
   ```

3. **Run unit & integration test suite:**
   ```bash
   pytest tests/
   ```

## Package Architecture & Extension

- **`enhancex/ai/aae.py`**: Adaptive AI Enhancement Engine (category & defect detectors).
- **`enhancex/models/manager.py`**: Checksum validation and local model registry.
- **`enhancex/audio/`**, **`enhancex/document/`**, **`enhancex/anime/`**, **`enhancex/medical/`**, **`enhancex/satellite/`**, **`enhancex/face/`**: Modular subpackage implementations.
- **`enhancex/sdk/`**: Enterprise batch queue and async streaming client.
- **`enhancex/core/telemetry.py`**: Prometheus metrics exporter.

## Coding & Style Guidelines
- Format code using `black` (100 char line limit).
- Add unit tests under `tests/` for any new pipeline stage or module.
