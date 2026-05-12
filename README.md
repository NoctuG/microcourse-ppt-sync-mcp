# Microcourse PPT Sync MCP

一个纯后端 MCP Server，用于快速生成 PPT 微课。支持将人声时间戳转换为 PowerPoint 动画计时，并导出保留动画效果的 PPT 背景视频。

## 🎯 项目定位

本项目聚焦**最核心的问题**：将已有的人声时间戳或 `timeline.json` 转换为 PowerPoint 动画计时与自动翻页计时，并通过 PowerPoint 原生能力导出保留动画效果的 PPT 背景视频。

**不包含**：前端界面、ASR、人像抠像、剪映自动化。

**采用 Python**：因为核心能力依赖 Windows PowerPoint COM 自动化。PPT 视频导出使用 PowerPoint 原生 `Presentation.CreateVideo`。FFmpeg 仅用于可选的最终视频合成。

## ✅ MVP 功能清单（v0.1）

### 核心能力

- [x] **PPT 动画时间轴同步** - 将 timeline.json 应用到 PPT 动画
- [x] **自动翻页计时** - 按 timeline 设置每页的自动翻页时间
- [x] **PPT 背景视频导出** - 导出保留动画效果的 MP4 视频
- [x] **同步报告生成** - 生成诊断报告，列出每页时长、动画数量、异常项
- [x] **MCP Server 接口** - 标准输入/输出 (stdio) 传输
- [x] **CLI 工具** - 单个命令执行完整工作流

### 输入/输出

**输入：**
- `input/lesson.pptx` - 源 PowerPoint 文件（带动画）
- `work/timeline.json` - 人声时间轴（JSON 格式）

**输出：**
- `work/lesson_timed.pptx` - 带动画计时的 PowerPoint 文件
- `output/ppt_bg.mp4` - PPT 背景视频（无声，保留动画）
- `output/sync_report.md` - 同步诊断报告

## 🚀 快速开始

### 前置要求

- **Windows 10/11**
- **Python 3.11+**
- **Microsoft PowerPoint 桌面版**（2019 或更新）
- **FFmpeg**（可选，用于最终视频合成）

### 安装

```bash
# 克隆仓库
git clone https://github.com/NoctuG/microcourse-ppt-sync-mcp.git
cd microcourse-ppt-sync-mcp

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

### 创建示例项目

```bash
# 生成示例项目结构
python tests/demo_project.py D:/demo_project

# 此时您需要手动创建 input/lesson.pptx：
# 1. 打开 PowerPoint
# 2. 创建 5 页幻灯片，每页至少 1 个动画
# 3. 保存到 D:/demo_project/input/lesson.pptx
```

### 运行完整工作流

```bash
# 一键执行：检查 → 应用时间轴 → 导出视频 → 生成报告
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

## 📖 文档

### 用户文档

- **[Timeline 格式说明](docs/timeline-format.md)** - Timeline JSON 数据结构、动画类型、时间单位
- **[OpenClaw 使用指南](docs/openclaw-usage.md)** - 如何在 OpenClaw 中使用本 MCP Server
- **[Windows 集成测试指南](tests/INTEGRATION_TEST.md)** - 手动测试步骤、性能基准、常见问题

### 开发文档

- **[架构设计](docs/architecture.md)** - 系统架构、模块划分、数据流
- **[API 文档](docs/api.md)** - MCP Tools 详细说明
- **[开发指南](docs/development.md)** - 开发环境、代码风格、贡献规则

## 🔧 MCP Tools

### inspect_project
检查项目目录结构和文件

```bash
microcourse-ppt-sync inspect D:/demo_project
```

### inspect_ppt
读取 PPT 文件的动画序列

```bash
microcourse-ppt-sync inspect_ppt D:/demo_project/input/lesson.pptx
```

### build_timeline
从 transcript 生成 timeline.json

```bash
microcourse-ppt-sync build D:/demo_project D:/demo_project/work/transcript.json -s 5
```

### apply
将 timeline 应用到 PPT 动画

```bash
microcourse-ppt-sync apply D:/demo_project D:/demo_project/input/lesson.pptx D:/demo_project/work/timeline.json
```

### export
导出 PPT 背景视频

```bash
microcourse-ppt-sync export D:/demo_project/work/lesson_timed.pptx D:/demo_project/output/ppt_bg.mp4 --quality HD --fps 30
```

### report
生成同步诊断报告

```bash
microcourse-ppt-sync report D:/demo_project D:/demo_project/work/timeline.json D:/demo_project/output/sync_report.md
```

## 📊 项目结构

```
microcourse-ppt-sync-mcp/
├── src/
│   ├── mcp_server.py           # MCP Server 主程序
│   ├── main.py                 # CLI 主程序
│   ├── models/                 # 数据模型
│   ├── services/               # 业务逻辑（PPT、Timeline、Video、Report）
│   ├── tools/                  # MCP Tools 实现
│   └── utils/                  # 工具函数（Logger、Config、Validators）
├── tests/
│   ├── test_models.py          # 模型单元测试
│   ├── test_tools.py           # 工具单元测试
│   ├── demo_project.py         # 示例项目生成器
│   ├── INTEGRATION_TEST.md     # 集成测试指南
│   └── conftest.py             # Pytest 配置
├── docs/
│   ├── architecture.md         # 架构设计
│   ├── api.md                  # API 文档
│   ├── timeline-format.md      # Timeline 格式说明
│   ├── openclaw-usage.md       # OpenClaw 使用指南
│   └── development.md          # 开发指南
├── examples/
│   └── basic_project/          # 基础示例项目
├── Makefile                    # 快速命令
├── pytest.ini                  # Pytest 配置
├── requirements.txt            # 依赖列表
├── setup.py                    # 安装配置
├── CHANGELOG.md                # 版本历史
├── CONTRIBUTING.md             # 贡献指南
└── README.md                   # 本文件
```

## 🧪 测试

### 运行所有测试

```bash
make test
```

### 运行测试并生成覆盖率报告

```bash
make test-cov
```

### 代码检查

```bash
make lint
```

### 代码格式化

```bash
make format
```

## 🔄 工作流示例

### 场景：快速生成 Python 基础教程微课

**步骤 1：准备 PPT**
- 创建 5 页 PPT（标题、内容 1-3、总结）
- 为每页添加动画（出现、强调等）
- 保存为 `D:/microcourse/input/lesson.pptx`

**步骤 2：准备时间轴**
- 创建 `D:/microcourse/work/timeline.json`：

```json
{
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
        }
      ],
      "advance_time": 5.0
    }
    // ... 其他页面
  ]
}
```

**步骤 3：运行工作流**
```bash
microcourse-ppt-sync run D:/microcourse --quality HD --fps 30
```

**步骤 4：检查输出**
- `work/lesson_timed.pptx` - 带动画计时的 PPT
- `output/ppt_bg.mp4` - PPT 背景视频
- `output/sync_report.md` - 诊断报告

**步骤 5：在剪映中合成**
- 导入 `ppt_bg.mp4` 作为背景
- 添加已抠像的人像视频
- 添加人声音频
- 添加字幕、片头片尾
- 导出最终微课视频

## ⚠️ 已知限制

### v0.1 MVP

- **仅支持 Windows** - 依赖 PowerPoint COM 自动化
- **需要桌面版 PowerPoint** - 不支持 Office 365 在线版
- **Timeline 手动编写** - 不支持自动 ASR 转录
- **不支持 SRT/VTT** - 仅支持 JSON 格式
- **无人像处理** - 不包含抠像、合成等功能
- **无剪映集成** - 需要手动在剪映中完成最后的合成

### 性能基准

在标准 Windows 10 机器上（i7, 16GB RAM）：

| 操作 | 时间 |
|------|------|
| 打开 PPT | 2-3 秒 |
| 应用 timeline | 1-2 秒 |
| 导出视频（5 页，HD） | 30-60 秒 |
| 生成报告 | < 1 秒 |
| **总计** | **35-70 秒** |

## 🗺️ 开发路线

### v0.1 (当前) ✅
- [x] PPT 动画时间轴同步
- [x] 自动翻页计时
- [x] 视频导出
- [x] 报告生成
- [x] MCP Server 接口
- [x] CLI 工具

### v0.2 (进行中)
- [ ] Transcript 自动生成 Timeline
- [ ] SRT 格式支持
- [ ] VTT 格式支持
- [ ] Timeline 验证

### v0.3
- [ ] 增强 sync_report 诊断
- [ ] 错误检查和建议

### v0.4
- [ ] FFmpeg 视频合成
- [ ] 人像透明度合成
- [ ] 音频混音
- [ ] 最终视频导出

### v0.5
- [ ] 音频按 slide 切分
- [ ] PPT 内嵌旁白视频模式

## 🤝 贡献

欢迎提交 Issue 和 PR！请参考 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📝 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 📧 联系方式

如有问题或建议，请：
1. 提交 [GitHub Issue](https://github.com/NoctuG/microcourse-ppt-sync-mcp/issues)
2. 查看 [常见问题](docs/faq.md)
3. 阅读 [集成测试指南](tests/INTEGRATION_TEST.md)
