document$.subscribe(() => {
  for (const card of document.querySelectorAll(".farm-card")) {
    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width - 0.5;
      const y = (event.clientY - rect.top) / rect.height - 0.5;
      card.style.setProperty("--farm-rotate-x", `${(-y * 4).toFixed(2)}deg`);
      card.style.setProperty("--farm-rotate-y", `${(x * 4).toFixed(2)}deg`);
    });

    card.addEventListener("pointerleave", () => {
      card.style.setProperty("--farm-rotate-x", "0deg");
      card.style.setProperty("--farm-rotate-y", "0deg");
    });
  }

  const desk = document.querySelector("[data-creator-desk]");
  if (!desk) return;

  const typeInput = document.querySelector("#creator-type");
  const titleInput = document.querySelector("#creator-title");
  const slugInput = document.querySelector("#creator-slug");
  const tagsInput = document.querySelector("#creator-tags");
  const summaryInput = document.querySelector("#creator-summary");
  const output = document.querySelector("#creator-output");
  const pathOutput = document.querySelector("#creator-path");
  const generateButton = document.querySelector("#creator-generate");
  const copyButton = document.querySelector("#creator-copy");
  const downloadButton = document.querySelector("#creator-download");

  const today = () => {
    const parts = new Intl.DateTimeFormat("en-CA", {
      timeZone: "Asia/Shanghai",
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }).formatToParts(new Date());
    const values = Object.fromEntries(parts.map((part) => [part.type, part.value]));
    return `${values.year}-${values.month}-${values.day}`;
  };
  const slugify = (value) =>
    value
      .trim()
      .toLowerCase()
      .replace(/[\s_]+/g, "-")
      .replace(/[^a-z0-9\u4e00-\u9fa5-]/g, "")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "");

  const splitTags = () =>
    tagsInput.value
      .split(/[,，]/)
      .map((tag) => tag.trim())
      .filter(Boolean);

  const frontMatter = (extra = []) => {
    const tags = splitTags();
    const lines = ["---", `date: ${today()}`, ...extra];
    if (tags.length) {
      lines.push("tags:");
      for (const tag of tags) lines.push(`  - ${tag}`);
    }
    lines.push("---", "");
    return lines.join("\n");
  };

  const templates = {
    blog: {
      path: (slug) => `docs/blog/posts/${today()}-${slug}.md`,
      body: (title, summary) =>
        `${frontMatter(["categories:", "  - 学习日志"])}# ${title}\n\n${summary}\n\n## 今天完成了什么\n\n\n## 关键收获\n\n\n## 下一步\n\n`,
    },
    paper: {
      path: (slug) => `docs/notes/papers/${slug}.md`,
      body: (title, summary) =>
        `${frontMatter()}# ${title}\n\n${summary}\n\n## 论文信息\n\n- 标题：\n- 年份：\n- 链接：\n\n## 核心问题\n\n\n## 方法摘要\n\n\n## 证据强度\n\n\n## 风险和边界\n\n\n## 是否值得复现\n\n`,
    },
    note: {
      path: (slug) => `docs/notes/ai/${slug}.md`,
      body: (title, summary) =>
        `${frontMatter()}# ${title}\n\n${summary}\n\n## 问题\n\n\n## 结论\n\n\n## 证据\n\n\n## 风险\n\n\n## 下一步\n\n`,
    },
    experiment: {
      path: (slug) => `docs/notes/research/${slug}.md`,
      body: (title, summary) =>
        `${frontMatter()}# ${title}\n\n${summary}\n\n## 假设\n\n\n## 设置\n\n- 数据：\n- 模型：\n- 指标：\n\n## 结果\n\n\n## 决策\n\n`,
    },
    plan: {
      path: (slug) => `docs/plans/${slug}.md`,
      body: (title, summary) =>
        `${frontMatter()}# ${title}\n\n${summary}\n\n## 本周任务\n\n- [ ] 阅读：\n- [ ] 实验：\n- [ ] 写作：\n- [ ] 发布：\n\n## 决策点\n\n`,
    },
  };

  const generate = () => {
    const title = titleInput.value.trim() || "未命名笔记";
    const slug = slugInput.value.trim() || slugify(title) || "untitled";
    const summary = summaryInput.value.trim() || "这篇内容要回答的核心问题。";
    const template = templates[typeInput.value] || templates.blog;
    pathOutput.textContent = template.path(slug);
    output.value = template.body(title, summary);
    localStorage.setItem(
      "medical-vlm-creator",
      JSON.stringify({
        type: typeInput.value,
        title,
        slug,
        tags: tagsInput.value,
        summary,
      })
    );
  };

  titleInput.addEventListener("input", () => {
    if (!slugInput.value.trim()) slugInput.value = slugify(titleInput.value);
  });

  generateButton.addEventListener("click", generate);

  copyButton.addEventListener("click", async () => {
    if (!output.value) generate();
    await navigator.clipboard.writeText(output.value);
    copyButton.textContent = "已复制";
    window.setTimeout(() => {
      copyButton.textContent = "复制";
    }, 1200);
  });

  downloadButton.addEventListener("click", () => {
    if (!output.value) generate();
    const filename = pathOutput.textContent.split("/").pop() || "note.md";
    const blob = new Blob([output.value], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    link.click();
    URL.revokeObjectURL(url);
  });

  const saved = localStorage.getItem("medical-vlm-creator");
  if (saved) {
    try {
      const state = JSON.parse(saved);
      typeInput.value = state.type || "blog";
      titleInput.value = state.title || "";
      slugInput.value = state.slug || "";
      tagsInput.value = state.tags || "";
      summaryInput.value = state.summary || "";
    } catch {
      localStorage.removeItem("medical-vlm-creator");
    }
  }

  generate();
});
