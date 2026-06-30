# Book Reader — HTML 页面模板

## 单章 HTML 结构模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{书名} - {章节标题}</title>
<style>
/* === 基础变量 === */
:root {
  --bg: #faf9f7;
  --text: #2d2d2d;
  --text-secondary: #666;
  --border: #e0ddd8;
  --sidebar-bg: #f5f3f0;
  --card-bg: #fff;
  --accent: #c75b39;
  --concept-colors: #e8d5c4, #d4e5d7, #d5dce8, #e8d5e0, #e0e8d5, #d5e0e8;
  --tooltip-bg: #2d2d2d;
  --tooltip-text: #fff;
  --progress: #c75b39;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #1a1a1a; --text: #e0e0e0; --text-secondary: #999; --border: #333; --sidebar-bg: #222; --card-bg: #2a2a2a; }
}

/* === 布局 === */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Noto Serif SC", "PingFang SC", "Microsoft YaHei", serif; background: var(--bg); color: var(--text); line-height: 1.8; }

/* 顶部导航 */
.header {
  position: fixed; top: 0; left: 0; right: 0; height: 52px;
  background: var(--card-bg); border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px; z-index: 100;
}
.book-title { font-size: 14px; font-weight: 600; color: var(--accent); }
.chapter-nav { display: flex; gap: 6px; align-items: center; }
.chapter-nav a {
  padding: 4px 10px; border-radius: 4px; font-size: 12px;
  text-decoration: none; color: var(--text-secondary); border: 1px solid var(--border);
  transition: all 0.2s;
}
.chapter-nav a:hover, .chapter-nav a.active { background: var(--accent); color: #fff; border-color: var(--accent); }
.progress-bar { position: fixed; top: 52px; left: 0; right: 0; height: 2px; background: var(--border); z-index: 99; }
.progress-bar .fill { height: 100%; background: var(--progress); width: 0%; transition: width 0.1s; }

/* 主体分栏 */
.main { display: grid; grid-template-columns: 1fr 380px; margin-top: 54px; min-height: calc(100vh - 54px); }

/* 左侧原文 */
.content { padding: 40px 48px; max-width: 800px; margin: 0 auto; }
.content h1 { font-size: 28px; margin-bottom: 8px; color: var(--text); }
.content h2 { font-size: 20px; margin: 32px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
.content h3 { font-size: 16px; margin: 24px 0 12px; color: var(--text-secondary); }
.content p { margin-bottom: 16px; text-align: justify; }
.content blockquote { margin: 16px 0; padding: 12px 20px; border-left: 3px solid var(--accent); background: var(--sidebar-bg); font-style: italic; }

/* 概念高亮 */
mark.concept {
  background: linear-gradient(transparent 60%, var(--highlight-color) 60%);
  cursor: pointer; border-radius: 2px; padding: 0 2px;
  transition: background 0.2s;
}
mark.concept:hover { background: var(--highlight-color); }
mark.concept.active { background: var(--accent); color: #fff; }

/* Tooltip */
.tooltip {
  position: fixed; background: var(--tooltip-bg); color: var(--tooltip-text);
  padding: 10px 14px; border-radius: 6px; font-size: 13px; line-height: 1.6;
  max-width: 300px; pointer-events: none; opacity: 0; transition: opacity 0.2s;
  z-index: 200; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.tooltip.visible { opacity: 1; }

/* 右侧概念面板 */
.sidebar {
  background: var(--sidebar-bg); border-left: 1px solid var(--border);
  padding: 20px; overflow-y: auto; height: calc(100vh - 54px); position: sticky; top: 54px;
}
.sidebar-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; color: var(--text-secondary); display: flex; align-items: center; gap: 6px; }

/* 概念卡片 */
.concept-card {
  background: var(--card-bg); border-radius: 8px; padding: 14px 16px;
  margin-bottom: 10px; border: 1px solid var(--border);
  transition: all 0.2s; cursor: pointer;
}
.concept-card:hover { border-color: var(--accent); transform: translateX(-2px); }
.concept-card.active { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(199,91,57,0.15); }
.concept-card .card-title { font-size: 14px; font-weight: 600; margin-bottom: 6px; color: var(--text); }
.concept-card .card-layman { font-size: 12px; color: var(--text-secondary); line-height: 1.7; }
.concept-card .card-details { display: none; margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); font-size: 12px; color: var(--text-secondary); }
.concept-card .card-details.visible { display: block; }
.concept-card .card-details .detail-label { font-weight: 600; color: var(--text); margin: 8px 0 4px; }
.concept-card .card-details .detail-label:first-child { margin-top: 0; }

/* 底部导航 */
.footer-nav {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 48px; border-top: 1px solid var(--border); max-width: 800px; margin: 0 auto;
}
.footer-nav a { color: var(--accent); text-decoration: none; font-size: 14px; }
.footer-nav a:hover { text-decoration: underline; }

/* 响应式 */
@media (max-width: 1024px) {
  .main { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .content { padding: 24px; }
}
</style>
</head>
<body>

<!-- 顶部导航 -->
<header class="header">
  <div class="book-title">📖 {书名}</div>
  <nav class="chapter-nav">{章节导航按钮}</nav>
</header>
<div class="progress-bar"><div class="fill" id="progressFill"></div></div>

<!-- 主体 -->
<div class="main">
  <!-- 左侧原文 -->
  <article class="content" id="content">
    <h1>{章节标题}</h1>
    {原文内容（概念已标注）}
  </article>

  <!-- 右侧概念面板 -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-title">💡 本章概念</div>
    <div id="conceptList">{概念卡片列表}</div>
  </aside>
</div>

<!-- 底部导航 -->
<nav class="footer-nav">
  <a href="{上一章}.html">← {上一章标题}</a>
  <span style="color:var(--text-secondary);font-size:12px;">{当前章节}</span>
  <a href="{下一章}.html">{下一章标题} →</a>
</nav>

<!-- Tooltip -->
<div class="tooltip" id="tooltip"></div>

<script>
// === 概念数据 ===
const concepts = {概念JSON数据};

// === 交互逻辑 ===
(function() {
  const tooltip = document.getElementById('tooltip');
  const conceptMarks = document.querySelectorAll('mark.concept');
  const conceptCards = document.querySelectorAll('.concept-card');
  const progressFill = document.getElementById('progressFill');

  // Tooltip 悬浮提示
  conceptMarks.forEach(mark => {
    const name = mark.dataset.concept;
    const c = concepts[name];
    if (!c) return;

    mark.addEventListener('mouseenter', (e) => {
      tooltip.textContent = c.layman || c.definition || c.explanation;
      tooltip.classList.add('visible');
      positionTooltip(e);
    });
    mark.addEventListener('mousemove', positionTooltip);
    mark.addEventListener('mouseleave', () => tooltip.classList.remove('visible'));

    // 点击高亮关联
    mark.addEventListener('click', () => {
      conceptMarks.forEach(m => m.classList.remove('active'));
      conceptCards.forEach(card => card.classList.remove('active'));
      mark.classList.add('active');
      const card = document.querySelector(`.concept-card[data-concept="${name}"]`);
      if (card) {
        card.classList.add('active');
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        card.querySelector('.card-details').classList.add('visible');
      }
    });
  });

  function positionTooltip(e) {
    const x = e.clientX + 12, y = e.clientY - 12;
    tooltip.style.left = Math.min(x, window.innerWidth - 320) + 'px';
    tooltip.style.top = Math.max(y, 10) + 'px';
  }

  // 概念卡片点击展开
  conceptCards.forEach(card => {
    card.addEventListener('click', () => {
      const details = card.querySelector('.card-details');
      details.classList.toggle('visible');
    });
  });

  // 进度条
  const content = document.getElementById('content');
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = content.scrollHeight - window.innerHeight;
    progressFill.style.width = Math.min(100, (scrollTop / docHeight) * 100) + '%';
  });

  // 滚动联动：左侧段落进入视口时高亮右侧对应概念
  const paragraphs = content.querySelectorAll('p');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const marks = entry.target.querySelectorAll('mark.concept');
        conceptCards.forEach(c => c.classList.remove('active'));
        marks.forEach(m => {
          const card = document.querySelector(`.concept-card[data-concept="${m.dataset.concept}"]`);
          if (card) card.classList.add('active');
        });
      }
    });
  }, { rootMargin: '-30% 0px -50% 0px' });
  paragraphs.forEach(p => observer.observe(p));
})();
</script>

</body>
</html>
```

## 概念 JSON 数据格式

```json
{
  "意识": {
    "title": "意识",
    "term": "意识 / consciousness",
    "definition": "被个体的内在生活所伴随的行为的因果关系",
    "explanation": "主观经验、感受质、'成为某种感觉像什么'的现象",
    "layman": "想象你正在吃一颗草莓...",
    "related": ["困难问题", "经验", "感受质"]
  }
}
```

## 概念标注规则

1. 在原文中查找概念名称，替换为：
   ```html
   <mark class="concept" data-concept="意识" style="--highlight-color:#e8d5c4">意识</mark>
   ```
2. 每个概念分配不同的 `--highlight-color`
3. 同一概念在同一段内只标注首次出现
4. 较长的复合术语优先匹配
