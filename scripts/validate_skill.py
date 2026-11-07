#!/usr/bin/env python3
"""Validate a Codex/Agent Skill directory without executing it."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in broken environments
    print("ERROR: PyYAML is required. Install it with: python -m pip install pyyaml")
    raise SystemExit(2)

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
ALLOWED_FRONTMATTER = {"name", "description", "license", "allowed-tools", "metadata"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
TODO_PATTERN = re.compile(r"^\s*\[TODO:[^\n]*\]\s*$")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _validate_openai_yaml(skill_dir: Path) -> list[str]:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return []

    errors: list[str] = []
    try:
        data = yaml.safe_load(_read_text(path))
    except yaml.YAMLError as exc:
        return [f"invalid YAML in agents/openai.yaml: {exc}"]

    if not isinstance(data, dict):
        return ["agents/openai.yaml must contain a YAML mapping"]

    interface = data.get("interface")
    if interface is not None and not isinstance(interface, dict):
        errors.append("agents/openai.yaml interface must be a mapping")

    if isinstance(interface, dict):
        default_prompt = interface.get("default_prompt")
        if default_prompt and not isinstance(default_prompt, str):
            errors.append("interface.default_prompt must be a string")

    policy = data.get("policy")
    if policy is not None and not isinstance(policy, dict):
        errors.append("agents/openai.yaml policy must be a mapping")
    if isinstance(policy, dict):
        implicit = policy.get("allow_implicit_invocation")
        if implicit is not None and not isinstance(implicit, bool):
            errors.append("policy.allow_implicit_invocation must be a boolean")

    return errors


def validate_skill(skill_dir: str | Path) -> list[str]:
    """Return a list of validation errors. An empty list means valid."""

    root = Path(skill_dir).resolve()
    errors: list[str] = []

    if not root.is_dir():
        return [f"skill directory does not exist: {root}"]

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md not found"]

    content = _read_text(skill_md)
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return ["SKILL.md must start with YAML frontmatter delimited by ---"]

    try:
        frontmatter: Any = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"invalid YAML frontmatter: {exc}"]

    if not isinstance(frontmatter, dict):
        return ["frontmatter must be a YAML mapping"]

    unexpected = sorted(set(frontmatter) - ALLOWED_FRONTMATTER)
    if unexpected:
        errors.append(
            "unexpected frontmatter key(s): "
            + ", ".join(unexpected)
            + "; allowed: "
            + ", ".join(sorted(ALLOWED_FRONTMATTER))
        )

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("frontmatter.name must be a non-empty string")
    else:
        name = name.strip()
        if len(name) > MAX_NAME_LENGTH:
            errors.append(f"name is longer than {MAX_NAME_LENGTH} characters")
        if not NAME_PATTERN.fullmatch(name):
            errors.append("name must be lowercase hyphen-case: letters, digits, and single hyphens")
        if root.name != name:
            errors.append(f"directory name '{root.name}' must match skill name '{name}'")

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append("frontmatter.description must be a non-empty string")
    else:
        description = description.strip()
        if len(description) > MAX_DESCRIPTION_LENGTH:
            errors.append(
                f"description is longer than {MAX_DESCRIPTION_LENGTH} characters"
            )
        if description.startswith("[TODO:"):
            errors.append("description still contains a TODO placeholder")
        if "<" in description or ">" in description:
            errors.append("description must not contain angle brackets")

    body = content[match.end() :].strip()
    if not body:
        errors.append("SKILL.md body is empty")

    in_fence = False
    fence_char = ""
    fence_length = 0
    for line_number, line in enumerate(body.splitlines(), start=1):
        fence = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
            continue
        if not in_fence and TODO_PATTERN.fullmatch(line):
            errors.append(f"SKILL.md body contains unfinished TODO at body line {line_number}")

    errors.extend(_validate_openai_yaml(root))

    for relative in ("references", "scripts", "assets"):
        directory = root / relative
        if directory.exists() and not directory.is_dir():
            errors.append(f"{relative} must be a directory when present")

    return errors


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print("Usage: python scripts/validate_skill.py <skill-directory>")
        return 2

    errors = validate_skill(args[0])
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())