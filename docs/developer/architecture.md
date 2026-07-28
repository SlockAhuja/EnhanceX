# EnhanceX Developer & Architecture Guide

## System Architecture Overview

EnhanceX is structured as a multi-tier modular AI platform:

```
                  +-----------------------------------+
                  |         EnhanceX CLI & GUI        |
                  +-----------------------------------+
                                    |
                  +-----------------------------------+
                  |         High-Level Python API     |
                  +-----------------------------------+
                                    |
         +--------------------------+--------------------------+
         |                                                     |
+-------------------+                                 +------------------+
|  Adaptive AI      |                                 | Model Manager    |
|  Engine (AAE)     |                                 | & Registry       |
+-------------------+                                 +------------------+
         |                                                     |
         +--------------------------+--------------------------+
                                    |
   +--------------------------------+--------------------------------+
   |                                                                 |
+------------------------------------+             +----------------------------------+
| Domain Engines (Image, Video, Audio|             | Enterprise SDK, Server & Cluster |
| Document, Anime, Medical, Satellite|             | (FastAPI, gRPC, Prometheus)      |
+------------------------------------+             +----------------------------------+
                                    |
                  +-----------------------------------+
                  |     CUDA / C++ Engine & GPU Mgr   |
                  +-----------------------------------+
```

## Key Components

1. **Adaptive AI Enhancement Engine (`enhancex.ai.aae`):** Category detection (`CategoryDetector`) and defect analysis (`QualityAnalyzer`).
2. **Model Management System (`enhancex.models.manager`):** Checksum-validated download and local caching manager.
3. **Modular Subpackages:** Domain-specific enhancement modules for audio, document, anime, medical, satellite, and face restoration.
4. **Enterprise Platform:** Multi-GPU cluster distribution, Prometheus telemetry collector, and Kubernetes integration.
