# book-reading-share 使用示例

## 输入

```bash
/book-reading-share /Users/chouchou/books/原子习惯.pdf
```

## 执行过程

### 步骤 1：深度读书

调用：

```bash
/book-master /Users/chouchou/books/原子习惯.pdf
```

生成项目目录：

```
原子习惯/
├── chapters/
├── reports/
│   ├── chapter-01-report.md
│   ├── chapter-02-report.md
│   └── ...
└── _master-index.md
```

### 步骤 2：论据收集

对每个章节报告运行：

```bash
/evidence-collector 原子习惯/reports/chapter-01-report.md
/evidence-collector 原子习惯/reports/chapter-02-report.md
...
```

提取到的部分论据示例：

- **概念**：习惯堆叠（Habit Stacking）—— 把新习惯绑定到已有习惯之后。
- **数据**：每天进步 1%，一年后成果提升 37.78 倍。
- **案例**：英国自行车队通过 1% 边际收益策略获得奥运冠军。
- **金句**："You do not rise to the level of your goals. You fall to the level of your systems."

### 步骤 3：生成口播文案

调用：

```bash
/broadcast-maker 原子习惯/_master-index.md
```

最终输出文件：`原子习惯/原子习惯-reading-share-script.md`

## 输出示例（节选）

---

**《原子习惯》：普通人变厉害的底层操作系统**

你有没有发现，很多人年初立的 flag 到年底一个都没实现？

问题可能不在于目标太大，而在于他们只盯着目标，却忽略了系统。

《原子习惯》这本书，讲的就是怎么不靠意志力，靠一套 tiny changes 的系统，让好习惯自然发生、坏习惯自然消失。

书里最让我震惊的一个数字是：每天进步 1%，一年后不是进步 365%，而是 37.78 倍。反过来，每天退步 1%，一年后几乎归零。

这就是作者 James Clear 说的——复利，不只发生在金钱上，也发生在习惯上。

...

所以，别再用"我要减肥""我要学习"这种空泛目标折磨自己了。从"我每天早上喝完咖啡后，做 5 个俯卧撑"开始。一个微小到不可能失败的动作，才是改变的起点。

---
