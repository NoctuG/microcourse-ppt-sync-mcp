# 基础示例项目

这是 v0.1.0 的最小示例项目，用来说明 `timeline.json` 应该如何组织，以及如何把 Timeline 应用到一个已有 PPT。

## 目录结构

```text
examples/basic_project/
├── input/
│   └── lesson.pptx              # 用户自行创建或复制；仓库不提交真实 PPT 大文件
├── work/
│   ├── timeline.example.json    # Timeline 示例文件
│   └── timeline.json            # 实际运行时读取的 Timeline，可由示例复制得到
└── output/
```

> `input/.gitkeep` 和 `output/.gitkeep` 只用于让 Git 保留空目录。运行前请将真实 PPT 保存为 `input/lesson.pptx`。

## 准备 PPT

创建或复制 `input/lesson.pptx`，建议按以下最小结构制作：

| PPT 页 | 建议动画 |
| --- | --- |
| 第 1 页 | 标题、副标题，共 2 个动画 |
| 第 2 页 | 内容标题、内容文本、重点，共 3 个动画 |
| 第 3 页 | 代码标题、代码块，共 2 个动画 |
| 第 4 页 | 示例标题、示例内容，共 2 个动画 |
| 第 5 页 | 总结，共 1 个动画 |

Timeline 中的 `slide_index` 和 `animation_index` 均从 `0` 开始。例如第 1 页第 1 个动画是 `slide_index: 0`、`animation_index: 0`。

## 准备 Timeline

示例文件在 `work/timeline.example.json`。如果要直接运行完整工作流，请复制为 `work/timeline.json`：

```bash
cp examples/basic_project/work/timeline.example.json examples/basic_project/work/timeline.json
```

示例 Timeline 总时长为 28 秒：

| 页 | 动画数量 | `advance_time` |
| --- | ---: | ---: |
| 第 1 页 | 2 | 5.0 秒 |
| 第 2 页 | 3 | 8.0 秒 |
| 第 3 页 | 2 | 6.0 秒 |
| 第 4 页 | 2 | 5.0 秒 |
| 第 5 页 | 1 | 4.0 秒 |

字段说明请阅读 [Timeline JSON 格式说明](../../docs/timeline_format.md)。

## 运行完整工作流

在 Windows + PowerPoint 桌面版环境中，从仓库根目录执行：

```bash
microcourse-ppt-sync run examples/basic_project --quality HD --fps 30
```

成功后应生成：

```text
examples/basic_project/work/lesson_timed.pptx
examples/basic_project/output/ppt_bg.mp4
examples/basic_project/output/sync_report.md
```

## 分步运行

```bash
microcourse-ppt-sync inspect examples/basic_project
microcourse-ppt-sync inspect_ppt examples/basic_project/input/lesson.pptx
microcourse-ppt-sync apply examples/basic_project examples/basic_project/input/lesson.pptx examples/basic_project/work/timeline.json
microcourse-ppt-sync export examples/basic_project/work/lesson_timed.pptx examples/basic_project/output/ppt_bg.mp4 --quality HD --fps 30
microcourse-ppt-sync report examples/basic_project examples/basic_project/work/timeline.json examples/basic_project/output/sync_report.md
```

## 验证要点

- 打开 `work/lesson_timed.pptx`，进入放映模式后应无需点击即可按 Timeline 自动播放动画并翻页。
- 打开 `output/ppt_bg.mp4`，应能看到保留 PPT 动画效果的无声背景视频。
- 打开 `output/sync_report.md`，应能看到每页时长、动画数量和异常提示。
