#!/usr/bin/env python3
"""Validate repository skill structure and `skill.yaml` metadata."""

from __future__ import annotations

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


def main() -> int:
    if not SKILLS_DIR.exists():
        fail("skills directory not found")

    skill_dirs = [entry for entry in SKILLS_DIR.iterdir() if entry.is_dir()]
    if not skill_dirs:
        fail("no skills found")

    try:
        schema = load_schema()
    except (ValidationError, json.JSONDecodeError) as exc:
        fail(str(exc))

    for skill_dir in sorted(skill_dirs):
        metadata_path = skill_dir / "skill.yaml"
        if not metadata_path.exists():
            fail(f"{skill_dir.name}: missing `skill.yaml`")

        try:
            metadata = load_metadata(metadata_path)
            validate_schema(skill_dir.name, metadata, schema)
            validate_skill_files(skill_dir, metadata)
        except (ValidationError, json.JSONDecodeError, yaml.YAMLError) as exc:
            fail(str(exc))

    print("All skills passed schema and structure validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
