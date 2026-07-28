import os
import sys
from setuptools import setup, find_packages

setup(
    name="enhancex",
    version="1.0.0",
    description="Universal AI-Powered Image & Video Enhancement Framework",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="EnhanceX Core Team",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "opencv-python>=4.8.0",
        "pillow>=9.5.0",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "click>=8.1.0"
    ],
    entry_points={
        "console_scripts": [
            "enhancex=enhancex.cli.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
