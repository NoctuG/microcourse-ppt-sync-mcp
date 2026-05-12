# 基础示例项目

这是一个最小化的示例项目，展示如何使用 Microcourse PPT Sync MCP。

## 项目结构

```
basic_project/
├── input/
│   └── lesson.pptx          # 源 PPT 文件（需要手动创建）
├── work/
│   ├── transcript.json      # 人声时间戳（可选）
│   └── timeline.json        # 时间轴配置
└── output/
```

## 快速开始

### 1. 准备 PPT 文件

创建 `input/lesson.pptx`：

1. 打开 PowerPoint
2. 创建 5 页幻灯片：
   - 第 1 页：标题 + 副标题（各 1 个"出现"动画）
   - 第 2 页：内容标题 + 内容文本 + 重点（3 个动画）
   - 第 3 页：代码标题 + 代码块（2 个动画）
   - 第 4 页：示例标题 + 示例内容（2 个动画）
   - 第 5 页：总结（1 个动画）
3. 为每个文本框添加"出现"动画
4. 保存为 `input/lesson.pptx`

### 2. 运行工作流

```bash
# 从项目根目录
cd /path/to/microcourse-ppt-sync-mcp

# 运行完整工作流
microcourse-ppt-sync run examples/basic_project --quality HD --fps 30
```

### 3. 检查输出

```
output/
├── ppt_bg.mp4           # PPT 背景视频（无声）
└── sync_report.md       # 同步诊断报告
```

## 文件说明

### timeline.json

包含 5 页幻灯片的时间轴配置：

- **第 1 页**：2 个动画，总时长 5 秒
- **第 2 页**：3 个动画，总时长 8 秒
- **第 3 页**：2 个动画，总时长 6 秒
- **第 4 页**：2 个动画，总时长 5 秒
- **第 5 页**：1 个动画，总时长 4 秒

**总时长**：28 秒

### transcript.json（可选）

如果您有人声时间戳，可以使用 `build_timeline` 自动生成 `timeline.json`：

```bash
microcourse-ppt-sync build examples/basic_project examples/basic_project/work/transcript.json -s 5
```

## 工作流步骤

### 步骤 1：检查项目

```bash
microcourse-ppt-sync inspect examples/basic_project
```

**输出：**
```
{
  "status": "success",
  "structure": {
    "input": ["lesson.pptx"],
    "work": ["timeline.json"],
    "output": []
  }
}
```

### 步骤 2：检查 PPT

```bash
microcourse-ppt-sync inspect_ppt examples/basic_project/input/lesson.pptx
```

**输出：**
```
{
  "status": "success",
  "slide_count": 5,
  "slides": [...]
}
```

### 步骤 3：应用 Timeline

```bash
microcourse-ppt-sync apply examples/basic_project examples/basic_project/input/lesson.pptx examples/basic_project/work/timeline.json
```

**输出：**
```
{
  "status": "success",
  "output_path": "examples/basic_project/work/lesson_timed.pptx",
  "total_animations": 11,
  "slides_processed": 5
}
```

### 步骤 4：导出视频

```bash
microcourse-ppt-sync export examples/basic_project/work/lesson_timed.pptx examples/basic_project/output/ppt_bg.mp4 --quality HD --fps 30
```

**输出：**
```
{
  "status": "success",
  "file_path": "examples/basic_project/output/ppt_bg.mp4",
  "file_size": 52428800,
  "duration": 28.0
}
```

### 步骤 5：生成报告

```bash
microcourse-ppt-sync report examples/basic_project examples/basic_project/work/timeline.json examples/basic_project/output/sync_report.md
```

**输出：**
```
{
  "status": "success",
  "report_path": "examples/basic_project/output/sync_report.md",
  "issue_count": 0
}
```

## 验证结果

### 检查 PPT 动画

打开 `work/lesson_timed.pptx`：

1. 进入幻灯片放映模式
2. 验证每页动画按时间轴自动播放（无需点击）
3. 验证每页自动翻页（按 advance_time）

### 检查视频

使用 FFmpeg 检查视频信息：

```bash
ffprobe -v error -show_format -show_streams output/ppt_bg.mp4
```

**预期：**
- 视频编码：h264
- 分辨率：1920x1080（HD）
- 帧率：30 fps
- 时长：约 28 秒

### 检查报告

查看 `output/sync_report.md`：

```markdown
# PPT 同步报告

## 项目信息
- 项目路径：...
- 生成时间：...

## 幻灯片统计
- 总幻灯片数：5
- 总时长：28.0 秒

## 每页详情
- 第 1 页：2 个动画，时长 5.0 秒
- 第 2 页：3 个动画，时长 8.0 秒
- ...

## 问题和警告
- 无问题
```

## 常见问题

### Q: 如何修改 timeline？

**A:** 编辑 `work/timeline.json`，然后重新运行工作流。

### Q: 如何添加更多页面？

**A:** 
1. 在 PPT 中添加新页面
2. 在 `timeline.json` 中添加新的 slide 对象
3. 重新运行工作流

### Q: 如何调整动画时间？

**A:** 编辑 `timeline.json` 中的 `trigger_time` 和 `duration`。

### Q: 视频导出失败怎么办？

**A:** 
1. 检查 PowerPoint 是否正在运行
2. 尝试降低质量：`--quality SD`
3. 查看 `sync_report.md` 中的错误信息

## 下一步

- 修改 `timeline.json` 以适应您的 PPT
- 添加您自己的 PPT 文件
- 尝试不同的质量和帧率设置
- 在剪映中合成最终微课视频

## 参考资源

- [Timeline 格式说明](../../docs/timeline-format.md)
- [集成测试指南](../../tests/INTEGRATION_TEST.md)
- [API 文档](../../docs/api.md)
