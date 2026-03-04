#!/usr/bin/env python3
"""Validate repository skill structure and `skill.yaml` metadata."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
SCHEMA_PATH = ROOT / "schemas" / "skill.schema.json"


class ValidationError(Exception):
    """Raised when a skill fails validation."""


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        raise ValidationError("schema file not found at `schemas/skill.schema.json`")
    return json.loads(SCHEMA_PATH.read_text())


def load_metadata(path: pathlib.Path) -> dict:
    metadata = yaml.safe_load(path.read_text())
    if not isinstance(metadata, dict):
        raise ValidationError(f"{path}: expected mapping at document root")
    return metadata


def validate_schema(skill_name: str, metadata: dict, schema: dict) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(metadata), key=lambda item: list(item.absolute_path))
    if errors:
        first = errors[0]
        where = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise ValidationError(f"{skill_name}: schema validation failed at `{where}`: {first.message}")


def validate_skill_files(skill_dir: pathlib.Path, metadata: dict) -> None:
    skill_name = skill_dir.name

    required_files = metadata.get("required_files", [])
    for rel in required_files:
        path = skill_dir / rel
        if not path.exists():
            raise ValidationError(f"{skill_name}: required file missing: `{rel}`")

    supported_agents = metadata.get("supported_agents", [])
    for agent in supported_agents:
        adapter_dir = skill_dir / "adapters" / agent
        if not adapter_dir.is_dir():
            raise ValidationError(f"{skill_name}: adapter directory missing for `{agent}`")


def render_summary(results: list[dict], failures: list[str]) -> str:
    lines: list[str] = []
    lines.append("# Validate Skills Report")
    lines.append("")
    lines.append(f"- Skills checked: **{len(results)}**")
    lines.append(f"- Failures: **{len(failures)}**")
    lines.append("")
    lines.append("| Skill | Version | Agents | Status |")
    lines.append("| --- | --- | --- | --- |")
    for result in results:
        agents = ", ".join(result["agents"])
        status = "PASS" if result["status"] == "pass" else "FAIL"
        lines.append(f"| `{result['name']}` | `{result['version']}` | `{agents}` | {status} |")

    if failures:
        lines.append("")
        lines.append("## Failures")
        lines.append("")
        for failure in failures:
            lines.append(f"- {failure}")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate skill structure and metadata.")
    parser.add_argument(
        "--summary-file",
        help="Write a markdown validation summary to this file path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not SKILLS_DIR.exists():
        fail("skills directory not found")

    skill_dirs = [entry for entry in SKILLS_DIR.iterdir() if entry.is_dir()]
    if not skill_dirs:
        fail("no skills found")

    try:
        schema = load_schema()
    except (ValidationError, json.JSONDecodeError) as exc:
        fail(str(exc))

    results: list[dict] = []
    failures: list[str] = []

    for skill_dir in sorted(skill_dirs):
        metadata_path = skill_dir / "skill.yaml"
        if not metadata_path.exists():
            failures.append(f"{skill_dir.name}: missing `skill.yaml`")
            results.append(
                {
                    "name": skill_dir.name,
                    "version": "unknown",
                    "agents": ["unknown"],
                    "status": "fail",
                }
            )
            continue

        try:
            metadata = load_metadata(metadata_path)
            validate_schema(skill_dir.name, metadata, schema)
            validate_skill_files(skill_dir, metadata)
            results.append(
                {
                    "name": skill_dir.name,
                    "version": str(metadata.get("version", "unknown")),
                    "agents": list(metadata.get("supported_agents", [])) or ["unknown"],
                    "status": "pass",
                }
            )
        except (ValidationError, json.JSONDecodeError, yaml.YAMLError) as exc:
            failures.append(str(exc))
            results.append(
                {
                    "name": skill_dir.name,
                    "version": "unknown",
                    "agents": ["unknown"],
                    "status": "fail",
                }
            )

    if args.summary_file:
        pathlib.Path(args.summary_file).write_text(render_summary(results, failures))

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1

    print("All skills passed schema and structure validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
