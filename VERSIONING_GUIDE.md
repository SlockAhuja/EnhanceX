# VERSIONING_GUIDE.md: EnhanceX Semantic Versioning Specification

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. Semantic Versioning Standard

EnhanceX adheres to **Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`)**:

- **MAJOR (`2.0.0`):** Incompatible API changes, major platform architectural redesigns, or subpackage infrastructure overhauls.
- **MINOR (`2.1.0`):** Backwards-compatible new features, new domain pipelines, model additions, or new CLI commands.
- **PATCH (`2.0.1`):** Backwards-compatible bug fixes, security patches, performance tuning, or documentation corrections.

---

## 2. Version Verification Protocol

Before any package distribution, all 5 version anchors must match identically:

1. `enhancex/__init__.py`: `__version__ = "X.Y.Z"`
2. `pyproject.toml`: `version = "X.Y.Z"`
3. `setup.py`: `version="X.Y.Z"`
4. `CMakeLists.txt`: `project(EnhanceX VERSION X.Y.Z)`
5. `CITATION.cff`: `version: X.Y.Z`

Run automated verification:
```bash
python scripts/release_manager.py verify
```
