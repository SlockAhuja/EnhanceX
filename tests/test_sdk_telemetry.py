import pytest
from enhancex.sdk import EnhanceXClient
from enhancex.gpu.cluster import ClusterManager
from enhancex.core.telemetry import TelemetryCollector


def test_sdk_client_and_cluster():
    client = EnhanceXClient()
    task = client.submit_task("input.jpg", "output.jpg", mode="auto")
    assert task.status == "pending"
    assert task.task_id.startswith("task_")

    cluster = ClusterManager()
    workers = cluster.get_available_workers()
    assert len(workers) >= 1
    assignments = cluster.dispatch_batch(["img1.jpg", "img2.jpg"])
    assert len(assignments) >= 1


def test_telemetry_exporter():
    collector = TelemetryCollector()
    collector.record_inference("portrait", 45.2, success=True)
    collector.record_inference("document", 12.8, success=True)
    metrics_str = collector.export_prometheus_format()
    assert "enhancex_inference_requests_total 2" in metrics_str
    assert "enhancex_avg_latency_ms" in metrics_str
