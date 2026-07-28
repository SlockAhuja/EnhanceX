import pytest
import numpy as np
import cv2

try:
    from fastapi.testclient import TestClient
    from enhancex.server.fastapi_server import app
    HAS_FASTAPI_TEST = True
except ImportError:
    HAS_FASTAPI_TEST = False

from enhancex.server.grpc_server import EnhanceXGRPCServer


@pytest.mark.skipif(not HAS_FASTAPI_TEST or app is None, reason="FastAPI not installed")
def test_fastapi_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "framework" in data


@pytest.mark.skipif(not HAS_FASTAPI_TEST or app is None, reason="FastAPI not installed")
def test_fastapi_enhance_image_endpoint():
    client = TestClient(app)
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    _, encoded = cv2.imencode(".jpg", img)

    response = client.post(
        "/api/v1/enhance/image",
        files={"file": ("test.jpg", encoded.tobytes(), "image/jpeg")},
        data={"sharpen": "1.0", "clahe": "true"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_grpc_server_stub():
    server = EnhanceXGRPCServer(port=50055)
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    _, encoded = cv2.imencode(".jpg", img)
    res_bytes = server.process_image_rpc(encoded.tobytes())
    assert len(res_bytes) > 0
