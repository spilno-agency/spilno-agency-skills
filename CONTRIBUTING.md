# Contributing

Thanks for helping! Skills here automate routine marketing & analytics work in Claude Code.

## Adding a skill

1. Create a folder named after the skill, e.g. `gsc-quick-wins/`.
2. Add `SKILL.md` with YAML frontmatter; `name` must equal the folder name.
3. Keep it vendor-neutral: brand, responsible person and currency come from `config.json` (see `config.example.json`), never hardcoded.
4. Never commit real client domains, account IDs or exported data — use `example.com` and fake IDs.
5. Run `python scripts/validate_skills.py` and add a line to `CHANGELOG.md`.

## Fixing a broken skill

Ad and analytics UIs change often. If a skill stops finding a menu or column, open a bug with the platform UI language and a short description of the new layout — or send a PR updating the steps.
