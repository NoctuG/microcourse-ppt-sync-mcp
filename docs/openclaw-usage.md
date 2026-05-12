# OpenClaw 使用指南

本文档说明如何在 OpenClaw 中使用 Microcourse PPT Sync MCP Server。

## 概述

Microcourse PPT Sync MCP 是一个 MCP Server，提供 6 个工具用于 PPT 动画时间轴同步和视频导出。

**工作流：**
1. 检查项目结构
2. 检查 PPT 文件
3. 生成或读取 Timeline
4. 应用 Timeline 到 PPT
5. 导出 PPT 背景视频
6. 生成同步报告

## 安装

### 前置要求

- Windows 10/11
- Python 3.11+
- Microsoft PowerPoint 桌面版
- FFmpeg（可选）

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/NoctuG/microcourse-ppt-sync-mcp.git
cd microcourse-ppt-sync-mcp

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装包
pip install -e .

# 4. 验证安装
python src/mcp_server.py --help
```

## 在 OpenClaw 中配置

### 1. 添加 MCP Server

在 OpenClaw 配置中添加：

```json
{
  "mcpServers": {
    "microcourse-ppt-sync": {
      "command": "python",
      "args": ["-m", "src.mcp_server"],
      "cwd": "/path/to/microcourse-ppt-sync-mcp"
    }
  }
}
```

### 2. 启动 OpenClaw

启动 OpenClaw 后，应该能看到 6 个可用的工具。

## 工具参考

### 1. inspect_project

**功能：** 检查项目目录结构

**输入：**
```json
{
  "project_path": "D:/microcourse/demo"
}
```

**输出：**
```json
{
  "status": "success",
  "structure": {
    "input": ["lesson.pptx"],
    "work": ["transcript.json", "timeline.json"],
    "output": []
  }
}
```

**用途：** 验证项目结构是否正确

---

### 2. inspect_ppt

**功能：** 读取 PPT 文件的动画序列

**输入：**
```json
{
  "ppt_path": "D:/microcourse/demo/input/lesson.pptx"
}
```

**输出：**
```json
{
  "status": "success",
  "slide_count": 5,
  "slides": [
    {
      "slide_index": 0,
      "animation_count": 2,
      "animations": [
        {
          "animation_index": 0,
          "effect_type": "Appear",
          "object_name": "标题",
          "shape_text": "Python 基础"
        }
      ]
    }
  ]
}
```

**用途：** 了解 PPT 中的动画结构

---

### 3. build_timeline

**功能：** 从 Transcript 生成 Timeline

**输入：**
```json
{
  "project_path": "D:/microcourse/demo",
  "transcript_path": "D:/microcourse/demo/work/transcript.json",
  "slide_count": 5,
  "default_slide_duration": 5.0
}
```

**输出：**
```json
{
  "status": "success",
  "timeline_path": "D:/microcourse/demo/work/timeline.json",
  "slides_count": 5,
  "total_duration": 28.0
}
```

**用途：** 自动生成时间轴

**Transcript 格式：**
```json
{
  "lesson_name": "Python 基础",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "大家好"
    }
  ]
}
```

---

### 4. apply_ppt_timeline

**功能：** 将 Timeline 应用到 PPT 动画

**输入：**
```json
{
  "project_path": "D:/microcourse/demo",
  "ppt_path": "D:/microcourse/demo/input/lesson.pptx",
  "timeline_path": "D:/microcourse/demo/work/timeline.json"
}
```

**输出：**
```json
{
  "status": "success",
  "output_path": "D:/microcourse/demo/work/lesson_timed.pptx",
  "total_animations": 5,
  "slides_processed": 5
}
```

**用途：** 将时间轴应用到 PPT，生成带动画计时的新 PPT 文件

---

### 5. export_ppt_video

**功能：** 导出 PPT 背景视频

**输入：**
```json
{
  "ppt_path": "D:/microcourse/demo/work/lesson_timed.pptx",
  "output_path": "D:/microcourse/demo/output/ppt_bg.mp4",
  "quality": "HD",
  "fps": 30
}
```

**输出：**
```json
{
  "status": "success",
  "file_path": "D:/microcourse/demo/output/ppt_bg.mp4",
  "file_size": 52428800,
  "duration": 28.0,
  "resolution": "1920x1080",
  "fps": 30
}
```

**参数说明：**
- `quality`：`LD` (低), `SD` (标清), `HD` (高清)
- `fps`：帧率，通常 24 或 30

**用途：** 导出保留动画效果的 MP4 视频

---

### 6. generate_sync_report

**功能：** 生成同步诊断报告

**输入：**
```json
{
  "project_path": "D:/microcourse/demo",
  "timeline_path": "D:/microcourse/demo/work/timeline.json",
  "output_path": "D:/microcourse/demo/output/sync_report.md"
}
```

**输出：**
```json
{
  "status": "success",
  "report_path": "D:/microcourse/demo/output/sync_report.md",
  "issue_count": 0,
  "warning_count": 2
}
```

**报告内容：**
- 每页时长统计
- 动画数量统计
- 时间冲突检测
- 对象名称匹配失败
- 建议和修复方案

**用途：** 诊断 PPT 和 Timeline 的同步问题

---

## 工作流示例

### 场景：快速生成 Python 基础教程微课

**步骤 1：准备项目**

```python
# 在 OpenClaw 中调用
inspect_project({
  "project_path": "D:/python_tutorial"
})
```

**步骤 2：检查 PPT**

```python
inspect_ppt({
  "ppt_path": "D:/python_tutorial/input/lesson.pptx"
})
```

**步骤 3：生成 Timeline**

如果您有 `transcript.json`：

```python
build_timeline({
  "project_path": "D:/python_tutorial",
  "transcript_path": "D:/python_tutorial/work/transcript.json",
  "slide_count": 5
})
```

或者手动创建 `timeline.json`。

**步骤 4：应用 Timeline**

```python
apply_ppt_timeline({
  "project_path": "D:/python_tutorial",
  "ppt_path": "D:/python_tutorial/input/lesson.pptx",
  "timeline_path": "D:/python_tutorial/work/timeline.json"
})
```

**步骤 5：导出视频**

```python
export_ppt_video({
  "ppt_path": "D:/python_tutorial/work/lesson_timed.pptx",
  "output_path": "D:/python_tutorial/output/ppt_bg.mp4",
  "quality": "HD",
  "fps": 30
})
```

**步骤 6：生成报告**

```python
generate_sync_report({
  "project_path": "D:/python_tutorial",
  "timeline_path": "D:/python_tutorial/work/timeline.json",
  "output_path": "D:/python_tutorial/output/sync_report.md"
})
```

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| `PPT file not found` | PPT 文件不存在 | 检查路径，确保文件存在 |
| `PowerPoint not installed` | 未安装 PowerPoint | 安装 Microsoft PowerPoint 桌面版 |
| `animation_index out of range` | 动画索引超出范围 | 检查 timeline.json 中的索引 |
| `object_name not found` | 对象名称不匹配 | 使用 inspect_ppt 查看正确的名称 |
| `Video export timeout` | 视频导出超时 | 尝试降低质量（`quality: "SD"`） |

### 调试

1. **查看完整错误信息**
   - 检查 OpenClaw 的错误日志
   - 查看 `sync_report.md` 中的详细信息

2. **使用 inspect_ppt 验证**
   ```python
   inspect_ppt({
     "ppt_path": "D:/project/input/lesson.pptx"
   })
   ```

3. **生成诊断报告**
   ```python
   generate_sync_report({
     "project_path": "D:/project",
     "timeline_path": "D:/project/work/timeline.json",
     "output_path": "D:/project/output/sync_report.md"
   })
   ```

## 性能优化

### 导出速度

- **降低质量**：使用 `quality: "SD"` 而不是 `"HD"`
- **降低帧率**：使用 `fps: 24` 而不是 `30`
- **关闭其他程序**：释放系统资源

### 典型性能

| 操作 | 时间 |
|------|------|
| 应用 timeline（5 页） | 1-2 秒 |
| 导出视频（HD, 30fps） | 30-60 秒 |
| 生成报告 | < 1 秒 |

## 最佳实践

### 1. 项目结构

始终使用标准的项目结构：

```
project/
├── input/
│   └── lesson.pptx
├── work/
│   ├── transcript.json
│   └── timeline.json
└── output/
```

### 2. Timeline 验证

在应用 timeline 前，始终生成报告检查：

```python
# 先生成报告
generate_sync_report({...})

# 检查 sync_report.md 中是否有错误
# 然后再应用
apply_ppt_timeline({...})
```

### 3. 备份

在修改 PPT 前备份原文件：

```
input/
├── lesson.pptx          # 原始文件
└── lesson_backup.pptx   # 备份
```

### 4. 迭代开发

- 先用小规模 PPT 测试（2-3 页）
- 验证工作流后再处理完整 PPT
- 保存中间结果（timeline.json）

## 与 Manus 集成

在 Manus 中使用本 MCP Server：

1. **配置 MCP Server**
   - 在 Manus 项目设置中添加本 MCP Server
   - 指定 Python 解释器路径
   - 指定项目目录

2. **调用工具**
   - 在 Manus 中直接调用 6 个工具
   - 使用 Manus 的 UI 查看结果
   - 在 Manus 中编辑 timeline.json

3. **自动化工作流**
   - 使用 Manus 的自动化功能
   - 定时生成微课视频
   - 批量处理多个 PPT 文件

## 下一步

- [Timeline 格式说明](timeline-format.md)
- [集成测试指南](../tests/INTEGRATION_TEST.md)
- [API 文档](api.md)
- [开发指南](development.md)
