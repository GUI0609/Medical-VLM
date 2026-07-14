document$.subscribe(() => {
  const copyText = async (text) => {
    if (navigator.clipboard?.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        return;
      } catch {
        // Fall back for browsers that block Clipboard API outside secure contexts.
      }
    }
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "");
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
  };

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
  if (desk) {
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
    const publishButton = document.querySelector("#creator-publish");
    const confirmInput = document.querySelector("#creator-confirm");
    const statusOutput = document.querySelector("#creator-status");

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
        .replace(/[^a-z0-9-]/g, "")
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
      const slug = slugify(slugInput.value) || slugify(title) || "untitled";
      const summary = summaryInput.value.trim() || "这篇内容要回答的核心问题。";
      const template = templates[typeInput.value] || templates.blog;
      slugInput.value = slug;
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

    const setPublishStatus = (message, state = "") => {
      statusOutput.textContent = message;
      if (state) {
        statusOutput.dataset.state = state;
      } else {
        delete statusOutput.dataset.state;
      }
    };

    titleInput.addEventListener("input", () => {
      if (!slugInput.value.trim()) slugInput.value = slugify(titleInput.value);
    });

    generateButton.addEventListener("click", generate);

    copyButton.addEventListener("click", async () => {
      if (!output.value) generate();
      await copyText(output.value);
      copyButton.textContent = "已复制";
      window.setTimeout(() => {
        copyButton.textContent = "复制";
      }, 2000);
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

    publishButton.addEventListener("click", async () => {
      if (!confirmInput.checked) {
        setPublishStatus("发布前必须确认内容不包含密钥、患者信息、未公开材料和内网凭证。", "error");
        return;
      }
      if (!output.value) generate();
      publishButton.disabled = true;
      setPublishStatus("正在连接本地发布服务并执行严格构建...");
      try {
        const response = await fetch("http://127.0.0.1:8765/api/publish-note", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            path: pathOutput.textContent,
            content: output.value,
          }),
        });
        const result = await response.json();
        if (!response.ok || !result.ok) {
          throw new Error(result.error || "自动发布失败。");
        }
        setPublishStatus(
          `已提交 ${result.commit} 并推送到 main。GitHub Actions 会自动部署：${result.actions_url}`,
          "success"
        );
      } catch (error) {
        setPublishStatus(
          `未发布：${error.message} 先在服务器运行 .venv/bin/python scripts/local_publish_server.py。`,
          "error"
        );
      } finally {
        publishButton.disabled = false;
      }
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
  }

  const library = document.querySelector("[data-asset-library]");
  if (!library) return;

  const searchInput = library.querySelector("#asset-search");
  const filterButtons = library.querySelectorAll("[data-asset-filter]");
  const cards = library.querySelectorAll(".asset-card");
  let activeFilter = "all";

  const applyAssetFilters = () => {
    const query = searchInput.value.trim().toLowerCase();
    for (const card of cards) {
      const matchesCategory =
        activeFilter === "all" || card.dataset.assetCategory === activeFilter;
      const matchesSearch = !query || card.dataset.assetName.toLowerCase().includes(query);
      card.classList.toggle("is-hidden", !matchesCategory || !matchesSearch);
    }
  };

  for (const button of filterButtons) {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.assetFilter || "all";
      for (const item of filterButtons) {
        item.setAttribute("aria-pressed", String(item === button));
      }
      applyAssetFilters();
    });
  }

  searchInput.addEventListener("input", applyAssetFilters);

  for (const button of library.querySelectorAll("[data-copy-asset]")) {
    button.addEventListener("click", async () => {
      await copyText(button.dataset.copyAsset);
      const original = button.textContent;
      button.textContent = "已复制";
      window.setTimeout(() => {
        button.textContent = original;
      }, 2000);
    });
  }
});
