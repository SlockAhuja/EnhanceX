import argparse
from enhancex.ai.model_loader import ModelLoader


def main():
    parser = argparse.ArgumentParser(description="Download pre-trained weights for EnhanceX AI models.")
    parser.add_argument("--models", nargs="+", default=["real-esrgan", "edsr", "srcnn", "rife"], help="Models to download")
    args = parser.parse_args()

    loader = ModelLoader()
    for model_name in args.models:
        try:
            loader.download_model(model_name)
        except Exception as e:
            print(f"Failed to download {model_name}: {e}")


if __name__ == "__main__":
    main()
