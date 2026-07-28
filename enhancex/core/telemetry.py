"""
Telemetry & Prometheus Metrics Exporter - EnhanceX v2.0.0
Collects inference latencies, throughput, GPU memory usage, and error metrics.
"""

import time
from typing import Dict, Any
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Telemetry")


class TelemetryCollector:
    """Collects runtime telemetry metrics for Prometheus / Grafana observability."""

    def __init__(self):
        self.metrics = {
            "total_inference_requests": 0,
            "failed_inference_requests": 0,
            "total_latency_ms": 0.0,
            "categories_processed": {}
        }

    def record_inference(self, category: str, latency_ms: float, success: bool = True):
        self.metrics["total_inference_requests"] += 1
        if not success:
            self.metrics["failed_inference_requests"] += 1
        self.metrics["total_latency_ms"] += latency_ms
        self.metrics["categories_processed"][category] = self.metrics["categories_processed"].get(category, 0) + 1

    def export_prometheus_format(self) -> str:
        avg_latency = self.metrics["total_latency_ms"] / max(1, self.metrics["total_inference_requests"])
        lines = [
            "# HELP enhancex_inference_requests_total Total number of inference requests.",
            "# TYPE enhancex_inference_requests_total counter",
            f"enhancex_inference_requests_total {self.metrics['total_inference_requests']}",
            "# HELP enhancex_inference_failures_total Total failed inference requests.",
            "# TYPE enhancex_inference_failures_total counter",
            f"enhancex_inference_failures_total {self.metrics['failed_inference_requests']}",
            "# HELP enhancex_avg_latency_ms Average inference latency in milliseconds.",
            "# TYPE enhancex_avg_latency_ms gauge",
            f"enhancex_avg_latency_ms {avg_latency:.2f}"
        ]
        return "\n".join(lines) + "\n"
