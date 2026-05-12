# Timeline JSON 格式说明

本文档定义 v0.1.0 支持的 `timeline.json` 格式。OpenClaw、脚本或人工编写 Timeline 时，应以本文档为兼容性依据。

## 1. 用途

`timeline.json` 描述一份 PPT 微课中每页幻灯片的动画触发时间、动画持续时间和自动翻页时间。服务会读取该文件，并将数据写入 PowerPoint：

- `animations[].trigger_time` → PowerPoint 动画触发延迟。
- `animations[].duration` → PowerPoint 动画持续时间。
- `slides[].advance_time` → 当前幻灯片自动翻页时间。

所有时间单位均为**秒**，并且每页动画时间均相对于**该页开始播放的时间**，不是相对于整份课件的绝对时间。

## 2. 最小可用示例

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
        },
        {
          "animation_index": 1,
          "animation_type": "appear",
          "trigger_time": 1.2,
          "duration": 0.5,
          "object_name": "副标题"
        }
      ],
      "advance_time": 5.0,
      "notes": "第 1 页旁白摘要"
    }
  ],
  "total_duration": 5.0,
  "metadata": {
    "schema_version": "0.1.0"
  }
}
```

更多示例见 [`examples/basic_project/work/timeline.example.json`](../examples/basic_project/work/timeline.example.json)。

## 3. 顶层字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `lesson_name` | string | 建议 | 课程或课件名称。缺省时按空字符串处理。 |
| `slides` | array&lt;Slide&gt; | 是 | 幻灯片时间轴数组。每个元素描述一页 PPT。 |
| `total_duration` | number | 建议 | 整份课件预计总时长，单位秒。通常等于所有 `advance_time` 之和。 |
| `metadata` | object | 否 | 扩展信息。v0.1.0 不依赖其中任何字段。 |

## 4. Slide 字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `slide_index` | integer | 是 | 幻灯片索引，**从 0 开始**。`0` 表示 PowerPoint 中第 1 页。 |
| `animations` | array&lt;Animation&gt; | 是 | 当前页动画时间轴。可以为空数组。 |
| `advance_time` | number / null | 建议 | 当前页自动翻页时间，单位秒。为空时由服务或 PowerPoint 默认行为决定。 |
| `notes` | string | 否 | 给人或上游模型阅读的备注，不参与 PPT 计时写入。 |
| `metadata` | object | 否 | 当前页扩展信息。v0.1.0 不依赖其中任何字段。 |

### `slide_index` 约定

- 使用 0-based 索引：第 1 页是 `0`，第 2 页是 `1`。
- 建议按升序排列，且不要重复。
- Timeline 中的页数应与 PPT 实际页数一致，或至少不要引用不存在的页。

### `advance_time` 约定

- `advance_time` 应大于等于当前页最后一个动画的结束时间。
- 当前页最后一个动画结束时间 = `max(trigger_time + duration)`。
- 建议保留 0.2～1.0 秒缓冲，避免动画结束后立即翻页造成视觉截断。

示例：

```json
{
  "slide_index": 1,
  "animations": [
    {"animation_index": 0, "animation_type": "appear", "trigger_time": 0.0, "duration": 0.5},
    {"animation_index": 1, "animation_type": "emphasis", "trigger_time": 3.0, "duration": 0.8}
  ],
  "advance_time": 4.5
}
```

该页最后动画在 `3.8` 秒结束，`advance_time` 为 `4.5` 秒，留有 `0.7` 秒缓冲。

## 5. Animation 字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `animation_index` | integer | 是 | 当前页动画索引，**从 0 开始**，对应 PowerPoint 动画窗格中的顺序。 |
| `animation_type` | string | 是 | 逻辑动画类型。v0.1.0 支持的枚举见下表。 |
| `trigger_time` | number | 是 | 动画相对当前页开始播放的触发时间，单位秒。 |
| `duration` | number | 否 | 动画持续时间，单位秒；缺省值为 `0.5`。 |
| `object_name` | string / null | 否 | 动画对象名称，主要用于可读性和报告，不作为 v0.1.0 匹配动画的唯一依据。 |
| `metadata` | object | 否 | 动画扩展信息。v0.1.0 不依赖其中任何字段。 |

### `animation_type` 枚举

| 值 | 含义 |
| --- | --- |
| `appear` | 进入 / 出现类动画。 |
| `disappear` | 隐藏 / 消失类动画。 |
| `emphasis` | 强调类动画。 |
| `exit` | 退出类动画。 |
| `motion_path` | 路径动画。 |

> 注意：`animation_type` 是项目内部的逻辑分类，不等同于 PowerPoint COM 的所有 EffectType 枚举。v0.1.0 主要使用 `animation_index` 找到已有 PPT 动画并写入计时，不负责创建复杂动画效果。

### `animation_index` 约定

- 使用 0-based 索引。
- `animation_index: 0` 对应当前页动画窗格中的第 1 个动画。
- Timeline 只写入已有动画的计时；如果 PPT 当前页动画数量不足，会导致应用失败或报告异常。
- 若 PPT 中调整了动画顺序，应同步更新 Timeline。

### `trigger_time` 与 `duration` 约定

- `trigger_time` 必须是非负数字。
- `duration` 建议为正数；缺省为 `0.5` 秒。
- 同一页动画允许重叠。例如两个动画都在 `1.0` 秒触发，可形成同步出现效果。
- 同一页动画也允许留白。例如第一个动画 `0.0` 秒触发，第二个动画 `4.0` 秒触发。

## 6. 推荐生成规则

面向 OpenClaw 或其他上游工具生成 Timeline 时，建议遵守以下规则：

1. 先确定 PPT 页数和每页动画数量。
2. 为每页生成一个 `Slide` 对象，`slide_index` 从 `0` 连续递增。
3. 为每页已有动画生成一个 `Animation` 对象，`animation_index` 从 `0` 连续递增。
4. 将每页旁白切成该页内的相对时间，写入 `trigger_time`。
5. 确保 `advance_time >= max(trigger_time + duration) + buffer`。
6. 将 `total_duration` 设置为所有 `advance_time` 之和。
7. 将额外信息放入 `metadata`，不要新增必填字段。

## 7. 常见错误

### 7.1 使用了 1-based 索引

错误：

```json
{"slide_index": 1, "animations": [{"animation_index": 1, "animation_type": "appear", "trigger_time": 0}]}
```

如果这是 PPT 第 1 页、第 1 个动画，应写成：

```json
{"slide_index": 0, "animations": [{"animation_index": 0, "animation_type": "appear", "trigger_time": 0}]}
```

### 7.2 `advance_time` 小于最后动画结束时间

错误：

```json
{
  "slide_index": 0,
  "animations": [
    {"animation_index": 0, "animation_type": "appear", "trigger_time": 4.8, "duration": 1.0}
  ],
  "advance_time": 5.0
}
```

该动画会在 `5.8` 秒结束，但页面在 `5.0` 秒翻页。应将 `advance_time` 调整到 `5.8` 秒以上，例如 `6.2`。

### 7.3 引用不存在的动画

如果 PPT 第 2 页只有 1 个动画，则不要写 `animation_index: 1` 或更大的动画索引。请先在 PPT 中补齐动画，或删除 Timeline 中多余动画。

## 8. JSON Schema（简化版）

```json
{
  "type": "object",
  "required": ["slides"],
  "properties": {
    "lesson_name": {"type": "string"},
    "slides": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["slide_index", "animations"],
        "properties": {
          "slide_index": {"type": "integer", "minimum": 0},
          "animations": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["animation_index", "animation_type", "trigger_time"],
              "properties": {
                "animation_index": {"type": "integer", "minimum": 0},
                "animation_type": {
                  "type": "string",
                  "enum": ["appear", "disappear", "emphasis", "exit", "motion_path"]
                },
                "trigger_time": {"type": "number", "minimum": 0},
                "duration": {"type": "number", "exclusiveMinimum": 0},
                "object_name": {"type": ["string", "null"]},
                "metadata": {"type": "object"}
              }
            }
          },
          "advance_time": {"type": ["number", "null"], "minimum": 0},
          "notes": {"type": "string"},
          "metadata": {"type": "object"}
        }
      }
    },
    "total_duration": {"type": "number", "minimum": 0},
    "metadata": {"type": "object"}
  }
}
```

## 9. 与代码模型的对应关系

| JSON 字段 | 代码模型 |
| --- | --- |
| `lesson_name` | `Timeline.lesson_name` |
| `slides` | `Timeline.slides` |
| `total_duration` | `Timeline.total_duration` |
| `metadata` | `Timeline.metadata` / `Slide.metadata` / `Animation.metadata` |
| `slide_index` | `Slide.slide_index` |
| `animations` | `Slide.animations` |
| `advance_time` | `Slide.advance_time` |
| `notes` | `Slide.notes` |
| `animation_index` | `Animation.animation_index` |
| `animation_type` | `Animation.animation_type` |
| `trigger_time` | `Animation.trigger_time` |
| `duration` | `Animation.duration` |
| `object_name` | `Animation.object_name` |
