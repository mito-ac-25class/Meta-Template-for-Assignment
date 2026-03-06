"""build_prompts.py のテスト"""
import subprocess
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

import build_prompts


REPO_ROOT = Path(__file__).parent.parent.parent


def configure_temp_repo(monkeypatch, repo_root: Path):
    """build_prompts モジュールの出力先を一時ディレクトリに向ける。"""
    monkeypatch.setattr(build_prompts, "REPO_ROOT", repo_root)
    monkeypatch.setattr(build_prompts, "PROMPTS_DIR", repo_root / "prompts")
    monkeypatch.setattr(build_prompts, "SHARED_DIR", repo_root / "prompts" / "_shared")
    monkeypatch.setattr(build_prompts, "CLAUDE_COMMANDS_DIR", repo_root / ".claude" / "commands")
    monkeypatch.setattr(build_prompts, "CLAUDE_SKILLS_DIR", repo_root / ".claude" / "skills")
    monkeypatch.setattr(build_prompts, "COPILOT_PROMPTS_DIR", repo_root / ".github" / "prompts")
    monkeypatch.setattr(build_prompts, "CODEX_SKILLS_DIR", repo_root / ".agents" / "skills")


def test_build_prompts_dry_run_lists_codex_outputs():
    """dry-run に Claude / Copilot / Codex の出力先が表示されることを確認"""
    script = REPO_ROOT / "scripts" / "build_prompts.py"
    result = subprocess.run(
        [sys.executable, str(script), "--dry-run"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Claude:" in result.stdout
    assert "Copilot:" in result.stdout
    assert "Codex:" in result.stdout
    assert ".agents/skills/design-admin/SKILL.md" in result.stdout


def test_build_prompts_generates_codex_skills(tmp_path, monkeypatch):
    """Codex 用スキルと openai.yaml が生成されることを確認"""
    shutil.copytree(REPO_ROOT / "prompts", tmp_path / "prompts")
    configure_temp_repo(monkeypatch, tmp_path)

    build_prompts.clean_output_dirs()

    shared = build_prompts.load_shared_files()
    for prompt_file in sorted(build_prompts.PROMPTS_DIR.glob("*.md")):
        metadata, body = build_prompts.parse_frontmatter(prompt_file.read_text(encoding="utf-8"))
        resolved_body = build_prompts.resolve_includes(body, shared)
        build_prompts.build_phase_outputs(
            prompt_file.stem,
            metadata,
            resolved_body,
            dry_run=False,
        )
    build_prompts.build_shared_outputs(dry_run=False)

    skill_path = tmp_path / ".agents" / "skills" / "design-admin" / "SKILL.md"
    openai_path = tmp_path / ".agents" / "skills" / "design-admin" / "agents" / "openai.yaml"
    shared_skill_path = tmp_path / ".agents" / "skills" / "assignment-types" / "SKILL.md"
    shared_openai_path = (
        tmp_path / ".agents" / "skills" / "assignment-types" / "agents" / "openai.yaml"
    )

    assert skill_path.exists()
    assert openai_path.exists()
    assert shared_skill_path.exists()
    assert shared_openai_path.exists()

    skill_content = skill_path.read_text(encoding="utf-8")
    openai_content = openai_path.read_text(encoding="utf-8")
    shared_openai_content = shared_openai_path.read_text(encoding="utf-8")

    assert "name: design-admin" in skill_content
    assert "description: |" in skill_content
    assert "# $design-admin スキル" in skill_content
    assert 'display_name: "Design Admin"' in openai_content
    assert 'default_prompt: "$design-admin を使って topics.yaml を検証し、課題プランを作成してください。"' in openai_content
    assert "allow_implicit_invocation: false" in openai_content
    assert "allow_implicit_invocation: true" in shared_openai_content
