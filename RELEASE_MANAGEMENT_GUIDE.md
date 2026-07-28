# RELEASE_MANAGEMENT_GUIDE.md: EnhanceX Professional Release Engineering Guide

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. Overview & Philosophy

EnhanceX follows a strict release engineering discipline modeled after major open-source infrastructure projects (PyTorch, OpenCV, TensorFlow, Kubernetes). 

Every stable release must satisfy the **Permanent Availability Guarantee**:
Once a tag (e.g. `v1.0.0`, `v1.1.0`, `v1.2.0`, `v2.0.0`) is published, it remains permanently accessible on GitHub Releases, PyPI, and git commit history. Users must always be able to pin and install any historical version:
```bash
pip install enhancex==1.0.0
pip install enhancex==1.1.0
pip install enhancex==1.2.0
pip install enhancex==2.0.0
```

---

## 2. Release Lifecycle & Checklist

Each release milestone follows a 6-stage release pipeline:

```
[ 1. Feature Freeze ] --> [ 2. Automated Testing ] --> [ 3. Release Verification ]
                                                                 |
[ 6. Permanent Archive ] <-- [ 5. GitHub & PyPI Release ] <-- [ 4. Git Tagging ]
```

### Stage 1: Feature Freeze
- Freeze all pull requests targetting main branch.
- No new features introduced after tag candidate declaration.

### Stage 2: Automated Verification
```bash
python scripts/release_manager.py verify
pytest tests/
```

### Stage 3: Release Documentation Update
- Update `CHANGELOG.md`, `RELEASE_NOTES.md`, and versioned docs (`docs/vX.Y/`).

### Stage 4: Git Tagging
```bash
git tag -a v2.0.0 -m "EnhanceX v2.0.0 Official Stable Release"
git push origin v2.0.0
```

### Stage 5: Artifact Build & Distribution
```bash
python -m build
twine upload dist/*
```

---

## 3. Historical & Future Version Map

| Version | Status | Release Date | Key Highlight |
| :--- | :--- | :--- | :--- |
| **v1.0.0** | Archived | 2026-07-26 | Initial Core Release (Super Resolution, Stabilization) |
| **v1.1.0** | Archived | 2026-07-28 | Professional Experience Update (`doctor`, `info`, `version`) |
| **v1.2.0** | Archived | 2026-07-28 | Adaptive AI Enhancement Engine (AAE) |
| **v2.0.0** | **Current Stable** | 2026-07-28 | Enterprise Platform (SDK, Subpackages, Telemetry, K8s) |
| **v3.0.0** | Planned | Future | Real-Time Video Streaming Engine (WebRTC / gRPC) |
| **v4.0.0** | Planned | Future | 3D NeRF & Spatial Video Enhancement |
| **v5.0.0** | Planned | Future | Edge NPU Hardware Acceleration |
