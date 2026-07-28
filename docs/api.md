# EnhanceX API Reference Guide

## Python API

### `VideoEnhancer`

```python
class VideoEnhancer(device: str = "auto", backend: str = "auto", config_path: str = None)
```

#### Methods

- `enhance(input_path: str, output_path: str, sharpen: float = 1.0, denoise: float = 0.0, clahe: bool = False, white_balance: bool = False, face_enhance: bool = False, hdr: bool = False) -> str`
- `stabilize(input_path: str, output_path: str, smoothing_radius: int = 30, border_mode: str = "reflect") -> str`
- `upscale(input_path: str, output_path: str, model_name: str = "real-esrgan", scale: int = 4, tile_size: int = 512) -> str`
- `denoise(input_path: str, output_path: str, method: str = "fastnl", strength: float = 10.0) -> str`
- `interpolate(input_path: str, output_path: str, target_fps: float = 60.0, engine: str = "rife") -> str`

### `ImageEnhancer`

```python
class ImageEnhancer(device: str = "auto", config_path: str = None)
```

#### Methods

- `enhance(image_input: Union[str, np.ndarray], output_path: str = None, sharpen: float = 1.0, denoise: float = 0.0, clahe: bool = True, white_balance: bool = True, face_enhance: bool = False, hdr: bool = False) -> np.ndarray`

---

## C++ API

Include the master header `#include "enhancex/enhancex.hpp"`:

- `enhancex::GPUManager::getInstance()`
- `enhancex::ModelManager`
- `enhancex::ImageEnhancer`
- `enhancex::Stabilizer`
- `enhancex::FrameInterpolator`
- `enhancex::VideoEnhancer`
