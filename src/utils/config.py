"""Configuration management."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the MCP server."""
    
    DEFAULT_CONFIG = {
        "ppt_video_quality": "HD",  # HD, SD, LD
        "ppt_video_fps": 30,
        "ppt_video_vertical_res": 720,
        "default_slide_duration": 5.0,  # seconds
        "ffmpeg_preset": "medium",  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to config file (JSON/YAML)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def load_config(self, config_path: str) -> None:
        """Load configuration from file.
        
        Args:
            config_path: Path to config file
        """
        path = Path(config_path)
        
        if path.suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
                self.config.update(user_config)
        elif path.suffix in [".yaml", ".yml"]:
            try:
                import yaml
                with open(path, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        self.config.update(user_config)
            except ImportError:
                raise ImportError("PyYAML is required to load YAML config files")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return self.config.copy()
