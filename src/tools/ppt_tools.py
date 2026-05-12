"""PPT tools for MCP."""

import json
from pathlib import Path
from typing import Dict, Any
from src.utils import get_logger, validators
from src.services import PPTService, TimelineService


logger = get_logger(__name__)


def apply_ppt_timeline(
    project_path: str,
    ppt_path: str,
    timeline_path: str,
) -> Dict[str, Any]:
    """Apply timeline to PPT.
    
    Args:
        project_path: Path to project directory
        ppt_path: Path to PPT file
        timeline_path: Path to timeline JSON file
        
    Returns:
        Dictionary with result information
    """
    try:
        project_path = str(validators.validate_project_path(project_path))
        ppt_path = str(validators.validate_ppt_file(ppt_path))
        
        # Load timeline
        timeline = TimelineService.load_timeline_from_json(timeline_path)
        if not timeline:
            return {
                "status": "error",
                "message": "Failed to load timeline",
            }
        
        # Initialize PPT service
        ppt_service = PPTService()
        
        # Open presentation
        if not ppt_service.open_presentation(ppt_path):
            return {
                "status": "error",
                "message": "Failed to open PPT file",
            }
        
        try:
            # Apply timeline to each slide
            for slide in timeline.slides:
                if not ppt_service.apply_timeline_to_slide(slide.slide_index, slide):
                    logger.warning(f"Failed to apply timeline to slide {slide.slide_index + 1}")
            
            # Save modified presentation
            work_dir = Path(project_path) / "work"
            work_dir.mkdir(exist_ok=True)
            
            output_path = work_dir / "lesson_timed.pptx"
            if not ppt_service.save_presentation(str(output_path)):
                return {
                    "status": "error",
                    "message": "Failed to save modified PPT",
                }
            
            result = {
                "status": "success",
                "output_path": str(output_path),
                "slides_processed": len(timeline.slides),
                "total_animations": sum(len(slide.animations) for slide in timeline.slides),
            }
            
            logger.info(f"Applied timeline to PPT: {output_path}")
            return result
        finally:
            ppt_service.close_presentation()
            ppt_service.quit()
    except Exception as e:
        logger.error(f"Failed to apply timeline to PPT: {e}")
        return {
            "status": "error",
            "message": str(e),
        }
