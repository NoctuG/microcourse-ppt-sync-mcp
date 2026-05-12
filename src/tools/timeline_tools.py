"""Timeline tools for MCP."""

import json
from pathlib import Path
from typing import Dict, Any
from src.utils import get_logger, validators
from src.services import TimelineService


logger = get_logger(__name__)


def build_timeline(
    project_path: str,
    transcript_path: str,
    slide_count: int,
    default_slide_duration: float = 5.0,
) -> Dict[str, Any]:
    """Build timeline from transcript.
    
    Args:
        project_path: Path to project directory
        transcript_path: Path to transcript JSON file
        slide_count: Number of slides in presentation
        default_slide_duration: Default duration per slide in seconds
        
    Returns:
        Dictionary with timeline information
    """
    try:
        project_path = str(validators.validate_project_path(project_path))
        
        # Load transcript
        with open(transcript_path, "r", encoding="utf-8") as f:
            transcript = json.load(f)
        
        validators.validate_transcript_data(transcript)
        
        # Parse transcript to timeline
        timeline = TimelineService.parse_transcript_to_timeline(
            transcript,
            slide_count,
            default_slide_duration,
        )
        
        if not timeline:
            return {
                "status": "error",
                "message": "Failed to parse transcript to timeline",
            }
        
        # Save timeline
        work_dir = Path(project_path) / "work"
        work_dir.mkdir(exist_ok=True)
        
        timeline_path = work_dir / "timeline.json"
        TimelineService.save_timeline_to_json(timeline, str(timeline_path))
        
        result = {
            "status": "success",
            "timeline_path": str(timeline_path),
            "lesson_name": timeline.lesson_name,
            "total_slides": len(timeline.slides),
            "slides_count": len(timeline.slides),
            "total_animations": sum(len(slide.animations) for slide in timeline.slides),
            "total_duration": timeline.total_duration,
        }
        
        logger.info(f"Built timeline: {timeline_path}")
        return result
    except Exception as e:
        logger.error(f"Failed to build timeline: {e}")
        return {
            "status": "error",
            "message": str(e),
        }
