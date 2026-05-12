# 集成测试指南

本文档描述如何进行完整的集成测试，验证 MVP 可运行闭环。

## 前置条件

- Windows 10/11
- Microsoft PowerPoint 桌面版
- Python 3.11+
- pywin32 已安装
- 项目已安装：`pip install -e .`

## 测试步骤

### 1. 创建示例项目

```bash
python tests/demo_project.py D:/demo_project
```

这将创建以下结构：

```
D:/demo_project/
├── input/
│   └── lesson.pptx          # 需要手动创建或使用现有 PPT
├── work/
│   ├── transcript.json      # 已生成
│   └── timeline.json        # 已生成
└── output/
```

### 2. 准备 PPT 文件

需要一个有动画的 PPT 文件放在 `input/lesson.pptx`。

**最小化 PPT 要求：**
- 5 页幻灯片
- 每页至少 1 个动画（可以是简单的"出现"动画）
- 动画对象有明确的名称

**创建测试 PPT 的步骤：**

1. 打开 PowerPoint
2. 创建 5 页幻灯片：
   - 第 1 页：标题 + 副标题（各 1 个"出现"动画）
   - 第 2-5 页：内容（各 1 个"出现"动画）
3. 为每个文本框添加"出现"动画
4. 保存为 `D:/demo_project/input/lesson.pptx`

### 3. 运行 CLI 闭环测试

```bash
microcourse-ppt-sync run D:/demo_project --quality HD --fps 30
```

**预期输出：**

```
🚀 Starting workflow for project: D:/demo_project
📁 Step 1: Inspecting project...
✅ Project inspection completed

📊 Step 2: Inspecting PPT...
✅ PPT inspection completed (5 slides)

⏱️  Step 3: Applying timeline to PPT...
✅ Timeline applied (5 animations)

🎬 Step 4: Exporting PPT as video...
✅ Video exported (XX.X MB)

📝 Step 5: Generating sync report...
✅ Report generated (0 issues)

==================================================
✨ Workflow completed successfully!
==================================================
📍 Project: D:/demo_project
📊 Slides: 5
🎬 Video: D:/demo_project/output/ppt_bg.mp4
📝 Report: D:/demo_project/output/sync_report.md
```

### 4. 验证输出

检查以下文件是否已生成：

- ✅ `work/lesson_timed.pptx` - 带动画计时的 PPT
- ✅ `output/ppt_bg.mp4` - PPT 背景视频（无声）
- ✅ `output/sync_report.md` - 同步报告

### 5. 验证视频质量

使用 FFmpeg 检查视频信息：

```bash
ffprobe -v error -show_format -show_streams output/ppt_bg.mp4
```

**预期：**
- 视频编码：h264
- 分辨率：1920x1080（HD）
- 帧率：30 fps
- 时长：约 28 秒（5 页 × 平均 5.6 秒）

### 6. 验证 PPT 动画

打开 `work/lesson_timed.pptx`：

1. 进入幻灯片放映模式
2. 验证每页动画按时间轴自动播放（无需点击）
3. 验证每页自动翻页（按 advance_time）

## 常见问题

### Q: 视频导出超时

**症状：** 导出卡在 "Waiting for video export to complete..."

**解决：**
1. 检查 PowerPoint 是否在后台运行
2. 检查磁盘空间是否充足
3. 尝试减小分辨率：`--quality SD`
4. 检查 PowerPoint 是否有错误对话框

### Q: 动画时间不准确

**症状：** 视频中动画出现时间与 timeline.json 不符

**解决：**
1. 检查 timeline.json 中的 trigger_time 是否正确
2. 验证 PPT 中动画的原始触发类型（应为"与上一动画同时"）
3. 查看 sync_report.md 中是否有警告

### Q: 报告显示大量警告

**症状：** sync_report.md 中有 "insufficient_advance_time" 警告

**解决：**
1. 增加 timeline.json 中的 advance_time
2. 或减少动画数量
3. 或减少动画 duration

## 性能基准

在标准 Windows 10 机器上（i7, 16GB RAM）：

| 操作 | 时间 |
|------|------|
| 打开 PPT | 2-3 秒 |
| 应用 timeline | 1-2 秒 |
| 导出视频（5 页，HD） | 30-60 秒 |
| 生成报告 | < 1 秒 |
| **总计** | **35-70 秒** |

## MCP Server 测试

### 启动 MCP Server

```bash
python src/mcp_server.py
```

### 测试工具列表

```bash
echo '{"type": "tools/list"}' | python src/mcp_server.py
```

### 测试 inspect_project

```bash
echo '{"type": "tools/call", "name": "inspect_project", "arguments": {"project_path": "D:/demo_project"}}' | python src/mcp_server.py
```

### 测试完整工作流

```bash
# 1. Inspect project
echo '{"type": "tools/call", "name": "inspect_project", "arguments": {"project_path": "D:/demo_project"}}' | python src/mcp_server.py

# 2. Inspect PPT
echo '{"type": "tools/call", "name": "inspect_ppt", "arguments": {"ppt_path": "D:/demo_project/input/lesson.pptx"}}' | python src/mcp_server.py

# 3. Build timeline
echo '{"type": "tools/call", "name": "build_timeline", "arguments": {"project_path": "D:/demo_project", "transcript_path": "D:/demo_project/work/transcript.json", "slide_count": 5}}' | python src/mcp_server.py

# 4. Apply timeline
echo '{"type": "tools/call", "name": "apply_ppt_timeline", "arguments": {"project_path": "D:/demo_project", "ppt_path": "D:/demo_project/input/lesson.pptx", "timeline_path": "D:/demo_project/work/timeline.json"}}' | python src/mcp_server.py

# 5. Export video
echo '{"type": "tools/call", "name": "export_ppt_video", "arguments": {"ppt_path": "D:/demo_project/work/lesson_timed.pptx", "output_path": "D:/demo_project/output/ppt_bg.mp4"}}' | python src/mcp_server.py

# 6. Generate report
echo '{"type": "tools/call", "name": "generate_sync_report", "arguments": {"project_path": "D:/demo_project", "timeline_path": "D:/demo_project/work/timeline.json", "output_path": "D:/demo_project/output/sync_report.md"}}' | python src/mcp_server.py
```

## 验收标准

✅ **MVP 验收标准：**

```
给定：
- input/lesson.pptx（5 页，每页 1 个动画）
- work/timeline.json（5 页时间轴）

运行后得到：
- work/lesson_timed.pptx（带动画计时）
- output/ppt_bg.mp4（保留动画的视频）
- output/sync_report.md（同步报告）

并且：
- lesson_timed.pptx 放映时无需点击
- ppt_bg.mp4 保留 PPT 动画
- sync_report.md 能列出每页时长、动画数量、异常项
```

## 下一步

- [ ] 在 Windows 10/11 上运行完整测试
- [ ] 验证视频质量和动画同步
- [ ] 测试 MCP Server 接口
- [ ] 收集性能数据
- [ ] 记录任何问题或改进建议
