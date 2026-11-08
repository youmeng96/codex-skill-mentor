# Codex Skill Mentor

[中文](README.md)

A project-based Agent Skill coach for beginners. It diagnoses a real task, guides the user through a minimal `SKILL.md`, validates the package, forward-tests the behavior, and prepares a GitHub release.

Works with Codex, Claude Code, Cursor, OpenClaw, DeepSeek Harness, and other Agent Skills-compatible runtimes.

## Install

Auto-detect the current runtime:

```bash
npx skills add youmeng96/codex-skill-mentor -g
```

Or select a runtime explicitly:

```bash
npx skills add youmeng96/codex-skill-mentor -g -a codex
npx skills add youmeng96/codex-skill-mentor -g -a claude-code
npx skills add youmeng96/codex-skill-mentor -g -a cursor
# Install to multiple runtimes:
npx skills add youmeng96/codex-skill-mentor -g -a codex claude-code cursor
```

`-g` installs at user scope; omit it for a project-local install.

Typical install directories:

| Runtime | Directory |
|---|---|
| Codex | `~/.codex/skills/codex-skill-mentor/` |
| Claude Code | `~/.claude/skills/codex-skill-mentor/` |
| Cursor | `~/.cursor/skills/codex-skill-mentor/` |
| OpenClaw | `~/.openclaw/workspace/skills/codex-skill-mentor/` |
| DeepSeek Harness | `~/.dsh/skills/codex-skill-mentor/` |

`agents/openai.yaml` is optional Codex UI metadata. Other runtimes can ignore it.

## Use

```text
Use codex-skill-mentor to help me build a skill that turns meeting notes into action items.
```

Modes:

- Diagnose a vague idea.
- Build a minimal skill.
- Review an existing `SKILL.md`.
- Validate and publish.
- Answer a focused concept question.

For Codex, `$codex-skill-mentor` is also supported.

## Validate

```bash
python -m pip install pyyaml
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
```

## Runtime compatibility

See [`references/runtime-compatibility.md`](references/runtime-compatibility.md).

## Design principles

1. A skill changes behavior, not just documentation.
2. `description` is a routing rule.
3. Start with the smallest working version.
4. Disclose detail progressively.
5. Validate with real tasks.

## Sources

The structure baseline comes from OpenAI's bundled `skill-creator`. The teaching method is inspired by Huashu's [Nuwa Skill](https://github.com/alchaincyf/nuwa-skill). This project uses an original coach persona and does not impersonate the author.

## License

MIT. See [`LICENSE`](LICENSE).