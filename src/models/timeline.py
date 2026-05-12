"""Timeline data models."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class AnimationType(Enum):
    """Animation type enumeration."""
    APPEAR = "appear"
    DISAPPEAR = "disappear"
    EMPHASIS = "emphasis"
    EXIT = "exit"
    MOTION_PATH = "motion_path"


@dataclass
class Animation:
    """Animation definition."""
    animation_index: int
    animation_type: AnimationType
    trigger_time: float  # seconds from slide start
    duration: float = 0.5  # animation duration in seconds
    object_name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "animation_index": self.animation_index,
            "animation_type": self.animation_type.value,
            "trigger_time": self.trigger_time,
            "duration": self.duration,
            "object_name": self.object_name,
            "metadata": self.metadata,
        }


@dataclass
class Slide:
    """Slide definition with animations."""
    slide_index: int
    animations: List[Animation] = field(default_factory=list)
    advance_time: Optional[float] = None  # auto advance time in seconds
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "slide_index": self.slide_index,
            "animations": [anim.to_dict() for anim in self.animations],
            "advance_time": self.advance_time,
            "notes": self.notes,
            "metadata": self.metadata,
        }


@dataclass
class Timeline:
    """Timeline definition for a lesson."""
    lesson_name: str
    slides: List[Slide] = field(default_factory=list)
    total_duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "lesson_name": self.lesson_name,
            "slides": [slide.to_dict() for slide in self.slides],
            "total_duration": self.total_duration,
            "metadata": self.metadata,
        }
    
    def get_total_duration(self) -> float:
        """Calculate total duration from slide advance times.

        Returns the explicit total_duration when set, otherwise sums slide
        advance_time values for compatibility with unit tests and reports.
        """
        if self.total_duration:
            return self.total_duration
        return sum(slide.advance_time or 0.0 for slide in self.slides)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Timeline":
        """Create Timeline from dictionary."""
        timeline = cls(
            lesson_name=data.get("lesson_name", ""),
            total_duration=data.get("total_duration", 0.0),
            metadata=data.get("metadata", {}),
        )
        
        for slide_data in data.get("slides", []):
            slide = Slide(
                slide_index=slide_data["slide_index"],
                advance_time=slide_data.get("advance_time"),
                notes=slide_data.get("notes", ""),
                metadata=slide_data.get("metadata", {}),
            )
            
            for anim_data in slide_data.get("animations", []):
                animation = Animation(
                    animation_index=anim_data["animation_index"],
                    animation_type=AnimationType(anim_data["animation_type"]),
                    trigger_time=anim_data["trigger_time"],
                    duration=anim_data.get("duration", 0.5),
                    object_name=anim_data.get("object_name"),
                    metadata=anim_data.get("metadata", {}),
                )
                slide.animations.append(animation)
            
            timeline.slides.append(slide)
        
        return timeline
