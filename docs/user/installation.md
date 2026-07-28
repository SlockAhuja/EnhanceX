# EnhanceX Installation Guide

## System Requirements
- **OS:** Windows 10/11, Ubuntu 20.04+, macOS 12+
- **Python:** 3.8 - 3.12
- **GPU (Optional but recommended):** NVIDIA GPU with CUDA 11.8 / 12.x support

## Standard Installation via PyPI

Install the complete EnhanceX platform with all subpackages:
```bash
pip install enhancex
```

## Modular Installation (Subpackages)

Install only specific domain packages:
```bash
# Image Enhancement only
pip install enhancex-image

# Video & Stabilization only
pip install enhancex-video

# Audio Denoising only
pip install enhancex-audio

# Document Binarization & Deskew
pip install enhancex-document

# Anime Super Resolution
pip install enhancex-anime

# Medical Image Contrast
pip install enhancex-medical
```

## Installation Verification

Run the platform diagnostic tool:
```bash
enhancex doctor
```
