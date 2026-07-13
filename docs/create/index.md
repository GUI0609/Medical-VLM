---
hide:
  - toc
---

# 创作台

<section class="manor-page-hero manor-page-hero--create">
  <div>
    <p class="farm-kicker">Writing Desk</p>
    <h2>从新建到写完：先生成模板，再进入 Git</h2>
    <p>这是静态 GitHub Pages 站点，网页不能直接写入仓库。这里负责生成规范 Markdown，你复制后放入对应目录，构建通过再提交。</p>
  </div>
</section>

<section class="creator-desk" data-creator-desk>
  <div class="creator-panel creator-form">
    <h2>新建内容</h2>
    <label>
      类型
      <select id="creator-type">
        <option value="blog">博客日志</option>
        <option value="paper">论文卡片</option>
        <option value="note">学习笔记</option>
        <option value="experiment">实验复盘</option>
        <option value="plan">计划任务</option>
      </select>
    </label>
    <label>
      标题
      <input id="creator-title" type="text" placeholder="例如：Med-VLM 论文阅读第一周" />
    </label>
    <label>
      Slug
      <input id="creator-slug" type="text" placeholder="med-vlm-week-1" />
    </label>
    <label>
      标签
      <input id="creator-tags" type="text" placeholder="Medical-VLM, 论文, 实验" />
    </label>
    <label>
      摘要
      <textarea id="creator-summary" rows="4" placeholder="一句话说明这篇内容回答什么问题。"></textarea>
    </label>
    <div class="creator-actions">
      <button type="button" id="creator-generate">生成 Markdown</button>
      <button type="button" id="creator-copy">复制</button>
      <button type="button" id="creator-download">下载</button>
    </div>
  </div>
  <div class="creator-panel creator-result">
    <h2>生成结果</h2>
    <p class="creator-path" id="creator-path">路径会显示在这里</p>
    <textarea id="creator-output" rows="24" spellcheck="false"></textarea>
  </div>
</section>

## 发布流程

1. 在创作台生成 Markdown。
2. 放入页面提示的路径，例如 `docs/blog/posts/2026-07-14-title.md`。
3. 运行 `.venv/bin/mkdocs build --strict`。
4. 检查无隐私、无患者信息、无 Token、无未公开论文内容。
5. `git add`、`git commit`、`git push`，等待 GitHub Pages 部署。
