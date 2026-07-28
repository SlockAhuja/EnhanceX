import os
import uuid
import tempfile
import cv2
import numpy as np
from typing import Optional, Dict, Any

try:
    from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect, Form, HTTPException, Header, BackgroundTasks, Depends, Security
    from fastapi.security.api_key import APIKeyHeader
    from fastapi.responses import FileResponse, JSONResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from enhancex.api.high_level import VideoEnhancer, ImageEnhancer, Stabilizer, SuperResolutionEngine
from enhancex.gpu.manager import GPUManager
from enhancex.core.logger import get_logger
from enhancex.core.exceptions import EnhanceXError, ValidationError

logger = get_logger("EnhanceX.Server")

JOBS_DB: Dict[str, Dict[str, Any]] = {}

from enhancex.core.telemetry import TelemetryCollector
from enhancex import __version__

telemetry = TelemetryCollector()

if HAS_FASTAPI:
    app = FastAPI(
        title="EnhanceX Enterprise REST & Streaming Platform",
        description="Production REST, Prometheus Telemetry & WebSocket Streaming API for AI Media Enhancement",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    image_enhancer = ImageEnhancer()
    video_enhancer = VideoEnhancer()
    gpu_manager = GPUManager.get_instance()

    API_KEY_NAME = "X-API-Key"
    api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

    async def verify_api_key(api_key: Optional[str] = Security(api_key_header)):
        expected_key = os.environ.get("ENHANCEX_API_KEY", "")
        if expected_key and api_key != expected_key:
            raise HTTPException(status_code=401, detail="Invalid or missing API key.")
        return api_key

    @app.get("/health", tags=["System"])
    async def health_check():
        gpu_info = gpu_manager.get_device_info()
        return {
            "status": "healthy",
            "framework": f"EnhanceX v{__version__}",
            "device": gpu_info
        }

    @app.get("/metrics", tags=["Telemetry"])
    async def get_metrics():
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(telemetry.export_prometheus_format())

    @app.post("/api/v1/enhance/image", tags=["Image Enhancement"])
    async def enhance_image(
        file: UploadFile = File(...),
        sharpen: float = Form(1.0),
        denoise: float = Form(0.0),
        clahe: bool = Form(True),
        white_balance: bool = Form(True),
        api_key: str = Depends(verify_api_key)
    ):
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image payload.")

        enhanced = image_enhancer.enhance(
            img,
            sharpen=sharpen,
            denoise=denoise,
            clahe=clahe,
            white_balance=white_balance
        )

        _, buffer = cv2.imencode(".jpg", enhanced)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.write(buffer.tobytes())
        temp_file.close()

        return FileResponse(temp_file.name, media_type="image/jpeg", filename="enhanced.jpg")

    @app.post("/api/v1/upscale", tags=["AI Processing"])
    async def upscale_image(
        file: UploadFile = File(...),
        scale: int = Form(2),
        model: str = Form("real-esrgan"),
        api_key: str = Depends(verify_api_key)
    ):
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image payload.")

        sr = SuperResolutionEngine(model_name=model, scale=scale)
        upscaled = sr.upscale(img)

        _, buffer = cv2.imencode(".jpg", upscaled)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        temp_file.write(buffer.tobytes())
        temp_file.close()

        return FileResponse(temp_file.name, media_type="image/jpeg", filename="upscaled.jpg")

    def _process_video_job(job_id: str, in_path: str, out_path: str):
        try:
            JOBS_DB[job_id]["status"] = "processing"
            video_enhancer.enhance(in_path, out_path)
            JOBS_DB[job_id]["status"] = "completed"
            JOBS_DB[job_id]["result_path"] = out_path
        except Exception as e:
            JOBS_DB[job_id]["status"] = "failed"
            JOBS_DB[job_id]["error"] = str(e)

    @app.post("/api/v1/jobs/video", tags=["Async Background Jobs"])
    async def submit_video_job(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        api_key: str = Depends(verify_api_key)
    ):
        job_id = str(uuid.uuid4())
        in_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        out_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        content = await file.read()
        in_temp.write(content)
        in_temp.close()
        out_temp.close()

        JOBS_DB[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "result_path": None,
            "error": None
        }

        background_tasks.add_task(_process_video_job, job_id, in_temp.name, out_temp.name)

        return {"job_id": job_id, "status": "queued"}

    @app.get("/api/v1/jobs/{job_id}", tags=["Async Background Jobs"])
    async def get_job_status(job_id: str, api_key: str = Depends(verify_api_key)):
        if job_id not in JOBS_DB:
            raise HTTPException(status_code=404, detail="Job not found.")
        return JOBS_DB[job_id]

    @app.websocket("/ws/stream")
    async def websocket_stream(websocket: WebSocket):
        """Real-time live video frame enhancement stream over WebSockets."""
        await websocket.accept()
        logger.info("WebSocket video stream client connected.")
        try:
            while True:
                bytes_data = await websocket.receive_bytes()
                nparr = np.frombuffer(bytes_data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if frame is not None:
                    enhanced_frame = image_enhancer.enhance(frame, sharpen=1.2, clahe=True)
                    _, encoded = cv2.imencode(".jpg", enhanced_frame)
                    await websocket.send_bytes(encoded.tobytes())
        except WebSocketDisconnect:
            logger.info("WebSocket video stream client disconnected.")
else:
    app = None
