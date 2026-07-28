# EnhanceX Migration & Upgrade Guide

## Upgrading from v1.0.0 to Next Gen (v1.1.0 - v2.0.0)

EnhanceX maintains **100% backward compatibility** with all v1.0.0 Python APIs and CLI flags.

### 1. New Features Migration

#### Automatic Adaptive Mode (Default)
In v1.0.0, manual parameters were required. In v1.1.0+, Auto Mode is enabled by default:
```python
from enhancex import ImageEnhancer

# Automatically analyzes input category and quality defects
enhancer = ImageEnhancer(mode="auto")
out = enhancer.enhance("input.jpg", "output.jpg")
```

#### Manual / Research Mode
To specify exact model weights for research or benchmarking:
```python
enhancer = ImageEnhancer(mode="manual", model="GFPGAN")
out = enhancer.enhance("input.jpg", "output.jpg")
```

### 2. Modular Installations
If you only need specific functionality (e.g. document processing or audio denoise), install subpackages:
```bash
pip install enhancex-document
pip install enhancex-audio
```
