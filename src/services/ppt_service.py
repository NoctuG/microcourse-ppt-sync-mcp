"""PowerPoint service for PPT manipulation."""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from src.utils import get_logger
from src.models import PPTAnimation, AnimationSequence, Timeline, Slide


logger = get_logger(__name__)


class PPTService:
    """Service for PowerPoint operations."""
    
    def __init__(self):
        """Initialize PPT service."""
        self.ppt_app = None
        self.presentation = None
        self._initialize_com()
    
    def _initialize_com(self) -> None:
        """Initialize COM interface for PowerPoint.
        
        This requires Windows and Microsoft PowerPoint to be installed.
        """
        try:
            import win32com.client
            self.win32com = win32com.client
            logger.info("COM interface initialized for PowerPoint")
        except ImportError:
            logger.warning("pywin32 not available - PPT operations will be limited")
            self.win32com = None
    
    def open_presentation(self, ppt_path: str) -> bool:
        """Open a PowerPoint presentation.
        
        Args:
            ppt_path: Path to PPT file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.win32com:
            logger.error("Cannot open presentation: pywin32 not available")
            return False
        
        try:
            if not self.ppt_app:
                self.ppt_app = self.win32com.client.Dispatch("PowerPoint.Application")
                self.ppt_app.Visible = True
            
            ppt_path = str(Path(ppt_path).absolute())
            self.presentation = self.ppt_app.Presentations.Open(
                ppt_path,
                msoTrue := -1,  # msoTrue
                msoTrue,  # msoTrue
                1  # ppOpenNormal
            )
            logger.info(f"Opened presentation: {ppt_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to open presentation: {e}")
            return False
    
    def close_presentation(self, save: bool = False) -> bool:
        """Close the current presentation.
        
        Args:
            save: Whether to save before closing
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.presentation:
                if save:
                    self.presentation.Save()
                self.presentation.Close()
                self.presentation = None
                logger.info("Presentation closed")
            return True
        except Exception as e:
            logger.error(f"Failed to close presentation: {e}")
            return False
    
    def get_slide_count(self) -> int:
        """Get the number of slides in the presentation.
        
        Returns:
            Number of slides
        """
        if not self.presentation:
            logger.error("No presentation is open")
            return 0
        
        try:
            return self.presentation.Slides.Count
        except Exception as e:
            logger.error(f"Failed to get slide count: {e}")
            return 0
    
    def get_slide_animations(self, slide_index: int) -> Optional[AnimationSequence]:
        """Get animations for a specific slide.
        
        Args:
            slide_index: Zero-based slide index
            
        Returns:
            AnimationSequence object or None
        """
        if not self.presentation:
            logger.error("No presentation is open")
            return None
        
        try:
            slide = self.presentation.Slides(slide_index + 1)
            sequence = AnimationSequence(slide_index=slide_index)
            
            # Get main animation sequence
            if hasattr(slide, "TimeLine") and hasattr(slide.TimeLine, "MainSequence"):
                main_seq = slide.TimeLine.MainSequence
                
                for i, effect in enumerate(main_seq):
                    anim = PPTAnimation(
                        animation_id=i,
                        effect_type=effect.Name if hasattr(effect, "Name") else "Unknown",
                        trigger_delay_time=0.0,  # Will be set from timeline
                        duration=effect.Duration if hasattr(effect, "Duration") else 0.5,
                        object_name=effect.Shape.Name if hasattr(effect, "Shape") else None,
                    )
                    sequence.animations.append(anim)
            
            logger.info(f"Retrieved {len(sequence.animations)} animations from slide {slide_index + 1}")
            return sequence
        except Exception as e:
            logger.error(f"Failed to get slide animations: {e}")
            return None
    
    def apply_timeline_to_slide(self, slide_index: int, slide_timeline: Slide) -> bool:
        """Apply timeline to a specific slide.
        
        Args:
            slide_index: Zero-based slide index
            slide_timeline: Slide timeline with animation timings
            
        Returns:
            True if successful, False otherwise
        """
        if not self.presentation:
            logger.error("No presentation is open")
            return False
        
        try:
            slide = self.presentation.Slides(slide_index + 1)
            
            # Apply animation timings
            if hasattr(slide, "TimeLine") and hasattr(slide.TimeLine, "MainSequence"):
                main_seq = slide.TimeLine.MainSequence
                
                for i, animation in enumerate(slide_timeline.animations):
                    if i < main_seq.Count:
                        effect = main_seq(i + 1)
                        
                        # Set trigger delay time
                        if hasattr(effect, "Timing"):
                            effect.Timing.TriggerDelayTime = animation.trigger_time
                            effect.Timing.Duration = animation.duration
            
            # Set slide advance time
            if slide_timeline.advance_time is not None:
                slide.SlideShowTransition.AdvanceTime = int(slide_timeline.advance_time * 1000)
                slide.SlideShowTransition.AdvanceOnTime = -1  # msoTrue
            
            logger.info(f"Applied timeline to slide {slide_index + 1}")
            return True
        except Exception as e:
            logger.error(f"Failed to apply timeline to slide: {e}")
            return False
    
    def save_presentation(self, output_path: str) -> bool:
        """Save presentation to a file.
        
        Args:
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        if not self.presentation:
            logger.error("No presentation is open")
            return False
        
        try:
            output_path = str(Path(output_path).absolute())
            self.presentation.SaveAs(output_path)
            logger.info(f"Saved presentation to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save presentation: {e}")
            return False
    
    def export_video(self, output_path: str, quality: str = "HD", fps: int = 30) -> bool:
        """Export presentation as video.
        
        Args:
            output_path: Output video file path
            quality: Video quality (LD, SD, HD)
            fps: Frames per second
            
        Returns:
            True if successful, False otherwise
        """
        if not self.presentation:
            logger.error("No presentation is open")
            return False
        
        try:
            output_path = str(Path(output_path).absolute())
            
            # Map quality to vertical resolution
            quality_map = {
                "LD": 360,
                "SD": 480,
                "HD": 720,
            }
            vertical_res = quality_map.get(quality, 720)
            
            # CreateVideo method signature:
            # Presentation.CreateVideo(Filename, [Width], [Height], [Quality], [FPS], [UseTimings], [UseNarrations], [StartingSlide], [EndingSlide])
            self.presentation.CreateVideo(
                output_path,
                1280,  # Width
                vertical_res,  # Height
                fps,  # FPS
                True,  # Use timings
                True,  # Use narrations
            )
            
            logger.info(f"Exported video to: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export video: {e}")
            return False
    
    def quit(self) -> None:
        """Quit PowerPoint application."""
        try:
            if self.ppt_app:
                self.ppt_app.Quit()
                self.ppt_app = None
                logger.info("PowerPoint application closed")
        except Exception as e:
            logger.error(f"Failed to quit PowerPoint: {e}")
