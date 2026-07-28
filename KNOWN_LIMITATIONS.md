# EnhanceX Known Limitations

1. **CPU Inference Latency:** Large super-resolution models (e.g. SwinIR 4x) running on CPU may take several seconds per megapixel. CUDA acceleration is strongly recommended for real-time video inference.
2. **PyTorch Optional Dependency:** In environments without PyTorch pre-installed, EnhanceX uses high-speed OpenCV digital signal processing algorithms as fallback.
