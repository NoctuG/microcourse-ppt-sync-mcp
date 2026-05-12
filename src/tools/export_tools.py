"""Export tools for MCP."""

from pathlib import Path
from typing import Dict, Any
from src.utils import get_logger, validators
from src.services import PPTService


logger = get_logger(__name__)


def export_ppt_video(
    ppt_path: str,
    output_path: str,
    quality: str = "HD",
    fps: int = 30,
) -> Dict[str, Any]:
    """Export PPT as video.
    
    Args:
        ppt_path: Path to PPT file
        output_path: Output video file path
        quality: Video quality (LD, SD, HD)
        fps: Frames per second
        
    Returns:
        Dictionary with result information
    """
    try:
        ppt_path = str(validators.validate_ppt_file(ppt_path))
        
        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize PPT service
        ppt_service = PPTService()
        
        # Open presentation
        if not ppt_service.open_presentation(ppt_path):
            return {
                "status": "error",
                "message": "Failed to open PPT file",
            }
        
        try:
            # Export video
            if not ppt_service.export_video(output_path, quality, fps):
                return {
                    "status": "error",
                    "message": "Failed to export video",
                }
            
            # Check if output file exists
            if not Path(output_path).exists():
                return {
                    "status": "error",
                    "message": "Output video file was not created",
                }
            
            result = {
                "status": "success",
                "output_path": str(output_path),
                "quality": quality,
                "fps": fps,
                "file_size": Path(output_path).stat().st_size,
            }
            
            logger.info(f"Exported video: {output_path}")
            return result
        finally:
            ppt_service.close_presentation()
            ppt_service.quit()
    except Exception as e:
        logger.error(f"Failed to export video: {e}")
        return {
            "status": "error",
            "message": str(e),
        }
