# 使用示例

## 示例 1：批量生成整本书的文案

### 用户输入

```
/batch-content-to-script 弥散的心智
```

### 系统发现

```
发现 12 份精读报告：
  reports/chapter-01-心智与意识-report.md
  reports/chapter-02-感知的真相-report.md
  reports/chapter-03-弥散的主体-report.md
  ...
  reports/chapter-12-回归日常-report.md
```

### 用户选择

```
请选择时长策略：
[1] 统一时长 - 所有章节使用相同时长
[2] 分别指定 - 每个章节单独选择
[3] 智能推荐 - 根据内容量自动选择

用户：1

请选择统一时长：
[1] 短视频 (1-2分钟 / 300-500字)
[2] 中视频 (5-15分钟 / 1200-3500字)
[3] 长视频 (15-40分钟 / 3500-10000字)

用户：2
```

### 并行执行

```
启动子代理 1/8: chapter-01 → chapter-01-script.md
启动子代理 2/8: chapter-02 → chapter-02-script.md
...
启动子代理 8/8: chapter-08 → chapter-08-script.md

第一批完成，启动第二批...
启动子代理 9/4: chapter-09 → chapter-09-script.md
...
```

### 生成结果

```
✅ 全部 12 份文案生成完成！

总字数: 28,500 字
平均时长: 约 8 分钟/集
总预估时长: 约 96 分钟

输出位置:
  scripts/chapter-01-心智与意识-script.md (2,400字)
  scripts/chapter-02-感知的真相-script.md (3,100字)
  ...
  scripts/chapter-12-回归日常-script.md (2,800字)

总索引: _script-index.md
```

---

## 示例 2：只处理部分报告

### 用户输入

```
/batch-content-to-script 弥散的心智

（系统发现报告后）
用户：只处理 chapter-03 到 chapter-05
```

### 结果

```
只处理 3 份报告：
  chapter-03 → chapter-03-script.md
  chapter-04 → chapter-04-script.md
  chapter-05 → chapter-05-script.md

✅ 3 份文案生成完成！
```

---

## 示例 3：追加生成

### 场景

之前已经生成过 8 个章节的文案，现在新增了 4 个章节的精读报告。

### 执行

```
/batch-content-to-script 弥散的心智

系统检测到 scripts/ 目录已存在：
- 已有文案: 8 份
- 新报告: 4 份
- 是否只处理新增报告？[Y/n]

用户：Y
```

### 结果

```
只处理新增的 4 份报告：
  chapter-09 → chapter-09-script.md
  chapter-10 → chapter-10-script.md
  chapter-11 → chapter-11-script.md
  chapter-12 → chapter-12-script.md

✅ 追加完成！更新 _script-index.md
当前总计: 12 份文案
```
