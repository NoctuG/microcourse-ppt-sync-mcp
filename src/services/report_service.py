"""Report service for generating sync reports."""

from pathlib import Path
from typing import Optional
from src.utils import get_logger
from src.models import SyncReport, SyncIssue, Timeline


logger = get_logger(__name__)


class ReportService:
    """Service for report generation."""
    
    @staticmethod
    def generate_sync_report(timeline: Timeline) -> SyncReport:
        """Generate sync report from timeline.
        
        Args:
            timeline: Timeline object
            
        Returns:
            SyncReport object
        """
        report = SyncReport(
            lesson_name=timeline.lesson_name,
            total_slides=len(timeline.slides),
            total_animations=sum(len(slide.animations) for slide in timeline.slides),
            total_duration=timeline.total_duration,
        )
        
        # Validate timeline and add issues
        for slide_idx, slide in enumerate(timeline.slides):
            if not slide.animations:
                issue = SyncIssue(
                    slide_index=slide_idx,
                    issue_type="no_animations",
                    description="幻灯片没有动画",
                    severity="info",
                )
                report.issues.append(issue)
            
            # Check for timing conflicts
            animation_times = []
            for anim in slide.animations:
                anim_end = anim.trigger_time + anim.duration
                
                # Check overlap with previous animations
                for prev_time in animation_times:
                    if anim.trigger_time < prev_time[1]:
                        issue = SyncIssue(
                            slide_index=slide_idx,
                            issue_type="timing_overlap",
                            description=f"动画 {anim.animation_index} 与前一个动画时间重叠",
                            severity="warning",
                        )
                        report.issues.append(issue)
                        break
                
                animation_times.append((anim.trigger_time, anim_end))
            
            # Check if advance time is sufficient
            if slide.animations and slide.advance_time:
                max_anim_end = max(anim.trigger_time + anim.duration for anim in slide.animations)
                if max_anim_end > slide.advance_time:
                    issue = SyncIssue(
                        slide_index=slide_idx,
                        issue_type="insufficient_advance_time",
                        description=f"幻灯片翻页时间 {slide.advance_time}s 不足以完成所有动画（需要 {max_anim_end}s）",
                        severity="warning",
                    )
                    report.issues.append(issue)
        
        logger.info(f"Generated sync report with {len(report.issues)} issues")
        return report
    
    @staticmethod
    def save_report_to_markdown(report: SyncReport, output_path: str) -> bool:
        """Save report to Markdown file.
        
        Args:
            report: SyncReport object
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = str(Path(output_path).absolute())
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report.to_markdown())
            
            logger.info(f"Saved report to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            return False
