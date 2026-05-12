# Microcourse PPT Sync MCP

一个纯后端 MCP Server，用于快速生成 PPT 微课。支持将人声时间戳转换为 PowerPoint 动画计时，并导出保留动画效果的 PPT 背景视频。

## 项目定位

本项目第一阶段是纯后端 MCP Server，不包含前端界面、ASR、人像抠像或剪映自动化。

第一阶段只聚焦最核心的问题：将已有的人声时间戳或 `timeline.json` 转换为 PowerPoint 动画计时与自动翻页计时，并通过 PowerPoint 原生能力导出保留动画效果的 PPT 背景视频。

项目采用 Python 实现，因为核心能力依赖 Windows PowerPoint COM 自动化。PPT 视频导出使用 PowerPoint 原生 `Presentation.CreateVideo`。FFmpeg 仅用于可选的最终视频合成。

## 核心特性

### 第一阶段：PPT 背景视频模式

**输入：**
- `lesson.pptx` - 源 PowerPoint 文件
- `timeline.json` 或 `transcript.json` - 人声时间戳

**输出：**
- `lesson_timed.pptx` - 带动画计时的 PowerPoint 文件
- `ppt_bg.mp4` - PPT 背景视频（无声）
- `sync_report.md` - 同步报告

**工作流：**
1. 读取项目目录
2. 找到 `input/lesson.pptx`
3. 读取 `work/timeline.json`
4. 打开 PowerPoint
5. 读取每页动画序列
6. 按 timeline 设置动画 `TriggerDelayTime` 和 `Duration`
7. 设置每页自动翻页 `AdvanceTime`
8. 另存为 `work/lesson_timed.pptx`
9. 调用 PowerPoint `CreateVideo` 导出 `work/ppt_bg.mp4`
10. 生成 `output/sync_report.md`

## MCP Tools

### inspect_project
检查项目目录结构和文件

### inspect_ppt
读取 PPT 文件的动画序列

### build_timeline
从 transcript 生成 timeline.json

### apply_ppt_timeline
将 timeline 应用到 PPT 动画

### export_ppt_video
导出 PPT 背景视频

### generate_sync_report
生成同步报告

## 技术栈

- **语言**：Python 3.12+
- **MCP**：modelcontextprotocol Python SDK
- **PowerPoint 控制**：pywin32 / PowerPoint COM
- **视频合成**：FFmpeg
- **配置格式**：JSON / YAML
- **运行环境**：Windows 10/11 + Microsoft PowerPoint 桌面版

## 项目结构

```
microcourse-ppt-sync-mcp/
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   ├── mcp_server.py           # MCP Server 入口
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── inspect_tools.py    # 检查工具
│   │   ├── timeline_tools.py   # 时间轴工具
│   │   ├── ppt_tools.py        # PPT 处理工具
│   │   ├── export_tools.py     # 导出工具
│   │   └── report_tools.py     # 报告生成工具
│   ├── models/
│   │   ├── __init__.py
│   │   ├── timeline.py         # Timeline 数据模型
│   │   ├── ppt_animation.py    # PPT 动画模型
│   │   └── report.py           # 报告模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ppt_service.py      # PPT 服务（COM 操作）
│   │   ├── timeline_service.py # 时间轴服务
│   │   ├── video_service.py    # 视频导出服务
│   │   └── report_service.py   # 报告生成服务
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # 日志
│       ├── config.py           # 配置
│       └── validators.py       # 验证器
├── tests/
│   ├── __init__.py
│   ├── test_timeline.py
│   ├── test_ppt_service.py
│   ├── test_export.py
│   └── fixtures/
│       └── sample_project/     # 测试项目样本
├── docs/
│   ├── architecture.md         # 架构文档
│   ├── api.md                  # API 文档
│   ├── timeline_format.md      # Timeline 格式说明
│   └── development.md          # 开发指南
└── .gitignore
```

## 安装与运行

### 前置要求

- Windows 10/11
- Python 3.12+
- Microsoft PowerPoint 桌面版
- FFmpeg

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行 MCP Server

```bash
python src/mcp_server.py
```

### CLI 调试

```bash
python -m src.cli run D:/microcourse/demo
```

## 开发路线

### 第一阶段（MVP）
- [x] 项目结构设计
- [ ] MCP Server 基础框架
- [ ] PPT COM 操作模块
- [ ] Timeline 解析模块
- [ ] 动画时间轴应用
- [ ] 视频导出功能
- [ ] 报告生成功能
- [ ] 单元测试
- [ ] 集成测试
- [ ] 文档

### 第二阶段
- [ ] Transcript 解析和 Timeline 自动生成
- [ ] 支持 SRT、VTT 格式

### 第三阶段
- [ ] 最终视频合成（PPT 背景 + 人像 + 音频）

### 第四阶段
- [ ] PPT 内嵌旁白视频模式

## 许可证

MIT

## 联系方式

如有问题或建议，请提交 Issue 或 PR。
