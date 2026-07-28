"""
Enterprise SDK Client - EnhanceX v2.0.0
Provides batch queue processing, async streaming pipelines, and server integration SDK.
"""

import time
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Callable
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.SDK")


@dataclass
class EnhancementTask:
    task_id: str
    input_path: str
    output_path: str
    mode: str = "auto"
    status: str = "pending"  # pending, processing, completed, failed
    result_metrics: Optional[Dict[str, float]] = None


class EnhanceXClient:
    """Enterprise SDK Client for orchestrating high-throughput enhancement jobs."""

    def __init__(self, endpoint: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.endpoint = endpoint
        self.api_key = api_key
        self.task_queue: List[EnhancementTask] = []

    def submit_task(self, input_path: str, output_path: str, mode: str = "auto") -> EnhancementTask:
        task_id = f"task_{len(self.task_queue) + 1:04d}_{int(time.time())}"
        task = EnhancementTask(task_id=task_id, input_path=input_path, output_path=output_path, mode=mode)
        self.task_queue.append(task)
        logger.info(f"SDK Task submitted: {task_id}")
        return task

    def process_batch_sync(self, progress_callback: Optional[Callable[[int, int], None]] = None) -> List[EnhancementTask]:
        from enhancex.api.high_level import ImageEnhancer
        enhancer = ImageEnhancer()
        total = len(self.task_queue)

        for idx, task in enumerate(self.task_queue):
            if task.status == "completed":
                continue
            task.status = "processing"
            try:
                enhancer.enhance(task.input_path, task.output_path, mode=task.mode)
                task.status = "completed"
                task.result_metrics = enhancer.last_metrics
            except Exception as e:
                task.status = "failed"
                logger.error(f"Task {task.task_id} failed: {e}")

            if progress_callback:
                progress_callback(idx + 1, total)

        return self.task_queue
