"""Unit tests for tools."""

import json
import tempfile
import unittest
from pathlib import Path
from src.tools import inspect_project, build_timeline


class TestInspectProject(unittest.TestCase):
    """Test inspect_project tool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = self.temp_dir.name
        
        # Create standard directories
        Path(self.project_path, "input").mkdir(exist_ok=True)
        Path(self.project_path, "work").mkdir(exist_ok=True)
        Path(self.project_path, "output").mkdir(exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_inspect_valid_project(self):
        """Test inspecting a valid project."""
        result = inspect_project(self.project_path)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("structure", result)
        self.assertIn("input", result["structure"])
        self.assertIn("work", result["structure"])
        self.assertIn("output", result["structure"])
    
    def test_inspect_nonexistent_project(self):
        """Test inspecting a non-existent project."""
        result = inspect_project("/nonexistent/path")
        
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)


class TestBuildTimeline(unittest.TestCase):
    """Test build_timeline tool."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = self.temp_dir.name
        
        # Create directories
        Path(self.project_path, "input").mkdir(exist_ok=True)
        Path(self.project_path, "work").mkdir(exist_ok=True)
        Path(self.project_path, "output").mkdir(exist_ok=True)
        
        # Create sample transcript
        self.transcript = {
            "lesson_name": "Test Lesson",
            "segments": [
                {"start": 0.0, "end": 3.0, "text": "Introduction"},
                {"start": 3.0, "end": 8.0, "text": "Content 1"},
                {"start": 8.0, "end": 12.0, "text": "Content 2"},
            ]
        }
        
        self.transcript_path = Path(self.project_path) / "work" / "transcript.json"
        with open(self.transcript_path, "w") as f:
            json.dump(self.transcript, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_build_timeline_valid(self):
        """Test building a valid timeline."""
        result = build_timeline(
            self.project_path,
            str(self.transcript_path),
            slide_count=3,
            default_slide_duration=5.0
        )
        
        self.assertEqual(result["status"], "success")
        self.assertIn("timeline_path", result)
        self.assertIn("slides_count", result)
    
    def test_build_timeline_invalid_transcript(self):
        """Test building timeline with invalid transcript."""
        result = build_timeline(
            self.project_path,
            "/nonexistent/transcript.json",
            slide_count=3
        )
        
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)
    
    def test_timeline_file_created(self):
        """Test that timeline file is created."""
        result = build_timeline(
            self.project_path,
            str(self.transcript_path),
            slide_count=3
        )
        
        if result["status"] == "success":
            timeline_path = Path(result["timeline_path"])
            self.assertTrue(timeline_path.exists())
            
            # Verify timeline content
            with open(timeline_path) as f:
                timeline = json.load(f)
            
            self.assertEqual(timeline["lesson_name"], "Test Lesson")
            self.assertEqual(len(timeline["slides"]), 3)


class TestMCPServerTools(unittest.TestCase):
    """Test MCP Server tool registration."""
    
    def test_tools_available(self):
        """Test that all tools are available."""
        from src.mcp_server import MCPServer
        
        server = MCPServer()
        tools = server.get_tools()
        
        expected_tools = [
            "inspect_project",
            "inspect_ppt",
            "build_timeline",
            "apply_ppt_timeline",
            "export_ppt_video",
            "generate_sync_report",
        ]
        
        for tool_name in expected_tools:
            self.assertIn(tool_name, tools)
    
    def test_tool_schema(self):
        """Test that tools have valid schema."""
        from src.mcp_server import MCPServer
        
        server = MCPServer()
        tools = server.get_tools()
        
        for tool_name, tool_info in tools.items():
            self.assertIn("description", tool_info)
            self.assertIn("inputSchema", tool_info)
            
            schema = tool_info["inputSchema"]
            self.assertIn("type", schema)
            self.assertIn("properties", schema)


if __name__ == "__main__":
    unittest.main()
