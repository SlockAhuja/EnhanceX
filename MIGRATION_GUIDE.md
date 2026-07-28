# EnhanceX Migration Guide (v0.x to v1.0.0)

This guide assists developers and maintainers in upgrading existing projects to **EnhanceX v1.0.0**.

---

## Key Changes & Breaking Updates

### 1. Exception Handling Hierarchy
In v1.0.0, generic standard exceptions (like `ValueError` or `FileNotFoundError`) raised in AI and path processing modules are replaced with structured domain exceptions inheriting from `EnhanceXError`:

```python
# Old Exception handling
try:
    path = model_loader.get_model_path("../invalid")
except Exception as e:
    print(e)

# Modern v1.0.0 Exception handling
from enhancex.core.exceptions import ValidationError, ModelNotFoundError, EnhanceXError

try:
    path = model_loader.get_model_path("real-esrgan")
except ValidationError as e:
    logger.error(f"Invalid input parameter: {e}")
except ModelNotFoundError as e:
    logger.error(f"Model weight unavailable: {e}")
```

### 2. Video Pipeline Manager
The video enhancement flow is now orchestrated through `VideoPipelineManager` instead of manually invoking individual video readers and writers:

```python
from enhancex.video import VideoPipelineManager

pipeline = VideoPipelineManager(
    enable_stabilization=True,
    enable_super_resolution=True,
    sr_model="real-esrgan",
    sr_scale=4
)
pipeline.process_video("input.mp4", "output.mp4")
```

### 3. REST API Authentication
When deploying the FastAPI REST server in production, pass the `X-API-Key` header if the `ENHANCEX_API_KEY` environment variable is defined.
