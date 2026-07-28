# EnhanceX User Guide (v2.0.0)

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. Introduction

EnhanceX v2.0.0 is a universal AI-powered media enhancement platform. It handles image super-resolution, video stabilization, frame interpolation, audio denoise, document binarization/deskew, medical imagery contrast, and satellite image sharpening.

## 2. Operating Modes

### Auto Mode (Adaptive AAE)
Auto Mode utilizes the **Adaptive AI Enhancement Engine (AAE)** to automatically analyze input images and videos:
- **Category Detection:** Detects `Portrait`, `Landscape`, `Anime`, `Document`, `Night`, `Medical`, `Satellite`, `Artwork`, `Screenshot`.
- **Defect Detection:** Detects `Blur`, `Noise`, `Compression`, `Low Res`, `Scratches`, `Color Imbalance`, `Motion Blur`, `Low Light`.
- **Pipeline Execution:** Builds and executes only necessary processing stages.

```python
from enhancex import ImageEnhancer

enhancer = ImageEnhancer(mode="auto")
out = enhancer.enhance("sample.jpg", "enhanced.jpg")
```

### Research / Manual Mode
Allows explicit model selection for benchmarking, academic research, and reproducibility:
```python
enhancer = ImageEnhancer(mode="manual", model="RealESRGAN")
out = enhancer.enhance("sample.jpg", "upscaled.jpg")
```

## 3. Model Management

Manage official weights and local models via CLI:
```bash
enhancex models list
enhancex models install RealESRGAN
enhancex models verify
```
