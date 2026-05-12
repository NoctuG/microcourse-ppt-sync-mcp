# Timeline 格式说明

## 概述

Timeline 是一个 JSON 格式的文件，用于定义 PPT 每一页的动画时间轴和翻页时间。

## 文件结构

```json
{
  "lesson_name": "示例微课",
  "slides": [
    {
      "slide_index": 0,
      "animations": [
        {
          "animation_index": 0,
          "animation_type": "appear",
          "trigger_time": 0.0,
          "duration": 0.5,
          "object_name": "标题",
          "metadata": {}
        }
      ],
      "advance_time": 5.0,
      "notes": "这是第一页的备注",
      "metadata": {}
    }
  ],
  "total_duration": 25.0,
  "metadata": {}
}
```

## 字段说明

### 顶层字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `lesson_name` | string | 是 | 微课名称 |
| `slides` | array | 是 | 幻灯片列表 |
| `total_duration` | number | 否 | 总时长（秒） |
| `metadata` | object | 否 | 元数据 |

### Slide 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `slide_index` | integer | 是 | 幻灯片索引（从 0 开始） |
| `animations` | array | 是 | 动画列表 |
| `advance_time` | number | 否 | 自动翻页时间（秒） |
| `notes` | string | 否 | 幻灯片备注 |
| `metadata` | object | 否 | 元数据 |

### Animation 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `animation_index` | integer | 是 | 动画索引（从 0 开始） |
| `animation_type` | string | 是 | 动画类型（appear, disappear, emphasis, exit, motion_path） |
| `trigger_time` | number | 是 | 触发时间（秒，相对于幻灯片开始） |
| `duration` | number | 否 | 动画持续时间（秒，默认 0.5） |
| `object_name` | string | 否 | 对象名称 |
| `metadata` | object | 否 | 元数据 |

## 动画类型

- **appear**：出现动画
- **disappear**：消失动画
- **emphasis**：强调动画
- **exit**：退出动画
- **motion_path**：运动路径动画

## 示例

### 简单示例

```json
{
  "lesson_name": "Python 基础",
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
        },
        {
          "animation_index": 1,
          "animation_type": "appear",
          "trigger_time": 1.0,
          "duration": 0.5,
          "object_name": "副标题"
        }
      ],
      "advance_time": 5.0
    },
    {
      "slide_index": 1,
      "animations": [
        {
          "animation_index": 0,
          "animation_type": "appear",
          "trigger_time": 0.0,
          "duration": 0.3,
          "object_name": "内容"
        }
      ],
      "advance_time": 8.0
    }
  ],
  "total_duration": 13.0
}
```

### 复杂示例（多个动画）

```json
{
  "lesson_name": "数据可视化",
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
        },
        {
          "animation_index": 1,
          "animation_type": "appear",
          "trigger_time": 1.5,
          "duration": 0.5,
          "object_name": "图表背景"
        },
        {
          "animation_index": 2,
          "animation_type": "emphasis",
          "trigger_time": 2.5,
          "duration": 1.0,
          "object_name": "数据系列1"
        },
        {
          "animation_index": 3,
          "animation_type": "emphasis",
          "trigger_time": 3.8,
          "duration": 1.0,
          "object_name": "数据系列2"
        }
      ],
      "advance_time": 6.0,
      "notes": "展示数据对比"
    }
  ],
  "total_duration": 6.0
}
```

## 从 Transcript 生成 Timeline

### Transcript 格式

```json
{
  "lesson_name": "示例微课",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "大家好，欢迎来到本次微课"
    },
    {
      "start": 3.5,
      "end": 8.2,
      "text": "今天我们要学习的是..."
    }
  ]
}
```

### 生成过程

1. 读取 transcript.json
2. 根据幻灯片数量分配 segments
3. 为每个 segment 创建一个 animation
4. 设置 trigger_time 和 duration
5. 计算 advance_time
6. 保存为 timeline.json

## 验证规则

### 必需字段检查

- `lesson_name` 不能为空
- `slides` 必须是非空数组
- 每个 slide 必须有 `slide_index` 和 `animations`
- 每个 animation 必须有 `animation_index`、`animation_type` 和 `trigger_time`

### 逻辑检查

- `slide_index` 必须从 0 开始，连续递增
- `animation_index` 在每个 slide 内必须从 0 开始，连续递增
- `trigger_time` 和 `duration` 必须是非负数
- `animation_type` 必须是有效的类型之一
- `advance_time` 应该大于等于所有 animation 的 end_time

## 最佳实践

1. **时间精度**：使用小数点精确到 0.1 秒
2. **命名规范**：`object_name` 应该与 PPT 中的对象名称一致
3. **元数据**：在 `metadata` 中记录额外信息（如来源、版本等）
4. **验证**：生成后使用 `generate_sync_report` 验证
5. **备注**：在 `notes` 中记录关键信息，便于后期编辑
