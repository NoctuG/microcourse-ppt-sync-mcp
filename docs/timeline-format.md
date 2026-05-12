# Timeline 格式说明

Timeline 是一个 JSON 文件，定义了 PPT 每页的动画时间轴和自动翻页计时。

## 文件位置

```
project/
├── input/
│   └── lesson.pptx
├── work/
│   └── timeline.json          # 时间轴文件
└── output/
```

## 基本结构

```json
{
  "lesson_name": "课程名称",
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
  ],
  "total_duration": 28.0
}
```

## 字段说明

### 顶级字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `lesson_name` | string | 是 | 课程名称 |
| `slides` | array | 是 | 幻灯片数组 |
| `total_duration` | number | 否 | 总时长（秒），自动计算 |

### Slide 对象

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `slide_index` | integer | 是 | 幻灯片索引（0-based） |
| `animations` | array | 是 | 动画数组 |
| `advance_time` | number | 是 | 自动翻页时间（秒） |
| `slide_count` | integer | 否 | 总幻灯片数（用于验证） |

### Animation 对象

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `animation_index` | integer | 是 | 动画索引（0-based，页面内） |
| `animation_type` | string | 是 | 动画类型（见下表） |
| `trigger_time` | number | 是 | 触发时间（秒，相对于页面开始） |
| `duration` | number | 是 | 动画时长（秒） |
| `object_name` | string | 是 | 对象名称（PPT 中的形状名称） |
| `effect_type` | string | 否 | 效果类型（如 "Appear", "Emphasis"） |
| `trigger_type` | string | 否 | 触发类型（如 "on_click", "with_previous"） |

## 动画类型

支持的动画类型：

| 类型 | 说明 | 示例 |
|------|------|------|
| `appear` | 出现 | 文本、图片突然出现 |
| `fade` | 淡入 | 文本、图片逐渐淡入 |
| `wipe` | 擦除 | 从一个方向擦除 |
| `fly` | 飞入 | 从屏幕边缘飞入 |
| `emphasis` | 强调 | 放大、变色等强调效果 |
| `exit` | 退出 | 消失、淡出等退出效果 |

## 时间单位

- **trigger_time**：秒（相对于页面开始）
- **duration**：秒（动画持续时间）
- **advance_time**：秒（页面自动翻页时间）

## 示例

### 简单示例：单页 PPT

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
    }
  ],
  "total_duration": 5.0
}
```

### 复杂示例：多页 PPT

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
          "object_name": "标题",
          "effect_type": "Appear"
        },
        {
          "animation_index": 1,
          "animation_type": "appear",
          "trigger_time": 1.0,
          "duration": 0.5,
          "object_name": "副标题",
          "effect_type": "Appear"
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
          "object_name": "内容",
          "effect_type": "Appear"
        },
        {
          "animation_index": 1,
          "animation_type": "emphasis",
          "trigger_time": 1.5,
          "duration": 0.5,
          "object_name": "重点",
          "effect_type": "GrowShrink"
        }
      ],
      "advance_time": 8.0
    },
    {
      "slide_index": 2,
      "animations": [
        {
          "animation_index": 0,
          "animation_type": "appear",
          "trigger_time": 0.0,
          "duration": 0.3,
          "object_name": "代码示例",
          "effect_type": "Appear"
        }
      ],
      "advance_time": 6.0
    }
  ],
  "total_duration": 19.0
}
```

## 最佳实践

### 1. 对象名称

确保 `object_name` 与 PPT 中的形状名称完全匹配：

- 打开 PPT
- 选择一个形状
- 在"选择窗格"中查看名称
- 或右键 → "编辑名称"

### 2. 时间间隔

- **trigger_time**：应该递增，避免重叠
- **duration**：通常 0.3-1.0 秒
- **advance_time**：应该 >= 最后一个动画的结束时间

### 3. 验证

运行报告生成工具检查时间轴：

```bash
microcourse-ppt-sync report D:/project D:/project/work/timeline.json D:/project/output/sync_report.md
```

查看 `sync_report.md` 中的警告和错误。

## 常见问题

### Q: 如何确定 advance_time？

**A:** 
- 最后一个动画的结束时间 = `trigger_time + duration`
- `advance_time` 应该 >= 最后一个动画的结束时间
- 通常设置为 `最后动画结束时间 + 1.0` 秒

示例：
```json
{
  "animations": [
    {"trigger_time": 0.0, "duration": 0.5},    // 结束于 0.5
    {"trigger_time": 1.0, "duration": 0.5}     // 结束于 1.5
  ],
  "advance_time": 3.0  // >= 1.5，建议 2.5-3.0
}
```

### Q: 对象名称不匹配会怎样？

**A:** 
- 报告中会显示 "object_name matching failures"
- 该动画不会被应用到 PPT
- 检查拼写、空格、特殊字符

### Q: 能否跳过某些动画？

**A:** 
- 可以，但 `animation_index` 必须连续
- 如果 PPT 中有 5 个动画，timeline 中应该有 0-4 的索引
- 不能跳过索引（如只有 0, 2, 4）

### Q: 时间轴与 PPT 总时长不符怎么办？

**A:** 
- 检查 `total_duration` 是否等于所有 `advance_time` 之和
- 如果不符，报告会显示警告
- 调整 `advance_time` 使其匹配

## 从 Transcript 生成 Timeline

如果您有 `transcript.json`，可以自动生成 `timeline.json`：

```bash
microcourse-ppt-sync build D:/project D:/project/work/transcript.json -s 5
```

参数说明：
- `-s 5`：指定 5 页幻灯片
- `-d 5.0`：默认每页时长 5.0 秒

## 从 SRT/VTT 生成 Timeline

v0.2 将支持从 SRT/VTT 字幕文件生成 timeline：

```bash
# 暂不支持，敬请期待 v0.2
microcourse-ppt-sync build-from-srt D:/project/transcript.srt -s 5
```

## 验证 Timeline

使用验证工具检查 timeline 是否有效：

```bash
# 生成诊断报告
microcourse-ppt-sync report D:/project D:/project/work/timeline.json D:/project/output/sync_report.md

# 查看 sync_report.md 中的问题
```

## 参考资源

- [PowerPoint 动画类型](https://support.microsoft.com/en-us/office/animation-types-in-powerpoint-6f40266b-5d19-41f0-b3ff-e85a0addc965)
- [Timeline 示例文件](../examples/basic_project/work/timeline.json)
- [集成测试指南](../tests/INTEGRATION_TEST.md)
