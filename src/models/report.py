"""Sync report models."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class SyncIssue:
    """Sync issue report."""
    slide_index: int
    issue_type: str  # e.g., "missing_animation", "timing_conflict"
    description: str
    severity: str = "warning"  # "info", "warning", "error"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "slide_index": self.slide_index,
            "issue_type": self.issue_type,
            "description": self.description,
            "severity": self.severity,
            "metadata": self.metadata,
        }


@dataclass
class SyncReport:
    """Sync report."""
    lesson_name: str
    total_slides: int
    total_animations: int
    total_duration: float
    issues: List[SyncIssue] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "lesson_name": self.lesson_name,
            "total_slides": self.total_slides,
            "total_animations": self.total_animations,
            "total_duration": self.total_duration,
            "issues": [issue.to_dict() for issue in self.issues],
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
    
    def to_markdown(self) -> str:
        """Convert to Markdown format."""
        lines = [
            f"# 同步报告：{self.lesson_name}",
            "",
            f"**生成时间**：{self.timestamp}",
            "",
            "## 统计信息",
            "",
            f"- **总幻灯片数**：{self.total_slides}",
            f"- **总动画数**：{self.total_animations}",
            f"- **总时长**：{self.total_duration:.2f} 秒",
            "",
        ]
        
        if self.issues:
            lines.extend([
                "## 问题列表",
                "",
            ])
            
            for issue in self.issues:
                severity_emoji = {
                    "info": "ℹ️",
                    "warning": "⚠️",
                    "error": "❌",
                }.get(issue.severity, "•")
                
                lines.append(
                    f"{severity_emoji} **幻灯片 {issue.slide_index + 1}**：{issue.description}"
                )
            
            lines.append("")
        else:
            lines.extend([
                "## 问题列表",
                "",
                "✅ 没有发现问题",
                "",
            ])
        
        return "\n".join(lines)
