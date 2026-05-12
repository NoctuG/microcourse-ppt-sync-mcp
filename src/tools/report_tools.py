"""Report tools for MCP."""

from pathlib import Path
from typing import Dict, Any
from src.utils import get_logger, validators
from src.services import TimelineService, ReportService


logger = get_logger(__name__)


def generate_sync_report(
    project_path: str,
    timeline_path: str,
    output_path: str,
) -> Dict[str, Any]:
    """Generate sync report.
    
    Args:
        project_path: Path to project directory
        timeline_path: Path to timeline JSON file
        output_path: Output report file path
        
    Returns:
        Dictionary with result information
    """
    try:
        project_path = str(validators.validate_project_path(project_path))
        
        # Load timeline
        timeline = TimelineService.load_timeline_from_json(timeline_path)
        if not timeline:
            return {
                "status": "error",
                "message": "Failed to load timeline",
            }
        
        # Generate report
        report = ReportService.generate_sync_report(timeline)
        
        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save report
        if not ReportService.save_report_to_markdown(report, output_path):
            return {
                "status": "error",
                "message": "Failed to save report",
            }
        
        result = {
            "status": "success",
            "output_path": str(output_path),
            "lesson_name": report.lesson_name,
            "total_slides": report.total_slides,
            "total_animations": report.total_animations,
            "total_duration": report.total_duration,
            "issue_count": len(report.issues),
            "issues": [
                {
                    "slide_index": issue.slide_index,
                    "issue_type": issue.issue_type,
                    "description": issue.description,
                    "severity": issue.severity,
                }
                for issue in report.issues
            ],
        }
        
        logger.info(f"Generated sync report: {output_path}")
        return result
    except Exception as e:
        logger.error(f"Failed to generate sync report: {e}")
        return {
            "status": "error",
            "message": str(e),
        }
