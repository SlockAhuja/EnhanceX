# WEBSITE_STRUCTURE.md: EnhanceX Official Web Portal Architecture

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. Overview & Architecture

The EnhanceX Web Portal is a standalone, offline-ready HTML5/CSS3 site situated under `website/`. It provides an enterprise developer web portal, download center, multi-version documentation browser, model hub framework, and version archive.

```text
website/
├── index.html        # Main Landing Page (Hero, Features, AAE Overview, v2.0.0 Banner)
├── download.html     # Download Center (Windows, Linux, macOS, Docker, PyPI, Releases)
├── docs.html         # Multi-Version Documentation Browser (v1.0, v1.1, v1.2, v2.0)
├── releases.html     # Version Archive & Release Changelogs
├── models.html       # Model Hub Framework (Real-ESRGAN, GFPGAN, CodeFormer, SwinIR)
├── developer.html    # Developer Portal (Architecture, SDK, C++, Pybind11, REST, gRPC)
├── benchmarks.html   # Performance Sweeps & Hardware FPS Benchmarks
└── styles.css        # Premium Dark-Mode Glassmorphism Design System
```

---

## 2. Portal Pages Map

| Page | Primary Content |
| :--- | :--- |
| **Home (`index.html`)** | Platform overview, AAE engine highlight, quick start, badges, author attribution |
| **Download (`download.html`)** | Installation commands (`pip install enhancex==2.0.0`), binary packages, Docker tags |
| **Docs (`docs.html`)** | Interactive documentation tab selector for v2.0 (Stable), v1.2, v1.1, and v1.0 |
| **Releases (`releases.html`)** | Permanent release archive for all historical tags (v1.0.0 to v2.0.0) |
| **Models (`models.html`)** | Model registry metadata, SHA-256 checksums, VRAM requirements, sample tasks |
| **Developer (`developer.html`)** | System architecture diagrams, C++ SDK build instructions, API references |
| **Benchmarks (`benchmarks.html`)** | FPS comparison charts across NVIDIA RTX GPUs, Apple Silicon, and CPUs |
