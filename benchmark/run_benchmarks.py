import time
import os
import argparse
import json
import numpy as np
import cv2
from enhancex.api.high_level import VideoEnhancer, ImageEnhancer, Stabilizer, SuperResolutionEngine
from enhancex.gpu.manager import GPUManager


def run_benchmark(device: str = "auto", backend: str = "auto", output_report: str = "benchmark_report.json"):
    print(f"=== EnhanceX Performance Benchmarking Suite ===")
    gpu_info = GPUManager.get_instance(device).get_device_info()
    print(f"Hardware Profile: {gpu_info}")

    # Generate test image
    test_img = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)

    results = {
        "hardware": gpu_info,
        "benchmarks": {}
    }

    # 1. Image CLAHE & Sharpening Benchmark
    img_enhancer = ImageEnhancer(device=device)
    start_t = time.perf_counter()
    iterations = 20
    for _ in range(iterations):
        _ = img_enhancer.enhance(test_img, sharpen=1.5, clahe=True, denoise=5.0)
    elapsed = time.perf_counter() - start_t
    fps = iterations / elapsed
    latency_ms = (elapsed / iterations) * 1000.0
    results["benchmarks"]["1080p_image_enhancement"] = {"fps": round(fps, 2), "latency_ms": round(latency_ms, 2)}
    print(f"1080p Image Enhancement: {fps:.2f} FPS ({latency_ms:.2f} ms/frame)")

    # 2. Super Resolution 4x Benchmark
    sr_engine = SuperResolutionEngine(model_name="real-esrgan", scale=4, device=device, backend=backend, tile_size=512)
    small_img = np.random.randint(0, 256, (512, 512, 3), dtype=np.uint8)
    start_t = time.perf_counter()
    sr_iterations = 5
    for _ in range(sr_iterations):
        _ = sr_engine.upscale(small_img)
    elapsed = time.perf_counter() - start_t
    sr_fps = sr_iterations / elapsed
    sr_latency_ms = (elapsed / sr_iterations) * 1000.0
    results["benchmarks"]["512p_to_2k_super_resolution"] = {"fps": round(sr_fps, 2), "latency_ms": round(sr_latency_ms, 2)}
    print(f"512p->2K Super Resolution: {sr_fps:.2f} FPS ({sr_latency_ms:.2f} ms/frame)")

    # 3. Video Stabilization Motion Estimation Benchmark
    stabilizer = Stabilizer(smoothing_radius=30)
    # Benchmark synthetic motion estimation calculation
    gray1 = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    start_t = time.perf_counter()
    stab_iters = 30
    for _ in range(stab_iters):
        _ = stabilizer.stabilizer_engine._estimate_motion(gray1, gray2)
    elapsed = time.perf_counter() - start_t
    stab_fps = stab_iters / elapsed
    stab_latency_ms = (elapsed / stab_iters) * 1000.0
    results["benchmarks"]["motion_estimation_optical_flow"] = {"fps": round(stab_fps, 2), "latency_ms": round(stab_latency_ms, 2)}
    print(f"Optical Flow Motion Estimation: {stab_fps:.2f} FPS ({stab_latency_ms:.2f} ms/frame)")

    # Write report
    with open(output_report, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[SUCCESS] Benchmark report saved to: {output_report}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EnhanceX Benchmark Suite")
    parser.add_argument("--device", default="auto", help="Execution device target")
    parser.add_argument("--backend", default="auto", help="Inference backend target")
    parser.add_argument("--output", default="benchmark_report.json", help="Report output json path")
    args = parser.parse_args()

    run_benchmark(device=args.device, backend=args.backend, output_report=args.output)
