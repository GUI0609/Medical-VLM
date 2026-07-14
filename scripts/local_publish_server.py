from __future__ import annotations

import json
import re
import subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HOST = "127.0.0.1"
PORT = 8765
MAX_BODY_BYTES = 512 * 1024

ALLOWED_PREFIXES = (
    "docs/blog/posts/",
    "docs/notes/ai/",
    "docs/notes/papers/",
    "docs/notes/research/",
    "docs/plans/",
)

SENSITIVE_PATTERNS = (
    re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"(?i)\b(password|passwd|api[_-]?key|secret|token)\s*[:=]"),
    re.compile(r"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"\b172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"),
    re.compile(r"(住院号|病历号|门诊号|身份证号?|医保号|手机号|联系电话|患者姓名)\s*[:：]"),
)


class PublishError(Exception):
    pass


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def ensure_clean_worktree() -> None:
    result = run_command(["git", "status", "--porcelain"])
    if result.returncode != 0:
        raise PublishError(result.stderr.strip() or "无法读取 Git 状态")
    dirty = [line for line in result.stdout.splitlines() if line and not line.startswith("!!")]
    if dirty:
        raise PublishError("工作区有未提交改动，请先提交或清理后再自动发布。")


def validate_note_path(value: Any) -> tuple[str, Path]:
    if not isinstance(value, str) or not value.strip():
        raise PublishError("缺少发布路径。")
    normalized = value.strip().replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts:
        raise PublishError("发布路径不合法。")
    if path.suffix != ".md" or path.name == "index.md":
        raise PublishError("只能发布非 index 的 Markdown 文件。")
    rel_path = path.as_posix()
    if not any(rel_path.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        raise PublishError("发布路径不在允许的笔记目录内。")
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", rel_path):
        raise PublishError("文件路径只能包含英文、数字、点、下划线、短横线和斜杠。")
    return rel_path, ROOT / rel_path


def validate_content(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PublishError("Markdown 内容为空。")
    if len(value.encode("utf-8")) > MAX_BODY_BYTES:
        raise PublishError("Markdown 内容超过 512 KB，拒绝自动发布。")
    for pattern in SENSITIVE_PATTERNS:
        match = pattern.search(value)
        if match:
            raise PublishError(f"内容疑似包含敏感信息：{match.group(0)[:48]}")
    return value.rstrip() + "\n"


def commit_message(content: str, rel_path: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    else:
        title = Path(rel_path).stem
    title = re.sub(r"\s+", " ", title).strip()[:72] or Path(rel_path).stem
    return f"Add note: {title}"


def publish_note(payload: dict[str, Any]) -> dict[str, Any]:
    rel_path, target = validate_note_path(payload.get("path"))
    content = validate_content(payload.get("content"))
    if payload.get("dry_run"):
        return {"ok": True, "path": rel_path, "dry_run": True}

    ensure_clean_worktree()
    if target.exists():
        raise PublishError("目标文件已存在，自动发布不会覆盖已有笔记。")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    build = run_command([".venv/bin/mkdocs", "build", "--strict"])
    if build.returncode != 0:
        raise PublishError(build.stderr.strip() or build.stdout.strip() or "mkdocs build --strict 失败")

    add = run_command(["git", "add", rel_path])
    if add.returncode != 0:
        raise PublishError(add.stderr.strip() or "git add 失败")

    check = run_command(["git", "diff", "--cached", "--check"])
    if check.returncode != 0:
        raise PublishError(check.stderr.strip() or check.stdout.strip() or "暂存区检查失败")

    commit = run_command(["git", "commit", "-m", commit_message(content, rel_path), "--", rel_path])
    if commit.returncode != 0:
        raise PublishError(commit.stderr.strip() or commit.stdout.strip() or "git commit 失败")

    push = run_command(["git", "push", "origin", "main"])
    if push.returncode != 0:
        raise PublishError(push.stderr.strip() or push.stdout.strip() or "git push 失败")

    head = run_command(["git", "rev-parse", "--short", "HEAD"])
    return {
        "ok": True,
        "path": rel_path,
        "commit": head.stdout.strip(),
        "actions_url": "https://github.com/GUI0609/Medical-VLM/actions",
        "pages_url": "https://gui0609.github.io/Medical-VLM/",
    }


class Handler(BaseHTTPRequestHandler):
    def end_headers(self) -> None:
        origin = self.headers.get("Origin", "")
        if origin.startswith(("http://127.0.0.1:", "http://localhost:", "https://gui0609.github.io")):
            self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        if self.path != "/health":
            self.send_json(404, {"ok": False, "error": "Not found"})
            return
        self.send_json(200, {"ok": True, "service": "Medical-VLM local publisher"})

    def do_POST(self) -> None:
        if self.path != "/api/publish-note":
            self.send_json(404, {"ok": False, "error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise PublishError("请求体为空或过大。")
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise PublishError("请求体必须是 JSON 对象。")
            self.send_json(200, publish_note(payload))
        except PublishError as error:
            self.send_json(400, {"ok": False, "error": str(error)})
        except json.JSONDecodeError:
            self.send_json(400, {"ok": False, "error": "JSON 格式错误。"})
        except Exception as error:  # noqa: BLE001
            self.send_json(500, {"ok": False, "error": f"发布服务内部错误：{error}"})

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Medical-VLM local publisher running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()
