#!/usr/bin/env python3
"""Validate agent-input/topics.yaml against schema/topics.schema.yaml.

Usage:
    python scripts/validate.py
    python scripts/validate.py --topics path/to/topics.yaml
"""
import argparse
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TOPICS = REPO_ROOT / "agent-input" / "topics.yaml"
DEFAULT_SCHEMA = REPO_ROOT / "schema" / "topics.schema.yaml"


def load_yaml(path: Path) -> dict:
    """Load a YAML file and return its contents."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate_schema(topics: dict, schema: dict) -> list[str]:
    """Validate topics against JSON Schema. Returns list of error messages."""
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(topics), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"[{path}] {error.message}")
    return errors


def validate_business_rules(topics: dict) -> list[str]:
    """Validate business rules beyond JSON Schema. Returns list of error messages."""
    errors = []

    stages = topics.get("stages", [])

    # Check stage names are sequential
    for i, stage in enumerate(stages):
        expected_name = f"stage{i + 1:02d}"
        actual_name = stage.get("name", "")
        if actual_name != expected_name:
            errors.append(
                f"[stages[{i}].name] Expected '{expected_name}', got '{actual_name}'"
            )

    # Check scores sum to 100
    total_score = sum(s.get("score", 0) for s in stages)
    if stages and total_score != 100:
        errors.append(
            f"[stages] Scores must sum to 100, got {total_score}"
        )

    # Check total_minutes >= tutorial_minutes + implementation_minutes
    time = topics.get("estimated_time", {})
    tutorial = time.get("tutorial_minutes", 0)
    impl = time.get("implementation_minutes", 0)
    total = time.get("total_minutes", 0)
    if total < tutorial + impl:
        errors.append(
            f"[estimated_time] total_minutes ({total}) must be >= "
            f"tutorial_minutes ({tutorial}) + implementation_minutes ({impl})"
        )

    # If tutorial_required, tutorial_minutes should be > 0
    if topics.get("tutorial_required") and tutorial == 0:
        errors.append(
            "[estimated_time.tutorial_minutes] Should be > 0 when tutorial_required is true"
        )

    return errors


def validate(topics_path: Path, schema_path: Path) -> list[str]:
    """Run all validations. Returns list of error messages, empty if valid."""
    if not topics_path.exists():
        return [f"File not found: {topics_path}"]
    if not schema_path.exists():
        return [f"Schema not found: {schema_path}"]

    topics = load_yaml(topics_path)
    schema = load_yaml(schema_path)

    errors = validate_schema(topics, schema)
    if not errors:
        errors = validate_business_rules(topics)

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate topics.yaml")
    parser.add_argument(
        "--topics", type=Path, default=DEFAULT_TOPICS,
        help="Path to topics.yaml"
    )
    parser.add_argument(
        "--schema", type=Path, default=DEFAULT_SCHEMA,
        help="Path to schema file"
    )
    args = parser.parse_args()

    errors = validate(args.topics, args.schema)
    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print("Validation passed.")


if __name__ == "__main__":
    main()
