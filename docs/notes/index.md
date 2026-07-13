---
tags:
  - 学习笔记
---

# 学习地图

<section class="manor-page-hero manor-page-hero--notes">
  <div>
    <p class="farm-kicker">Notes Map</p>
    <h2>把学习材料分成可维护的地块</h2>
    <p>未整理、含隐私或未确认可公开的材料先放在本地 `inbox/`。进入 Git 的内容必须是已经脱敏、可公开、可复查的笔记。</p>
  </div>
</section>

<div class="manor-link-grid">
  <a class="manor-link-card" href="ai/">
    <img src="../assets/images/manor/icon-book.webp" alt="" />
    <strong>AI 菜圃</strong>
    <span>模型、训练、评估、部署。</span>
  </a>
  <a class="manor-link-card" href="programming/">
    <img src="../assets/images/manor/icon-laptop.webp" alt="" />
    <strong>编程小屋</strong>
    <span>脚本、依赖、自动化、工程问题。</span>
  </a>
  <a class="manor-link-card" href="papers/">
    <img src="../assets/images/manor/icon-house.webp" alt="" />
    <strong>论文蘑菇屋</strong>
    <span>论文卡片、方法比较、复现判断。</span>
  </a>
  <a class="manor-link-card" href="research/">
    <img src="../assets/images/manor/icon-trophy.webp" alt="" />
    <strong>科研任务榜</strong>
    <span>假设、实验、结果复盘、下一步决策。</span>
  </a>
</div>

## 笔记写作原则

每篇笔记优先回答一个明确问题：当前结论支持什么判断，还缺少什么证据。实验记录应包含假设、数据、方法、指标、结果和下一步决策。

```mermaid
flowchart LR
  Inbox[本地 inbox] --> Draft[创作台生成模板]
  Draft --> Review[脱敏和整理]
  Review --> Notes[公开笔记]
  Notes --> Build[mkdocs build --strict]
```
