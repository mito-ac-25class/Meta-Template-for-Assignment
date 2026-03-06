#!/usr/bin/env python3
"""Build tool-specific prompts from canonical sources in prompts/.

Reads prompts/*.md and generates:
  - .claude/commands/{name}.md                 (Claude Code slash commands)
  - .claude/skills/{name}/SKILL.md             (Claude Code shared skills)
  - .github/prompts/{name}.admin.prompt.md     (GitHub Copilot prompts)
  - .agents/skills/{name}/SKILL.md             (Codex skills)
  - .agents/skills/{name}/agents/openai.yaml   (Codex skill metadata)

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
CODEX_SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

INCLUDE_PATTERN = re.compile(r"\{\{(\w+)\}\}")
HEADING_PATTERN = re.compile(r"^# .+$", re.MULTILINE)

INCLUDE_MAP = {
    "ASSIGNMENT_TYPES": "assignment-types.md",
    "GIT_WORKFLOW": "git-workflow.md",
    "REVIEW_PROCESS": "review-process.md",
}

SHARED_SKILL_CONFIGS = {
    "assignment-types.md": {
        "name": "assignment-types",
        "description": (
            "4つの課題実施方式（プログラム実装課題、リファクタリング課題、"
            "テスト実装課題、テスト駆動開発課題）の定義を提供します。\n"
            "課題プラン作成時や課題形式の選定時に自動参照されます。\n"
            "「課題形式」「実施方式」「プログラム実装」「リファクタリング」"
            "「テスト実装」「TDD」などのキーワードで自動的に適用されます。"
        ),
        "display_name": "Assignment Types",
        "short_description": "課題実施方式の選定基準と定義を参照します",
        "default_prompt": (
            "$assignment-types を使って今回の課題に適した実施方式を比較してください。"
        ),
        "allow_implicit_invocation": True,
    },
    "git-workflow.md": {
        "name": "git-workflow",
        "description": (
            "課題作成時のGitブランチ・コミット・プッシュの標準手順を提供します。\n"
            "ブランチ作成、コミットメッセージ作成、プルリクエスト作成時に自動参照されます。\n"
            "「ブランチを作成」「コミット」「プッシュ」などのキーワードで自動的に適用されます。"
        ),
        "display_name": "Git Workflow",
        "short_description": "課題作成用の Git 運用手順を参照します",
        "default_prompt": (
            "$git-workflow を使ってこのフェーズの Git 手順を確認してください。"
        ),
        "allow_implicit_invocation": True,
    },
}

PHASE_SKILL_CONFIGS = {
    "design": {
        "name": "design-admin",
        "display_name": "Design Admin",
        "short_description": "課題設計フェーズを明示的に実行します",
        "default_prompt": (
            "$design-admin を使って topics.yaml を検証し、課題プランを作成してください。"
        ),
        "allow_implicit_invocation": False,
    },
    "build": {
        "name": "build-admin",
        "display_name": "Build Admin",
        "short_description": "課題構築フェーズを明示的に実行します",
        "default_prompt": (
            "$build-admin を使って README、テスト、CI の構築を進めてください。"
        ),
        "allow_implicit_invocation": False,
    },
    "release": {
        "name": "release-admin",
        "display_name": "Release Admin",
        "short_description": "課題リリース準備フェーズを明示実行します",
        "default_prompt": (
            "$release-admin を使って包括検証とリリース準備を進めてください。"
        ),
        "allow_implicit_invocation": False,
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


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
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

    def replacer(match: re.Match[str]) -> str:
        tag = match.group(1)
        if tag in shared:
            return shared[tag]
        return match.group(0)

    return INCLUDE_PATTERN.sub(replacer, body)


def replace_first_heading(body: str, heading: str) -> str:
    """Replace the first H1 heading with a tool-specific heading."""
    if HEADING_PATTERN.search(body):
        return HEADING_PATTERN.sub(heading, body, count=1)
    return f"{heading}\n\n{body}"


def add_invocation_note(body: str, note: str) -> str:
    """Insert a short invocation hint immediately after the first heading."""
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        rebuilt = [lines[0], "", f"> {note}", ""]
        rebuilt.extend(lines[1:])
        return "\n".join(rebuilt)
    return f"> {note}\n\n{body}"


def format_phase_body(name: str, body: str, tool: str) -> str:
    """Customize the canonical phase body for a specific tool."""
    if tool == "claude":
        heading = f"# /{name} コマンド"
        note = f"起動方法: Claude Code で `/{name}` を実行します。"
    elif tool == "copilot":
        heading = f"# /{name}.admin プロンプト"
        note = f"起動方法: GitHub Copilot で `/{name}.admin` を実行します。"
    elif tool == "codex":
        skill_name = PHASE_SKILL_CONFIGS[name]["name"]
        heading = f"# ${skill_name} スキル"
        note = f"起動方法: Codex で `${skill_name}` を明示的に起動します。"
    else:
        raise ValueError(f"Unknown tool: {tool}")

    formatted = replace_first_heading(body, heading)
    return add_invocation_note(formatted, note)


def build_claude_command(name: str, metadata: dict[str, str], body: str) -> str:
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
    lines.append(format_phase_body(name, body, tool="claude"))
    return "\n".join(lines)


def build_copilot_prompt(name: str, metadata: dict[str, str], body: str) -> str:
    """Build a GitHub Copilot admin prompt file."""
    description = metadata.get("description", "")

    lines = ["---"]
    if description:
        lines.append(f'description: "{description}"')
    lines.append("---")
    lines.append("")
    lines.append(format_phase_body(name, body, tool="copilot"))
    return "\n".join(lines)


def build_skill(content: str, config: dict[str, str]) -> str:
    """Build a SKILL.md file from markdown content and config."""
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


def build_codex_openai_yaml(config: dict[str, str]) -> str:
    """Build the minimal agents/openai.yaml used by Codex skill UIs."""
    allow_implicit = str(config["allow_implicit_invocation"]).lower()
    return "\n".join([
        "interface:",
        f'  display_name: "{config["display_name"]}"',
        f'  short_description: "{config["short_description"]}"',
        f'  default_prompt: "{config["default_prompt"]}"',
        "policy:",
        f"  allow_implicit_invocation: {allow_implicit}",
        "",
    ])


def write_file(path: Path, content: str):
    """Write UTF-8 text to a file, creating parent directories when needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def clean_output_dirs():
    """Remove existing generated files."""
    if CLAUDE_COMMANDS_DIR.exists():
        shutil.rmtree(CLAUDE_COMMANDS_DIR)
    CLAUDE_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    if CLAUDE_SKILLS_DIR.exists():
        shutil.rmtree(CLAUDE_SKILLS_DIR)
    CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    if CODEX_SKILLS_DIR.exists():
        shutil.rmtree(CODEX_SKILLS_DIR)
    CODEX_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    if COPILOT_PROMPTS_DIR.exists():
        for file_path in COPILOT_PROMPTS_DIR.glob("*.admin.prompt.md"):
            file_path.unlink()
    COPILOT_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)


def build_phase_outputs(
    name: str,
    metadata: dict[str, str],
    body: str,
    dry_run: bool,
):
    """Build generated files for a prompt phase."""
    claude_path = CLAUDE_COMMANDS_DIR / f"{name}.md"
    copilot_path = COPILOT_PROMPTS_DIR / f"{name}.admin.prompt.md"
    codex_config = {
        **PHASE_SKILL_CONFIGS[name],
        "description": metadata.get("description", ""),
    }
    codex_skill_dir = CODEX_SKILLS_DIR / codex_config["name"]
    codex_skill_path = codex_skill_dir / "SKILL.md"
    codex_openai_path = codex_skill_dir / "agents" / "openai.yaml"

    if dry_run:
        print(f"  Claude:  {claude_path.relative_to(REPO_ROOT)}")
        print(f"  Copilot: {copilot_path.relative_to(REPO_ROOT)}")
        print(f"  Codex:   {codex_skill_path.relative_to(REPO_ROOT)}")
        print(f"  Codex:   {codex_openai_path.relative_to(REPO_ROOT)}")
        return

    write_file(claude_path, build_claude_command(name, metadata, body))
    write_file(copilot_path, build_copilot_prompt(name, metadata, body))
    write_file(
        codex_skill_path,
        build_skill(format_phase_body(name, body, tool="codex"), codex_config),
    )
    write_file(codex_openai_path, build_codex_openai_yaml(codex_config))

    print(f"Generated: {claude_path.relative_to(REPO_ROOT)}")
    print(f"Generated: {copilot_path.relative_to(REPO_ROOT)}")
    print(f"Generated: {codex_skill_path.relative_to(REPO_ROOT)}")
    print(f"Generated: {codex_openai_path.relative_to(REPO_ROOT)}")


def build_shared_outputs(dry_run: bool):
    """Build shared skills for Claude and Codex from prompts/_shared."""
    for filename, config in SHARED_SKILL_CONFIGS.items():
        shared_path = SHARED_DIR / filename
        if not shared_path.exists():
            continue

        content = shared_path.read_text(encoding="utf-8")

        claude_skill_dir = CLAUDE_SKILLS_DIR / config["name"]
        claude_skill_path = claude_skill_dir / "SKILL.md"
        codex_skill_dir = CODEX_SKILLS_DIR / config["name"]
        codex_skill_path = codex_skill_dir / "SKILL.md"
        codex_openai_path = codex_skill_dir / "agents" / "openai.yaml"

        if dry_run:
            print(f"  Skill:   {claude_skill_path.relative_to(REPO_ROOT)}")
            print(f"  Codex:   {codex_skill_path.relative_to(REPO_ROOT)}")
            print(f"  Codex:   {codex_openai_path.relative_to(REPO_ROOT)}")
            continue

        write_file(claude_skill_path, build_skill(content, config))
        write_file(codex_skill_path, build_skill(content, config))
        write_file(codex_openai_path, build_codex_openai_yaml(config))

        print(f"Generated: {claude_skill_path.relative_to(REPO_ROOT)}")
        print(f"Generated: {codex_skill_path.relative_to(REPO_ROOT)}")
        print(f"Generated: {codex_openai_path.relative_to(REPO_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Build tool-specific prompts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    args = parser.parse_args()

    shared = load_shared_files()

    if not args.dry_run:
        clean_output_dirs()

    prompt_files = sorted(PROMPTS_DIR.glob("*.md"))
    for prompt_file in prompt_files:
        name = prompt_file.stem
        content = prompt_file.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)
        resolved_body = resolve_includes(body, shared)
        build_phase_outputs(name, metadata, resolved_body, dry_run=args.dry_run)

    build_shared_outputs(dry_run=args.dry_run)

    if args.dry_run:
        print("\n(dry run — no files written)")
    else:
        print("\nBuild complete.")


if __name__ == "__main__":
    main()
