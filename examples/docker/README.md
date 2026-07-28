# EnhanceX Docker Deployment Example

```bash
# Build Docker Image
docker build -t slockahuja/enhancex:latest .

# Run Docker Container with GPU Support
docker run --gpus all -p 8000:8000 slockahuja/enhancex:latest
```
