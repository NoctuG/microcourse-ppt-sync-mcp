"""Video service for video operations."""

import subprocess
from pathlib import Path
from typing import Optional, List
from src.utils import get_logger


logger = get_logger(__name__)


class VideoService:
    """Service for video operations."""
    
    @staticmethod
    def check_ffmpeg() -> bool:
        """Check if FFmpeg is available.
        
        Returns:
            True if FFmpeg is available, False otherwise
        """
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True,
                timeout=5,
            )
            logger.info("FFmpeg is available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("FFmpeg is not available")
            return False
    
    @staticmethod
    def compose_videos(
        ppt_bg_video: str,
        presenter_video: str,
        audio_file: str,
        output_path: str,
        preset: str = "medium",
    ) -> bool:
        """Compose PPT background video with presenter video and audio.
        
        Args:
            ppt_bg_video: Path to PPT background video
            presenter_video: Path to presenter video (with alpha channel)
            audio_file: Path to audio file
            output_path: Output video file path
            preset: FFmpeg preset (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = str(Path(output_path).absolute())
            
            # FFmpeg command for compositing
            cmd = [
                "ffmpeg",
                "-i", str(Path(ppt_bg_video).absolute()),
                "-i", str(Path(presenter_video).absolute()),
                "-i", str(Path(audio_file).absolute()),
                "-filter_complex", "[0:v][1:v]overlay=x=10:y=10[v]",
                "-map", "[v]",
                "-map", "2:a",
                "-c:v", "libx264",
                "-preset", preset,
                "-c:a", "aac",
                output_path,
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            
            if result.returncode == 0:
                logger.info(f"Successfully composed video to: {output_path}")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Failed to compose videos: {e}")
            return False
    
    @staticmethod
    def extract_audio(
        video_path: str,
        output_path: str,
        format: str = "wav",
    ) -> bool:
        """Extract audio from video.
        
        Args:
            video_path: Path to video file
            output_path: Output audio file path
            format: Audio format (wav, mp3, aac)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = str(Path(output_path).absolute())
            
            cmd = [
                "ffmpeg",
                "-i", str(Path(video_path).absolute()),
                "-q:a", "0",
                "-map", "a",
                output_path,
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info(f"Successfully extracted audio to: {output_path}")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Failed to extract audio: {e}")
            return False
    
    @staticmethod
    def get_video_duration(video_path: str) -> Optional[float]:
        """Get video duration in seconds.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Duration in seconds or None if failed
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1:nokey=1",
                str(Path(video_path).absolute()),
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                logger.info(f"Video duration: {duration:.2f} seconds")
                return duration
            else:
                logger.error(f"FFprobe error: {result.stderr}")
                return None
        except Exception as e:
            logger.error(f"Failed to get video duration: {e}")
            return None
