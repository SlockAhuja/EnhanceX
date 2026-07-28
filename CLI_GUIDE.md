# EnhanceX CLI Guide (v2.0.0)

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## Command Reference

### `enhancex doctor`
Runs full system diagnostics: Python version, OpenCV, PyTorch, CUDA GPU detection, installed models, and subpackage ecosystem.

### `enhancex info`
Shows active environment specs, compute devices, and loaded modules.

### `enhancex version`
Displays exact framework version (`EnhanceX Version: 2.0.0`).

### `enhancex enhance`
Enhances an image or video using Adaptive AAE or Manual Research Mode.
```bash
# Auto Mode (Default)
enhancex enhance input.jpg output.jpg --mode auto

# Research Mode (Explicit Model)
enhancex enhance input.jpg output.jpg --mode manual --model RealESRGAN
```

### `enhancex models`
Subcommand group for AI model weight lifecycle management:
- `enhancex models list`: List registered, installed, and remote models.
- `enhancex models install <name>`: Download & verify model SHA-256 checksums.
- `enhancex models remove <name>`: Remove cached model weights.
- `enhancex models update`: Check for model updates.
- `enhancex models verify`: Verify checksum integrity of local models.
