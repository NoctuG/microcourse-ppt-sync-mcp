#!/usr/bin/env python3
"""Setup script for microcourse-ppt-sync-mcp."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="microcourse-ppt-sync-mcp",
    version="0.1.0",
    author="Manus Agent",
    author_email="agent@manus.im",
    description="MCP Server for PPT animation timeline synchronization and video export",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NoctuG/microcourse-ppt-sync-mcp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.12",
    install_requires=[
        "modelcontextprotocol>=0.1.0",
        "pywin32>=306",
        "pyyaml>=6.0.1",
        "python-json-logger>=2.0.7",
    ],
    entry_points={
        "console_scripts": [
            "microcourse-ppt-sync=src.cli:main",
        ],
    },
)
