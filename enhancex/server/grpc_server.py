import time
import cv2
import numpy as np
from typing import Optional

try:
    import grpc
    from concurrent import futures
    HAS_GRPC = True
except ImportError:
    HAS_GRPC = False

from enhancex.api.high_level import ImageEnhancer, SuperResolutionEngine
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.gRPC")


class EnhanceXGRPCServer:
    """Enterprise gRPC Server Implementation for High-Throughput Remote Processing."""

    def __init__(self, port: int = 50051):
        self.port = port
        self.image_enhancer = ImageEnhancer()
        self.sr_engine = SuperResolutionEngine(scale=2)

    def process_image_rpc(self, image_bytes: bytes, sharpen: float = 1.0, clahe: bool = True) -> bytes:
        start_t = time.perf_counter()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid gRPC image payload.")

        enhanced = self.image_enhancer.enhance(img, sharpen=sharpen, clahe=clahe)
        _, encoded = cv2.imencode(".jpg", enhanced)
        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        logger.info(f"Processed gRPC Image Request in {elapsed_ms:.2f} ms")
        return encoded.tobytes()

    def process_upscale_rpc(self, image_bytes: bytes, scale: int = 2, model: str = "real-esrgan") -> bytes:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid gRPC image payload.")

        sr = SuperResolutionEngine(model_name=model, scale=scale)
        upscaled = sr.upscale(img)
        _, encoded = cv2.imencode(".jpg", upscaled)
        return encoded.tobytes()

    def start(self):
        logger.info(f"gRPC Server active on port {self.port}...")
        if HAS_GRPC:
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            server.add_insecure_port(f"[::]:{self.port}")
            server.start()
            logger.info("gRPC server listener bound successfully.")
            return server
        return None


if __name__ == "__main__":
    server = EnhanceXGRPCServer()
    server.start()
