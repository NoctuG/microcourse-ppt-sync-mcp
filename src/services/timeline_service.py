"""Timeline service for parsing and managing timelines."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.utils import get_logger
from src.models import Timeline, Slide, Animation, AnimationType


logger = get_logger(__name__)


class TimelineService:
    """Service for timeline operations."""
    
    @staticmethod
    def load_timeline_from_json(json_path: str) -> Optional[Timeline]:
        """Load timeline from JSON file.
        
        Args:
            json_path: Path to timeline JSON file
            
        Returns:
            Timeline object or None if failed
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            timeline = Timeline.from_dict(data)
            logger.info(f"Loaded timeline from: {json_path}")
            return timeline
        except Exception as e:
            logger.error(f"Failed to load timeline from JSON: {e}")
            return None
    
    @staticmethod
    def save_timeline_to_json(timeline: Timeline, output_path: str) -> bool:
        """Save timeline to JSON file.
        
        Args:
            timeline: Timeline object
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = str(Path(output_path).absolute())
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(timeline.to_dict(), f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved timeline to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save timeline to JSON: {e}")
            return False
    
    @staticmethod
    def parse_transcript_to_timeline(
        transcript: Dict[str, Any],
        slide_count: int,
        default_slide_duration: float = 5.0,
    ) -> Optional[Timeline]:
        """Parse transcript to timeline.
        
        Args:
            transcript: Transcript data with segments
            slide_count: Number of slides in presentation
            default_slide_duration: Default duration per slide in seconds
            
        Returns:
            Timeline object or None if failed
        """
        try:
            timeline = Timeline(
                lesson_name=transcript.get("lesson_name", "Untitled"),
                metadata=transcript.get("metadata", {}),
            )
            
            segments = transcript.get("segments", [])
            
            # Distribute segments across slides
            if not segments:
                logger.warning("No segments in transcript")
                # Create empty slides
                for i in range(slide_count):
                    slide = Slide(
                        slide_index=i,
                        advance_time=default_slide_duration,
                    )
                    timeline.slides.append(slide)
            else:
                # Group segments by slide
                segment_idx = 0
                for slide_idx in range(slide_count):
                    slide = Slide(slide_index=slide_idx)
                    
                    slide_start_time = 0.0
                    slide_end_time = 0.0
                    
                    # Collect segments for this slide
                    while segment_idx < len(segments):
                        segment = segments[segment_idx]
                        segment_start = segment.get("start", 0.0)
                        segment_end = segment.get("end", 0.0)
                        
                        # Create animation for this segment
                        animation = Animation(
                            animation_index=len(slide.animations),
                            animation_type=AnimationType.APPEAR,
                            trigger_time=segment_start - slide_start_time,
                            duration=0.3,
                            metadata={
                                "text": segment.get("text", ""),
                                "segment_index": segment_idx,
                            },
                        )
                        slide.animations.append(animation)
                        
                        slide_end_time = max(slide_end_time, segment_end - slide_start_time)
                        segment_idx += 1
                        
                        # Move to next slide if we've covered enough time
                        if slide_end_time >= default_slide_duration:
                            break
                    
                    # Set advance time
                    slide.advance_time = max(slide_end_time, default_slide_duration)
                    timeline.slides.append(slide)
            
            # Calculate total duration
            timeline.total_duration = sum(slide.advance_time or 0.0 for slide in timeline.slides)
            
            logger.info(f"Parsed transcript to timeline with {len(timeline.slides)} slides")
            return timeline
        except Exception as e:
            logger.error(f"Failed to parse transcript to timeline: {e}")
            return None
    
    @staticmethod
    def merge_timelines(timelines: List[Timeline]) -> Optional[Timeline]:
        """Merge multiple timelines into one.
        
        Args:
            timelines: List of Timeline objects
            
        Returns:
            Merged Timeline object or None if failed
        """
        try:
            if not timelines:
                return None
            
            merged = Timeline(
                lesson_name=timelines[0].lesson_name + " (Merged)",
                metadata={"merged_from": len(timelines)},
            )
            
            for timeline in timelines:
                merged.slides.extend(timeline.slides)
            
            # Recalculate slide indices
            for i, slide in enumerate(merged.slides):
                slide.slide_index = i
            
            # Calculate total duration
            merged.total_duration = sum(slide.advance_time or 0.0 for slide in merged.slides)
            
            logger.info(f"Merged {len(timelines)} timelines")
            return merged
        except Exception as e:
            logger.error(f"Failed to merge timelines: {e}")
            return None
