# Runtime Compatibility

`codex-skill-mentor` follows the open Agent Skills structure: a folder with `SKILL.md` at its root and optional `agents/`, `scripts/`, `references/`, and `assets/` directories.

The name and description are the portable discovery layer. `agents/openai.yaml` is optional Codex UI metadata and is ignored by runtimes that do not read it.

## Recommended install

Auto-detect the current runtime:

```bash
npx skills add youmeng96/codex-skill-mentor -g
```

Or target a supported runtime explicitly:

```bash
npx skills add youmeng96/codex-skill-mentor -g -a codex
npx skills add youmeng96/codex-skill-mentor -g -a claude-code
npx skills add youmeng96/codex-skill-mentor -g -a cursor
```

The exact `-a` names available depend on the installed `skills` CLI version. If a name is rejected, run `npx skills --help` or use auto-detect.

## Manual install locations

| Runtime | Typical skill directory |
|---|---|
| Codex | `~/.codex/skills/codex-skill-mentor/` |
| Claude Code | `~/.claude/skills/codex-skill-mentor/` |
| Cursor | `~/.cursor/skills/codex-skill-mentor/` |
| OpenClaw | `~/.openclaw/workspace/skills/codex-skill-mentor/` |
| DeepSeek Harness | `~/.dsh/skills/codex-skill-mentor/` |
| Other runtimes | Use the runtime's documented skills directory |

Windows uses the same structure under `%USERPROFILE%`.

## What changes by runtime

- The skill folder location.
- The syntax used to invoke the skill.
- Whether the runtime reads `agents/openai.yaml`.
- The exact UI name shown in the skill picker.

What does not change:

- `SKILL.md` and its frontmatter.
- The teaching workflow and safety rules.
- `scripts/validate_skill.py`.
- The minimum Skill structure taught by the mentor.

## Verification

Run from the installed skill directory:

```bash
python scripts/validate_skill.py .
python -m unittest discover -s tests -v
```

Then use one realistic prompt in the target runtime:

```text
Use codex-skill-mentor to help me build a skill that turns meeting notes into action items.
```

## Publishing a portable skill

1. Keep `SKILL.md` at the repository root.
2. Use lowercase-hyphen-case for the folder and `name`.
3. Document any dependency outside the Python standard library.
4. Avoid Codex-only environment variables and tool names unless they are optional examples.
5. Test installation in at least one non-Codex runtime or a clean temporary skills directory.