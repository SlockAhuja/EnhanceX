# EnhanceX Changelog

All notable changes to the EnhanceX platform will be documented in this file.

## [2.0.0-RC] - 2026-07-28

### Added
- **v1.1.0 Professional Experience Update:**
  - Professional CLI installation banner and welcome experience.
  - Commands: `enhancex doctor`, `enhancex info`, `enhancex version`.
  - Comprehensive hardware, dependency, GPU, and model verification.
- **v1.2.0 Adaptive AI Enhancement Engine (AAE):**
  - Computer vision category detector for `Portrait`, `Landscape`, `Anime`, `Document`, `Night`, `Medical`, `Satellite`, `Artwork`, `Screenshot`.
  - Digital signal quality defect analyzer for `Blur`, `Noise`, `Compression`, `Low Res`, `Scratches`, `Color Imbalance`, `Motion Blur`, `Low Light`.
  - Automated adaptive pipeline builder.
- **v1.3.0 Modular Ecosystem:**
  - Independent domain subpackages: `enhancex-audio`, `enhancex-document`, `enhancex-anime`, `enhancex-medical`, `enhancex-satellite`, `enhancex-face`, `enhancex-studio`, `enhancex-server`, `enhancex-sdk`, `enhancex-cuda`.
- **v1.4.0 Model Management System:**
  - `enhancex models list`, `install`, `remove`, `update`, `verify`.
  - Checksum validation (SHA-256), version management, local discovery.
- **v1.5.0 Professional Research Mode:**
  - Dual Operating Modes in `ImageEnhancer`: AUTO mode (AAE powered) and MANUAL mode (explicit model selection for benchmarking and research).
- **v2.0.0 Enterprise Platform:**
  - Enterprise SDK Client (`EnhanceXClient`).
  - Multi-GPU Cluster Manager (`ClusterManager`).
  - Prometheus Telemetry Exporter (`TelemetryCollector`).
  - Kubernetes deployment & service manifests (`k8s/`).

### Backward Compatibility
- 100% backward compatible with `EnhanceX v1.0.0` high-level API and CLI flags.
