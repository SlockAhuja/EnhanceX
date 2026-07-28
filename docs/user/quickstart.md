# EnhanceX Quick Start Guide

## 1. CLI Quick Start

### Auto Mode (Adaptive AI Enhancement Engine)
```bash
enhancex enhance input.jpg output_enhanced.jpg --mode auto
```

### Research Mode (Explicit Model Selection)
```bash
enhancex enhance input.jpg output_gfpgan.jpg --mode manual --model GFPGAN
```

### System Diagnostics
```bash
enhancex doctor
enhancex info
enhancex version
```

### Model Management
```bash
enhancex models list
enhancex models install RealESRGAN
enhancex models verify
```

## 2. Python API Quick Start

```python
from enhancex import ImageEnhancer

# Initialize in Auto Mode (Adaptive AAE Engine)
enhancer = ImageEnhancer(mode="auto")

# Process image automatically
enhanced_img = enhancer.enhance("sample.jpg", output_path="enhanced.jpg")
print(f"AAE Detection Metrics: {enhancer.last_metrics}")
```
