# 架构文档

## 概述

Microcourse PPT Sync MCP 是一个纯后端 MCP Server，用于快速生成 PPT 微课。项目采用分层架构，将功能模块清晰地分离。

## 架构层次

### 1. MCP 工具层 (`src/tools/`)

暴露给 OpenClaw 的接口层。每个工具对应一个 MCP Tool。

- **inspect_tools.py**：项目和 PPT 检查工具
- **timeline_tools.py**：时间轴生成工具
- **ppt_tools.py**：PPT 处理工具
- **export_tools.py**：视频导出工具
- **report_tools.py**：报告生成工具

### 2. 服务层 (`src/services/`)

核心业务逻辑层。每个服务负责一个特定的功能域。

- **PPTService**：PowerPoint COM 操作
- **TimelineService**：时间轴解析和管理
- **VideoService**：视频处理（FFmpeg）
- **ReportService**：报告生成

### 3. 数据模型层 (`src/models/`)

数据结构定义。

- **Timeline**：时间轴数据结构
- **Slide**：幻灯片数据结构
- **Animation**：动画数据结构
- **PPTAnimation**：PPT 动画对象
- **SyncReport**：同步报告

### 4. 工具层 (`src/utils/`)

通用工具和配置。

- **logger.py**：日志配置
- **config.py**：配置管理
- **validators.py**：输入验证

## 数据流

### PPT 背景视频模式工作流

```
项目目录
  ├── input/
  │   └── lesson.pptx          # 源 PPT 文件
  ├── work/
  │   ├── transcript.json      # 人声时间戳（输入）
  │   ├── timeline.json        # 生成的时间轴
  │   └── lesson_timed.pptx    # 带动画计时的 PPT
  └── output/
      ├── ppt_bg.mp4           # PPT 背景视频
      └── sync_report.md       # 同步报告

工作流：
1. inspect_project → 检查项目结构
2. inspect_ppt → 检查 PPT 文件
3. build_timeline → 从 transcript.json 生成 timeline.json
4. apply_ppt_timeline → 将 timeline 应用到 PPT
5. export_ppt_video → 导出 PPT 背景视频
6. generate_sync_report → 生成同步报告
```

## 关键设计决策

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

## 扩展点

### 第二阶段：Transcript 解析扩展

添加对 SRT、VTT 格式的支持：

```python
# src/services/transcript_parser.py
class TranscriptParser:
    @staticmethod
    def parse_srt(srt_path: str) -> Dict[str, Any]:
        # 解析 SRT 文件
        pass
    
    @staticmethod
    def parse_vtt(vtt_path: str) -> Dict[str, Any]:
        # 解析 VTT 文件
        pass
```

### 第三阶段：视频合成

```python
# src/services/video_service.py
def compose_final_video(
    ppt_bg_video: str,
    presenter_video: str,
    audio_file: str,
    output_path: str,
) -> bool:
    # 使用 FFmpeg 合成最终视频
    pass
```

### 第四阶段：PPT 内嵌旁白模式

```python
# src/services/ppt_service.py
def embed_audio_to_ppt(
    ppt_path: str,
    audio_segments: List[str],
    output_path: str,
) -> bool:
    # 将音频嵌入到 PPT 每一页
    pass
```

## 错误处理

所有服务都遵循一致的错误处理模式：

```python
try:
    # 业务逻辑
    result = operation()
    logger.info(f"Success: {result}")
    return result
except ValidationError as e:
    logger.error(f"Validation error: {e}")
    return {"status": "error", "message": str(e)}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"status": "error", "message": str(e)}
```

## 性能考虑

### PPT 处理

- PowerPoint COM 操作在 Windows 上是同步的
- 大型 PPT 文件（100+ 页）可能需要较长时间
- 建议添加进度回调（未来版本）

### 视频导出

- `Presentation.CreateVideo` 是 CPU 密集操作
- 导出时间取决于幻灯片数量、动画复杂度、视频质量
- 建议在后台任务中运行

## 安全考虑

- 所有文件路径都通过 `validators.py` 验证
- 输入数据通过 `validate_*` 函数检查
- 日志不记录敏感信息
- PPT 文件操作在隔离的 COM 对象中进行
