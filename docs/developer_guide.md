# EnhanceX Developer Guide

## Building from Source

```bash
# Clone repository
git clone https://github.com/enhancex/enhancex.git
cd enhancex

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with development dependencies
pip install -e .[dev,ai,gpu]
```

## Running Tests

```bash
# Run pytest with coverage report
pytest --cov=enhancex --cov-report=term-missing tests/
```

## Building C++ Library & Pybind11 Extensions

```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DENHANCEX_BUILD_CUDA=ON
make -j$(nproc)
```
