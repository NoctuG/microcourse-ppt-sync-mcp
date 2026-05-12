"""PowerPoint service for PPT manipulation."""

import os
import time
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
        """Get animations for a specific slide using COM.
        
        Args:
            slide_index: Zero-based slide index
            
        Returns:
            AnimationSequence object with detailed animation info
        """
        if not self.presentation:
            logger.error("No presentation is open")
            return None
        
        try:
            slide = self.presentation.Slides(slide_index + 1)
            sequence = AnimationSequence(slide_index=slide_index)
            
            # Get slide properties
            sequence.slide_count = self.presentation.Slides.Count
            
            # Get main animation sequence
            if hasattr(slide, "TimeLine") and hasattr(slide.TimeLine, "MainSequence"):
                main_seq = slide.TimeLine.MainSequence
                
                for i in range(main_seq.Count):
                    effect = main_seq(i + 1)
                    
                    # Extract animation details
                    try:
                        shape_name = effect.Shape.Name if hasattr(effect, "Shape") else "Unknown"
                        shape_text = ""
                        if hasattr(effect, "Shape") and hasattr(effect.Shape, "TextFrame"):
                            if hasattr(effect.Shape.TextFrame, "TextRange"):
                                shape_text = effect.Shape.TextFrame.TextRange.Text[:100]
                        
                        # Get trigger type
                        trigger_type = "unknown"
                        if hasattr(effect, "Timing"):
                            tt = effect.Timing.TriggerType
                            trigger_map = {
                                1: "on_click",
                                2: "with_previous",
                                3: "after_previous",
                                4: "on_bookmark",
                            }
                            trigger_type = trigger_map.get(tt, f"type_{tt}")
                        
                        anim = PPTAnimation(
                            animation_id=i,
                            effect_type=effect.Name if hasattr(effect, "Name") else "Unknown",
                            trigger_delay_time=effect.Timing.TriggerDelayTime if hasattr(effect, "Timing") else 0.0,
                            duration=effect.Timing.Duration if hasattr(effect, "Timing") else 0.5,
                            object_name=shape_name,
                            shape_text=shape_text,
                            trigger_type=trigger_type,
                        )
                        sequence.animations.append(anim)
                    except Exception as e:
                        logger.warning(f"Failed to extract animation {i} details: {e}")
                        continue
            
            logger.info(f"Retrieved {len(sequence.animations)} animations from slide {slide_index + 1}")
            return sequence
        except Exception as e:
            logger.error(f"Failed to get slide animations: {e}")
            return None
    
    def apply_timeline_to_slide(self, slide_index: int, slide_timeline: Slide) -> bool:
        """Apply timeline to a specific slide.
        
        Fixes:
        - AdvanceTime uses seconds (not milliseconds)
        - All animations set to TriggerType = WithPrevious (2)
        - TriggerDelayTime uses page-local time
        - Duration in seconds
        
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
                        
                        # Set trigger type to "With Previous" for all animations
                        if hasattr(effect, "Timing"):
                            effect.Timing.TriggerType = 2  # msoAnimTriggerWithPrevious
                            
                            # Set trigger delay time (page-local time in seconds)
                            effect.Timing.TriggerDelayTime = animation.trigger_time
                            
                            # Set duration (in seconds)
                            effect.Timing.Duration = animation.duration
                            
                            logger.debug(
                                f"Slide {slide_index + 1}, Animation {i}: "
                                f"trigger_time={animation.trigger_time}s, duration={animation.duration}s"
                            )
            
            # Set slide advance time (in seconds, not milliseconds)
            if slide_timeline.advance_time is not None:
                slide.SlideShowTransition.AdvanceOnTime = -1  # msoTrue
                slide.SlideShowTransition.AdvanceTime = slide_timeline.advance_time
                
                logger.debug(f"Slide {slide_index + 1}: advance_time={slide_timeline.advance_time}s")
            
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
    
    def export_video(
        self,
        output_path: str,
        quality: str = "HD",
        fps: int = 30,
        vertical_res: int = 1080,
    ) -> bool:
        """Export presentation as video.
        
        Fixes:
        - Correct CreateVideo parameter order
        - Proper async handling with CreateVideoStatus polling
        - Default to 1080p / 30fps / quality 90
        
        Args:
            output_path: Output video file path
            quality: Video quality (LD, SD, HD)
            fps: Frames per second
            vertical_res: Vertical resolution in pixels (default 1080)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.presentation:
            logger.error("No presentation is open")
            return False
        
        try:
            output_path = str(Path(output_path).absolute())
            
            # Map quality to PowerPoint quality value (0-100)
            quality_map = {"LD": 50, "SD": 70, "HD": 90}
            quality_value = quality_map.get(quality, 90)
            
            logger.info(
                f"Starting video export: {output_path} "
                f"(quality={quality_value}, fps={fps}, res={vertical_res}p)"
            )
            
            # PowerPoint CreateVideo signature (correct parameter order):
            # CreateVideo(Filename, UseTimingsAndNarrations, DefaultSlideDuration, VertResolution, FramesPerSecond, Quality)
            self.presentation.CreateVideo(
                output_path,
                True,           # UseTimingsAndNarrations - use slide timings and narrations
                5,              # DefaultSlideDuration - default slide duration in seconds
                vertical_res,   # VertResolution - vertical resolution
                fps,            # FramesPerSecond
                quality_value,  # Quality (0-100)
            )
            
            # Poll for completion status
            # PowerPoint video export is asynchronous, need to wait for completion
            max_wait_time = 3600  # 1 hour timeout
            poll_interval = 2  # Check every 2 seconds
            elapsed = 0
            
            logger.info("Waiting for video export to complete...")
            
            while elapsed < max_wait_time:
                try:
                    # Check if CreateVideoStatus indicates completion
                    # 0 = Not started, 1 = In progress, 2 = Succeeded, 3 = Failed
                    status = self.presentation.CreateVideoStatus
                    
                    if status == 2:  # Succeeded
                        logger.info(f"Video export completed successfully: {output_path}")
                        return True
                    elif status == 3:  # Failed
                        logger.error(f"Video export failed with status code 3")
                        return False
                    elif status == 1:  # In progress
                        logger.debug(f"Video export in progress... ({elapsed}s elapsed)")
                    
                    time.sleep(poll_interval)
                    elapsed += poll_interval
                except AttributeError:
                    # If CreateVideoStatus is not available, wait and check file
                    logger.debug("CreateVideoStatus not available, checking file existence...")
                    time.sleep(2)
                    if Path(output_path).exists():
                        file_size = Path(output_path).stat().st_size
                        if file_size > 0:
                            logger.info(f"Video export completed: {output_path} ({file_size} bytes)")
                            return True
                    elapsed += 2
            
            logger.error(f"Video export timeout after {max_wait_time} seconds")
            return False
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
