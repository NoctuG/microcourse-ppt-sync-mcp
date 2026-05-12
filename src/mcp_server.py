"""MCP Server for Microcourse PPT Sync."""

import json
import sys
from typing import Any, Dict
from src.utils import get_logger
from src.tools import (
    inspect_project,
    inspect_ppt,
    build_timeline,
    apply_ppt_timeline,
    export_ppt_video,
    generate_sync_report,
)


logger = get_logger(__name__)


class MCPServer:
    """MCP Server implementation using stdio transport."""
    
    def __init__(self):
        """Initialize MCP server."""
        self.tools = {
            "inspect_project": {
                "description": "检查项目目录结构和文件",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "项目目录路径",
                        }
                    },
                    "required": ["project_path"],
                },
                "handler": inspect_project,
            },
            "inspect_ppt": {
                "description": "检查 PPT 文件信息和动画序列",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ppt_path": {
                            "type": "string",
                            "description": "PPT 文件路径",
                        }
                    },
                    "required": ["ppt_path"],
                },
                "handler": inspect_ppt,
            },
            "build_timeline": {
                "description": "从 Transcript 生成 Timeline",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "项目目录路径",
                        },
                        "transcript_path": {
                            "type": "string",
                            "description": "Transcript JSON 文件路径",
                        },
                        "slide_count": {
                            "type": "integer",
                            "description": "演示文稿中的幻灯片数量",
                        },
                        "default_slide_duration": {
                            "type": "number",
                            "description": "每页默认时长（秒）",
                            "default": 5.0,
                        },
                    },
                    "required": ["project_path", "transcript_path", "slide_count"],
                },
                "handler": build_timeline,
            },
            "apply_ppt_timeline": {
                "description": "将 Timeline 应用到 PPT",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "项目目录路径",
                        },
                        "ppt_path": {
                            "type": "string",
                            "description": "PPT 文件路径",
                        },
                        "timeline_path": {
                            "type": "string",
                            "description": "Timeline JSON 文件路径",
                        },
                    },
                    "required": ["project_path", "ppt_path", "timeline_path"],
                },
                "handler": apply_ppt_timeline,
            },
            "export_ppt_video": {
                "description": "导出 PPT 为视频",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ppt_path": {
                            "type": "string",
                            "description": "PPT 文件路径",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "输出视频文件路径",
                        },
                        "quality": {
                            "type": "string",
                            "description": "视频质量 (LD, SD, HD)",
                            "default": "HD",
                        },
                        "fps": {
                            "type": "integer",
                            "description": "帧率（每秒帧数）",
                            "default": 30,
                        },
                    },
                    "required": ["ppt_path", "output_path"],
                },
                "handler": export_ppt_video,
            },
            "generate_sync_report": {
                "description": "生成同步报告",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "项目目录路径",
                        },
                        "timeline_path": {
                            "type": "string",
                            "description": "Timeline JSON 文件路径",
                        },
                        "output_path": {
                            "type": "string",
                            "description": "输出报告文件路径",
                        },
                    },
                    "required": ["project_path", "timeline_path", "output_path"],
                },
                "handler": generate_sync_report,
            },
        }
    
    def get_tools(self) -> Dict[str, Any]:
        """Get available tools.
        
        Returns:
            Dictionary of available tools
        """
        return {
            name: {
                "description": tool["description"],
                "inputSchema": tool["inputSchema"],
            }
            for name, tool in self.tools.items()
        }
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool.
        
        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        if tool_name not in self.tools:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}",
            }
        
        try:
            handler = self.tools[tool_name]["handler"]
            result = handler(**arguments)
            return result
        except TypeError as e:
            logger.error(f"Invalid arguments for tool {tool_name}: {e}")
            return {
                "status": "error",
                "message": f"Invalid arguments: {str(e)}",
            }
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {
                "status": "error",
                "message": str(e),
            }
    
    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP message.
        
        Args:
            message: MCP message
            
        Returns:
            MCP response
        """
        try:
            msg_type = message.get("type")
            
            if msg_type == "tools/list":
                return {
                    "type": "tools/list",
                    "tools": self.get_tools(),
                }
            
            elif msg_type == "tools/call":
                tool_name = message.get("name")
                arguments = message.get("arguments", {})
                result = self.call_tool(tool_name, arguments)
                return {
                    "type": "tools/result",
                    "result": result,
                }
            
            else:
                return {
                    "type": "error",
                    "error": f"Unknown message type: {msg_type}",
                }
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return {
                "type": "error",
                "error": str(e),
            }


def main():
    """Main entry point for MCP server."""
    server = MCPServer()
    
    logger.info("MCP Server started (stdio mode)")
    logger.info(f"Available tools: {', '.join(server.tools.keys())}")
    
    # Read messages from stdin
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                message = json.loads(line)
                response = server.handle_message(message)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
                error_response = {
                    "type": "error",
                    "error": f"Invalid JSON: {str(e)}",
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
    except KeyboardInterrupt:
        logger.info("MCP Server shutting down (interrupted)")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
