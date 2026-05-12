# 测试与集成验证指南

本项目的测试分为两类：

1. **普通单元测试**：不依赖 PowerPoint 桌面版，可在 Linux/macOS/Windows 和 GitHub Actions 中运行。
2. **Windows 手动集成测试**：依赖 Windows + Microsoft PowerPoint 桌面版，用于验证 PowerPoint COM、写入动画计时和 `CreateVideo` 导出。

## 1. 普通单元测试（CI 可运行）

### 覆盖范围

- Timeline / Slide / Animation 等数据模型。
- validators 等纯 Python 校验逻辑。
- report 生成逻辑。
- 不打开 PowerPoint 的 MCP tool schema 和基础工具行为。

### 运行命令

```bash
pytest tests/test_models.py tests/test_tools.py
```

或使用 Makefile：

```bash
make test
```

### CI 建议

GitHub Actions 中建议只运行普通单元测试，不要在默认 CI 中调用 PowerPoint COM 或视频导出。原因是完整导出需要：

- Windows 桌面会话。
- 已安装并可交互启动的 Microsoft PowerPoint 桌面版。
- Office 授权状态正常。
- PowerPoint 没有弹窗阻塞自动化流程。

## 2. Windows 手动集成测试（本机运行）

### 覆盖范围

- PowerPoint COM 自动化。
- 读取 PPT 页数和动画序列。
- 将 Timeline 写入已有 PPT 动画计时。
- 设置自动翻页。
- 调用 PowerPoint `CreateVideo` 导出背景视频。
- 生成并检查同步报告。

### 前置条件

- Windows 10/11。
- Microsoft PowerPoint 桌面版。
- Python 3.11+。
- 已安装项目依赖：`pip install -r requirements.txt && pip install -e .`。
- 可选：FFmpeg / ffprobe，用于检查导出视频信息。

### 2.1 准备示例项目

仓库已提供最小示例目录：

```text
examples/basic_project/
├── input/
│   └── lesson.pptx              # 手动创建或复制
├── work/
│   ├── timeline.example.json
│   └── timeline.json
└── output/
```

如果 `work/timeline.json` 不存在，可从示例复制：

```bash
cp examples/basic_project/work/timeline.example.json examples/basic_project/work/timeline.json
```

### 2.2 准备 PPT 文件

将一个有动画的 PPT 保存为：

```text
examples/basic_project/input/lesson.pptx
```

最小 PPT 要求：

- 5 页幻灯片。
- 第 1 页 2 个动画。
- 第 2 页 3 个动画。
- 第 3 页 2 个动画。
- 第 4 页 2 个动画。
- 第 5 页 1 个动画。
- 每页动画窗格顺序与 `timeline.json` 中的 `animation_index` 顺序一致。

### 2.3 运行 CLI 闭环测试

```bash
microcourse-ppt-sync run examples/basic_project --quality HD --fps 30
```

预期生成：

```text
examples/basic_project/work/lesson_timed.pptx
examples/basic_project/output/ppt_bg.mp4
examples/basic_project/output/sync_report.md
```

### 2.4 分步验证

如需定位问题，可按步骤执行：

```bash
microcourse-ppt-sync inspect examples/basic_project
microcourse-ppt-sync inspect_ppt examples/basic_project/input/lesson.pptx
microcourse-ppt-sync apply examples/basic_project examples/basic_project/input/lesson.pptx examples/basic_project/work/timeline.json
microcourse-ppt-sync export examples/basic_project/work/lesson_timed.pptx examples/basic_project/output/ppt_bg.mp4 --quality HD --fps 30
microcourse-ppt-sync report examples/basic_project examples/basic_project/work/timeline.json examples/basic_project/output/sync_report.md
```

### 2.5 验证 PPT 动画

打开 `examples/basic_project/work/lesson_timed.pptx`：

1. 进入幻灯片放映模式。
2. 验证每页动画按 Timeline 自动播放，无需鼠标点击。
3. 验证每页按 `advance_time` 自动翻页。

### 2.6 验证导出视频

打开 `examples/basic_project/output/ppt_bg.mp4`，确认动画保留且视频可播放。

如安装了 FFmpeg，可运行：

```bash
ffprobe -v error -show_format -show_streams examples/basic_project/output/ppt_bg.mp4
```

预期：

- 视频可正常解析。
- HD 导出时分辨率约为 1920x1080。
- 帧率为 30 fps。
- 示例 Timeline 时长约为 28 秒。

### 2.7 验证同步报告

打开 `examples/basic_project/output/sync_report.md`，确认报告包含：

- 项目信息。
- 总幻灯片数和总时长。
- 每页动画数量和时长。
- 问题和警告列表。

## 3. 常见问题

### 视频导出卡住或超时

可能原因：

- PowerPoint 有弹窗等待处理。
- Office 未完成首次启动或授权。
- 输出目录无写入权限。
- PPT 文件过大或包含复杂媒体。

建议处理：

1. 手动打开 PowerPoint，确认没有弹窗。
2. 关闭所有 PowerPoint 进程后重试。
3. 先用 `--quality SD` 降低导出质量。
4. 确认磁盘空间充足。

### 动画时间不符合预期

检查项：

1. `slide_index` 和 `animation_index` 是否从 0 开始。
2. Timeline 动画顺序是否与 PowerPoint 动画窗格顺序一致。
3. `advance_time` 是否大于最后一个动画的结束时间。
4. PPT 中是否缺少 Timeline 引用的动画。

### CI 中是否应该跑完整导出？

不建议。v0.1.0 推荐 CI 只跑普通单元测试，完整 PowerPoint COM / `CreateVideo` 导出放在 Windows 本机手动验证。
