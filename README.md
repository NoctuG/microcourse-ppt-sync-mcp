# microcourse-ppt-sync-mcp

A Windows MCP server for syncing PowerPoint animations with voice timestamps and exporting microcourse videos.

## What it does

This MCP server helps an AI agent turn an existing PowerPoint deck, a timestamped transcript, and a transparent presenter video into a synchronized microcourse video.

## Why this exists

PowerPoint animations are often click-triggered. For microcourse production, animations must follow the teacher's voice timeline automatically. This server converts voice timestamps into PowerPoint animation timings and exports a video with preserved PowerPoint animations.

## Features

- Inspect PowerPoint slides, shapes, and animation sequences
- Parse timestamped transcript files
- Build slide-level and animation-level timeline
- Apply timing to PowerPoint animations
- Set automatic slide transitions
- Export PowerPoint as MP4 using native PowerPoint video export
- Compose PPT background video, presenter video, and voice audio with FFmpeg
- Generate synchronization report

## Requirements

- Windows 10/11
- Microsoft PowerPoint desktop app
- Python 3.11+
- FFmpeg
- pywin32
- MCP Python SDK

## Not in scope

- Background removal
- ASR transcription
- Jianying/CapCut automation
- Full PPT generation from scratch
- Video beautification or effects

## Project layout

## Quick start

## MCP tools

## Example workflow

## OpenClaw prompt example

## PPT template guide

## Security notes

## Roadmap

## License
