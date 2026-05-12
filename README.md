# Microcourse PPT Sync MCP

一个纯后端 MCP Server，用于快速生成 PPT 微课。v0.1.0 聚焦一个闭环：读取已有 `timeline.json`，写入 PowerPoint 动画计时与自动翻页计时，并通过 PowerPoint 原生能力导出保留动画效果的 PPT 背景视频。

## 🎯 项目定位

本项目只解决第一阶段最核心的问题：

1. 读取用户已经准备好的 PPT 和 Timeline JSON。
2. 将 Timeline 转换为 PowerPoint 动画 `TriggerDelayTime`、`Duration` 和自动翻页时间。
3. 调用 PowerPoint 桌面版 `Presentation.CreateVideo` 导出 PPT 背景视频。
4. 生成同步报告，便于检查每页时长、动画数量和潜在问题。

**不包含**：前端界面、ASR、SRT/VTT 解析、人像抠像、剪映自动化或最终视频合成。

## ✅ v0.1.0 已支持能力

- **读取 Timeline JSON**：支持读取 `lesson_name`、`slides`、`animations`、`trigger_time`、`duration`、`advance_time` 等字段。
- **写入 PPT 动画计时**：将 Timeline 中的动画触发时间和持续时间应用到 PowerPoint 动画序列。
- **设置自动翻页**：按每页 `advance_time` 设置幻灯片自动换页时间。
- **导出 PPT 背景视频**：通过 PowerPoint 原生导出能力生成保留动画效果的 MP4 背景视频。
- **生成同步报告**：输出每页时长、动画数量和异常提示。
- **提供 MCP Tools 与 CLI**：支持通过 MCP stdio 工具或 `microcourse-ppt-sync` 命令执行工作流。
- **提供基础示例项目**：`examples/basic_project/` 包含最小目录结构和 Timeline 示例。

## ✅ MVP 状态清单

### 第一阶段核心闭环

- [x] 项目结构设计
- [x] MCP Server 基础框架
- [x] PPT COM 操作模块
- [x] Timeline 解析模块
- [x] 动画时间轴应用
- [x] 自动翻页计时
- [x] 视频导出功能
- [x] 报告生成功能
- [x] CLI 工具
- [x] Timeline 格式文档
- [x] 基础示例项目
- [x] 集成测试说明

### 测试覆盖现状

- [x] 普通单元测试：Timeline / tools 等可在非 Windows 环境运行的测试。
- [x] Windows 手动集成测试说明：PowerPoint COM / CreateVideo 需要 Windows + PowerPoint 桌面版本机验证。
- [ ] CI 中完整覆盖 PowerPoint COM 导出：受 PowerPoint 桌面版和 Windows 图形环境限制，暂不作为 v0.1.0 自动化 CI 目标。

## 📁 标准项目结构

```text
project/
├── input/
│   └── lesson.pptx          # 源 PPT 文件，用户手动提供
├── work/
│   ├── timeline.json        # 输入 Timeline
│   └── lesson_timed.pptx    # 输出：写入计时后的 PPT
└── output/
    ├── ppt_bg.mp4           # 输出：PPT 背景视频
    └── sync_report.md       # 输出：同步报告
```

最小示例位于 [`examples/basic_project/`](examples/basic_project/README.md)。示例仓库不提交真实 PPT 大文件，请将自己的 PPT 保存为 `examples/basic_project/input/lesson.pptx`，并将 `work/timeline.example.json` 复制为 `work/timeline.json` 后运行。

## 🚀 快速开始

### 前置要求

- Windows 10/11
- Python 3.11+
- Microsoft PowerPoint 桌面版（2019 或更新）
- Git

> v0.1.0 的 PPT 处理和视频导出依赖 PowerPoint COM，仅 Windows + PowerPoint 桌面版可完整运行。

### 安装

```bash
git clone https://github.com/NoctuG/microcourse-ppt-sync-mcp.git
cd microcourse-ppt-sync-mcp
pip install -r requirements.txt
pip install -e .
```

### 准备示例项目

```bash
# 从仓库根目录执行
cp examples/basic_project/work/timeline.example.json examples/basic_project/work/timeline.json

# 手动创建或复制一个带动画的 PPT 到：
# examples/basic_project/input/lesson.pptx
```

PPT 最小要求：

- 与 Timeline 页数一致。
- 每页动画数量不少于该页 `animations` 数组中引用的数量。
- 动画顺序与 `animation_index` 一致。

### 运行完整工作流

```bash
microcourse-ppt-sync run examples/basic_project --quality HD --fps 30
```

预期输出：

```text
examples/basic_project/work/lesson_timed.pptx
examples/basic_project/output/ppt_bg.mp4
examples/basic_project/output/sync_report.md
```

## 🔧 MCP Tools / CLI

| MCP Tool | CLI 示例 | 说明 |
| --- | --- | --- |
| `inspect_project` | `microcourse-ppt-sync inspect examples/basic_project` | 检查项目目录结构。 |
| `inspect_ppt` | `microcourse-ppt-sync inspect_ppt examples/basic_project/input/lesson.pptx` | 读取 PPT 页数和动画序列。 |
| `build_timeline` | `microcourse-ppt-sync build examples/basic_project examples/basic_project/work/transcript.json -s 5` | 从 transcript 生成 Timeline（辅助能力）。 |
| `apply_ppt_timeline` | `microcourse-ppt-sync apply examples/basic_project examples/basic_project/input/lesson.pptx examples/basic_project/work/timeline.json` | 将 Timeline 写入 PPT 动画和翻页计时。 |
| `export_ppt_video` | `microcourse-ppt-sync export examples/basic_project/work/lesson_timed.pptx examples/basic_project/output/ppt_bg.mp4 --quality HD --fps 30` | 导出 PPT 背景视频。 |
| `generate_sync_report` | `microcourse-ppt-sync report examples/basic_project examples/basic_project/work/timeline.json examples/basic_project/output/sync_report.md` | 生成同步诊断报告。 |

## 📖 文档

- [Timeline 格式说明](docs/timeline_format.md)
- [基础示例项目](examples/basic_project/README.md)
- [Windows 手动集成测试指南](tests/INTEGRATION_TEST.md)
- [v0.1.0 Release Notes](docs/releases/v0.1.0.md)
- [API 文档](docs/api.md)
- [架构设计](docs/architecture.md)
- [开发指南](docs/development.md)

## 🧪 测试策略

### 普通单元测试（可用于 CI）

覆盖不依赖 PowerPoint 桌面版的逻辑，例如 Timeline 数据模型、validators、report 和 MCP tool schema。

```bash
pytest tests/test_models.py tests/test_tools.py
```

### Windows 手动集成测试（本机运行）

覆盖 PowerPoint COM、写入动画计时、自动翻页和 `CreateVideo` 导出。请在 Windows 10/11 + PowerPoint 桌面版环境按 [集成测试指南](tests/INTEGRATION_TEST.md) 执行。

## ⚠️ 已知限制

- 仅 Windows + Microsoft PowerPoint 桌面版可完整处理 PPT 和导出视频。
- 示例项目不包含真实 `lesson.pptx` 大文件，需要用户自行创建或复制。
- `timeline.json` 中的动画顺序必须与 PPT 动画窗格顺序匹配。
- 当前不处理 ASR、SRT/VTT、剪映自动化、人像合成或音频合成。
- 大型 PPT 导出耗时较长，期间应避免关闭 PowerPoint 或让系统休眠。

## 🗺️ 后续方向

v0.1.0 之后的功能将保持插件式和可选，不影响当前 Timeline → PPT 计时 → PPT 背景视频导出的核心闭环。后续可能补充更多输入格式、诊断能力和视频合成能力，但 v0.1.0 Release 不包含这些功能。

## 📝 许可证

MIT License。
