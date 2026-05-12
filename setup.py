#!/usr/bin/env python3
"""Setup script for microcourse-ppt-sync-mcp."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="microcourse-ppt-sync-mcp",
    version="0.2.0",
    author="NoctuG",
    author_email="",
    description="MCP Server for PPT animation timeline synchronization and video export",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/NoctuG/microcourse-ppt-sync-mcp",
    project_urls={
        "Bug Tracker": "https://github.com/NoctuG/microcourse-ppt-sync-mcp/issues",
        "Documentation": "https://github.com/NoctuG/microcourse-ppt-sync-mcp/tree/main/docs",
        "Source Code": "https://github.com/NoctuG/microcourse-ppt-sync-mcp",
    },
    packages=find_packages(exclude=["tests", "docs"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.11",
    install_requires=[
        "modelcontextprotocol>=0.1.0",
        "pywin32>=306",
        "pyyaml>=6.0.1",
        "python-json-logger>=2.0.7",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "microcourse-ppt-sync=src.main:cli",
        ],
    },
)
