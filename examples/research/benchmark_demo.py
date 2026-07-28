"""
EnhanceX Research Mode & PSNR Metric Evaluation Example
Created by Slock Ahuja (https://github.com/SlockAhuja/EnhanceX)
"""

from enhancex import ImageEnhancer

def benchmark_models(image_path: str):
    models = ["RealESRGAN", "GFPGAN", "CodeFormer", "SwinIR"]
    results = {}
    
    for m in models:
        enhancer = ImageEnhancer(mode="manual", model=m)
        enhancer.enhance(image_path)
        results[m] = enhancer.last_metrics
        print(f"Model {m:<12}: Execution Time = {enhancer.last_metrics['execution_time_ms']:.2f} ms | PSNR = {enhancer.last_metrics['psnr']:.2f} dB")
        
    return results

if __name__ == "__main__":
    print("EnhanceX Research Benchmarking Suite...")
