# API 文档

## MCP Tools

### inspect_project

检查项目目录结构和文件。

**请求参数：**

```json
{
  "project_path": "/path/to/project"
}
```

**响应示例：**

```json
{
  "status": "success",
  "project_path": "/path/to/project",
  "structure": {
    "input": {
      "exists": true,
      "is_dir": true
    },
    "work": {
      "exists": true,
      "is_dir": true
    },
    "output": {
      "exists": true,
      "is_dir": true
    }
  },
  "files": {
    "input": ["lesson.pptx"],
    "work": ["timeline.json", "transcript.json"],
    "output": []
  },
  "key_files": {
    "input": {
      "lesson.pptx": true
    },
    "work": {
      "timeline.json": true,
      "transcript.json": true
    },
    "output": {
      "lesson_timed.pptx": false,
      "ppt_bg.mp4": false,
      "sync_report.md": false
    }
  }
}
```

---

### inspect_ppt

检查 PPT 文件信息。

**请求参数：**

```json
{
  "ppt_path": "/path/to/lesson.pptx"
}
```

**响应示例：**

```json
{
  "status": "success",
  "ppt_path": "/path/to/lesson.pptx",
  "file_size": 2048576,
  "file_format": ".pptx",
  "slide_count": 10,
  "slides": [
    {
      "index": 0,
      "shape_count": 5,
      "has_notes": true
    }
  ]
}
```

---

### build_timeline

从 Transcript 生成 Timeline。

**请求参数：**

```json
{
  "project_path": "/path/to/project",
  "transcript_path": "/path/to/transcript.json",
  "slide_count": 10,
  "default_slide_duration": 5.0
}
```

**响应示例：**

```json
{
  "status": "success",
  "timeline_path": "/path/to/work/timeline.json",
  "lesson_name": "示例微课",
  "total_slides": 10,
  "total_animations": 20,
  "total_duration": 50.0
}
```

---

### apply_ppt_timeline

将 Timeline 应用到 PPT。

**请求参数：**

```json
{
  "project_path": "/path/to/project",
  "ppt_path": "/path/to/lesson.pptx",
  "timeline_path": "/path/to/work/timeline.json"
}
```

**响应示例：**

```json
{
  "status": "success",
  "output_path": "/path/to/work/lesson_timed.pptx",
  "slides_processed": 10,
  "total_animations": 20
}
```

---

### export_ppt_video

导出 PPT 为视频。

**请求参数：**

```json
{
  "ppt_path": "/path/to/lesson_timed.pptx",
  "output_path": "/path/to/output/ppt_bg.mp4",
  "quality": "HD",
  "fps": 30
}
```

**响应示例：**

```json
{
  "status": "success",
  "output_path": "/path/to/output/ppt_bg.mp4",
  "quality": "HD",
  "fps": 30,
  "file_size": 52428800
}
```

---

### generate_sync_report

生成同步报告。

**请求参数：**

```json
{
  "project_path": "/path/to/project",
  "timeline_path": "/path/to/work/timeline.json",
  "output_path": "/path/to/output/sync_report.md"
}
```

**响应示例：**

```json
{
  "status": "success",
  "output_path": "/path/to/output/sync_report.md",
  "lesson_name": "示例微课",
  "total_slides": 10,
  "total_animations": 20,
  "total_duration": 50.0,
  "issue_count": 2,
  "issues": [
    {
      "slide_index": 3,
      "issue_type": "insufficient_advance_time",
      "description": "幻灯片翻页时间 5.0s 不足以完成所有动画（需要 6.2s）",
      "severity": "warning"
    }
  ]
}
```

---

## 错误响应

所有 API 在发生错误时都返回以下格式：

```json
{
  "status": "error",
  "message": "错误描述信息"
}
```

**常见错误：**

- `"Project path does not exist"` - 项目路径不存在
- `"Invalid PPT file format"` - PPT 文件格式无效
- `"Failed to open PPT file"` - 无法打开 PPT 文件（可能是 Windows 环境问题）
- `"Failed to load timeline"` - 无法加载 Timeline 文件
- `"Timeline must be a dictionary"` - Timeline 数据格式错误

---

## 使用流程示例

### 完整的 PPT 背景视频生成流程

```python
import json
import requests

# 假设 MCP Server 运行在本地

def run_workflow(project_path):
    """运行完整的 PPT 微课生成工作流"""
    
    # 1. 检查项目结构
    result = requests.post("http://localhost:8000/tools/inspect_project", json={
        "project_path": project_path
    })
    print("Project inspection:", result.json())
    
    # 2. 检查 PPT 文件
    ppt_path = f"{project_path}/input/lesson.pptx"
    result = requests.post("http://localhost:8000/tools/inspect_ppt", json={
        "ppt_path": ppt_path
    })
    ppt_info = result.json()
    slide_count = ppt_info["slide_count"]
    print("PPT inspection:", ppt_info)
    
    # 3. 从 Transcript 生成 Timeline
    transcript_path = f"{project_path}/work/transcript.json"
    result = requests.post("http://localhost:8000/tools/build_timeline", json={
        "project_path": project_path,
        "transcript_path": transcript_path,
        "slide_count": slide_count,
        "default_slide_duration": 5.0
    })
    timeline_result = result.json()
    timeline_path = timeline_result["timeline_path"]
    print("Timeline built:", timeline_result)
    
    # 4. 将 Timeline 应用到 PPT
    result = requests.post("http://localhost:8000/tools/apply_ppt_timeline", json={
        "project_path": project_path,
        "ppt_path": ppt_path,
        "timeline_path": timeline_path
    })
    timed_ppt = result.json()
    print("Timeline applied:", timed_ppt)
    
    # 5. 导出 PPT 背景视频
    result = requests.post("http://localhost:8000/tools/export_ppt_video", json={
        "ppt_path": timed_ppt["output_path"],
        "output_path": f"{project_path}/output/ppt_bg.mp4",
        "quality": "HD",
        "fps": 30
    })
    video_result = result.json()
    print("Video exported:", video_result)
    
    # 6. 生成同步报告
    result = requests.post("http://localhost:8000/tools/generate_sync_report", json={
        "project_path": project_path,
        "timeline_path": timeline_path,
        "output_path": f"{project_path}/output/sync_report.md"
    })
    report_result = result.json()
    print("Report generated:", report_result)
    
    return {
        "status": "success",
        "timeline": timeline_result,
        "timed_ppt": timed_ppt,
        "video": video_result,
        "report": report_result
    }

# 运行工作流
if __name__ == "__main__":
    result = run_workflow("/path/to/project")
    print(json.dumps(result, indent=2))
```

---

## 数据格式

### Transcript 格式

```json
{
  "lesson_name": "示例微课",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "大家好，欢迎来到本次微课"
    },
    {
      "start": 3.5,
      "end": 8.2,
      "text": "今天我们要学习的是..."
    }
  ]
}
```

### Timeline 格式

详见 [Timeline 格式说明](./timeline_format.md)

---

## 限制和注意事项

1. **Windows 环境**：PPT 处理功能仅在 Windows 10/11 + Microsoft PowerPoint 环境下工作
2. **文件路径**：所有路径应该是绝对路径
3. **并发**：当前实现不支持并发处理多个项目
4. **超时**：大型 PPT 文件的导出可能需要较长时间
5. **内存**：建议在内存充足的机器上运行（至少 4GB）
