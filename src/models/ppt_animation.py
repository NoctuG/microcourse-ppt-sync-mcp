"""PPT animation models."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class PPTAnimation:
    """PPT animation object."""
    animation_id: int
    effect_type: str  # e.g., "Appear", "Emphasis", "Exit"
    trigger_delay_time: float  # in seconds
    duration: float  # in seconds
    object_name: Optional[str] = None
    shape_text: Optional[str] = None  # Text content of the shape
    trigger_type: Optional[str] = None  # e.g., "on_click", "with_previous"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "animation_id": self.animation_id,
            "effect_type": self.effect_type,
            "trigger_delay_time": self.trigger_delay_time,
            "duration": self.duration,
            "object_name": self.object_name,
            "shape_text": self.shape_text,
            "trigger_type": self.trigger_type,
            "metadata": self.metadata,
        }


@dataclass
class AnimationSequence:
    """Animation sequence for a slide."""
    slide_index: int
    animations: List[PPTAnimation] = field(default_factory=list)
    advance_time: Optional[float] = None  # auto advance time in seconds
    slide_count: Optional[int] = None  # total slide count in presentation
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "slide_index": self.slide_index,
            "animations": [anim.to_dict() for anim in self.animations],
            "advance_time": self.advance_time,
            "slide_count": self.slide_count,
            "metadata": self.metadata,
        }
    
    def get_max_end_time(self) -> float:
        """Get the maximum end time of all animations.
        
        Returns:
            Maximum end time in seconds
        """
        if not self.animations:
            return 0.0
        
        max_time = 0.0
        for anim in self.animations:
            end_time = anim.trigger_delay_time + anim.duration
            max_time = max(max_time, end_time)
        
        return max_time
