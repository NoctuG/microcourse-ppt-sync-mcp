"""Inspection tools for MCP."""

import os
import json
from pathlib import Path
from typing import Dict, Any
from src.utils import get_logger, validators
from src.services import PPTService


logger = get_logger(__name__)


def inspect_project(project_path: str) -> Dict[str, Any]:
    """Inspect project directory structure.
    
    Args:
        project_path: Path to project directory
        
    Returns:
        Dictionary with project information
    """
    try:
        project_path = str(validators.validate_project_path(project_path))
        
        result = {
            "status": "success",
            "project_path": project_path,
            "structure": {},
            "files": {},
        }
        
        # Check standard directories
        standard_dirs = ["input", "work", "output"]
        for dir_name in standard_dirs:
            dir_path = Path(project_path) / dir_name
            result["structure"][dir_name] = {
                "exists": dir_path.exists(),
                "is_dir": dir_path.is_dir(),
            }
            
            if dir_path.exists():
                files = list(dir_path.glob("*"))
                result["files"][dir_name] = [f.name for f in files]
        
        # Check for key files
        key_files = {
            "input": ["lesson.pptx"],
            "work": ["timeline.json", "transcript.json"],
            "output": ["lesson_timed.pptx", "ppt_bg.mp4", "sync_report.md"],
        }
        
        result["key_files"] = {}
        for dir_name, files in key_files.items():
            result["key_files"][dir_name] = {}
            for file_name in files:
                file_path = Path(project_path) / dir_name / file_name
                result["key_files"][dir_name][file_name] = file_path.exists()
        
        logger.info(f"Inspected project: {project_path}")
        return result
    except Exception as e:
        logger.error(f"Failed to inspect project: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


def inspect_ppt(ppt_path: str) -> Dict[str, Any]:
    """Inspect PPT file using PowerPoint COM.
    
    Args:
        ppt_path: Path to PPT file
        
    Returns:
        Dictionary with PPT information including slide count and animations
    """
    try:
        ppt_path = str(validators.validate_ppt_file(ppt_path))
        
        result = {
            "status": "success",
            "ppt_path": ppt_path,
            "file_size": os.path.getsize(ppt_path),
            "file_format": Path(ppt_path).suffix,
        }
        
        # Use PPTService to read PPT via COM
        ppt_service = PPTService()
        
        try:
            # Open presentation
            if not ppt_service.open_presentation(ppt_path):
                return {
                    "status": "error",
                    "message": "Failed to open PPT file - ensure PowerPoint is installed",
                }
            
            # Get slide count
            slide_count = ppt_service.get_slide_count()
            result["slide_count"] = slide_count
            
            # Get animation info for each slide
            result["slides"] = []
            for slide_idx in range(slide_count):
                anim_seq = ppt_service.get_slide_animations(slide_idx)
                
                if anim_seq:
                    slide_info = {
                        "index": slide_idx,
                        "animation_count": len(anim_seq.animations),
                        "animations": [
                            {
                                "animation_id": anim.animation_id,
                                "effect_type": anim.effect_type,
                                "object_name": anim.object_name,
                                "shape_text": anim.shape_text[:50] if anim.shape_text else None,
                                "trigger_type": anim.trigger_type,
                                "trigger_delay_time": anim.trigger_delay_time,
                                "duration": anim.duration,
                            }
                            for anim in anim_seq.animations
                        ],
                    }
                else:
                    slide_info = {
                        "index": slide_idx,
                        "animation_count": 0,
                        "animations": [],
                    }
                
                result["slides"].append(slide_info)
            
            logger.info(f"Inspected PPT: {ppt_path} ({slide_count} slides)")
            return result
        finally:
            ppt_service.close_presentation()
            ppt_service.quit()
    except Exception as e:
        logger.error(f"Failed to inspect PPT: {e}")
        return {
            "status": "error",
            "message": str(e),
        }
