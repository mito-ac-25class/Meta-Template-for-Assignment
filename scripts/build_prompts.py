#!/usr/bin/env python3
"""Build tool-specific prompts from canonical sources in prompts/.

Reads prompts/*.md and generates:
  - .claude/commands/{name}.md      (Claude Code slash commands)
  - .claude/skills/{name}/SKILL.md  (Claude Code skills, from _shared/)
  - .github/prompts/{name}.admin.prompt.md  (GitHub Copilot prompts)

Usage:
    python scripts/build_prompts.py
    python scripts/build_prompts.py --dry-run
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"
SHARED_DIR = PROMPTS_DIR / "_shared"

CLAUDE_COMMANDS_DIR = REPO_ROOT / ".claude" / "commands"
CLAUDE_SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
COPILOT_PROMPTS_DIR = REPO_ROOT / ".github" / "prompts"

# Mapping from include tag to shared file
INCLUDE_PATTERN = re.compile(r"\{\{(\w+)\}\}")

INCLUDE_MAP = {
    "ASSIGNMENT_TYPES": "assignment-types.md",
    "GIT_WORKFLOW": "git-workflow.md",
    "REVIEW_PROCESS": "review-process.md",
}

# Skill metadata for _shared files that should become Claude skills
SKILL_CONFIGS = {
    "assignment-types.md": {
        "name": "assignment-types",
        "description": (
            "4つの課題実施方式（プログラム実装課題、リファクタリング課題、"
            "テスト実装課題、テスト駆動開発課題）の定義を提供します。\n"
            "課題プラン作成時や課題形式の選定時に自動参照されます。\n"
            "「課題形式」「実施方式」「プログラム実装」「リファクタリング」"
            "「テスト実装」「TDD」などのキーワードで自動的に適用されます。"
        ),
    },
    "git-workflow.md": {
        "name": "git-workflow",
        "description": (
            "課題作成時のGitブランチ・コミット・プッシュの標準手順を提供します。\n"
            "ブランチ作成、コミットメッセージ作成、プルリクエスト作成時に自動参照されます。\n"
            "「ブランチを作成」「コミット」「プッシュ」などのキーワードで自動的に適用されます。"
        ),
    },
}


def load_shared_files() -> dict[str, str]:
    """Load all shared files into a dict: tag_name -> content."""
    shared = {}
    for tag_name, filename in INCLUDE_MAP.items():
        filepath = SHARED_DIR / filename
        if filepath.exists():
            shared[tag_name] = filepath.read_text(encoding="utf-8")
        else:
            print(f"WARNING: Shared file not found: {filepath}", file=sys.stderr)
            shared[tag_name] = f"<!-- MISSING: {filename} -->"
    return shared


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown. Returns (metadata, body)."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    metadata = {}
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            metadata[key.strip()] = value.strip().strip('"').strip("'")

    return metadata, parts[2].lstrip("\n")


def resolve_includes(body: str, shared: dict[str, str]) -> str:
    """Replace {{TAG_NAME}} with shared file content."""
    def replacer(match):
        tag = match.group(1)
        if tag in shared:
            return shared[tag]
        return match.group(0)  # Leave unknown tags as-is

    return INCLUDE_PATTERN.sub(replacer, body)


def build_claude_command(name: str, metadata: dict, body: str) -> str:
    """Build a Claude Code command file."""
    description = metadata.get("description", "")
    allowed_tools = metadata.get("allowed-tools", "")

    lines = ["---"]
    if description:
        lines.append(f"description: {description}")
    if allowed_tools:
        lines.append(f"allowed-tools: {allowed_tools}")
    lines.append("---")
    lines.append("")
    lines.append(body)

    return "\n".join(lines)


def build_copilot_prompt(name: str, metadata: dict, body: str) -> str:
    """Build a GitHub Copilot admin prompt file."""
    description = metadata.get("description", "")

    lines = ["---"]
    if description:
        lines.append(f'description: "{description}"')
    lines.append("---")
    lines.append("")
    lines.append(body)

    return "\n".join(lines)


def build_skill(filename: str, content: str, config: dict) -> str:
    """Build a Claude Code SKILL.md file from shared content."""
    lines = [
        "---",
        f"name: {config['name']}",
        "description: |",
    ]
    for desc_line in config["description"].splitlines():
        lines.append(f"  {desc_line}")
    lines.append("---")
    lines.append("")
    lines.append(content)

    return "\n".join(lines)


def clean_output_dirs():
    """Remove existing generated files."""
    # Clean Claude commands (only generated ones)
    if CLAUDE_COMMANDS_DIR.exists():
        shutil.rmtree(CLAUDE_COMMANDS_DIR)
    CLAUDE_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    # Clean Claude skills (only generated ones)
    if CLAUDE_SKILLS_DIR.exists():
        shutil.rmtree(CLAUDE_SKILLS_DIR)
    CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    # Clean Copilot prompts (only .admin.prompt.md files)
    if COPILOT_PROMPTS_DIR.exists():
        for f in COPILOT_PROMPTS_DIR.glob("*.admin.prompt.md"):
            f.unlink()
    COPILOT_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Build tool-specific prompts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    args = parser.parse_args()

    shared = load_shared_files()

    if not args.dry_run:
        clean_output_dirs()

    # Build command prompts from prompts/*.md
    prompt_files = sorted(PROMPTS_DIR.glob("*.md"))
    for prompt_file in prompt_files:
        name = prompt_file.stem
        content = prompt_file.read_text(encoding="utf-8")

        metadata, body = parse_frontmatter(content)
        resolved_body = resolve_includes(body, shared)

        # Claude Code command
        claude_content = build_claude_command(name, metadata, resolved_body)
        claude_path = CLAUDE_COMMANDS_DIR / f"{name}.md"

        # Copilot prompt
        copilot_content = build_copilot_prompt(name, metadata, resolved_body)
        copilot_path = COPILOT_PROMPTS_DIR / f"{name}.admin.prompt.md"

        if args.dry_run:
            print(f"  Claude:  {claude_path.relative_to(REPO_ROOT)}")
            print(f"  Copilot: {copilot_path.relative_to(REPO_ROOT)}")
        else:
            claude_path.write_text(claude_content, encoding="utf-8")
            copilot_path.write_text(copilot_content, encoding="utf-8")
            print(f"Generated: {claude_path.relative_to(REPO_ROOT)}")
            print(f"Generated: {copilot_path.relative_to(REPO_ROOT)}")

    # Build skills from _shared files
    for filename, config in SKILL_CONFIGS.items():
        shared_path = SHARED_DIR / filename
        if not shared_path.exists():
            continue

        content = shared_path.read_text(encoding="utf-8")
        skill_content = build_skill(filename, content, config)
        skill_dir = CLAUDE_SKILLS_DIR / config["name"]
        skill_path = skill_dir / "SKILL.md"

        if args.dry_run:
            print(f"  Skill:   {skill_path.relative_to(REPO_ROOT)}")
        else:
            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_path.write_text(skill_content, encoding="utf-8")
            print(f"Generated: {skill_path.relative_to(REPO_ROOT)}")

    if args.dry_run:
        print("\n(dry run — no files written)")
    else:
        print("\nBuild complete.")


if __name__ == "__main__":
    main()
