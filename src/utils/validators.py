"""Validators for input data."""

import os
from pathlib import Path
from typing import Dict, Any, List


class ValidationError(Exception):
    """Validation error."""
    pass


def validate_project_path(project_path: str) -> Path:
    """Validate project path exists.
    
    Args:
        project_path: Project directory path
        
    Returns:
        Path object
        
    Raises:
        ValidationError: If path doesn't exist
    """
    path = Path(project_path)
    if not path.exists():
        raise ValidationError(f"Project path does not exist: {project_path}")
    if not path.is_dir():
        raise ValidationError(f"Project path is not a directory: {project_path}")
    return path


def validate_ppt_file(ppt_path: str) -> Path:
    """Validate PPT file exists.
    
    Args:
        ppt_path: PPT file path
        
    Returns:
        Path object
        
    Raises:
        ValidationError: If file doesn't exist or is not a valid PPT
    """
    path = Path(ppt_path)
    if not path.exists():
        raise ValidationError(f"PPT file does not exist: {ppt_path}")
    if not path.suffix.lower() in [".pptx", ".ppt"]:
        raise ValidationError(f"Invalid PPT file format: {ppt_path}")
    return path


def validate_timeline_data(timeline: Dict[str, Any]) -> None:
    """Validate timeline data structure.
    
    Args:
        timeline: Timeline data dictionary
        
    Raises:
        ValidationError: If timeline structure is invalid
    """
    if not isinstance(timeline, dict):
        raise ValidationError("Timeline must be a dictionary")
    
    if "slides" not in timeline:
        raise ValidationError("Timeline must contain 'slides' key")
    
    if not isinstance(timeline["slides"], list):
        raise ValidationError("Timeline 'slides' must be a list")
    
    for i, slide in enumerate(timeline["slides"]):
        if not isinstance(slide, dict):
            raise ValidationError(f"Slide {i} must be a dictionary")
        
        if "slide_index" not in slide:
            raise ValidationError(f"Slide {i} must have 'slide_index'")
        
        if "animations" not in slide:
            raise ValidationError(f"Slide {i} must have 'animations'")
        
        if not isinstance(slide["animations"], list):
            raise ValidationError(f"Slide {i} 'animations' must be a list")
        
        for j, anim in enumerate(slide["animations"]):
            if not isinstance(anim, dict):
                raise ValidationError(f"Animation {j} in slide {i} must be a dictionary")
            
            if "trigger_time" not in anim:
                raise ValidationError(f"Animation {j} in slide {i} must have 'trigger_time'")
            
            if not isinstance(anim["trigger_time"], (int, float)):
                raise ValidationError(f"Animation {j} in slide {i} 'trigger_time' must be numeric")


def validate_transcript_data(transcript: Dict[str, Any]) -> None:
    """Validate transcript data structure.
    
    Args:
        transcript: Transcript data dictionary
        
    Raises:
        ValidationError: If transcript structure is invalid
    """
    if not isinstance(transcript, dict):
        raise ValidationError("Transcript must be a dictionary")
    
    if "segments" not in transcript:
        raise ValidationError("Transcript must contain 'segments' key")
    
    if not isinstance(transcript["segments"], list):
        raise ValidationError("Transcript 'segments' must be a list")
    
    for i, segment in enumerate(transcript["segments"]):
        if not isinstance(segment, dict):
            raise ValidationError(f"Segment {i} must be a dictionary")
        
        required_fields = ["start", "end", "text"]
        for field in required_fields:
            if field not in segment:
                raise ValidationError(f"Segment {i} must have '{field}'")
        
        if not isinstance(segment["start"], (int, float)):
            raise ValidationError(f"Segment {i} 'start' must be numeric")
        
        if not isinstance(segment["end"], (int, float)):
            raise ValidationError(f"Segment {i} 'end' must be numeric")
