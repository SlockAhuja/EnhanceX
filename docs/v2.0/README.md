# EnhanceX v2.0.0 Documentation (Current Stable)

**Release Date:** 2026-07-28  
**Status:** **Current Production Stable**  
**Author:** **Slock Ahuja**  
**Install Command:** `pip install enhancex==2.0.0` or `pip install git+https://github.com/SlockAhuja/EnhanceX.git`

---

## Overview

EnhanceX v2.0.0 is the official production release of the universal AI media enhancement platform. It features the Adaptive AI Engine (AAE), model weight management, domain subpackages, enterprise SDK, multi-GPU cluster management, Prometheus telemetry, and Kubernetes deployment integration.

### Quick Start
```python
from enhancex import ImageEnhancer

enhancer = ImageEnhancer(mode="auto")
out = enhancer.enhance("sample.jpg", "enhanced.jpg")
print("Analysis Metrics:", enhancer.last_metrics)
```
