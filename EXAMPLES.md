# EnhanceX Practical Code Examples (v2.0.0)

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. Automated Document Binarization & Deskew

```python
from enhancex.document import DocumentPipeline
import cv2

pipeline = DocumentPipeline()
doc_img = cv2.imread("scanned_doc.jpg")

cleaned_doc = pipeline.process(
    doc_img,
    binarize=True,
    deskew=True,
    remove_shadows=True
)

cv2.imwrite("cleaned_doc.jpg", cleaned_doc)
```

## 2. Audio Spectral Denoise & Gain Normalization

```python
from enhancex.audio import AudioPipeline
import numpy as np

audio_pipeline = AudioPipeline(sample_rate=44100)
pcm = np.random.randint(-10000, 10000, 44100, dtype=np.int16)

denoised_pcm = audio_pipeline.denoise_audio(pcm)
normalized_pcm = audio_pipeline.normalize_gain(denoised_pcm, target_dbfs=-3.0)
```

## 3. Satellite Haze Removal & Detail Sharpening

```python
from enhancex.satellite import SatellitePipeline
import cv2

sat_pipeline = SatellitePipeline()
aerial_img = cv2.imread("satellite.tif")

enhanced_sat = sat_pipeline.process(aerial_img, remove_haze=True, sharpen_strength=1.5)
cv2.imwrite("satellite_enhanced.png", enhanced_sat)
```
