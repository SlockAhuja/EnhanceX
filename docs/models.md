# EnhanceX Deep Learning Model Zoo Documentation

EnhanceX integrates neural network architectures for Super Resolution, Frame Interpolation, Face Restoration, and Image/Video Denoising. Pre-trained model weights are automatically downloaded on first use and cached locally in `~/.cache/enhancex/models`.

---

## 🧬 Integrated Neural Architectures

### 1. Real-ESRGAN (RRDBNet)
- **Task**: Real-World AI Super Resolution & Upscaling (4x / 8x).
- **Architecture**: Residual-in-Residual Dense Block Network (`RRDBNet`).
- **File**: [`enhancex/ai/architectures/rrdbnet.py`](file:///c:/Users/OM/OneDrive/Desktop/AI_Brain_Presentation/enhancex/enhancex/ai/architectures/rrdbnet.py)
- **Pretrained Weights**: `RealESRGAN_x4plus.pth`
- **Supported Backends**: PyTorch, ONNX Runtime, TensorRT, CPU Fallback.
- **Memory Protection**: Integrated with EnhanceX Tile-Inference engine to handle 4K/8K media without GPU out-of-memory.

### 2. RIFE (IFNet)
- **Task**: Real-Time Intermediate Flow Estimation for Neural Frame Interpolation (24 -> 60/120 FPS).
- **Architecture**: Multi-scale Intermediate Flow Network (`IFNet`).
- **File**: [`enhancex/ai/architectures/rife_net.py`](file:///c:/Users/OM/OneDrive/Desktop/AI_Brain_Presentation/enhancex/enhancex/ai/architectures/rife_net.py)
- **Pretrained Weights**: `rife_v4.6.pth`
- **Supported Backends**: PyTorch, ONNX Runtime, CPU Fallback.

### 3. GFPGAN (GFPGANv1Clean)
- **Task**: Generative Facial Prior GAN for Face Restoration & Artifact Removal.
- **Architecture**: StyleGAN2-based facial generator with spatial feature transform (`GFPGANv1Clean`).
- **File**: [`enhancex/ai/architectures/gfpgan_net.py`](file:///c:/Users/OM/OneDrive/Desktop/AI_Brain_Presentation/enhancex/enhancex/ai/architectures/gfpgan_net.py)
- **Pretrained Weights**: `GFPGANv1.3.pth`
- **Supported Backends**: PyTorch, ONNX Runtime, CPU Fallback.

### 4. CodeFormer (CodeFormerNet)
- **Task**: Vector-Quantized Transformer for Blind Face Restoration.
- **Architecture**: Transformer codebook dictionary network (`CodeFormerNet`).
- **File**: [`enhancex/ai/architectures/codeformer_net.py`](file:///c:/Users/OM/OneDrive/Desktop/AI_Brain_Presentation/enhancex/enhancex/ai/architectures/codeformer_net.py)
- **Pretrained Weights**: `codeformer.pth`
- **Supported Backends**: PyTorch, ONNX Runtime, CPU Fallback.

### 5. BasicSR (BasicSRNet)
- **Task**: General Residual Super-Resolution & Video Restoration backbone.
- **Architecture**: Deep Residual Convolutional Block Network (`BasicSRNet`).
- **File**: [`enhancex/ai/architectures/basicsr_net.py`](file:///c:/Users/OM/OneDrive/Desktop/AI_Brain_Presentation/enhancex/enhancex/ai/architectures/basicsr_net.py)
- **Pretrained Weights**: `BasicSR_restoration.pth`
- **Supported Backends**: PyTorch, ONNX Runtime, CPU Fallback.

---

## 🛠️ Usage Example

```python
from enhancex.ai import ModelLoader

loader = ModelLoader()
# Automatically downloads & caches pretrained weights on first call
model_path = loader.get_model_path("real-esrgan", auto_download=True)
print(f"Model weight cached at: {model_path}")
```
