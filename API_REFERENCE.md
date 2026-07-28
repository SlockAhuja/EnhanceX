# EnhanceX API Reference (v2.0.0)

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. High-Level Python API

### `ImageEnhancer`
```python
class ImageEnhancer:
    def __init__(
        self,
        device: str = "auto",
        mode: str = "auto",
        model: Optional[str] = None,
        config_path: Optional[str] = None
    ): ...

    def enhance(
        self,
        image_input: Union[str, np.ndarray],
        output_path: Optional[str] = None,
        sharpen: float = 1.0,
        denoise: float = 0.0,
        clahe: bool = True,
        white_balance: bool = True,
        face_enhance: bool = False,
        hdr: bool = False,
        mode: Optional[str] = None,
        model: Optional[str] = None
    ) -> np.ndarray: ...
```

### `VideoEnhancer`
```python
class VideoEnhancer:
    def __init__(self, device: str = "auto", backend: str = "auto"): ...
    def enhance(self, input_path: str, output_path: str, ...): ...
    def upscale(self, input_path: str, output_path: str, model_name: str = "real-esrgan", scale: int = 4): ...
```

### `Stabilizer`
```python
class Stabilizer:
    def __init__(self, smoothing_radius: int = 30, border_mode: str = "reflect"): ...
    def process(self, input_path: str, output_path: str) -> str: ...
```

### `FrameInterpolator`
```python
class FrameInterpolator:
    def __init__(self, engine: str = "rife", device: str = "auto"): ...
    def process_video(self, input_path: str, output_path: str, target_fps: float = 60.0) -> str: ...
```

---

## 2. Enterprise SDK Client

```python
from enhancex.sdk import EnhanceXClient

client = EnhanceXClient(endpoint="http://localhost:8000")
task = client.submit_task("input.jpg", "output.jpg", mode="auto")
client.process_batch_sync()
```
