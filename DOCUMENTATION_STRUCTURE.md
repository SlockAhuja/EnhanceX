# DOCUMENTATION_STRUCTURE.md: EnhanceX Multi-Version Documentation System

Created by **Slock Ahuja** | GitHub: [https://github.com/SlockAhuja/EnhanceX](https://github.com/SlockAhuja/EnhanceX)

---

## 1. Architecture & Directory Tree

EnhanceX maintains a permanent versioned documentation tree. Users can browse documentation by release version:

```text
docs/
├── latest -> v2.0
├── v1.0/
│   └── README.md         # Initial v1.0.0 Core Framework Documentation
├── v1.1/
│   └── README.md         # v1.1.0 Experience & Diagnostics Documentation
├── v1.2/
│   └── README.md         # v1.2.0 Adaptive AAE Engine Documentation
└── v2.0/
    ├── README.md         # v2.0.0 Current Production Stable Documentation
    ├── user/
    │   ├── installation.md
    │   ├── quickstart.md
    │   ├── cli.md
    │   └── python.md
    └── developer/
        ├── architecture.md
        └── aae_design.md
```

---

## 2. Version Browsing Guarantee

| Documentation Version | Target Platform Release | Status | Target Path |
| :--- | :--- | :--- | :--- |
| **v2.0 (Current Stable)** | EnhanceX v2.0.0 | Active Production | [`docs/v2.0/`](docs/v2.0/README.md) |
| **v1.2** | EnhanceX v1.2.0 | Archived Stable | [`docs/v1.2/`](docs/v1.2/README.md) |
| **v1.1** | EnhanceX v1.1.0 | Archived Stable | [`docs/v1.1/`](docs/v1.1/README.md) |
| **v1.0** | EnhanceX v1.0.0 | Archived Core | [`docs/v1.0/`](docs/v1.0/README.md) |
