"""Demo project setup for testing."""

import json
from pathlib import Path


def create_demo_project(project_dir: str) -> bool:
    """Create a demo project with sample files.
    
    Args:
        project_dir: Path to project directory
        
    Returns:
        True if successful, False otherwise
    """
    try:
        project_path = Path(project_dir)
        
        # Create directories
        input_dir = project_path / "input"
        work_dir = project_path / "work"
        output_dir = project_path / "output"
        
        input_dir.mkdir(parents=True, exist_ok=True)
        work_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sample transcript.json
        transcript = {
            "lesson_name": "Python 基础教程",
            "segments": [
                {
                    "start": 0.0,
                    "end": 3.5,
                    "text": "大家好，欢迎来到 Python 基础教程"
                },
                {
                    "start": 3.5,
                    "end": 8.2,
                    "text": "今天我们要学习的是变量和数据类型"
                },
                {
                    "start": 8.2,
                    "end": 12.0,
                    "text": "Python 中有多种数据类型，包括整数、浮点数、字符串等"
                },
                {
                    "start": 12.0,
                    "end": 16.5,
                    "text": "让我们先看一个简单的例子"
                },
                {
                    "start": 16.5,
                    "end": 20.0,
                    "text": "这就是今天的内容，谢谢大家"
                }
            ]
        }
        
        transcript_path = work_dir / "transcript.json"
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump(transcript, f, indent=2, ensure_ascii=False)
        
        # Create sample timeline.json
        timeline = {
            "lesson_name": "Python 基础教程",
            "slides": [
                {
                    "slide_index": 0,
                    "animations": [
                        {
                            "animation_index": 0,
                            "animation_type": "appear",
                            "trigger_time": 0.0,
                            "duration": 0.5,
                            "object_name": "标题"
                        },
                        {
                            "animation_index": 1,
                            "animation_type": "appear",
                            "trigger_time": 1.0,
                            "duration": 0.5,
                            "object_name": "副标题"
                        }
                    ],
                    "advance_time": 5.0
                },
                {
                    "slide_index": 1,
                    "animations": [
                        {
                            "animation_index": 0,
                            "animation_type": "appear",
                            "trigger_time": 0.0,
                            "duration": 0.3,
                            "object_name": "内容"
                        }
                    ],
                    "advance_time": 8.0
                },
                {
                    "slide_index": 2,
                    "animations": [
                        {
                            "animation_index": 0,
                            "animation_type": "appear",
                            "trigger_time": 0.0,
                            "duration": 0.3,
                            "object_name": "数据类型列表"
                        }
                    ],
                    "advance_time": 6.0
                },
                {
                    "slide_index": 3,
                    "animations": [
                        {
                            "animation_index": 0,
                            "animation_type": "appear",
                            "trigger_time": 0.0,
                            "duration": 0.3,
                            "object_name": "代码示例"
                        }
                    ],
                    "advance_time": 5.0
                },
                {
                    "slide_index": 4,
                    "animations": [
                        {
                            "animation_index": 0,
                            "animation_type": "appear",
                            "trigger_time": 0.0,
                            "duration": 0.3,
                            "object_name": "谢谢"
                        }
                    ],
                    "advance_time": 4.0
                }
            ],
            "total_duration": 28.0
        }
        
        timeline_path = work_dir / "timeline.json"
        with open(timeline_path, "w", encoding="utf-8") as f:
            json.dump(timeline, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Demo project created at: {project_path}")
        print(f"   - input/: {input_dir}")
        print(f"   - work/: {work_dir}")
        print(f"   - output/: {output_dir}")
        print(f"   - transcript.json: {transcript_path}")
        print(f"   - timeline.json: {timeline_path}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create demo project: {e}")
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python tests/demo_project.py <project_dir>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    success = create_demo_project(project_dir)
    sys.exit(0 if success else 1)
