# EnhanceX v1.0.0 Documentation (Archived)

**Release Date:** 2026-07-26  
**Status:** Archived Version  
**Install Command:** `pip install enhancex==1.0.0`

---

## Overview

EnhanceX v1.0.0 is the initial core release providing image super-resolution, video stabilization, frame interpolation, and basic CLI commands.

### Python Quick Start (v1.0.0)
```python
from enhancex import ImageEnhancer

enhancer = ImageEnhancer()
out = enhancer.enhance("sample.jpg", "enhanced.jpg", sharpen=1.2, clahe=True)
```
