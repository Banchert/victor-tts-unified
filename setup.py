#!/usr/bin/env python3
"""
Setup script for VICTOR-TTS UNIFIED
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="victor-tts-unified",
    version="1.0.0",
    author="VICTOR-TTS Team",
    author_email="your-email@example.com",
    description="Complete Text-to-Speech with Voice Conversion Platform",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Banchert/victor-tts-unified",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "victor-tts=start:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.toml", "*.json", "*.yaml", "*.yml"],
    },
    keywords="tts, voice-conversion, rvc, edge-tts, fastapi, gradio",
    project_urls={
        "Bug Reports": "https://github.com/Banchert/victor-tts-unified/issues",
        "Source": "https://github.com/Banchert/victor-tts-unified",
        "Documentation": "https://github.com/Banchert/victor-tts-unified#readme",
    },
) 