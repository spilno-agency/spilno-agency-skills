# Spilno Agency Skills

A collection of open-source [Claude Code](https://claude.com/claude-code) skills for marketing & analytics specialists.

Maintained by [Spilno Agency](https://spilno.agency) — released under MIT so any agency or freelancer can fork, customize, and use them.

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

Skills produce branded reports. To customize the brand name, default styling, language, etc., create a `config.json` inside the skill folder in your local `~/.claude/skills/<skill-name>/`:

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
- Translations (skills are bilingual UA/EN by default; we'd love DE, ES, PL contributions)
- Bug fixes for UI selectors when platforms change layout

Before submitting:
1. Test the skill end-to-end on a real account
2. Update the relevant `SKILL.md` triggers and checklist
3. Keep the skill vendor-neutral (no hardcoded agency names in the algorithm — use `{AGENCY_NAME}` placeholder)

---

## License

[MIT](./LICENSE) — use freely, including commercially. Attribution appreciated but not required.

---

## Authors

- **Spilno Agency** — [spilno.agency](https://spilno.agency)
- Community contributors (see `git log`)
