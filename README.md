# Spilno Agency Skills

[![Validate skills](https://github.com/spilno-agency/spilno-agency-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/spilno-agency/spilno-agency-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

A collection of open-source [Claude Code](https://claude.com/claude-code) skills for marketing & analytics specialists.

Maintained by [Spilno Agency](https://spilnoagency.com.ua) — released under MIT so any agency or freelancer can fork, customize, and use them.

---

## Skills in this repo

| Skill | What it does |
|---|---|
| [`ga4-roas-corridor-analysis`](./ga4-roas-corridor-analysis) | Pulls 6 months of Google Ads data from GA4 UI, calculates the ROAS corridor (min/avg/max + variance), and builds a branded Google Doc forecast of how revenue grows at different budget levels. |

More skills coming. PRs welcome.

---

## Installation

These skills are designed for [Claude Code](https://claude.com/claude-code) (the CLI by Anthropic).

### Option 1 — copy a single skill

```bash
git clone https://github.com/spilno-agency/spilno-agency-skills.git
cp -r spilno-agency-skills/ga4-roas-corridor-analysis ~/.claude/skills/
```

Restart Claude Code. The skill is now invocable via `/ga4-roas-corridor-analysis`.

### Option 2 — symlink the whole repo (auto-updates)

```bash
git clone https://github.com/spilno-agency/spilno-agency-skills.git ~/spilno-agency-skills
ln -s ~/spilno-agency-skills/ga4-roas-corridor-analysis ~/.claude/skills/ga4-roas-corridor-analysis
```

Then `cd ~/spilno-agency-skills && git pull` pulls updates.

---

## Prerequisites

Every skill in this repo expects:

1. **Claude Code** installed ([install guide](https://docs.claude.com/en/docs/claude-code/quickstart)).
2. **Claude for Chrome** extension if the skill drives the browser (most do — they automate platforms like GA4, Google Ads, Search Console).
3. **MCP connectors** as needed per skill (Google Drive for doc creation, etc.).

Each skill's `SKILL.md` lists its specific prerequisites at the top.

---

## Configuration

Skills produce branded reports. To customize the brand name, default styling, language, etc., copy `config.example.json` to `config.json` inside the skill folder in your local `~/.claude/skills/<skill-name>/`:

```json
{
  "agency_name": "Your Agency Name",
  "default_responsible": "Your Name",
  "language": "uk",
  "currency_symbol": "$"
}
```

Each skill's README documents the keys it reads.

---

## Why these skills exist

We built these tools because:

- **Routine analyses eat the most analyst-time** — the ROAS-corridor analysis takes 1.5 hours manually, ~2 minutes with this skill.
- **Methodology stays consistent** — the same calculation logic is applied across every project.
- **Reports look professional** — same Montserrat-based clean style, same section order, same charts.
- **Easy to extend** — fork, edit `SKILL.md`, ship.

---

## Contributing

PRs welcome — especially for:
- New analyses (Search Console, Meta Ads, TikTok Ads, GMB, etc.)
- Translations (the current skill is written in Ukrainian with bilingual UA/EN triggers; DE, ES, PL and EN versions are welcome)
- Bug fixes for UI selectors when platforms change layout

See [CONTRIBUTING.md](./CONTRIBUTING.md). CI runs `scripts/validate_skills.py` on every PR — it checks frontmatter and rejects hardcoded agency names (use the `{AGENCY_NAME}` placeholder).

---

## License

[MIT](./LICENSE) — use freely, including commercially. Attribution appreciated but not required.

---

## Authors

- **Spilno Agency** — [spilnoagency.com.ua](https://spilnoagency.com.ua)
- Community contributors (see `git log`)
