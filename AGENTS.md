# Microcourse PPT Sync MCP - Agent Notes

## 项目信息

**项目名称**：Microcourse PPT Sync MCP  
**项目类型**：纯后端 MCP Server  
**创建日期**：2024-05-12  
**技术栈**：Python 3.12+ | pywin32 | MCP Python SDK | FFmpeg  
**运行环境**：Windows 10/11 + Microsoft PowerPoint 桌面版  

## 项目定位

本项目是一个纯后端 MCP Server，用于快速生成 PPT 微课。第一阶段只聚焦最核心的问题：

**将已有的人声时间戳或 timeline.json 转换为 PowerPoint 动画计时与自动翻页计时，并通过 PowerPoint 原生能力导出保留动画效果的 PPT 背景视频。**

## 核心设计决策

### 1. 为什么使用 Python 而不是 Node.js？

- PowerPoint COM 自动化是核心需求
- Python 的 `pywin32` 比 Node.js 的 COM 库更成熟
- MCP Python SDK 完全支持 tools/resources/prompts

### 2. 为什么不内置 ASR？

- 项目假设用户已有时间戳文本（transcript.json）
- ASR 引入模型下载、GPU、API Key、隐私等问题
- 第一版只做 parse_transcript，不做 speech_to_text
- 后续可以做插件式适配（Whisper、Azure Speech 等）

### 3. 为什么使用 PowerPoint COM 而不是 python-pptx？

- `python-pptx` 不能可靠处理动画时间轴
- PowerPoint COM 提供原生的 `Timing.TriggerDelayTime` 和 `Timing.Duration`
- `Presentation.CreateVideo` 是唯一能保留动画效果的导出方式

### 4. 为什么 FFmpeg 不是核心？

- PPT 动画视频导出完全由 PowerPoint 负责
- FFmpeg 只用于可选的最终视频合成（第三阶段）
- 这样可以保持 MVP 范围清晰

## 项目结构

```
src/
├── tools/              # MCP Tools 实现（6 个工具）
├── models/             # 数据模型（Timeline、Slide、Animation 等）
├── services/           # 业务逻辑服务（PPT、Timeline、Video、Report）
└── utils/              # 工具函数（Logger、Config、Validators）

tests/                  # 单元测试和集成测试
docs/                   # 文档（架构、API、Timeline 格式、开发指南）
```

## MCP Tools

### 已实现的 6 个工具

1. **inspect_project** - 检查项目目录结构
2. **inspect_ppt** - 检查 PPT 文件信息
3. **build_timeline** - 从 Transcript 生成 Timeline
4. **apply_ppt_timeline** - 将 Timeline 应用到 PPT
5. **export_ppt_video** - 导出 PPT 背景视频
6. **generate_sync_report** - 生成同步报告

## 工作流

### PPT 背景视频模式（第一阶段）

```
项目目录
  ├── input/lesson.pptx          # 源 PPT 文件
  ├── work/
  │   ├── transcript.json        # 人声时间戳（输入）
  │   ├── timeline.json          # 生成的时间轴
  │   └── lesson_timed.pptx      # 带动画计时的 PPT
  └── output/
      ├── ppt_bg.mp4             # PPT 背景视频
      └── sync_report.md         # 同步报告

工作流：
1. inspect_project → 检查项目结构
2. inspect_ppt → 检查 PPT 文件
3. build_timeline → 从 transcript.json 生成 timeline.json
4. apply_ppt_timeline → 将 timeline 应用到 PPT
5. export_ppt_video → 导出 PPT 背景视频
6. generate_sync_report → 生成同步报告
```

## 开发路线

### 第一阶段（MVP）✅ 完成
- [x] 项目结构设计
- [x] MCP Server 基础框架
- [x] PPT COM 操作模块
- [x] Timeline 解析模块
- [x] 动画时间轴应用
- [x] 视频导出功能
- [x] 报告生成功能
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

## 关键文件

| 文件 | 说明 |
|------|------|
| `README.md` | 项目概述 |
| `setup.py` | 项目配置 |
| `requirements.txt` | 依赖列表 |
| `src/mcp_server.py` | MCP Server 主程序 |
| `docs/architecture.md` | 架构文档 |
| `docs/api.md` | API 文档 |
| `docs/timeline_format.md` | Timeline 格式说明 |
| `docs/development.md` | 开发指南 |

## 环境要求

### 必需
- Windows 10/11
- Python 3.12+
- Microsoft PowerPoint 桌面版
- Git

### 可选
- FFmpeg（用于视频合成）
- pywin32（用于 COM 操作）

## 安装和运行

```bash
# 克隆仓库
git clone https://github.com/NoctuG/microcourse-ppt-sync-mcp.git
cd microcourse-ppt-sync-mcp

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行 MCP Server
python src/mcp_server.py
```

## 已知限制

1. **Windows 环境**：PPT 处理功能仅在 Windows 10/11 + Microsoft PowerPoint 环境下工作
2. **文件路径**：所有路径应该是绝对路径
3. **并发**：当前实现不支持并发处理多个项目
4. **超时**：大型 PPT 文件的导出可能需要较长时间
5. **内存**：建议在内存充足的机器上运行（至少 4GB）

## 下一步工作

1. **编写单元测试**
   - 测试 Timeline 解析
   - 测试 PPT 服务
   - 测试报告生成

2. **编写集成测试**
   - 测试完整工作流
   - 测试错误处理

3. **性能优化**
   - 添加进度回调
   - 优化 COM 操作
   - 添加缓存机制

4. **功能扩展**
   - 支持 SRT/VTT 格式
   - 支持视频合成
   - 支持 PPT 内嵌旁白模式

## 联系方式

项目维护者：Manus Agent  
GitHub：https://github.com/NoctuG/microcourse-ppt-sync-mcp

## 许可证

MIT
