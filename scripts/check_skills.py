"""スキル集の決まった形を確かめる.

- 各スキルのフォルダに SKILL.md があり、frontmatter に name と description があって、name がフォルダ名と同じか
- Markdown に `` ` `` で囲んで書いた dotfiles のパス（`~/.dotfiles/...`）が、実際にあるか
- Markdown の相対リンク（`[表示名](./path)`）の先が、実際にあるか

dotfiles の場所は環境変数 DOTFILES_DIR で変えられる（既定は ~/.dotfiles。CI では取ってきた先を渡す）。
見つかった問題を表示し、1つでもあれば終了コード 1 で終わる。
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# スキルではないフォルダ
NOT_SKILLS = {"scripts"}

# 隠しフォルダと、追跡していない置き場（手元のクローンにだけあるもの）は見ない
IGNORED_DIRS = {"synced", "node_modules"}

DOTFILES_PATH = re.compile(r"`~/\.dotfiles/([^`\s]*)`")
# 日付や言語を当てはめるパターン（`~/.dotfiles/templates/<言語>/` など）は見ない
PLACEHOLDER = re.compile(r"<|>|\*")
RELATIVE_LINK = re.compile(r"\]\((\.{1,2}/[^)\s#]+)(?:#[^)]*)?\)")


def markdown_files() -> list[Path]:
    """確かめる Markdown の一覧."""
    files = []
    for md in sorted(ROOT.rglob("*.md")):
        parts = md.relative_to(ROOT).parts
        if any(p.startswith(".") or p in IGNORED_DIRS for p in parts[:-1]):
            continue
        files.append(md)
    return files


def skill_dirs() -> list[Path]:
    """スキルのフォルダの一覧（直下の、隠しでも除外でもないフォルダ）."""
    return sorted(
        p
        for p in ROOT.iterdir()
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name not in NOT_SKILLS | IGNORED_DIRS
    )


def read_frontmatter(path: Path) -> dict[str, str] | None:
    """先頭の --- で囲まれた frontmatter を、key: value の辞書にする."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return None
    fields = {}
    for line in lines[1:]:
        if line == "---":
            return fields
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return None


def check_skills() -> list[str]:
    """各スキルの SKILL.md の frontmatter を確かめる."""
    problems = []
    for skill_dir in skill_dirs():
        skill_md = skill_dir / "SKILL.md"
        where = skill_md.relative_to(ROOT)
        if not skill_md.exists():
            problems.append(f"{where}: SKILL.md がない")
            continue
        fields = read_frontmatter(skill_md)
        if fields is None:
            problems.append(f"{where}: frontmatter（先頭の --- の囲み）がない")
            continue
        for key in ("name", "description"):
            if not fields.get(key):
                problems.append(f"{where}: frontmatter に {key} がない")
        if fields.get("name") and fields["name"] != skill_dir.name:
            problems.append(
                f"{where}: name（{fields['name']}）がフォルダ名（{skill_dir.name}）と違う"
            )
    return problems


def check_paths(dotfiles: Path) -> list[str]:
    """dotfiles のパスと相対リンクの先があるかを確かめる."""
    problems = []
    for md in markdown_files():
        where = md.relative_to(ROOT)
        lines = md.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            for rest in DOTFILES_PATH.findall(line):
                if PLACEHOLDER.search(rest) or (dotfiles / rest).exists():
                    continue
                problems.append(f"{where}:{lineno}: `~/.dotfiles/{rest}` がない")
            for target in RELATIVE_LINK.findall(line):
                if not (md.parent / target).exists():
                    problems.append(f"{where}:{lineno}: リンク先 {target} がない")
    return problems


def main() -> int:
    dotfiles = Path(os.environ.get("DOTFILES_DIR", "~/.dotfiles")).expanduser()
    if not dotfiles.is_dir():
        print(f"dotfiles（{dotfiles}）がない。DOTFILES_DIR で場所を渡す")
        return 1
    problems = check_skills() + check_paths(dotfiles)
    for problem in problems:
        print(problem)
    if problems:
        print(f"問題が {len(problems)} 件ある")
        return 1
    print("SKILL.md の frontmatter と、スキルが指すパスに問題はない")
    return 0


if __name__ == "__main__":
    sys.exit(main())
