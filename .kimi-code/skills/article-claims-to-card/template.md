# article-claims-to-card 输出模板

## 输入

- 源文件：`{source_path}`
- 来源语言：`{source_language}`

---

## 格式化观点清单

```
1.{核心论点1}:{简要概括};2.{核心论点2}:{简要概括};3.{分论点1}:{简要概括};4.{分论点2}:{简要概括};.....
```

---

## 卡片生成结果（仅核心论点）

- xl-card 默认输出目录：`/Users/chouchou/Documents/Obsidian Vault/九局下半怎么破局/概念卡片`
- **最终卡片文件复制到**：`{source_dir}/`
- 仅对核心论点生成卡片，分论点不生成卡片
- 生成文件：
  - `{source_dir}/{card_1_name}.json`
  - `{source_dir}/{card_2_name}.json`
  - ...

---

## 原始观点提取报告

- 文件路径：`{source_path}-claims.md`
- 包含：核心论点、分论点、价值判断、因果判断、事实断言、隐含前提
