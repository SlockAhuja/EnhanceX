# EnhanceX

[![Release](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/SlockAhuja/EnhanceX)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](pyproject.toml)
[![CUDA](https://img.shields.io/badge/CUDA-11.8%20%7C%2012.x-nvidia)](https://developer.nvidia.com/cuda-toolkit)
[![Build Status](https://img.shields.io/badge/tests-48%2F48%20passing-success)](https://github.com/SlockAhuja/EnhanceX)

**Universal AI-Powered Media Enhancement Platform**  
*Created by [Slock Ahuja](https://github.com/SlockAhuja/EnhanceX)*  
GitHub Repository: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 🌟 Overview

**EnhanceX v2.0.0** is an enterprise-grade modular AI media enhancement platform designed for automated, high-throughput image, video, audio, and document processing.

Powered by the **Adaptive AI Enhancement Engine (AAE)**, EnhanceX automatically analyzes input media, detects quality defects (blur, noise, compression artifacts, low resolution, color imbalance, low light), and constructs optimal execution pipelines.

```text
========================================================

                EnhanceX v2.0.0

========================================================

Thank you for installing EnhanceX!

Created by: Slock Ahuja
GitHub: https://github.com/SlockAhuja/EnhanceX
```

---

## 🏗️ Platform Architecture

```
                  +-----------------------------------+
                  |   EnhanceX CLI & Desktop Studio   |
                  +-----------------------------------+
                                    |
                  +-----------------------------------+
                  |         High-Level Python API     |
                  +-----------------------------------+
                                    |
         +--------------------------+--------------------------+
         |                                                     |
+-------------------+                                 +------------------+
|  Adaptive AI      |                                 | Model Registry   |
|  Engine (AAE)     |                                 | & Manager        |
+-------------------+                                 +------------------+
         |                                                     |
         +--------------------------+--------------------------+
                                    |
   +--------------------------------+--------------------------------+
   |                                                                 |
+------------------------------------+             +----------------------------------+
| Domain Ecosystem Subpackages       |             | Enterprise SDK & Remote Server   |
| (Image, Video, Audio, Document,    |             | (FastAPI, gRPC, Prometheus)      |
|  Anime, Medical, Satellite, Face)  |             |                                  |
+------------------------------------+             +----------------------------------+
                                    |
                  +-----------------------------------+
                  |     CUDA / C++ Acceleration Core  |
                  +-----------------------------------+
```

---

## 📦 Installation

### Complete Distribution
```bash
pip install git+https://github.com/SlockAhuja/EnhanceX.git
```

### Domain Subpackage Installations
Install only required components:
```bash
pip install enhancex-image
pip install enhancex-video
pip install enhancex-audio
pip install enhancex-document
pip install enhancex-anime
pip install enhancex-medical
```

---

## 🚀 Quick Start

### 1. Python API

#### Auto Mode (Adaptive AAE Engine)
```python
from enhancex import ImageEnhancer

# Initialize in Auto Mode
enhancer = ImageEnhancer(mode="auto")

# Enhance image with automated category detection & defect repair
enhanced_image = enhancer.enhance("input.jpg", output_path="enhanced_output.jpg")
print("Metrics:", enhancer.last_metrics)
```

#### Research & Benchmark Mode (Manual Model Selection)
```python
# Explicit model selection for research and benchmarking
enhancer = ImageEnhancer(mode="manual", model="RealESRGAN")
enhanced_image = enhancer.enhance("input.jpg", output_path="upscaled.jpg")
```

### 2. Command Line Interface (CLI)

```bash
# System Diagnostics
enhancex doctor

# System Specs & Hardware Capabilities
enhancex info

# Version Check
enhancex version

# Auto Mode Image Enhancement
enhancex enhance input.jpg output.jpg --mode auto

# Research Mode Model Upscaling
enhancex enhance input.jpg output.jpg --mode manual --model RealESRGAN

# Model Management
enhancex models list
enhancex models install RealESRGAN
enhancex models verify
```

---

## 📖 Documentation Directory

* 📘 [User Guide](USER_GUIDE.md)
* 🛠️ [Developer Guide](DEVELOPER_GUIDE.md)
* 💡 [API Reference](API_REFERENCE.md)
* 🖥️ [CLI Guide](CLI_GUIDE.md)
* 💻 [Code Examples](EXAMPLES.md)
* ❓ [Frequently Asked Questions](FAQ.md)
* 🔄 [Migration Guide](MIGRATION_GUIDE.md)
* 📊 [Roadmap](ROADMAP.md)
* ⚡ [Compatibility Matrix](COMPATIBILITY.md)
* ⚠️ [Known Limitations](KNOWN_LIMITATIONS.md)

---

## 👥 Contribution & Security

* **Contribution Guide:** Please refer to [CONTRIBUTING.md](CONTRIBUTING.md).
* **Security Policy:** Please refer to [SECURITY.md](SECURITY.md).
* **Code of Conduct:** Please refer to [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## 🎓 Citation

If you use EnhanceX in your academic or industrial research projects, please cite:

```bibtex
@software{Ahuja_EnhanceX_2026,
  author = {Ahuja, Slock},
  title = {EnhanceX: Universal AI-Powered Image & Video Enhancement Framework},
  version = {2.0.0},
  year = {2026},
  url = {https://github.com/SlockAhuja/EnhanceX}
}
```

---

## 📄 License

EnhanceX is open-source software released under the [MIT License](LICENSE).  
Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)
