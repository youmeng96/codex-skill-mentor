from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_skill import validate_skill  # noqa: E402


VALID_SKILL = """---
name: demo-skill
description: Use when a demo task needs a deterministic example.
---

# Demo Skill

## Workflow

1. Do the task.
2. Verify the result.
"""


class ValidateSkillTests(unittest.TestCase):
    def make_skill(self, content: str = VALID_SKILL, name: str = "demo-skill") -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name) / name
        root.mkdir()
        (root / "SKILL.md").write_text(content, encoding="utf-8")
        return root

    def test_valid_skill(self) -> None:
        self.assertEqual(validate_skill(self.make_skill()), [])

    def test_missing_frontmatter(self) -> None:
        errors = validate_skill(self.make_skill("# Missing\n"))
        self.assertIn("SKILL.md must start with YAML frontmatter delimited by ---", errors)

    def test_bad_name(self) -> None:
        content = VALID_SKILL.replace("name: demo-skill", "name: Demo Skill")
        errors = validate_skill(self.make_skill(content))
        self.assertTrue(any("hyphen-case" in error for error in errors))

    def test_directory_name_must_match(self) -> None:
        errors = validate_skill(self.make_skill(name="different-name"))
        self.assertTrue(any("must match skill name" in error for error in errors))

    def test_todo_in_body(self) -> None:
        content = VALID_SKILL + "\n[TODO: finish this later]\n"
        errors = validate_skill(self.make_skill(content))
        self.assertTrue(any("unfinished TODO" in error for error in errors))

    def test_openai_yaml_shape(self) -> None:
        root = self.make_skill()
        agents = root / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text(
            'interface:\n  display_name: "Demo"\npolicy:\n  allow_implicit_invocation: "yes"\n',
            encoding="utf-8",
        )
        errors = validate_skill(root)
        self.assertTrue(any("must be a boolean" in error for error in errors))


if __name__ == "__main__":
    unittest.main()