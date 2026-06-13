# Book Master 使用示例

## 示例：精读《一人公司》

### 输入

```
/book-master /Users/chouchou/Desktop/myProject/learnAbook/books/一人公司：失业潮中的高新技术工作者（万相）.pdf
```

### 执行过程

#### Step 1: 创建项目目录

```bash
mkdir -p "一人公司_失业潮中的高新技术工作者/chapters"
mkdir -p "一人公司_失业潮中的高新技术工作者/reports"
```

#### Step 2: 拆分书籍

```bash
/book-splitter ".../一人公司.pdf" --output "一人公司_失业潮中的高新技术工作者/chapters"
```

**输出**:
```
chapters/
├── _index.md
├── front-01-封面.md
├── front-02-书名.md
├── front-03-版权.md
├── front-04-前言.md
├── front-05-目录.md
├── chapter-01-推荐序_当今高科技工作者的就业、失业与生活构建.md
├── chapter-02-序.md
├── back-01-致谢.md
├── chapter-03-导言_坚韧、信念与自由市场.md
├── chapter-04-第一章_硅草原.md
├── chapter-05-第二章_一人公司.md
├── chapter-06-第三章_最难的工作.md
├── chapter-07-第四章_失业期间的仪式.md
├── chapter-08-第五章_靠妻子养家的男人.md
├── back-02-后记.md
└── back-03-参考文献.md
```

#### Step 3: 过滤章节

**自动排除**:
- `_index.md` → 排除
- `front-01-封面.md` → 排除（关键词：封面）
- `front-02-书名.md` → 排除（关键词：书名）
- `front-03-版权.md` → 排除（关键词：版权）
- `front-05-目录.md` → 排除（关键词：目录）
- `back-03-参考文献.md` → 排除（关键词：参考文献）

**保留**:
- `front-04-前言.md` → 保留
- `chapter-01-推荐序...md` → 保留
- `chapter-02-序.md` → 保留
- `back-01-致谢.md` → 保留
- `chapter-03-导言...md` → 保留
- `chapter-04-第一章_硅草原.md` → 保留
- `chapter-05-第二章_一人公司.md` → 保留
- `chapter-06-第三章_最难的工作.md` → 保留
- `chapter-07-第四章_失业期间的仪式.md` → 保留
- `chapter-08-第五章_靠妻子养家的男人.md` → 保留
- `back-02-后记.md` → 保留

**共 11 个章节需要精读**。

#### Step 4: 并行启动子代理

由于 11 个章节超过建议的 8 个并行上限，分两批处理：

**第一批（8 个并行）**:
```
Agent 1 → deep-reader → front-04-前言.md
Agent 2 → deep-reader → chapter-01-推荐序...md
Agent 3 → deep-reader → chapter-02-序.md
Agent 4 → deep-reader → back-01-致谢.md
Agent 5 → deep-reader → chapter-03-导言...md
Agent 6 → deep-reader → chapter-04-第一章_硅草原.md
Agent 7 → deep-reader → chapter-05-第二章_一人公司.md
Agent 8 → deep-reader → chapter-06-第三章_最难的工作.md
```

**第二批（3 个并行）**:
```
Agent 9  → deep-reader → chapter-07-第四章_失业期间的仪式.md
Agent 10 → deep-reader → chapter-08-第五章_靠妻子养家的男人.md
Agent 11 → deep-reader → back-02-后记.md
```

每个子代理的提示词示例：
```
请对以下文件进行深度精读，使用 /deep-reader 的10维度分析框架：

文件：一人公司_失业潮中的高新技术工作者/chapters/chapter-03-导言_坚韧、信念与自由市场.md
输出：一人公司_失业潮中的高新技术工作者/reports/chapter-03-导言-report.md

要求：
1. 严格覆盖10个分析维度
2. 包含完整的自检清单
3. 将报告写入指定输出路径
```

#### Step 5: 等待完成 + 生成总索引

所有子代理完成后，生成 `_master-index.md`:

```markdown
# 一人公司：失业潮中的高新技术工作者 — 精读报告总索引

## 书籍信息
- 来源: 一人公司：失业潮中的高新技术工作者（万相）.pdf
- 总页数: 234
- 拆分章节数: 15
- 精读章节数: 11
- 排除章节: 封面、书名、版权、目录、参考文献、索引

## 章节精读报告

| 序号 | 章节 | 页码 | 报告 |
|------|------|------|------|
| 1 | 前言 | 1-? | [报告](reports/front-04-前言-report.md) |
| 2 | 推荐序 | 2-8 | [报告](reports/chapter-01-推荐序-report.md) |
| 3 | 序 | 9-13 | [报告](reports/chapter-02-序-report.md) |
| 4 | 致谢 | 14-17 | [报告](reports/back-01-致谢-report.md) |
| 5 | 导言 | 18-35 | [报告](reports/chapter-03-导言-report.md) |
| 6 | 第一章 硅草原 | 36-53 | [报告](reports/chapter-04-第一章-report.md) |
| 7 | 第二章 一人公司 | 54-89 | [报告](reports/chapter-05-第二章-report.md) |
| 8 | 第三章 最难的工作 | 90-105 | [报告](reports/chapter-06-第三章-report.md) |
| 9 | 第四章 失业期间的仪式 | 106-134 | [报告](reports/chapter-07-第四章-report.md) |
| 10 | 第五章 靠妻子养家的男人 | 135-166 | [报告](reports/chapter-08-第五章-report.md) |
| 11 | 后记 | 167-200 | [报告](reports/back-02-后记-report.md) |

## 全书核心论点速览

### 中心论点
失业的美国高科技工作者通过内化的"一人公司"叙事来应对结构性失业，这种叙事既是新自由主义意识形态的产物，也是一种身份防御机制。

### 分论点汇总
1. 新自由主义不仅是公共政策，更是深植于日常生活的世界观（导言）
2. 达拉斯科技产业的兴衰揭示了产业地理的脆弱性（第一章）
3. "一人公司"将结构性失业个体化，将不稳定重构为赋权选择（第二章）
4. 求职过程中的情感劳动和交际活动维持了新自由主义的自我叙事（第三、四章）
5. 双职工家庭中配偶收入的依赖揭示了"自由主体"的物质基础（第五章）

## 跨章节知识网络

### 核心概念图谱
- **一人公司**: 贯穿全书的核心概念，在第二章得到最深入分析
- **新自由主义**: 导言建立框架，各章从不同维度展开
- **身份工作**: 导言（亚历克斯案例）、第二章、第四章
- **组织人**: 导言、第二章作为历史对照
- **社会契约**: 导言、第二章描述其历史性终结

### 章节间逻辑关系
```
导言（理论框架 + 方法论）
    ↓
第一章（产业历史背景）
    ↓
第二章（核心理论：一人公司叙事）
    ↓
第三章（求职经历：实践层面）
    ↓
第四章（交际活动：社群层面）
    ↓
第五章（物质现实：家庭层面）
    ↓
后记（追踪验证：时间维度）
```

## 自检清单

- [x] 所有内容章节都已精读
- [x] 每章报告都包含10维度分析
- [x] 跨章节的论点一致性已检查
- [x] 总索引已生成
```

### 最终输出结构

```
一人公司_失业潮中的高新技术工作者/
├── chapters/
│   ├── _index.md
│   ├── front-01-封面.md
│   ├── front-02-书名.md
│   ├── front-03-版权.md
│   ├── front-04-前言.md
│   ├── front-05-目录.md
│   ├── chapter-01-推荐序...md
│   ├── chapter-02-序.md
│   ├── back-01-致谢.md
│   ├── chapter-03-导言...md
│   ├── chapter-04-第一章_硅草原.md
│   ├── chapter-05-第二章_一人公司.md
│   ├── chapter-06-第三章_最难的工作.md
│   ├── chapter-07-第四章_失业期间的仪式.md
│   ├── chapter-08-第五章_靠妻子养家的男人.md
│   ├── back-02-后记.md
│   └── back-03-参考文献.md
├── reports/
│   ├── front-04-前言-report.md
│   ├── chapter-01-推荐序-report.md
│   ├── chapter-02-序-report.md
│   ├── back-01-致谢-report.md
│   ├── chapter-03-导言-report.md
│   ├── chapter-04-第一章-report.md
│   ├── chapter-05-第二章-report.md
│   ├── chapter-06-第三章-report.md
│   ├── chapter-07-第四章-report.md
│   ├── chapter-08-第五章-report.md
│   └── back-02-后记-report.md
└── _master-index.md
```

## 时间预估

| 阶段 | 耗时 | 说明 |
|------|------|------|
| 拆分书籍 | 1-5 分钟 | 取决于PDF大小和页数 |
| 过滤章节 | <1 分钟 | 自动完成 |
| 并行精读（第一批） | 10-30 分钟 | 8 个子代理同时运行 |
| 并行精读（第二批） | 10-30 分钟 | 剩余章节 |
| 生成总索引 | 2-5 分钟 | 主会话汇总 |
| **总计** | **25-70 分钟** | 取决于章节数量和长度 |

## 常见问题

### Q: 子代理数量超过8个怎么办？

A: 分批处理。第一批启动8个，等待完成后启动第二批。这样可以避免系统资源过载。

### Q: 某个子代理失败了怎么办？

A: 检查失败原因（通常是文件读取问题或超时），然后单独重新派发该子代理。在 `_master-index.md` 中标注该章节为"待重新处理"。

### Q: 可以自定义排除规则吗？

A: 可以。编辑 `scripts/filter.sh` 中的 `EXCLUDE_PATTERNS` 数组，添加或移除关键词。修改后重新运行 `/book-master` 即可生效。

### Q: 项目文件夹可以自定义名称吗？

A: 当前版本自动从PDF文件名提取。如需自定义，可以先用 `/book-splitter` 手动拆分，再用 `/deep-reader` 手动处理。
