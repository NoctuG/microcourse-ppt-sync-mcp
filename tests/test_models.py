"""Unit tests for data models."""

import unittest
from src.models import PPTAnimation, AnimationSequence, Timeline, Slide


class TestPPTAnimation(unittest.TestCase):
    """Test PPTAnimation model."""
    
    def test_animation_creation(self):
        """Test creating a PPT animation."""
        anim = PPTAnimation(
            animation_id=0,
            effect_type="Appear",
            trigger_delay_time=0.0,
            duration=0.5,
            object_name="Title",
        )
        
        self.assertEqual(anim.animation_id, 0)
        self.assertEqual(anim.effect_type, "Appear")
        self.assertEqual(anim.trigger_delay_time, 0.0)
        self.assertEqual(anim.duration, 0.5)
        self.assertEqual(anim.object_name, "Title")
    
    def test_animation_to_dict(self):
        """Test converting animation to dictionary."""
        anim = PPTAnimation(
            animation_id=0,
            effect_type="Appear",
            trigger_delay_time=0.0,
            duration=0.5,
            object_name="Title",
            shape_text="Welcome",
            trigger_type="on_click",
        )
        
        anim_dict = anim.to_dict()
        
        self.assertEqual(anim_dict["animation_id"], 0)
        self.assertEqual(anim_dict["effect_type"], "Appear")
        self.assertEqual(anim_dict["object_name"], "Title")
        self.assertEqual(anim_dict["shape_text"], "Welcome")
        self.assertEqual(anim_dict["trigger_type"], "on_click")


class TestAnimationSequence(unittest.TestCase):
    """Test AnimationSequence model."""
    
    def test_sequence_creation(self):
        """Test creating an animation sequence."""
        seq = AnimationSequence(slide_index=0)
        
        self.assertEqual(seq.slide_index, 0)
        self.assertEqual(len(seq.animations), 0)
    
    def test_sequence_with_animations(self):
        """Test animation sequence with animations."""
        anim1 = PPTAnimation(
            animation_id=0,
            effect_type="Appear",
            trigger_delay_time=0.0,
            duration=0.5,
            object_name="Title",
        )
        anim2 = PPTAnimation(
            animation_id=1,
            effect_type="Appear",
            trigger_delay_time=1.0,
            duration=0.5,
            object_name="Subtitle",
        )
        
        seq = AnimationSequence(slide_index=0)
        seq.animations.append(anim1)
        seq.animations.append(anim2)
        
        self.assertEqual(len(seq.animations), 2)
        self.assertEqual(seq.get_max_end_time(), 1.5)
    
    def test_sequence_to_dict(self):
        """Test converting sequence to dictionary."""
        anim = PPTAnimation(
            animation_id=0,
            effect_type="Appear",
            trigger_delay_time=0.0,
            duration=0.5,
            object_name="Title",
        )
        
        seq = AnimationSequence(slide_index=0, advance_time=5.0, slide_count=10)
        seq.animations.append(anim)
        
        seq_dict = seq.to_dict()
        
        self.assertEqual(seq_dict["slide_index"], 0)
        self.assertEqual(seq_dict["advance_time"], 5.0)
        self.assertEqual(seq_dict["slide_count"], 10)
        self.assertEqual(len(seq_dict["animations"]), 1)


class TestSlide(unittest.TestCase):
    """Test Slide model."""
    
    def test_slide_creation(self):
        """Test creating a slide."""
        slide = Slide(slide_index=0)
        
        self.assertEqual(slide.slide_index, 0)
        self.assertEqual(len(slide.animations), 0)
    
    def test_slide_with_animations(self):
        """Test slide with animations."""
        anim = PPTAnimation(
            animation_id=0,
            effect_type="Appear",
            trigger_delay_time=0.0,
            duration=0.5,
            object_name="Content",
        )
        
        slide = Slide(slide_index=0, advance_time=5.0)
        slide.animations.append(anim)
        
        self.assertEqual(len(slide.animations), 1)
        self.assertEqual(slide.advance_time, 5.0)


class TestTimeline(unittest.TestCase):
    """Test Timeline model."""
    
    def test_timeline_creation(self):
        """Test creating a timeline."""
        timeline = Timeline(lesson_name="Python 101")
        
        self.assertEqual(timeline.lesson_name, "Python 101")
        self.assertEqual(len(timeline.slides), 0)
    
    def test_timeline_with_slides(self):
        """Test timeline with slides."""
        slide1 = Slide(slide_index=0, advance_time=5.0)
        slide2 = Slide(slide_index=1, advance_time=6.0)
        
        timeline = Timeline(lesson_name="Python 101")
        timeline.slides.append(slide1)
        timeline.slides.append(slide2)
        
        self.assertEqual(len(timeline.slides), 2)
        self.assertEqual(timeline.get_total_duration(), 11.0)
    
    def test_timeline_to_dict(self):
        """Test converting timeline to dictionary."""
        slide = Slide(slide_index=0, advance_time=5.0)
        anim = PPTAnimation(
            animation_id=0,
            effect_type="Appear",
            trigger_delay_time=0.0,
            duration=0.5,
            object_name="Title",
        )
        slide.animations.append(anim)
        
        timeline = Timeline(lesson_name="Python 101")
        timeline.slides.append(slide)
        
        timeline_dict = timeline.to_dict()
        
        self.assertEqual(timeline_dict["lesson_name"], "Python 101")
        self.assertEqual(len(timeline_dict["slides"]), 1)


if __name__ == "__main__":
    unittest.main()
