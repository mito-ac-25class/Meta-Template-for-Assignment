#!/usr/bin/env python3
"""Generate files from topics.yaml + Jinja2 templates.

Usage:
    python scripts/generate.py classroom   # Generate .github/workflows/classroom.yml
    python scripts/generate.py plan        # Generate agent-output/plan.md (skeleton)
    python scripts/generate.py readme      # Generate release/README.md (skeleton)
    python scripts/generate.py tutorial    # Generate TUTORIAL.md (skeleton)
    python scripts/generate.py all         # Generate all targets

Templates are read from templates/ directory (Jinja2 .j2 files).
Data is read from agent-input/topics.yaml.
"""
import argparse
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_PATH = REPO_ROOT / "agent-input" / "topics.yaml"
TEMPLATES_DIR = REPO_ROOT / "templates"

# Target mapping: name -> (template, output_path)
TARGETS = {
    "classroom": ("classroom.yml.j2", ".github/workflows/classroom.yml"),
    "plan": ("plan.md.j2", "agent-output/plan.md"),
    "readme": ("README.md.j2", "release/README.md"),
    "tutorial": ("TUTORIAL.md.j2", "TUTORIAL.md"),
}


def load_topics(path: Path) -> dict:
    """Load topics.yaml."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def render_template(template_name: str, context: dict) -> str:
    """Render a Jinja2 template with the given context."""
    from jinja2 import Environment, FileSystemLoader

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )
    template = env.get_template(template_name)
    return template.render(**context)


def generate_target(name: str, topics: dict) -> None:
    """Generate a single target file."""
    if name not in TARGETS:
        print(f"Unknown target: {name}", file=sys.stderr)
        sys.exit(1)

    template_name, output_rel = TARGETS[name]
    template_path = TEMPLATES_DIR / template_name

    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        print("(Templates will be created in Phase 3)", file=sys.stderr)
        return

    output_path = REPO_ROOT / output_rel
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = render_template(template_name, topics)
    output_path.write_text(content, encoding="utf-8")
    print(f"Generated: {output_rel}")


def main():
    parser = argparse.ArgumentParser(description="Generate files from templates")
    parser.add_argument(
        "targets", nargs="+",
        choices=list(TARGETS.keys()) + ["all"],
        help="Targets to generate"
    )
    parser.add_argument(
        "--topics", type=Path, default=TOPICS_PATH,
        help="Path to topics.yaml"
    )
    args = parser.parse_args()

    if not args.topics.exists():
        print(f"Topics file not found: {args.topics}", file=sys.stderr)
        sys.exit(1)

    topics = load_topics(args.topics)

    targets = list(TARGETS.keys()) if "all" in args.targets else args.targets
    for target in targets:
        generate_target(target, topics)


if __name__ == "__main__":
    main()
