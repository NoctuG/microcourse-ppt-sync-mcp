# 开发指南

## 环境设置

### 前置要求

- Windows 10/11
- Python 3.12+
- Microsoft PowerPoint 桌面版
- Git

### 安装开发环境

```bash
# 克隆仓库
git clone https://github.com/NoctuG/microcourse-ppt-sync-mcp.git
cd microcourse-ppt-sync-mcp

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -e .
```

### 验证安装

```bash
python -c "from src.utils import get_logger; logger = get_logger(__name__); logger.info('Setup OK')"
```

## 项目结构

```
src/
├── __init__.py
├── mcp_server.py           # MCP Server 主程序
├── tools/                  # MCP Tools 实现
│   ├── __init__.py
│   ├── inspect_tools.py
│   ├── timeline_tools.py
│   ├── ppt_tools.py
│   ├── export_tools.py
│   └── report_tools.py
├── models/                 # 数据模型
│   ├── __init__.py
│   ├── timeline.py
│   ├── ppt_animation.py
│   └── report.py
├── services/               # 业务逻辑服务
│   ├── __init__.py
│   ├── ppt_service.py
│   ├── timeline_service.py
│   ├── video_service.py
│   └── report_service.py
└── utils/                  # 工具函数
    ├── __init__.py
    ├── logger.py
    ├── config.py
    └── validators.py

tests/
├── __init__.py
├── test_timeline.py
├── test_ppt_service.py
├── test_export.py
└── fixtures/
    └── sample_project/

docs/
├── architecture.md
├── api.md
├── timeline_format.md
└── development.md
```

## 开发工作流

### 1. 创建新功能

#### 步骤 1：定义数据模型

在 `src/models/` 中创建新的数据模型：

```python
# src/models/new_model.py
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class NewModel:
    """新数据模型"""
    name: str
    value: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "value": self.value}
```

#### 步骤 2：实现服务

在 `src/services/` 中实现业务逻辑：

```python
# src/services/new_service.py
from src.utils import get_logger
from src.models import NewModel

logger = get_logger(__name__)

class NewService:
    @staticmethod
    def process(data: Dict[str, Any]) -> NewModel:
        """处理数据"""
        try:
            result = NewModel(
                name=data.get("name", ""),
                value=data.get("value", 0.0)
            )
            logger.info(f"Processed: {result}")
            return result
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            raise
```

#### 步骤 3：创建 MCP Tool

在 `src/tools/` 中创建新的工具：

```python
# src/tools/new_tools.py
from typing import Dict, Any
from src.utils import get_logger
from src.services import NewService

logger = get_logger(__name__)

def process_new_data(project_path: str, data_path: str) -> Dict[str, Any]:
    """处理新数据"""
    try:
        # 加载数据
        data = load_data(data_path)
        
        # 处理数据
        result = NewService.process(data)
        
        logger.info(f"Tool executed successfully")
        return {
            "status": "success",
            "result": result.to_dict()
        }
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
```

#### 步骤 4：注册 Tool

在 `src/mcp_server.py` 中注册新的工具：

```python
self.tools = {
    # ... 其他工具 ...
    "process_new_data": {
        "description": "处理新数据",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_path": {"type": "string"},
                "data_path": {"type": "string"}
            },
            "required": ["project_path", "data_path"]
        },
        "handler": process_new_data,
    },
}
```

### 2. 编写测试

#### 单元测试

```python
# tests/test_new_service.py
import pytest
from src.models import NewModel
from src.services import NewService

def test_new_service_process():
    """测试 NewService.process"""
    data = {"name": "test", "value": 3.14}
    result = NewService.process(data)
    
    assert isinstance(result, NewModel)
    assert result.name == "test"
    assert result.value == 3.14

def test_new_service_error_handling():
    """测试错误处理"""
    with pytest.raises(Exception):
        NewService.process(None)
```

#### 集成测试

```python
# tests/test_integration.py
import json
from pathlib import Path
from src.tools import process_new_data

def test_process_new_data_integration(tmp_path):
    """测试完整的数据处理流程"""
    # 创建测试数据
    project_path = tmp_path / "project"
    project_path.mkdir()
    
    data_path = project_path / "data.json"
    with open(data_path, "w") as f:
        json.dump({"name": "test", "value": 3.14}, f)
    
    # 执行工具
    result = process_new_data(str(project_path), str(data_path))
    
    assert result["status"] == "success"
    assert result["result"]["name"] == "test"
```

### 3. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_new_service.py

# 运行特定测试函数
pytest tests/test_new_service.py::test_new_service_process

# 生成覆盖率报告
pytest --cov=src tests/
```

### 4. 代码质量检查

```bash
# 代码格式检查
black src/ tests/

# 代码风格检查
flake8 src/ tests/

# 类型检查
mypy src/
```

## 常见任务

### 添加新的 Transcript 格式支持

1. 在 `src/services/timeline_service.py` 中添加新的解析方法：

```python
@staticmethod
def parse_srt_to_timeline(srt_path: str, slide_count: int) -> Optional[Timeline]:
    """从 SRT 文件解析 Timeline"""
    # 实现 SRT 解析逻辑
    pass
```

2. 在 `src/tools/timeline_tools.py` 中添加新的工具：

```python
def build_timeline_from_srt(
    project_path: str,
    srt_path: str,
    slide_count: int,
) -> Dict[str, Any]:
    """从 SRT 文件构建 Timeline"""
    # 实现工具逻辑
    pass
```

### 优化 PPT 处理性能

1. 在 `src/services/ppt_service.py` 中添加缓存机制：

```python
class PPTService:
    def __init__(self):
        self.cache = {}
    
    def get_slide_animations(self, slide_index: int):
        # 检查缓存
        if slide_index in self.cache:
            return self.cache[slide_index]
        
        # 获取数据
        result = self._fetch_animations(slide_index)
        
        # 缓存结果
        self.cache[slide_index] = result
        return result
```

### 添加日志输出

```python
from src.utils import get_logger

logger = get_logger(__name__)

# 不同级别的日志
logger.debug("调试信息")
logger.info("一般信息")
logger.warning("警告信息")
logger.error("错误信息")
```

## 调试技巧

### 1. 启用调试日志

```python
import logging
from src.utils import get_logger

# 设置为 DEBUG 级别
logger = get_logger(__name__, level=logging.DEBUG)
```

### 2. 使用 Python 调试器

```python
import pdb

# 在代码中设置断点
pdb.set_trace()

# 或者使用 breakpoint()（Python 3.7+）
breakpoint()
```

### 3. 检查 COM 对象状态

```python
# 在 PPTService 中添加调试代码
if self.presentation:
    print(f"Presentation: {self.presentation.Name}")
    print(f"Slide count: {self.presentation.Slides.Count}")
    for i, slide in enumerate(self.presentation.Slides):
        print(f"Slide {i}: {len(slide.Shapes)} shapes")
```

## 发布新版本

1. 更新版本号：

```python
# src/__init__.py
__version__ = "0.2.0"

# setup.py
version="0.2.0",
```

2. 更新 CHANGELOG：

```markdown
# Changelog

## [0.2.0] - 2024-05-12

### Added
- 新功能 1
- 新功能 2

### Fixed
- 修复问题 1
- 修复问题 2

### Changed
- 改进 1
- 改进 2
```

3. 提交更改并创建标签：

```bash
git add -A
git commit -m "Release v0.2.0"
git tag -a v0.2.0 -m "Version 0.2.0"
git push origin main --tags
```

## 常见问题

### Q: 如何在 Linux 上开发？

A: 第一版只支持 Windows + PowerPoint。如果需要在 Linux 上开发，可以：
1. 使用 Windows 虚拟机
2. 使用 WSL 2 + Windows PowerPoint
3. 等待第二版支持 LibreOffice（兼容性可能有限）

### Q: 如何处理大型 PPT 文件？

A: 建议：
1. 分割大型 PPT 为多个小文件
2. 使用后台任务处理
3. 监控内存使用情况

### Q: 如何调试 PowerPoint COM 操作？

A: 建议：
1. 启用 PowerPoint 的 VBA 编辑器查看 COM 对象结构
2. 使用 `pywin32` 的 `win32com.client.Dispatch("PowerPoint.Application")` 进行交互式调试
3. 查看 Microsoft Office VBA 文档

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 联系方式

如有问题或建议，请提交 Issue 或 PR。
