from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
from statistics import median

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PIC_DIR = ROOT / "pic"
ICON_DIR = ROOT / "docs" / "assets" / "images" / "library" / "icons"
PAGE_PATH = ROOT / "docs" / "assets-library" / "index.md"
SITE_PREFIX = "/Medical-VLM"


@dataclass(frozen=True)
class IconSpec:
    slug: str
    title: str
    source_suffix: str
    mode: str
    rows: int = 0
    cols: int = 0
    boxes: tuple[tuple[int, int, int, int], ...] = ()
    labels: tuple[str, ...] = ()


def centered_grid(
    x_centers: tuple[int, ...],
    y_centers: tuple[int, ...],
    width: int,
    height: int,
) -> tuple[tuple[int, int, int, int], ...]:
    return tuple(
        (round(x - width / 2), round(y - height / 2), width, height)
        for y in y_centers
        for x in x_centers
    )


FUNCTIONAL_BOXES = centered_grid(
    (195, 449, 703, 957, 1211),
    (120, 290, 460, 630, 800, 970),
    240,
    170,
)

STICKER_BOXES = centered_grid(
    (145, 385, 625, 865, 1105, 1335),
    (135, 360, 580, 800),
    230,
    190,
) + (
    (55, 920, 250, 150),
    (300, 920, 250, 150),
    (575, 920, 125, 150),
    (715, 920, 170, 150),
    (935, 920, 160, 150),
    (1185, 920, 160, 150),
)

ACHIEVEMENT_BOXES = (
    (45, 45, 210, 220),
    (280, 45, 200, 220),
    (505, 45, 190, 220),
    (705, 50, 230, 220),
    (930, 45, 240, 230),
    (1180, 40, 230, 230),
    (55, 285, 190, 220),
    (285, 285, 190, 220),
    (505, 285, 190, 220),
    (685, 295, 230, 190),
    (930, 295, 235, 190),
    (1200, 285, 200, 210),
    (40, 520, 220, 195),
    (285, 520, 205, 195),
    (500, 520, 220, 195),
    (695, 525, 215, 190),
    (930, 520, 230, 205),
    (1185, 520, 235, 205),
    (45, 720, 220, 175),
    (285, 720, 220, 175),
    (505, 720, 220, 175),
    (725, 720, 220, 175),
    (945, 700, 220, 200),
    (1175, 695, 240, 210),
    (40, 900, 225, 175),
    (285, 890, 215, 185),
    (510, 890, 220, 185),
    (715, 890, 230, 185),
    (940, 890, 225, 185),
    (1165, 890, 245, 185),
)


STUDY_ITEM_BOXES = (
    (35, 80, 220, 230),
    (275, 108, 210, 190),
    (495, 90, 160, 220),
    (680, 80, 160, 250),
    (890, 75, 125, 225),
    (1085, 130, 145, 150),
    (1260, 130, 120, 160),
    (35, 340, 145, 190),
    (210, 330, 230, 220),
    (470, 340, 180, 195),
    (650, 330, 175, 205),
    (855, 338, 180, 190),
    (1085, 350, 125, 190),
    (1240, 330, 170, 210),
    (25, 585, 230, 190),
    (310, 610, 190, 170),
    (575, 595, 190, 190),
    (845, 590, 110, 180),
    (995, 595, 160, 170),
    (1215, 565, 190, 225),
    (30, 840, 140, 190),
    (190, 820, 150, 180),
    (350, 805, 225, 220),
    (570, 825, 170, 155),
    (760, 820, 175, 190),
    (940, 820, 170, 185),
    (1110, 820, 145, 175),
    (1270, 800, 170, 190),
)


SPECS = (
    IconSpec(
        "functional",
        "功能入口",
        "00_13_48 (2).png",
        "manual",
        boxes=FUNCTIONAL_BOXES,
        labels=(
            "首页房屋",
            "写作便签",
            "学习本",
            "任务清单",
            "日历计划",
            "待办笔记",
            "标签分类",
            "收藏星标",
            "归档盒子",
            "搜索放大镜",
            "设置齿轮",
            "个人头像",
            "评论消息",
            "上传云朵",
            "下载云朵",
            "书签收藏",
            "提醒铃铛",
            "计时闹钟",
            "数据图表",
            "文件夹",
            "图片相册",
            "音乐音符",
            "商店小屋",
            "礼物奖励",
            "绘画调色盘",
            "退出入口",
            "阅读台灯",
            "植物成长",
            "便签备忘",
            "安全锁",
        ),
    ),
    IconSpec(
        "sticker",
        "卡通贴纸",
        "00_13_49 (3).png",
        "manual",
        boxes=STICKER_BOXES,
        labels=(
            "阅读",
            "写作",
            "铅笔",
            "睡觉",
            "加油",
            "思考",
            "惊讶",
            "眼镜阅读",
            "作业",
            "便签",
            "文件夹",
            "星星",
            "咖啡",
            "浇水",
            "疑问",
            "加油便签",
            "读书",
            "书堆",
            "爱心",
            "成绩单",
            "四叶草",
            "背包",
            "打招呼",
            "庆祝",
            "认真学习气泡",
            "快乐学习气泡",
            "幸运贴纸",
            "便签组",
            "胶带",
            "剪贴板",
        ),
    ),
    IconSpec(
        "study-item",
        "学习小物",
        "00_13_52 (7).png",
        "manual",
        boxes=STUDY_ITEM_BOXES,
        labels=(
            "打开的书",
            "书本堆",
            "笔筒",
            "铅笔",
            "尺子",
            "橡皮",
            "回形针",
            "放大镜",
            "书包",
            "台灯",
            "马克杯",
            "闹钟",
            "沙漏",
            "地球仪",
            "黑板",
            "电脑",
            "写字板",
            "书签",
            "奖牌",
            "奖杯",
            "印章",
            "花盆",
            "蘑菇屋",
            "蝴蝶结",
            "邮箱",
            "四叶草徽章",
            "毕业帽",
            "毕业表情",
        ),
    ),
    IconSpec(
        "achievement",
        "成就徽章",
        "00_13_53 (8).png",
        "manual",
        boxes=ACHIEVEMENT_BOXES,
        labels=(
            "金牌",
            "银牌",
            "铜牌",
            "星星奖杯",
            "水晶奖杯",
            "冠军奖杯",
            "金色皇冠",
            "银色皇冠",
            "铜色皇冠",
            "星章",
            "钻石徽章",
            "奖牌角色",
            "皇冠徽章",
            "阅读徽章",
            "铅笔徽章",
            "100 分",
            "7 天打卡",
            "30 天打卡",
            "任务完成",
            "学习打卡",
            "章节通关",
            "全部完成",
            "礼物盒",
            "宝箱",
            "领奖台",
            "50 知识点",
            "100 小时学习",
            "新纪录",
            "彩带庆祝",
            "星星礼盒",
        ),
    ),
)


def source_for(suffix: str) -> Path:
    matches = sorted(PIC_DIR.glob(f"*{suffix}"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one source ending with {suffix!r}, found {len(matches)}")
    return matches[0]


def grid_boxes(image: Image.Image, rows: int, cols: int) -> list[tuple[int, int, int, int]]:
    cell_w = image.width / cols
    cell_h = image.height / rows
    boxes = []
    for row in range(rows):
        for col in range(cols):
            x0 = round(col * cell_w)
            y0 = round(row * cell_h)
            x1 = round((col + 1) * cell_w)
            y1 = round((row + 1) * cell_h)
            boxes.append((x0, y0, x1 - x0, y1 - y0))
    return boxes


def crop_icon(source: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    x, y, width, height = box
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(source.width, x + width)
    y1 = min(source.height, y + height)
    crop = source.crop((x0, y0, x1, y1)).convert("RGB")
    crop = trim_foreground(crop)
    side = max(crop.width, crop.height)
    square = Image.new("RGB", (side, side), "#fffdf1")
    square.paste(crop, ((side - crop.width) // 2, (side - crop.height) // 2))
    square.thumbnail((192, 192), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (216, 216), "#fffdf1")
    canvas.paste(square, ((216 - square.width) // 2, (216 - square.height) // 2))
    return canvas


def trim_foreground(image: Image.Image) -> Image.Image:
    width, height = image.size
    pixels = image.load()
    border = []
    step = 6
    for x in range(0, width, step):
        border.append(pixels[x, 0])
        border.append(pixels[x, height - 1])
    for y in range(0, height, step):
        border.append(pixels[0, y])
        border.append(pixels[width - 1, y])
    bg = tuple(int(median(channel)) for channel in zip(*border))

    threshold = 54
    mask = bytearray(width * height)
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2]) > threshold:
                mask[y * width + x] = 1

    visited = bytearray(width * height)
    components = []
    for start in range(width * height):
        if not mask[start] or visited[start]:
            continue
        stack = [start]
        visited[start] = 1
        area = 0
        min_x = width
        min_y = height
        max_x = 0
        max_y = 0
        while stack:
            pos = stack.pop()
            px = pos % width
            py = pos // width
            area += 1
            min_x = min(min_x, px)
            min_y = min(min_y, py)
            max_x = max(max_x, px)
            max_y = max(max_y, py)
            for nx, ny in ((px - 1, py), (px + 1, py), (px, py - 1), (px, py + 1)):
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue
                npos = ny * width + nx
                if mask[npos] and not visited[npos]:
                    visited[npos] = 1
                    stack.append(npos)
        components.append((area, min_x, min_y, max_x, max_y))

    if not components:
        return image

    largest = max(area for area, *_ in components)
    keep = [component for component in components if component[0] >= max(90, largest * 0.018)]
    if not keep:
        return image

    min_x = min(component[1] for component in keep)
    min_y = min(component[2] for component in keep)
    max_x = max(component[3] for component in keep)
    max_y = max(component[4] for component in keep)
    if (max_x - min_x) * (max_y - min_y) > width * height * 0.92:
        return image

    pad = 12
    return image.crop(
        (
            max(0, min_x - pad),
            max(0, min_y - pad),
            min(width, max_x + pad + 1),
            min(height, max_y + pad + 1),
        )
    )


def render_page(icons: list[dict[str, str]]) -> str:
    filter_buttons = "\n".join(
        f'    <button type="button" data-asset-filter="{escape(spec.slug)}">{escape(spec.title)}</button>'
        for spec in SPECS
    )
    cards = "\n".join(render_card(icon) for icon in icons)
    return f"""---
hide:
  - toc
---

# 素材库

<section class="manor-page-hero manor-page-hero--assets">
  <div>
    <p class="farm-kicker">Asset Library</p>
    <h2>从素材库选取小图标</h2>
    <p>这里收纳已经从原始素材图切分、压缩并统一尺寸的小图标。点击复制后可直接粘贴到 Markdown 页面中。</p>
  </div>
</section>

<section class="asset-library" data-asset-library>
  <div class="asset-toolbar">
    <label>
      搜索素材
      <input id="asset-search" type="search" placeholder="输入功能、贴纸、学习小物、成就或文件名" />
    </label>
    <div class="asset-filters" aria-label="素材分类">
      <button type="button" data-asset-filter="all" aria-pressed="true">全部</button>
{filter_buttons}
    </div>
  </div>
  <div class="asset-grid">
{cards}
  </div>
</section>

## 使用原则

- 优先复制站点绝对路径，适合任意页面引用。
- 如果只在本地写作，也可以从 `docs/assets/images/library/icons/` 目录直接选择文件。
- 不要把 `/share/gguilin/Medical-VLM/pic` 中的原始大图直接提交到 Git。
"""


def render_card(icon: dict[str, str]) -> str:
    name = escape(icon["name"])
    category = escape(icon["category"])
    slug = escape(icon["slug"])
    file_name = escape(icon["file"])
    rel_path = f"../assets/images/library/icons/{file_name}"
    site_path = f"{SITE_PREFIX}/assets/images/library/icons/{file_name}"
    markdown = escape(f"![{icon['name']}]({site_path})", quote=True)
    return f"""    <article class="asset-card" data-asset-name="{name} {file_name}" data-asset-category="{slug}">
      <img src="{rel_path}" alt="{name}" />
      <strong>{name}</strong>
      <span>{category}</span>
      <code>{site_path}</code>
      <button type="button" data-copy-asset="{markdown}">复制 Markdown</button>
    </article>"""


def main() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    PAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    for old_file in ICON_DIR.glob("*.webp"):
        old_file.unlink()

    icons: list[dict[str, str]] = []
    for spec in SPECS:
        source = Image.open(source_for(spec.source_suffix)).convert("RGB")
        boxes = grid_boxes(source, spec.rows, spec.cols) if spec.mode == "grid" else list(spec.boxes)
        for index, box in enumerate(boxes, 1):
            file_name = f"{spec.slug}-{index:02d}.webp"
            label = spec.labels[index - 1] if index <= len(spec.labels) else f"{index:02d}"
            crop_icon(source, box).save(ICON_DIR / file_name, "WEBP", quality=84, method=6)
            icons.append(
                {
                    "name": f"{spec.title} {index:02d} {label}",
                    "category": spec.title,
                    "slug": spec.slug,
                    "file": file_name,
                }
            )

    PAGE_PATH.write_text(render_page(icons), encoding="utf-8")
    print(f"Generated {len(icons)} icons in {ICON_DIR}")
    print(f"Generated {PAGE_PATH}")


if __name__ == "__main__":
    main()
