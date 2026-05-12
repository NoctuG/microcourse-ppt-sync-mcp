"""CLI entry point for Microcourse PPT Sync."""

import sys
import json
from pathlib import Path
from typing import Optional
import click

from src.utils import get_logger
from src.tools import (
    inspect_project,
    inspect_ppt,
    build_timeline,
    apply_ppt_timeline,
    export_ppt_video,
    generate_sync_report,
)


logger = get_logger(__name__)


@click.group()
@click.version_option(version="0.2.0", prog_name="microcourse-ppt-sync")
def cli():
    """Microcourse PPT Sync - MCP Server for PPT animation timeline synchronization."""
    pass


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def inspect(project_path: str):
    """Inspect project directory structure."""
    result = inspect_project(project_path)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@cli.command()
@click.argument("ppt_path", type=click.Path(exists=True))
def inspect_ppt_cmd(ppt_path: str):
    """Inspect PPT file and animations."""
    result = inspect_ppt(ppt_path)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.argument("transcript_path", type=click.Path(exists=True))
@click.option("--slide-count", "-s", type=int, required=True, help="Number of slides")
@click.option("--duration", "-d", type=float, default=5.0, help="Default slide duration in seconds")
def build(project_path: str, transcript_path: str, slide_count: int, duration: float):
    """Build timeline from transcript."""
    result = build_timeline(project_path, transcript_path, slide_count, duration)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.argument("ppt_path", type=click.Path(exists=True))
@click.argument("timeline_path", type=click.Path(exists=True))
def apply(project_path: str, ppt_path: str, timeline_path: str):
    """Apply timeline to PPT."""
    result = apply_ppt_timeline(project_path, ppt_path, timeline_path)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@cli.command()
@click.argument("ppt_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.option("--quality", "-q", type=click.Choice(["LD", "SD", "HD"]), default="HD", help="Video quality")
@click.option("--fps", "-f", type=int, default=30, help="Frames per second")
def export(ppt_path: str, output_path: str, quality: str, fps: int):
    """Export PPT as video."""
    result = export_ppt_video(ppt_path, output_path, quality, fps)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.argument("timeline_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
def report(project_path: str, timeline_path: str, output_path: str):
    """Generate sync report."""
    result = generate_sync_report(project_path, timeline_path, output_path)
    click.echo(json.dumps(result, indent=2, ensure_ascii=False))


@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--ppt-file", "-p", type=click.Path(exists=True), help="PPT file path (auto-detect if not provided)")
@click.option("--timeline-file", "-t", type=click.Path(exists=True), help="Timeline file path (auto-detect if not provided)")
@click.option("--quality", "-q", type=click.Choice(["LD", "SD", "HD"]), default="HD", help="Video quality")
@click.option("--fps", "-f", type=int, default=30, help="Frames per second")
def run(project_path: str, ppt_file: Optional[str], timeline_file: Optional[str], quality: str, fps: int):
    """Run complete workflow: inspect → apply → export → report."""
    project_path = str(Path(project_path).absolute())
    
    click.echo(f"🚀 Starting workflow for project: {project_path}")
    click.echo("")
    
    # Step 1: Inspect project
    click.echo("📁 Step 1: Inspecting project...")
    inspect_result = inspect_project(project_path)
    if inspect_result["status"] != "success":
        click.echo(f"❌ Failed to inspect project: {inspect_result.get('message')}")
        sys.exit(1)
    click.echo("✅ Project inspection completed")
    
    # Auto-detect PPT file if not provided
    if not ppt_file:
        input_dir = Path(project_path) / "input"
        ppt_files = list(input_dir.glob("*.pptx"))
        if not ppt_files:
            click.echo("❌ No PPT file found in input/ directory")
            sys.exit(1)
        ppt_file = str(ppt_files[0])
    
    # Step 2: Inspect PPT
    click.echo("")
    click.echo("📊 Step 2: Inspecting PPT...")
    ppt_result = inspect_ppt(ppt_file)
    if ppt_result["status"] != "success":
        click.echo(f"❌ Failed to inspect PPT: {ppt_result.get('message')}")
        sys.exit(1)
    slide_count = ppt_result.get("slide_count", 0)
    click.echo(f"✅ PPT inspection completed ({slide_count} slides)")
    
    # Auto-detect timeline file if not provided
    if not timeline_file:
        work_dir = Path(project_path) / "work"
        timeline_files = list(work_dir.glob("timeline.json"))
        if not timeline_files:
            click.echo("❌ No timeline.json found in work/ directory")
            sys.exit(1)
        timeline_file = str(timeline_files[0])
    
    # Step 3: Apply timeline
    click.echo("")
    click.echo("⏱️  Step 3: Applying timeline to PPT...")
    apply_result = apply_ppt_timeline(project_path, ppt_file, timeline_file)
    if apply_result["status"] != "success":
        click.echo(f"❌ Failed to apply timeline: {apply_result.get('message')}")
        sys.exit(1)
    timed_ppt = apply_result.get("output_path")
    click.echo(f"✅ Timeline applied ({apply_result.get('total_animations')} animations)")
    
    # Step 4: Export video
    click.echo("")
    click.echo("🎬 Step 4: Exporting PPT as video...")
    output_dir = Path(project_path) / "output"
    output_dir.mkdir(exist_ok=True)
    video_output = str(output_dir / "ppt_bg.mp4")
    export_result = export_ppt_video(timed_ppt, video_output, quality, fps)
    if export_result["status"] != "success":
        click.echo(f"❌ Failed to export video: {export_result.get('message')}")
        sys.exit(1)
    click.echo(f"✅ Video exported ({export_result.get('file_size', 0) / 1024 / 1024:.1f} MB)")
    
    # Step 5: Generate report
    click.echo("")
    click.echo("📝 Step 5: Generating sync report...")
    report_output = str(output_dir / "sync_report.md")
    report_result = generate_sync_report(project_path, timeline_file, report_output)
    if report_result["status"] != "success":
        click.echo(f"❌ Failed to generate report: {report_result.get('message')}")
        sys.exit(1)
    click.echo(f"✅ Report generated ({report_result.get('issue_count', 0)} issues)")
    
    # Summary
    click.echo("")
    click.echo("=" * 50)
    click.echo("✨ Workflow completed successfully!")
    click.echo("=" * 50)
    click.echo(f"📍 Project: {project_path}")
    click.echo(f"📊 Slides: {slide_count}")
    click.echo(f"🎬 Video: {video_output}")
    click.echo(f"📝 Report: {report_output}")


if __name__ == "__main__":
    cli()
