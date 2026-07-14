---
hide:
  - toc
---

# 创作台

<section class="manor-page-hero manor-page-hero--create">
  <div>
    <p class="farm-kicker">Writing Desk</p>
    <h2>从新建到写完：先生成模板，再进入 Git</h2>
    <p>公开 GitHub Pages 不能直接写仓库。需要自动发布时，先在服务器启动本地发布服务，再从这里生成 Markdown 并推送到 Git。</p>
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
      Slug（英文路径）
      <input id="creator-slug" type="text" placeholder="例如：day1-simplify" />
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
    <label class="creator-confirm">
      <input id="creator-confirm" type="checkbox" />
      我确认内容不包含 SSH 私钥、Token、密码、患者信息、未公开论文、内网地址或其他敏感材料。
    </label>
    <div class="creator-actions">
      <button type="button" id="creator-publish">发布到 Git</button>
    </div>
    <p class="creator-status" id="creator-status">自动发布前先运行：`.venv/bin/python scripts/local_publish_server.py`</p>
  </div>
</section>

## 发布流程

1. 在创作台生成 Markdown。
2. 如需自动发布，先在服务器运行 `.venv/bin/python scripts/local_publish_server.py`。
3. 勾选敏感信息确认，点击“发布到 Git”。
4. 本地服务会写入文件、运行 `.venv/bin/mkdocs build --strict`、提交并推送到 `main`。
5. GitHub Actions 收到 push 后自动部署 GitHub Pages。
