"""
EnhanceX Python API Example - Auto Mode & Manual Mode Usage
Created by Slock Ahuja (https://github.com/SlockAhuja/EnhanceX)
"""

from enhancex import ImageEnhancer

def main():
    print("Initializing EnhanceX ImageEnhancer in Auto Mode...")
    enhancer_auto = ImageEnhancer(mode="auto")
    
    # Process image with Adaptive AAE Engine
    out_auto = enhancer_auto.enhance("input.jpg", output_path="output_auto.jpg")
    print(f"AAE Detection Metrics: {enhancer_auto.last_metrics}")

    print("\nInitializing EnhanceX ImageEnhancer in Manual Research Mode...")
    enhancer_manual = ImageEnhancer(mode="manual", model="RealESRGAN")
    out_manual = enhancer_manual.enhance("input.jpg", output_path="output_realesrgan.jpg")
    print(f"Manual Mode Metrics: {enhancer_manual.last_metrics}")

if __name__ == "__main__":
    main()
